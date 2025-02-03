from django import forms

class EstadoCivilForm(forms.Form):
    desc_estado_civil = forms.CharField(
        label="Descrição do Estado Civil",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
