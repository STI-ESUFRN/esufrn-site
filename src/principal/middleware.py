# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from .models import PageView

# Lista de UA (evite tokens muito genéricos)
BOT_UA_PATTERNS = [
    'googlebot', 'bingbot', 'yandexbot', 'duckduckbot', 'baiduspider',
    'semrush', 'ahrefs', 'mj12bot', 'dotbot', 'bytespider',
    'crawler', 'spider', 'slurp', 'curl', 'wget', 'l9explore',
    'python-requests', 'http-client', 'go-http-client', 'gptbot',
    'headless', 'headlesschrome',
]

# caminhos/ prefixos óbvios que não devem gerar pageview
IGNORED_PATH_PREFIXES = (
    '/static/', '/media/', '/admin/', '/favicon.ico', '/robots.txt',
    '/sitemap.xml', '/nginx_status', '/health', '/robots.txt',
)

# alvos comuns de scanners (verificar com cuidado para não bloquear rotas legítimas)
BOT_PATH_PATTERNS = [
    '/wp-login.php', '/wp-admin/', '/xmlrpc.php', '/.git/config',
    '/.env', '/phpmyadmin', '/vendor/phpunit/', '/eval-stdin.php',
    '/jquery-file-upload', '/filemanager', '/tinymce',
]

# TTL para evitar contagens duplicadas por sessão (em segundos)
DEDUP_TTL = 60 * 60 * 24  # 24h

class SitePageViewMiddleware(MiddlewareMixin):
    """
    Conta UMA PageView(page_type='site') por sessão.
    Melhorias:
      - Checa path/ua primeiro (evita I/O de sessão para bots)
      - Usa cache.add() atômico para evitar race conditions
      - Grava metadata mínima (session_key, path, ua, IP anonimizado)
    """
    def process_request(self, request):
        # path barato: ignorar assets/health/admin logo
        path = (request.path or '/').lower()
        for p in IGNORED_PATH_PREFIXES:
            if path.startswith(p):
                return None

        # filtro de caminhos tipicamente atacados por scanners
        for p in BOT_PATH_PATTERNS:
            if p in path:
                return None

        # UA: barato, antes de tocar session
        ua = (request.META.get('HTTP_USER_AGENT') or '').lower()
        if any(pat in ua for pat in BOT_UA_PATTERNS):
            return None

        # agora só acessar session se houver chance de contar
        if request.session.get('site_viewed'):
            return None

        # garantir session_key (gera uma se não existir)
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key

        # deduplicação atômica via cache
        cache_key = f"siteview:session:{session_key}"
        added = cache.add(cache_key, 1, DEDUP_TTL)
        if not added:
            # já contamos para essa sessão recentemente
            request.session['site_viewed'] = True
            request.session.save()
            return None

        # anonimização simples do IP (IPv4)
        remote = request.META.get('REMOTE_ADDR', '')
        remote_anon = remote
        if remote and '.' in remote:
            parts = remote.split('.')
            if len(parts) == 4:
                parts[-1] = '0'
                remote_anon = '.'.join(parts)

        # criar registro (não quebrar a requisição se o DB falhar)
        try:
            PageView.objects.create(
                page_type='site',
                session_key=session_key,
                path=path[:512],
                user_agent=(request.META.get('HTTP_USER_AGENT','')[:512]),
                remote_addr=remote_anon,
            )
        except Exception:
            cache.delete(cache_key)  # libera para tentar novamente no futuro

        # marcar sessão como já vista
        request.session['site_viewed'] = True
        request.session.save()
        return None