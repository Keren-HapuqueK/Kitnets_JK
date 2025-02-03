from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("inicio")  # Redireciona para a página inicial
            else:
                messages.error(request, "Usuário ou senha incorretos. Tente novamente.")
        else:
            messages.error(request, "Erro no login. Verifique os campos e tente novamente.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


@login_required
def inicio_view(request):
    return render(request, 'inicio.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def cadastrar_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect('login')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/cadastrar.html", {"form": form})
