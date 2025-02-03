from django import forms
from django.db import connection

class RegistroPagamentoForm(forms.Form):
    dt_paga = forms.DateField(label="Data de Pagamento", widget=forms.DateInput(attrs={'type': 'date'}))
    ref_mes_ano = forms.CharField(label="Referência Mês/Ano", max_length=7)
    observacao = forms.CharField(label="Observação", max_length=255, required=False)
    id_contrato = forms.ChoiceField(label="Contrato", choices=[])
    id_locatario = forms.ChoiceField(label="Locatário", choices=[])
    id_forma_pagamento = forms.ChoiceField(label="Forma de Pagamento", choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_contrato'].choices = self.get_contrato_choices()
        self.fields['id_locatario'].choices = self.get_locatario_choices()
        self.fields['id_forma_pagamento'].choices = self.get_forma_pagamento_choices()

    def get_contrato_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Contrato, NU_Contrato FROM Contrato")
            contrato_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in contrato_options]

    def get_locatario_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Locatario, Nome FROM Locatario")
            locatario_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in locatario_options]

    def get_forma_pagamento_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Forma_Pagamento, Desc_Forma_Pgto FROM Forma_Pagamento")
            forma_pagamento_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in forma_pagamento_options]

class FormaPagamentoForm(forms.Form):
    desc_forma_pgto = forms.CharField(label="Descrição", max_length=255)



