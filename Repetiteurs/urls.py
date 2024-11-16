from django.urls import path

from . import views

app_name = "Repetiteurs"

urlpatterns = [
    path('', views.home, name='home'),
    path('primaire/', views.que_cherchez_vous, name='que_cherchez_vous'),
    path('connecte/', views.connecte, name='connecte'),
    path('groupeEtude/', views.groupeEtude, name='groupeEtude'),
    path('Apropos/', views.Apropos, name='Apropos'),
    path('verifier_demande/', views.verifier_demande, name='verifier_demande'),
    path('rechercher_soutien/', views.rechercher_soutien, name='rechercher_soutien'),
    path('creer_profile/', views.creer_profile, name='creer_profile'),
]
