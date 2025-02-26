from django.contrib import admin

from .models import (Apprenants, Enseignants, Message_apprenants,
                     Message_enseignants, Document)


# Classe d'administration pour les enseignants
@admin.register(Enseignants)
class EnseignantsAdmin(admin.ModelAdmin):
    # Colonnes à afficher dans la liste des enseignants
    list_display = ('user', 'nom', 'prenom', 'matieres', 'contacts', 'experiences', 'niveau', 'quartier')

    # Ajout de filtres pour faciliter la recherche et la gestion des enseignants
    list_filter = ('niveau', 'matieres', 'quartier')
 
    # Ajout d'une fonctionnalité de recherche par nom, prénom et matière
    search_fields = ('nom', 'prenom', 'matieres')

    # Définir les champs à afficher pour l'ajout ou la modification d'un enseignant
    fieldsets = (
        (None, {
            'fields': ('user', 'nom', 'prenom', 'matieres', 'contacts', 'experiences', 'niveau', 'quartier')
        }),
    )

# Classe d'administration pour les apprenants
@admin.register(Apprenants)
class ApprenantsAdmin(admin.ModelAdmin):
    # Colonnes à afficher dans la liste des apprenants
    list_display = ('user', 'nom', 'prenom', 'niveau', 'modalites', 'objectifs', 'ecole', 'moyenne')

    # Ajout de filtres pour faciliter la recherche et la gestion des apprenants
    list_filter = ('niveau', 'matieres', 'ecole')

    # Ajout d'une fonctionnalité de recherche par nom, prénom et matière
    search_fields = ('nom', 'prenom', 'matieres', 'ecole')

    # Définir les champs à afficher pour l'ajout ou la modification d'un apprenant
    fieldsets = (
        (None, {
            'fields': ('user', 'nom', 'prenom', 'niveau', 'matieres', 'objectifs', 'modalites', 'ecole', 'moyenne')
        }),
    )
@admin.register(Message_apprenants)
class Message_apprenantsAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'date_sent')

@admin.register(Message_enseignants)
class Message_enseignantsAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'date_sent')
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title', 'description')