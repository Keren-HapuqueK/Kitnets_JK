from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_locatarios, name='listar_locatarios'),
    path('criar/', views.criar_locatario, name='criar_locatario'),
    path('editar/<int:id_locatario>/', views.editar_locatario, name='editar_locatario'),
    path('locatarios/excluir/<int:id_locatario>/', views.excluir_locatario, name='excluir_locatario'),
    path('visualizar/<int:id_locatario>/', views.visualizar_locatario, name='visualizar_locatario'),
]
