from django import forms  # Importa o módulo de formulários do Django
from django.db import connection  # Importa o módulo de conexão com o banco de dados do Django

class LocadorForm(forms.Form):  # Define uma nova classe de formulário chamada LocadorForm
    nome = forms.CharField(label="Nome", max_length=100)  # Cria um campo de texto para o nome com um rótulo e um tamanho máximo de 100 caracteres
    telefone = forms.CharField(label="Telefone", max_length=20)  # Cria um campo de texto para o telefone com um rótulo e um tamanho máximo de 20 caracteres
    rg = forms.CharField(label="RG", max_length=20)  # Cria um campo de texto para o RG com um rótulo e um tamanho máximo de 20 caracteres
    cpf_cnpj = forms.CharField(label="CPF/CNPJ", max_length=14)  # Cria um campo de texto para o CPF/CNPJ com um rótulo e um tamanho máximo de 14 caracteres
    estado_civil = forms.ChoiceField(label="Estado Civil", choices=[])  # Cria um campo de escolha para o estado civil com um rótulo e uma lista de opções vazia

    def __init__(self, *args, **kwargs):  # Define o método inicializador da classe
        super().__init__(*args, **kwargs)  # Chama o método inicializador da classe pai (forms.Form)
        self.fields['estado_civil'].choices = self.get_estado_civil_choices()  # Define as opções do campo estado_civil chamando o método get_estado_civil_choices

    def get_estado_civil_choices(self):  # Define um método para obter as opções de estado civil
        with connection.cursor() as cursor:  # Abre uma conexão com o banco de dados
            cursor.execute("SELECT ID_Estado_Civil, Desc_Estado_Civil FROM Estado_Civil")  # Executa uma consulta SQL para obter os estados civis
            estado_civil_options = cursor.fetchall()  # Armazena os resultados da consulta em uma variável
        return [(str(option[0]), option[1]) for option in estado_civil_options]  # Retorna uma lista de tuplas com os IDs e descrições dos estados civis
    