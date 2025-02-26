from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from Repetiteurs.models import (Apprenants, Enseignants, Message_apprenants,
                     Message_enseignants, Document)


# Create your views here.
def home (request):
    return render(request, 'Repetiteurs/page_de_base/home.html')
def hom (request):
    return render(request, 'Repetiteurs/page_de_base/hom.html')
def groupeEtude(request):
    return render (request, 'Repetiteurs/page_de_base/groupeEtude.html') 
def Apropos(request):
    return render (request, 'Repetiteurs/page_de_base/Apropos.html') 



@login_required
def rechercher_soutien(request):
    return render(request, 'Repetiteurs/rechercher_soutien.html')


def que_cherchez_vous(request):
    source = request.GET.get('source')
    if source == "primaire":
        gabarit = 'Repetiteurs/profiles_apprenants/niveaux/eleve_du_primaire.html' 
    elif source == "secondaire":
        gabarit = 'Repetiteurs/profiles_apprenants/niveaux/secondaire.html'
    elif source == "etudiant":
        gabarit = 'Repetiteurs/profiles_apprenants/niveaux/etudiant.html' 
    elif source == "enseignant":
        gabarit = 'Repetiteurs/enseignants/page_que_cherchez_vous/enseignant.html'
    else:
        gabarit = None
    
    return render(request, 'Repetiteurs/page_de_base/base_que cherchez_vous/que_cherchez_vous.html', {'gabarit': gabarit}) 



@login_required
def creer_profile(request):
    source = request.GET.get('source')
    print(f"Valeur de source : {source}")  # Vérifier la source

    # Vérifier la présence du profil
    user = request.user
    profil = Apprenants.objects.filter(user=user).first()

    # Configurations des sources et gabarits
    gabarits = {
        "creer_profil_apprenant": "Repetiteurs/profiles_apprenants/creer_profiles/creer_profil_apprenants.html", 
    }

    # Vérifier si la source est valide
    gabarit = gabarits.get(source)
    if not gabarit:
        print(f"Source invalide ou manquante : {source}")  # Log si la source est invalide
        return redirect('Repetiteurs:home')  # Rediriger si la source est invalide

    # Traiter le formulaire POST
    if request.method == 'POST':
        print(f"Data POST : {request.POST}")  # Log pour vérifier les données POST
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        niveau = request.POST.get('niveau')
        matieres = request.POST.get('matieres')
        objectifs = request.POST.get('objectifs')
        modalites = request.POST.get('modalites')
        ecole = request.POST.get('ecole')
        moyenne = request.POST.get('moyenne')

        # Validation des champs requis
        if not nom or not prenom:
            return render(request, gabarit, {
                'error': "Les champs Nom et Prénom sont obligatoires.",
            })

        # Mise à jour ou création du profil
        try:
            if profil:
                profil.nom = nom
                profil.prenom = prenom
                profil.niveau = niveau
                profil.matieres = matieres
                profil.objectifs = objectifs
                profil.modalites = modalites
                profil.ecole = ecole
                profil.moyenne = moyenne
                profil.save()
            else:
                Apprenants.objects.create(
                    user=user,
                    nom=nom,
                    prenom=prenom,
                    niveau=niveau,
                    matieres=matieres,
                    objectifs=objectifs,
                    modalites=modalites,
                    ecole=ecole,
                    moyenne=moyenne,
                )
            print("Profil sauvegardé avec succès.")  # Log pour confirmer la sauvegarde
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")  # Log des erreurs

        return redirect('Repetiteurs:home')  # Rediriger après la sauvegarde

    # Préparer les données initiales pour le formulaire
    initial_data = {
        'nom': profil.nom if profil else user.first_name,
        'prenom': profil.prenom if profil else user.last_name,
    }

    # Affichage du formulaire avec gabarit spécifique
    return render(request, gabarit, {
        'initial_data': initial_data,
    })


@login_required
def creer_profile_enseignants_base(request):
    source = request.GET.get('source')
    print(f"Valeur de source : {source}")  # Vérifier la source

    # Vérifier la présence du profil
    user = request.user
    profil = Enseignants.objects.filter(user=user).first()

    # Configurations des sources et gabarits
    gabarits = {
        "creer_profil_enseignant": "Repetiteurs/enseignants/creer_profiles/creer_profil_enseignants.html", 
    }

    # Vérifier si la source est valide
    gabarit = gabarits.get(source)
    if not gabarit:
        print(f"Source invalide ou manquante : {source}")  # Log si la source est invalide
        return redirect('Repetiteurs:home')  # Rediriger si la source est invalide

    # Traiter le formulaire POST
    if request.method == 'POST':
        print(f"Data POST : {request.POST}")  # Log pour vérifier les données POST
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        matieres = request.POST.get('matieres')
        contacts = request.POST.get('contacts')
        experiences = request.POST.get('experiences')
        niveau = request.POST.get('niveau')
        quartier = request.POST.get('quartier')

        # Validation des champs requis
        if not nom or not prenom:
            return render(request, gabarit, {
                'error': "Les champs Nom et Prénom sont obligatoires.",
            })

        # Mise à jour ou création du profil
        try:
            if profil:
                profil.nom = nom
                profil.prenom = prenom
                profil.matieres = matieres
                profil.contacts = contacts
                profil.experiences = experiences
                profil.niveau = niveau
                profil.quartier = quartier
                profil.save()
            else:
                Enseignants.objects.create(
                    user=user,
                    nom=nom,
                    prenom=prenom,
                    matieres=matieres,
                    contacts=contacts,
                    experiences=experiences,
                    niveau=niveau,
                    quartier=quartier,
                )
            print("Profil sauvegardé avec succès.")  # Log pour confirmer la sauvegarde
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")  # Log des erreurs

        return redirect('Repetiteurs:home')  # Rediriger après la sauvegarde

    # Préparer les données initiales pour le formulaire
    initial_data = {
        'nom': profil.nom if profil else user.first_name,
        'prenom': profil.prenom if profil else user.last_name,
    }

    # Affichage du formulaire avec gabarit spécifique
    return render(request, gabarit, {
        'initial_data': initial_data,
    })



