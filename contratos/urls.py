from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_contratos, name='listar_contratos'),
    path('criar/', views.criar_contrato, name='criar_contrato'),
    path('editar/<int:id_contrato>/', views.editar_contrato, name='editar_contrato'),
    path('excluir/<int:id_contrato>/', views.excluir_contrato, name='excluir_contrato'),
    path('visualizar/<int:id_contrato>/', views.visualizar_contrato, name='visualizar_contrato'),
]
