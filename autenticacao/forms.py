from django import forms  # Importa o módulo de formulários do Django
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # Importa formulários de autenticação e criação de usuário do Django
from django.contrib.auth.models import User  # Importa o modelo de usuário do Django
from django.core.exceptions import ValidationError  # Importa a exceção de validação do Django

class CustomAuthenticationForm(AuthenticationForm):  # Define um formulário de autenticação personalizado
    username = forms.CharField(label="Nome de Usuário ou Email", max_length=254)  # Campo de texto para nome de usuário ou email
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)  # Campo de senha com widget de entrada de senha

    def clean_username(self):  # Método para limpar e validar o campo de nome de usuário
        username = self.cleaned_data.get('username')  # Obtém o valor do campo de nome de usuário
        user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()  # Procura um usuário com o nome de usuário ou email fornecido
        
        if user is None:  # Se nenhum usuário for encontrado
            raise forms.ValidationError("Usuário ou email não encontrado. Verifique e tente novamente.")  # Levanta um erro de validação
        
        return user.username  # Retorna o nome de usuário real do banco de dados

class CustomUserCreationForm(UserCreationForm):  # Define um formulário de criação de usuário personalizado
    email = forms.EmailField(label="Email", required=True)  # Campo de email obrigatório

    class Meta:  # Metadados do formulário
        model = User  # Modelo associado ao formulário
        fields = ["username", "email", "password1", "password2"]  # Campos incluídos no formulário

    def clean_email(self):  # Método para limpar e validar o campo de email
        email = self.cleaned_data.get("email")  # Obtém o valor do campo de email
        if User.objects.filter(email=email).exists():  # Verifica se já existe um usuário com o email fornecido
            raise forms.ValidationError("Este email já está em uso.")  # Levanta um erro de validação
        return email  # Retorna o email validado
    
    def clean_password2(self):  # Método para limpar e validar o campo de confirmação de senha
        password1 = self.cleaned_data.get("password1")  # Obtém o valor do campo de senha
        password2 = self.cleaned_data.get("password2")  # Obtém o valor do campo de confirmação de senha
        if password1 and password2 and password1 != password2:  # Verifica se as senhas não coincidem
            raise ValidationError("As senhas não coincidem.")  # Levanta um erro de validação
        return password2  # Retorna a confirmação de senha validada