from django import forms


class SiginForm(forms.Form):
    field_user_name = forms.CharField(
        label="Usuário",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-0 border-0 my-4",
                "placeholder": "Usuário",
                "required": "required",
            },
        ),
    )
    field_passwd = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control rounded-0 border-0 my-4",
                "placeholder": "Senha",
                "required": "required",
            },
        ),
    )
