# Dans urls.py de l'application authentication

from django.urls import path

from . import views

app_name= 'authentication'

urlpatterns = [
    path('loging/', views.login_user, name = 'loging'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
     path('loging_required/', views.loging_required, name='loging_required'),
]
