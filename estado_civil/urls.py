from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_estados_civis, name='listar_estados_civis'),
    path('criar/', views.criar_estado_civil, name='criar_estado_civil'),
    path('editar/<int:id_estado_civil>/', views.editar_estado_civil, name='editar_estado_civil'),
    path('excluir/<int:id_estado_civil>/', views.excluir_estado_civil, name='excluir_estado_civil'),
    path('visualizar/<int:id_estado_civil>/', views.visualizar_estado_civil, name='visualizar_estado_civil'),
]
