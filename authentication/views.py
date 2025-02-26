from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (AuthenticationForm)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from .forms import CustomUserCreationForm
from .models import Profile


# Vue pour la connexion des utilisateurs
@csrf_protect
def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Repetiteurs:home')  # Redirection après connexion réussie
        else:
            messages.info(request, "Identifiants incorrects")  # Message d'erreur si échec
            
    form = AuthenticationForm()  # Formulaire de connexion Django
    return render(request, "authentication/loging.html", {"form": form})


# Vue pour la déconnexion des utilisateurs
@csrf_protect
def logout_user(request):
    logout(request)  # Déconnexion de l'utilisateur
    return redirect("Repetiteurs:home")  # Redirection vers la page d'accueil


# Vue pour l'inscription des utilisateurs
def register_user(request):
    # Initialisation du formulaire d'inscription personnalisé
    form = CustomUserCreationForm(request.POST or None)

    # Si la méthode est POST et que le formulaire est valide
    if request.method == 'POST' and form.is_valid():
        # Vérification des doublons sur email/numéro de téléphone
        email_or_phone = form.cleaned_data.get('email_or_phone')
        
        if Profile.objects.filter(phone_number=email_or_phone).exists():
            messages.error(request, "L'adresse email ou le numéro de téléphone existe déjà.")
        else:
            # Création de l'utilisateur et enregistrement dans la base
            user = form.save()

            # Création du profil utilisateur
            try:
                # Assurez-vous que l'email ou le numéro de téléphone n'existe pas déjà
                if not Profile.objects.filter(user=user).exists():
                    profile = Profile.objects.create(user=user, phone_number=email_or_phone)
                else:
                    profile = Profile.objects.get(user=user)
            except IntegrityError as e:
                # Gestion de l'erreur en cas de duplication de la clé
                messages.error(request, "Erreur lors de la création du profil utilisateur. Veuillez réessayer.")
                return redirect('authentication:register')

            # Authentification automatique de l'utilisateur
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirection après l'inscription
                messages.success(request, "Votre compte a été créé avec succès !")
                return redirect('Repetiteurs:home')

    # Rendu du formulaire (avec messages d'erreur si nécessaire)
    return render(request, 'authentication/register.html', {'form': form})


# Vue pour afficher une page indiquant que la connexion est requise
def loging_required(request):
    return render(request, 'authentication/loging_required.html')
from django.contrib.auth import views as auth_views
from django.urls import path

from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Vue pour la demande de réinitialisation de mot de passe
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Réinitialisation de mot de passe"
                    email_template_name = "authentication/registration/password_reset_email.html"
                    context = {
                        "email": user.email,
                        "domain": request.get_host(),  # Récupère automatiquement le domaine et le port (ex: localhost:8000)
                        "site_name": "e_School",  # Nom du site
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",  # Utilisez HTTP en local
                            }
                    email_message = render_to_string(email_template_name, context)
                    send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email])
                return redirect('authentication:password_reset_done')
            else:
                messages.error(request, "Aucun utilisateur trouvé avec cette adresse email.")
    else:
        form = PasswordResetForm()
    return render(request, 'authentication/registration/password_reset.html', {'form': form})

# Vue pour la confirmation d'envoi de l'email
def password_reset_done(request):
    return render(request,'authentication/registration/password_reset_done.html')

# Vue pour la saisie du nouveau mot de passe
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError

# authentication/views.py

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from .forms import CustomSetPasswordForm  # Importez le formulaire personnalisé

# authentication/views.py

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from .forms import CustomSetPasswordForm  # Importez le formulaire personnalisé

from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from .forms import CustomSetPasswordForm  # Import du formulaire personnalisé

User = get_user_model()

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Votre mot de passe a été réinitialisé avec succès !")
                return redirect('authentication:password_reset_complete')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'authentication/registration/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
        return render(request, 'authentication/registration/password_reset_invalid.html')

# Vue pour la confirmation de réinitialisation réussie
def password_reset_complete(request):
    return render(request, 'authentication/registration/password_reset_complete.html')