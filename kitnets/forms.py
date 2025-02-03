from django import forms
from django.db import connection

class ImovelForm(forms.Form):
    id_locador = forms.ChoiceField(label="Locador", choices=[])
    endereco = forms.CharField(label="Endereço", max_length=200)
    descricao = forms.CharField(label="Descrição", max_length=200)
    disponivel = forms.ChoiceField(label="Disponível", choices=[('S', 'Sim'), ('N', 'Não')])
    vlr_aluguel = forms.DecimalField(label="Valor Aluguel", max_digits=6, decimal_places=2)
    uc = forms.IntegerField(label="UC")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_locador'].choices = self.get_locador_choices()

    def get_locador_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Locador, Nome FROM Locador")
            locador_options = cursor.fetchall()
        return [(str(option[0]), option[1]) for option in locador_options]
