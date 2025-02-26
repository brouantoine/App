from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    name = forms.CharField(
        required=True,
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        required=True,
        label='Prénoms',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email_or_phone = forms.CharField(
        required=True,
        label='Numéro de téléphone ou adresse e-mail',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=None
    )
    password2 = forms.CharField(
        label='Confirmation du mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=None
    )

    class Meta:
        model = User
        fields = ('username', 'name', 'last_name', 'email_or_phone', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Nom d'utilisateur déjà pris.")
        return username

    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data.get('email_or_phone')
        if User.objects.filter(email=email_or_phone).exists() or Profile.objects.filter(phone_number=email_or_phone).exists():
            raise ValidationError("Adresse e-mail ou numéro de téléphone déjà utilisé.")
        return email_or_phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email_or_phone']
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data['email_or_phone'],
            )
        return user
# authentication/forms.py

from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        try:
            # Valider le mot de passe
             validate_password(password1, self.user)
        except ValidationError as error:
            # Stocker l'erreur pour l'afficher après soumission
            self.add_error('new_password1', error)
        return password1
