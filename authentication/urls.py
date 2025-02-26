# Dans urls.py de l'application authentication

from django.urls import path
from Repetiteurs import views
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views  # Importez les vues d'authentification

app_name= 'authentication'

urlpatterns = [
    path('loging/', views.login_user, name = 'loging'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
     path('loging_required/', views.loging_required, name='loging_required'),
path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
]