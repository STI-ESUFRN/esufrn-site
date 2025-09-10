from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PessoaForm, PessoaDeclaracaoMultiUploadForm
from .models import Pessoa, PessoaDeclaracao

# Create your views here.
@login_required
def registro(request):
    pessoas = Pessoa.objects.all().prefetch_related("declaracoes")
    return render(request, "registro/relacao.html", {"pessoas": pessoas})

@login_required
def formulario(request):
    if request.method == "POST":
        form = PessoaForm(request.POST)
        files_form = PessoaDeclaracaoMultiUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pessoa = form.save()
            if files_form.is_valid():
                arquivos = request.FILES.getlist("arquivos")
                for f in arquivos:
                    PessoaDeclaracao.objects.create(pessoa=pessoa, arquivo=f)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                item = {
                    "id": pessoa.id,
                    "uid": str(pessoa.uid),
                    "numero": pessoa.numero,
                    "saberes_competencias": pessoa.saberes_competencias,
                    "descricao_item": pessoa.descricao_item,
                    "documentos_comprobatorios": pessoa.documentos_comprobatorios,
                    "unidade_medida": pessoa.unidade_medida,
                    "pontuacao": float(pessoa.pontuacao or 0),
                    "declaracoes": [
                        {"url": d.arquivo.url, "id": d.id} for d in pessoa.declaracoes.all()
                    ],
                    "pessoas": pessoa.pessoas,
                    "solicitar_documentacao_chefia": pessoa.solicitar_documentacao_chefia,
                    "observacoes": pessoa.observacoes,
                }
                return JsonResponse({"ok": True, "item": item})
            return redirect("registro")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                # mescla erros se necessário
                errors = form.errors.copy()
                errors.update(files_form.errors)
                return JsonResponse(errors, status=400)
            return render(request, "registro/formulario.html", {"form": form, "files_form": files_form})

    form = PessoaForm()
    files_form = PessoaDeclaracaoMultiUploadForm()
    return render(request, "registro/formulario.html", {"form": form, "files_form": files_form})