from django import forms
from django.db import connection

class LocatarioForm(forms.Form):
    nome = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=20)
    rg = forms.CharField(max_length=20)
    cpf_cnpj = forms.CharField(max_length=14)
    estado_civil = forms.ChoiceField(choices=[], required=False)  # Estado civil será preenchido dinamicamente

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preencher o estado civil com dados do banco
        self.fields['estado_civil'].choices = self.get_estado_civil_choices()

    def get_estado_civil_choices(self):
        # Consulta SQL para obter os estados civis
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Estado_Civil, Desc_Estado_Civil FROM Estado_Civil")
            estado_civil_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in estado_civil_options]
