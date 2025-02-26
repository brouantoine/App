from django import forms
from django.contrib.auth.models import ProfilUtilisateur
from django.db import models


class CustomUserCreationForm(ProfilUtilisateur):
    choix_niveau = [
        ('Seconde', '2nde A'), ('Seconde', '2nde C'), ('Seconde', '2nde G2'),
        ('Premiere', '1ère A'), ('Premiere', '1ère D'), ('Premiere', '1ère C'),
        ('Premiere', '1ère G2'), ('Terminale', 'Terminale A'), ('Terminale', 'Terminale C'),
        ('Terminale', 'Terminale D'), ('Terminale', 'Terminale G2'), ('cours preparatoir1', 'CP1'),
        ('cours preparatoir1', 'CP2'), ('cours élémentaire1', 'CE1'), ('cours élémentaire2', 'CE2'),
        ('Cours moyen1', 'CM1'), ('Cours moyen2', 'CM2'), ('Sixième', '6eme'),
        ('Cinquième', '5eme'), ('quartrième', '4eme'), ('Troixième', '3eme'),
    ]
    niveau  = forms.ChoiceField(
    required=True,
    label="Niveau d'étude",
    widget=forms.Select(attrs={'class': 'form-control'}),
    choices=choix_niveau
    )