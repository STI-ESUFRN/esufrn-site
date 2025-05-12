from django.utils.deprecation import MiddlewareMixin
from .models import PageView

class SitePageViewMiddleware(MiddlewareMixin):
    """
    Registra exatamente UMA PageView(page_type='site') por sessão,
    na primeira requisição HTTP de qualquer URL do projeto.
    """

    def process_request(self, request):
        # Se já registrou nesta sessão, não faz de novo
        if request.session.get('site_viewed'):
            return None

        # Senão: cria o registro e marca a sessão
        PageView.objects.create(page_type='site')
        request.session['site_viewed'] = True
        return None