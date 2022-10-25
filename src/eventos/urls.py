from django.urls import path

from eventos.views import evento, eventos

urlpatterns = [
    path("", eventos, name="eventos"),
    path("<int:pk>/", evento, name="evento"),
]
