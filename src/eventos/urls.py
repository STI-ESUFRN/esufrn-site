from django.urls import path

from eventos.views import evento

urlpatterns = [
    path("<slug:slug>/", evento, name="evento"),
]
