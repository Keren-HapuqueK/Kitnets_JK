from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, cadastrar_view, inicio_view

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Mantemos apenas esta
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path("cadastrar/", cadastrar_view, name="cadastrar"),
    path('inicio/', inicio_view, name='inicio'),

    # URLs para redefinição de senha
    path('reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset.html'), name='reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
]
