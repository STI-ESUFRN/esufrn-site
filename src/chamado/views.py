from django.shortcuts import render


def inserirChamado(request):
    context = {"crumbs": [{"name": "Informática"}, {"name": "Chamado Suporte"}]}

    return render(request, "informatica.chamado.inserir.html", context)
