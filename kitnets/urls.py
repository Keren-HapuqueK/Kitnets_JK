from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_imoveis, name='listar_imoveis'),
    path('criar/', views.criar_imovel, name='criar_imovel'),
    path('editar/<int:id_imovel>/', views.editar_imovel, name='editar_imovel'),
    path('excluir-imovel/<int:id_imovel>/', views.excluir_imovel, name='excluir_imovel'),
    path('visualizar/<int:id_imovel>/', views.visualizar_imovel, name='visualizar_imovel'),
]
