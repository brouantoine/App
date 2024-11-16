from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


# Create your views here.
def home (request):
    return render(request, 'Repetiteurs/home.html')
def connecte(request):
    return render (request, 'Repetiteurs/connecté.html')
def groupeEtude(request):
    return render (request, 'Repetiteurs/groupeEtude.html')
def Apropos(request):
    return render (request, 'Repetiteurs/Apropos.html')


from django.shortcuts import render


@login_required
def creer_profile(request):
    return render(request, 'Repetiteurs/creer_profile.html')

def rechercher_soutien(request):
    return render(request, 'Repetiteurs/rechercher_soutien.html')

def verifier_demande(request):
    return render(request, 'Repetiteurs/verifier_demande.html')

from django.shortcuts import render


def que_cherchez_vous(request):
    source = request.GET.get('source')
    
    if source == "primaire":
        gabarit = 'Repetiteurs/eleve_du_primaire.html'
    elif source == "secondaire":
        gabarit = 'Repetiteurs/enseignant.html'
    elif source == "etudiant":
        gabarit = 'Repetiteurs/etudiant.html'
    elif source == "enseignant":
        gabarit = 'Repetiteurs/enseignant.html'
    else:
        gabarit = None
    
    return render(request, 'Repetiteurs/que_cherchez_vous.html', {'gabarit': gabarit})
