from django.utils.deprecation import MiddlewareMixin
from .models import PageView

# Defina aqui os padrões que caracterizam bots
BOT_UA_PATTERNS = [
    'bot', 'crawler', 'spider', 'slurp', 'curl', 'wget',
    'googlebot', 'bingbot', 'yandexbot', 'duckduckbot',
]

class SitePageViewMiddleware(MiddlewareMixin):
    """
    Registra exatamente UMA PageView(page_type='site') por sessão,
    na primeira requisição HTTP de qualquer URL do projeto,
    ignorando User‑Agents de bots.
    """

    def process_request(self, request):
        # 1) Session-based lock: já contou?
        if request.session.get('site_viewed'):
            return None

        # 2) Bot‑filter: se o UA tiver qualquer padrão de bot, não conta
        ua = request.META.get('HTTP_USER_AGENT', '').lower()
        if any(pat in ua for pat in BOT_UA_PATTERNS):
            return None

        # 3) Cria o registro e marca a sessão
        PageView.objects.create(page_type='site')
        request.session['site_viewed'] = True
        return None