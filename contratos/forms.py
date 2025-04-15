from django import forms
from django.db import connection

class ContratoForm(forms.Form):
    nu_contrato = forms.CharField(label="Número do Contrato", max_length=20)
    vlr_aluguel = forms.DecimalField(label="Valor do Aluguel", max_digits=6, decimal_places=2)
    dt_inicio = forms.DateField(label="Data de Início", widget=forms.DateInput(attrs={'type': 'date'}))
    dia_base = forms.CharField(label="Dia Base", max_length=2)
    dt_fim = forms.DateField(label="Data de Fim", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    cidade = forms.CharField(label="Cidade", max_length=20)
    uf = forms.CharField(label="UF", max_length=2)
    id_imovel = forms.ChoiceField(label="Imóvel", choices=[])
    id_locatario = forms.ChoiceField(label="Locatário", choices=[])
    id_locador = forms.ChoiceField(label="Locador", choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_imovel'].choices = self.get_imovel_choices()
        self.fields['id_locatario'].choices = self.get_locatario_choices()
        self.fields['id_locador'].choices = self.get_locador_choices()

    def get_imovel_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Imovel, Endereco FROM Imovel")
            imovel_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in imovel_options]

    def get_locatario_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ID_Locatario, Nome 
                FROM Locatario 
                WHERE ID_Locatario NOT IN (SELECT ID_Locatario FROM Contrato)
            """)
            locatario_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in locatario_options]

    def get_locador_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Locador, Nome FROM Locador")
            locador_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in locador_options]
