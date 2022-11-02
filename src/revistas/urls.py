from django.urls import path

from revistas.views import revistas

urlpatterns = [
    path("", revistas, name="revistas"),
]
