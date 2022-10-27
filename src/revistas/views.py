from django.shortcuts import render

from revistas.models import Revista


def revistas(request):
    context = {
        "crumbs": [
            {"name": "Publicações"},
            {"name": "Revistas"},
        ],
        "revistas": Revista.objects.all(),
    }
    return render(request, "revista.revistas.html", context)
