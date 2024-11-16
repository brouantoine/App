# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil'  # Nom du profil dans l'interface

class CustomUserAdmin(UserAdmin):
    # Ajouter l'inline pour afficher le profil dans la page de l'utilisateur
    inlines = [ProfileInline]

    # Définir list_display pour afficher les champs du profil
    def education_level(self, obj):
        return obj.profile.education_level if hasattr(obj, 'profile') else 'N/A'
    education_level.short_description = 'Niveau d\'étude'

    def city(self, obj):
        return obj.profile.city if hasattr(obj, 'profile') else 'N/A'
    city.short_description = 'Ville'

    def commune(self, obj):
        return obj.profile.commune if hasattr(obj, 'profile') else 'N/A'
    commune.short_description = 'Commune'

    def district(self, obj):
        return obj.profile.district if hasattr(obj, 'profile') else 'N/A'
    district.short_description = 'Quartier'

    # Mettre à jour list_display pour inclure les champs du profil
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'education_level', 'city', 'commune', 'district')

# Enregistrer la nouvelle classe d'admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


from django.contrib import admin
from django.utils.safestring import mark_safe


class CustomAdminSite(admin.AdminSite):
    def get_media(self):
        media = super().get_media()
        media.add_css({'all': ('css/Admin.css',)})
        return media

admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(User, CustomUserAdmin)
