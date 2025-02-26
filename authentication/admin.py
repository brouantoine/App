# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    # pour afficher le profil dans la page de l'utilisateur
    inlines = [ProfileInline]

    #  list_display pour inclure les champs du profil
list_display = ('username', 'first_name', 'last_name', 'email',)

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