def profiles_enseignants(request):
    enseignants = Enseignants.objects.all().order_by('-id')
    
    context = {
        'enseignants': enseignants,
    }
    return render(request, 'Repetiteurs/enseignants/profiles/profiles_enseignants.html', context)  


def profiles_etudiants(request):
    apprenants = Apprenants.objects.all().order_by('-id')
    
    context = {
        'apprenants': apprenants
    }
    return render(request, 'Repetiteurs/profiles_apprenants/creer_profiles/profiles_etudiants.html', context)


def Enseignants_details(request):
    pass


def apprenants_details(request, profil_id):  
    apprenants = get_object_or_404(Apprenants, id=profil_id)
    print (apprenants)
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            # Enregistrer le message dans la base de données
            message = Message_apprenants.objects.create(
                sender=request.user if request.user.is_authenticated else None,
                recipient=apprenants,
                content=message_content
            )
    return render(request, 'Repetiteurs/profiles_apprenants/apprenants_details.html', {'apprenants': apprenants})



def enseignants_details(request, profil_id):
    enseignants = get_object_or_404(Enseignants, id=profil_id)
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            message = Message_enseignants.objects.create(
                sender=request.user if request.user.is_authenticated else None,
                recipient=enseignants,
                content=message_content
            )
    return render(request, 'Repetiteurs/enseignants/profiles/enseignants_details.html', {'enseignants':enseignants})

@login_required
def verifier_demande(request):
    # Vérifier si l'utilisateur est connecté
    if not request.user.is_authenticated:
        return render(request, 'Repetiteurs/verifier_demande.html', {'error': "Vous devez être connecté pour voir vos messages."})
    
    # Identifier le profil connecté (Apprenant ou Enseignant)
    apprenant = Apprenants.objects.filter(user=request.user).first()
    enseignant = Enseignants.objects.filter(user=request.user).first()

    # Récupérer les messages pour le profil connecté
    if apprenant:
        messages = Message_apprenants.objects.filter(recipient=apprenant).order_by('-date_sent')
    elif enseignant:
        messages = Message_enseignants.objects.filter(recipient=enseignant).order_by('-date_sent')
    else:
        # Si aucun profil n'est associé à l'utilisateur connecté
        return render(request, 'Repetiteurs/verifier_demande.html', {'error': "Aucun profil associé à cet utilisateur."})

    return render(request, 'Repetiteurs/verifier_demande.html', {'messages': messages})



@login_required
def get_conversation(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    apprenant = Apprenants.objects.filter(user=recipient).first()
    enseignant = Enseignants.objects.filter(user=recipient).first()

    if apprenant:
        messages = (Message_apprenants.objects.filter(sender=request.user, recipient=apprenant) |
                    Message_apprenants.objects.filter(sender=recipient, recipient__user=request.user))
    elif enseignant:
        messages = (Message_enseignants.objects.filter(sender=request.user, recipient=enseignant) |
                    Message_enseignants.objects.filter(sender=recipient, recipient__user=request.user))
    else:
        return JsonResponse({'error': 'Utilisateur invalide !'}, status=400)

    messages = messages.order_by('date_sent').values('sender__username', 'content', 'date_sent')
    return JsonResponse(list(messages), safe=False)

@login_required
@csrf_exempt
def repondre_message(request, recipient_id):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        recipient = get_object_or_404(User, id=recipient_id)
        apprenant = Apprenants.objects.filter(user=recipient).first()
        enseignant = Enseignants.objects.filter(user=recipient).first()

        if apprenant:
            Message_apprenants.objects.create(sender=request.user, recipient=apprenant, content=content)
        elif enseignant:
            Message_enseignants.objects.create(sender=request.user, recipient=enseignant, content=content)
        else:
            return JsonResponse({'success': False, 'error': 'Utilisateur invalide !'}, status=400)

        return JsonResponse({'success': True, 'message': 'Message envoyé !'})

    return JsonResponse({'success': False, 'error': 'Requête invalide !'}, status=400)

def je_m_exerce(request):
    documents = Document.objects.all()
    return render(request, 'Repetiteurs/je_m_exerce/je_m_exerce.html', {'documents': documents})

def ajouter_document(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        document = request.FILES.get('document')
        if not title or not description or not document:
            return render(request, 'Repetiteurs/je_m_exerce/ajouter_document.html', {'error': 'Veuillez remplir tous les champs !'})