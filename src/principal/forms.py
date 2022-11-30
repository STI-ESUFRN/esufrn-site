from django import forms

from principal.models import Newsletter


class ContactES(forms.Form):
    name = forms.CharField(
        label="Nome",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"name": "nome", "placeholder": "Nome", "required": True}
        ),
    )
    contact = forms.CharField(
        label="Contato",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"name": "contato", "placeholder": "Contato", "required": True}
        ),
    )
    message = forms.CharField(
        label="Mensagem",
        required=True,
        widget=forms.TextInput(
            attrs={
                "name": "mensagem",
                "placeholder": "Mensagem",
                "required": True,
            }
        ),
    )


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ("name_person", "email", "category", "consent")
        widgets = {
            "name_person": forms.TextInput(
                attrs={
                    "class": "w-100 p-2",
                    "placeholder": "Nome",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-100 p-2",
                    "placeholder": "Email",
                    "required": True,
                }
            ),
            "category": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input text-black"}
            ),
            "consent": forms.CheckboxInput(attrs={"required": True}),
        }


class UnsubscribeES(forms.Form):
    email = forms.CharField(
        label="Email",
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "name": "email",
                "placeholder": "Email",
                "required": True,
                "class": "w-100 px-2",
            }
        ),
    )


class siginForm(forms.Form):
    field_user_name = forms.CharField(
        label="Usuário",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-0 border-0 my-4",
                "placeholder": "Usuário",
                "required": "required",
            }
        ),
    )
    field_passwd = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control rounded-0 border-0 my-4",
                "placeholder": "Senha",
                "required": "required",
            }
        ),
    )
