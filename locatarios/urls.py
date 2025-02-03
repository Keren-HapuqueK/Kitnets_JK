from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_locatarios, name='listar_locatarios'),
    path('criar/', views.criar_locatario, name='criar_locatario'),
    path('editar/<int:id_locatario>/', views.editar_locatario, name='editar_locatario'),
    path('excluir/<int:id_locatario>/', views.excluir_locatario, name='excluir_locatario'),
]
