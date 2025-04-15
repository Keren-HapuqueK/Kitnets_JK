from django import forms

class FormaPagamentoForm(forms.Form):
    desc_forma_pgto = forms.CharField(label="Descrição", max_length=255)
