from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_locadores, name='listar_locadores'),
    path('criar/', views.criar_locador, name='criar_locador'),
    path('editar/<int:id_locador>/', views.editar_locador, name='editar_locador'),
    path('excluir/<int:id_locador>/', views.excluir_locador, name='excluir_locador'),
]
