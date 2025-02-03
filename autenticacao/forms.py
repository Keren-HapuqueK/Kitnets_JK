from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Nome de Usuário ou Email", max_length=254)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()
        
        if user is None:
            raise forms.ValidationError("Usuário ou email não encontrado. Verifique e tente novamente.")
        
        return user.username  # Retorna o username real do banco de dados

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
