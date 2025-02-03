from django import forms
from django.db import connection

class LocadorForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=100)
    telefone = forms.CharField(label="Telefone", max_length=20)
    rg = forms.CharField(label="RG", max_length=20)
    cpf_cnpj = forms.CharField(label="CPF/CNPJ", max_length=14)
    estado_civil = forms.ChoiceField(label="Estado Civil", choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado_civil'].choices = self.get_estado_civil_choices()

    def get_estado_civil_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Estado_Civil, Desc_Estado_Civil FROM Estado_Civil")
            estado_civil_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in estado_civil_options]
