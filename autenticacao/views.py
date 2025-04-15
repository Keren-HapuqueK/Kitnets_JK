from django.contrib.auth import authenticate, login, logout  # Importa funções de autenticação, login e logout do Django
from django.contrib.auth.decorators import login_required  # Importa o decorador para exigir login
from django.shortcuts import render, redirect  # Importa funções para renderizar templates e redirecionar URLs
from django.contrib import messages  # Importa o sistema de mensagens do Django
from django.http import JsonResponse  # Importa a classe JsonResponse para retornar respostas JSON
from .forms import CustomAuthenticationForm, CustomUserCreationForm  # Importa formulários personalizados

def login_view(request):  # Define a view para login
    if request.method == "POST":  # Verifica se o método da requisição é POST
        form = CustomAuthenticationForm(request, data=request.POST)  # Cria uma instância do formulário de autenticação com os dados do POST
        if form.is_valid():  # Verifica se o formulário é válido
            user = form.get_user()  # Obtém o usuário autenticado
            login(request, user)  # Faz o login do usuário
            return redirect("inicio")  # Redireciona para a página inicial
    else:  # Se o método da requisição não for POST
        form = CustomAuthenticationForm()  # Cria uma instância vazia do formulário de autenticação

    return render(request, "registration/login.html", {"form": form})  # Renderiza a página de login com o formulário

@login_required  # Exige que o usuário esteja logado para acessar esta view
def inicio_view(request):  # Define a view para a página inicial
    return render(request, 'inicio.html')  # Renderiza a página inicial

def logout_view(request):  # Define a view para logout
    logout(request)  # Faz o logout do usuário
    messages.info(request, "Você saiu da sua conta.")  # Adiciona uma mensagem informando que o usuário saiu da conta
    return redirect('login')  # Redireciona para a página de login

def cadastrar_view(request):  # Define a view para cadastro de novos usuários
    if request.method == "POST":  # Verifica se o método da requisição é POST
        form = CustomUserCreationForm(request.POST)  # Cria uma instância do formulário de criação de usuário com os dados do POST
        if form.is_valid():  # Verifica se o formulário é válido
            form.save()  # Salva o novo usuário
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")  # Adiciona uma mensagem de sucesso
            return redirect('login')  # Redireciona para a página de login
        else:  # Se o formulário não for válido
            for field in form:  # Itera sobre os campos do formulário
                for error in field.errors:  # Itera sobre os erros de cada campo
                    messages.error(request, f"{field.label}: {error}")  # Adiciona uma mensagem de erro para cada campo
            for error in form.non_field_errors():  # Itera sobre os erros não relacionados a campos específicos
                messages.error(request, error)  # Adiciona uma mensagem de erro geral
    else:  # Se o método da requisição não for POST
        form = CustomUserCreationForm()  # Cria uma instância vazia do formulário de criação de usuário
    return render(request, "registration/cadastrar.html", {"form": form})  # Renderiza a página de cadastro com o formulário
