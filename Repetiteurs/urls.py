from django.urls import path

from . import views

app_name = "Repetiteurs"

urlpatterns = [
    path('', views.home, name='home'),
    path('primaire/', views.que_cherchez_vous, name='que_cherchez_vous'),
    path('groupeEtude/', views.groupeEtude, name='groupeEtude'),
    path('Apropos/', views.Apropos, name='Apropos'),
    path('rechercher_soutien/', views.rechercher_soutien, name='rechercher_soutien'),
    path('creer_profile/', views.creer_profile, name='creer_profile'),
    path('profiles_enseignants/', views.profiles_enseignants, name='profiles_enseignants'),
    path('profiles_etudiants/', views.profiles_etudiants, name='profiles_etudiants'),
    path('creer_profile_enseignants_base/', views.creer_profile_enseignants_base, name='creer_profile_enseignants_base'),
    path('enseignants_details/', views.Enseignants_details, name='enseignants_details'),
    path('apprenants_details/<int:profil_id>/', views.apprenants_details, name='apprenants_details'),
    path('enseignants_details/<int:profil_id>/', views.enseignants_details, name='enseignants_details'),
    path('verifier_demande/', views.verifier_demande, name='verifier_demande'),
    path('repondre_message/<int:recipient_id>/', views.repondre_message, name='repondre_message'),
    path('je-m-exerce/', views.je_m_exerce, name='je_m_exerce'),
path('ajouter_document/', views.ajouter_document, name='ajouter_document'),
]