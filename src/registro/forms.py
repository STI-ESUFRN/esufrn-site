from django import forms

from .models import Pessoa


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = [
            "numero",
            "saberes_competencias",
            "descricao_item",
            "documentos_comprobatorios",
            "unidade_medida",
            "pontuacao",
            "pessoas",
            "solicitar_documentacao_chefia",
            "observacoes",
        ]
        widgets = {
            "numero": forms.NumberInput(attrs={"class": "form-control"}),
            "saberes_competencias": forms.TextInput(attrs={"class": "form-control"}),
            "descricao_item": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "documentos_comprobatorios": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "unidade_medida": forms.TextInput(attrs={"class": "form-control"}),
            "pontuacao": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "pessoas": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: Ana, João, Maria"}),
            "solicitar_documentacao_chefia": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class PessoaDeclaracaoMultiUploadForm(forms.Form):
    arquivos = forms.FileField(
        label="Declarações",
    widget=MultipleFileInput(attrs={"class": "form-control", "multiple": True}),
        required=False,
    )
