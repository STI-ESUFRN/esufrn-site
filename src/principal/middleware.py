# middleware.py
import logging
from urllib.parse import urlparse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.db import transaction
from .models import PageView

logger = logging.getLogger(__name__)

BOT_UA_PATTERNS = [
    'googlebot','bingbot','yandexbot','duckduckbot','baiduspider',
    'semrush','ahrefs','mj12bot','dotbot','bytespider',
    'crawler','spider','slurp','curl','wget','l9explore',
    'python-requests','http-client','go-http-client','gptbot',
    'headless','headlesschrome',
]

IGNORED_PATH_PREFIXES = (
    '/static/', '/media/', '/admin/', '/favicon.ico', '/robots.txt',
    '/sitemap.xml', '/nginx_status', '/health',
)

BOT_PATH_PATTERNS = [
    '/wp-login.php', '/wp-admin/', '/xmlrpc.php', '/.git/config',
    '/.env', '/phpmyadmin', '/vendor/phpunit/', '/eval-stdin.php',
]

DEDUP_TTL = 60 * 60 * 24  # 24h

class SitePageViewMiddleware(MiddlewareMixin):
    """
    Conta UMA PageView(page_type='site') por sessão.
    Compatível com PageView(page_type, object_id, timestamp) — NÃO altera schema.
    Workaround para HTML servido por cache: "promove" requests de assets quando o Referer
    aponta para o mesmo host e é uma página HTML.
    """
    def _is_bot_ua(self, ua):
        ua = (ua or '').lower()
        return any(pat in ua for pat in BOT_UA_PATTERNS)

    def _is_ignored_path(self, path):
        path = (path or '/').lower()
        return any(path.startswith(p) for p in IGNORED_PATH_PREFIXES)

    def _is_bot_path(self, path):
        path = (path or '/').lower()
        return any(p in path for p in BOT_PATH_PATTERNS)

    def _get_client_ip(self, request):
        # prefere X-Forwarded-For, mas não exige Nginx
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')

    def _anon_ip(self, ip):
        try:
            if '.' in ip:
                parts = ip.split('.')
                if len(parts) == 4:
                    parts[-1] = '0'
                    return '.'.join(parts)
            if ':' in ip:
                parts = ip.split(':')
                parts[-1] = '0'
                return ':'.join(parts)
        except Exception:
            pass
        return ''

    def process_request(self, request):
        # apenas métodos GET e preferivelmente HTML
        if request.method != 'GET':
            return None
        accept = request.META.get('HTTP_ACCEPT', '')
        if 'text/html' not in accept and '*/*' not in accept:
            return None

        path = (request.path or '/').lower()

        # Se for asset ignorado, verificar Referer (workaround) — promote se o referer for interno e não-asset
        if self._is_ignored_path(path):
            referer = request.META.get('HTTP_REFERER', '')
            if not referer:
                return None
            try:
                parsed = urlparse(referer)
                # se referer apontar para o mesmo host
                if parsed.netloc and parsed.netloc == request.get_host():
                    referer_path = (parsed.path or '/').lower()
                    # se o referer não for asset e não for path de bot, "promovemos" a contagem usando o referer_path
                    if not self._is_ignored_path(referer_path) and not self._is_bot_path(referer_path):
                        path = referer_path
                    else:
                        return None
                else:
                    return None
            except Exception:
                return None

        # filtra caminhos de scanner
        if self._is_bot_path(path):
            return None

        # filtra UA
        ua = request.META.get('HTTP_USER_AGENT', '')
        if self._is_bot_ua(ua):
            return None

        # já marcada na sessão?
        if request.session.get('site_viewed'):
            return None

        # garantir session_key (pode criar cookie de sessão)
        if not request.session.session_key:
            try:
                request.session.save()
            except Exception:
                logger.exception("Falha ao salvar session_key")

        session_key = request.session.session_key or 'no-session'

        # dedup atômico via cache
        cache_key = f"siteview:session:{session_key}"
        try:
            added = cache.add(cache_key, 1, DEDUP_TTL)
        except Exception:
            logger.exception("Falha ao acessar cache; permitindo criar PageView para evitar bloqueio")
            added = True

        if not added:
            # já contamos recentemente: marca sessão pra evitar I/O repetido
            try:
                request.session['site_viewed'] = True
                request.session.save()
            except Exception:
                logger.exception("Falha ao marcar session quando cache indicou existência")
            return None

        # IP (não gravamos no modelo atual, mas calculamos caso queira log)
        ip = self._get_client_ip(request)
        remote_anon = self._anon_ip(ip)

        # CRIAÇÃO compatível com schema atual: somente page_type
        try:
            pv = PageView.objects.create(page_type='site')
            # marcar sessão apenas depois do commit do DB
            def _mark_session():
                try:
                    request.session['site_viewed'] = True
                    request.session.save()
                except Exception:
                    logger.exception("Falha ao marcar session após transaction.on_commit")
            transaction.on_commit(_mark_session)
        except Exception:
            logger.exception("Falha ao criar PageView")
            # liberar chave de dedup para permitir nova tentativa futura
            try:
                cache.delete(cache_key)
            except Exception:
                logger.exception("Falha ao deletar cache_key após falha no DB")
        return None