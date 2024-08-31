from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bio, Service, CmdService, Avis, Realisation, Commentaire


# Modèle pour UserProfile (avec affichage des champs importants)
class UserAdmin(UserAdmin):
    list_display = ('email', 'noms', 'sexe', 'pays', 'tel', 'is_staff', 'is_active')
    search_fields = ('email', 'noms')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('noms', 'sexe', 'pays', 'tel')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

class BioAdmin(admin.ModelAdmin):
    list_display = ('id','titre', 'date_modification')
    search_fields = ('titre',)
    prepopulated_fields = {'slug': ('titre',)} 

# Modèle pour Service (admin seul peut gérer le prix et la qualité)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'nom', 'detail_short', 'detail_long', 'image', 'prix', 'note_moyenne', 'qualite')
    search_fields = ('nom',)
    list_filter = ('prix', 'qualite')
    list_editable = ('position',)
    readonly_fields = ('note_moyenne',)  # Empêche la modification manuelle
    fields = ('nom', 'detail_short', 'detail_long', 'image', 'prix', 'note_moyenne', 'qualite')
    def save_model(self, request, obj, form, change):
        obj.save()  # Appelle la méthode `save()` du modèle

# Modèle pour CmdService
class CmdServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_users', 'service', 'date_cmd', 'prix_cmd')
    search_fields = ('user__noms', 'service__nom')
    list_filter = ('date_cmd',)
    autocomplete_fields = ['user', 'service']

    def get_users(self, obj):
        return obj.user.noms  # Accédez directement aux noms de l'utilisateur



# Modèle pour Avis
class AvisAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'note', 'texte')
    search_fields = ('user__noms', 'service__nom')
    list_filter = ('note',)

# Modèle pour Realisation (affichage image ou vidéo géré par admin)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'nom_client', 'lieu_real', 'date_real', 'display_content')
    search_fields = ('titre', 'nom_client')
    list_filter = ('date_real',)

    # Action pour approuver ou désapprouver les réalisations
    actions = ['marquer_comme_approuve']

    def marquer_comme_approuve(self, request, queryset):
        queryset.update(approuve=True)
        self.message_user(request, f"{queryset.count()} réalisations approuvées.")
    marquer_comme_approuve.short_description = "Marquer les réalisations sélectionnées comme approuvées"

# Modèle pour Commentaire
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'realisation', 'contenu', 'date_com')
    search_fields = ('user__noms', 'realisation__titre')
    list_filter = ('date_com',)

    actions = ['supprimer_commentaires']

    def supprimer_commentaires(self, request, queryset):
        queryset.delete()
        self.message_user(request, f"{queryset.count()} commentaires supprimés.")
    supprimer_commentaires.short_description = "Supprimer les commentaires sélectionnés"

# Enregistrement des modèles dans l'interface d'administration
admin.site.register(User, UserAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(CmdService, CmdServiceAdmin)
admin.site.register(Avis, AvisAdmin)
admin.site.register(Realisation, RealisationAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
admin.site.register(Bio, BioAdmin)
