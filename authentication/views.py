from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from .forms import CustomUserCreationForm
from .models import Profile


@csrf_protect
def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Repetiteurs:home')
        else:
            messages.info(request, "Identifiants incorrects")
            
    form = AuthenticationForm()
    return render(request, "authentication/loging.html", {"form": form})

@csrf_protect
def logout_user(request):
    logout(request)
    return redirect("Repetiteurs:home")

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError

# def register_user(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f"Compte créé pour {username}!")
#             return redirect("Repetiteurs:home")
#     else:
#         form = UserCreationForm()
#     return render(request, "authentication/register.html", {"form": form})

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            try:
                # Sauvegarde de l'utilisateur
                user = form.save(commit=False)
                user.save()  # Sauvegarde l'utilisateur ici avant de créer le profil
                
                # Création du profil associé à l'utilisateur
                profile = Profile.objects.create(
                    user=user,
                    education_level=form.cleaned_data.get('education_level'),
                    city=form.cleaned_data.get('city'),
                    commune=form.cleaned_data.get('commune'),
                    district=form.cleaned_data.get('district'),
                    phone_number=form.cleaned_data.get('email_or_phone')
                )

                # Authentification et redirection après inscription réussie
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('Repetiteurs:home')  # Rediriger vers une page appropriée après l'inscription

            except IntegrityError as e:
                if 'UNIQUE constraint' in str(e):
                    messages.error(request, "L'adresse email ou le numéro de téléphone existe déjà.")
                else:
                    messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')

                # Retourner le formulaire avec les erreurs
                return render(request, 'authentication/loging.html', {'form': form})

        else:
            # Si le formulaire n'est pas valide, retourner à la page de connexion avec les erreurs
            return render(request, 'authentication/loging.html', {'form': form})

    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/register.html', {'form': form})

def loging_required(request):
    return render(request, 'authentication/loging_required.html')