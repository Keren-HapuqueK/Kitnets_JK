"""
URL configuration for projeto_kitnets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')),  # Inclui as rotas de login/logout
    path('autenticacao/', include('django.contrib.auth.urls')),  # Inclui as rotas de redefinição de senha
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('pagamentos/', include('pagamentos.urls')),  # Inclui as rotas de pagamentos
    path('locatarios/', include('locatarios.urls')),  # Inclui as rotas de locatarios
    path('kitnets/', include('kitnets.urls')),  # Inclui as rotas de kitnets
    path('contratos/', include('contratos.urls')),  # Inclui as rotas de contratos
    path('locadores/', include('locadores.urls')),  # Inclui as rotas de locadores
    path('estado_civil/', include('estado_civil.urls')),  # Inclui as rotas de estado civil
    path('inicio.html', TemplateView.as_view(template_name='inicio.html'), name='inicio'),
    path('pagamentos/', include('pagamentos.urls')),  # Inclui as rotas de pagamentos
]
