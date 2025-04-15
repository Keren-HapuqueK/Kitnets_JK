from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, cadastrar_view, inicio_view

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # URL for the login page
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),  # URL for logging out
    path("cadastrar/", cadastrar_view, name="cadastrar"),  # URL for the registration page
    path('inicio/', inicio_view, name='inicio'),  # URL for the home page

    # URLs for password reset functionality
    path('reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset.html'), name='reset'),  # URL to request a password reset
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),  # URL for password reset done page
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),  # URL to confirm the password reset
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),  # URL for password reset complete page
]
