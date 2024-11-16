from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

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
    EDUCATION_LEVEL_CHOICES = [
        ('Seconde', '2nde A'), ('Seconde', '2nde C'), ('Seconde', '2nde G2'),
        ('Premiere', '1ère A'), ('Premiere', '1ère D'), ('Premiere', '1ère C'),
        ('Premiere', '1ère G2'), ('Terminale', 'Terminale A'), ('Terminale', 'Terminale C'),
        ('Terminale', 'Terminale D'), ('Terminale', 'Terminale G2'), ('cours preparatoir1', 'CP1'),
        ('cours preparatoir1', 'CP2'), ('cours élémentaire1', 'CE1'), ('cours élémentaire2', 'CE2'),
        ('Cours moyen1', 'CM1'), ('Cours moyen2', 'CM2'), ('Sixième', '6eme'),
        ('Cinquième', '5eme'), ('quartrième', '4eme'), ('Troixième', '3eme'),
    ]
    education_level = forms.ChoiceField(
        required=True,
        label="Niveau d'étude",
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=EDUCATION_LEVEL_CHOICES
    )
    city = forms.ChoiceField(
        required=True,
        label='Ville',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[
            ('Abidjan', 'Abidjan'), ('Bouaké', 'Bouaké'), ('Daloa', 'Daloa')
            # Ajoutez toutes les villes ici
        ]
    )
    commune = forms.CharField(
        required=True,
        label='Commune',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    district = forms.CharField(
        required=True,
        label='Quartier',
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
        fields = ('username', 'name', 'last_name', 'email_or_phone', 'education_level', 'city', 'commune', 'district', 'password1', 'password2')

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
                education_level=self.cleaned_data['education_level'],
                city=self.cleaned_data['city'],
                commune=self.cleaned_data['commune'],
                district=self.cleaned_data['district']
            )
        return user
