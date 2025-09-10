from django.urls import path
from ..views import registro, formulario

urlpatterns = [
    path('', registro, name='registro'),
    path('formulario/', formulario, name='formulario'),
]