from django.db import models

# Create your models here.
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group  # Pour gérer les utilisateurs, y compris toi-même en tant qu'admin
import secrets
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
   



def generate_default_password():
    return secrets.token_urlsafe(32)


# Custom manager pour le modèle User
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Modèle utilisateur personnalisé
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    noms = models.CharField(max_length=255)
    sexe = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    pays = CountryField()
    tel = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['noms']

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        Group,
        related_name='name1',
        blank=True,
        help_text=('The groups this user belongs to. A user may belong to multiple groups. A group typically includes a set of permissions to perform specific operations.')
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='name2',
        blank=True,
        help_text=('Specific permissions for this user.')
    )

    
class Bio(models.Model):
    titre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    detail_court = models.TextField(max_length=500)
    detail = models.TextField()
    date_modification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

# Modèle pour les services
class Service(models.Model):
    position = models.PositiveIntegerField(default=0)
    nom = models.CharField(max_length=255)
    detail_short = models.TextField(max_length=255)
    detail_long = models.TextField()
    image = models.ImageField(upload_to='services/images/', blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Géré par l'admin
    qualite = models.CharField(max_length=50)  # Géré par l'admin
    note_moyenne = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)  # Note moyenne calculée automatiquement

    def __str__(self):
        return self.nom

    # Méthode pour calculer la note moyenne à partir des avis
    def calculer_note_moyenne(self):
        if not self.pk:
            # L'instance n'est pas encore sauvegardée, donc ne pas calculer la note
            return 0
        notes = Avis.objects.filter(service=self).values_list('note', flat=True)
        if notes:
            return sum(notes) / len(notes)
        return 0

    # Redéfinir la méthode save correctement
    def save(self, *args, **kwargs):
        if self.pk:  # Seulement calculer la note si l'instance a déjà été sauvegardée
            self.note_moyenne = self.calculer_note_moyenne()  # Calcule la note moyenne avant d'enregistrer
        super(Service, self).save(*args, **kwargs)  # Appel correct à la méthode save d'origine



# Modèle pour les commandes de services
class CmdService(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_cmd = models.DateField(auto_now_add=True)
    prix_cmd = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Commande de {self.user.noms} pour {self.service.nom}'

    def save(self, *args, **kwargs):
        #actualise le prix de commende en fonction de celui du service
        self.prix_cmd = self.service.prix
        super().save(*args, **kwargs)


# Modèle pour les avis sur les services
class Avis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    note = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=None,  # Valeur par défaut si aucune note n'est attribuée
        null=True,  # Permet de ne pas avoir de note si nécessaire
        blank=True
    )  # Note de 1 à 5, par exemple
    texte = models.TextField(null=True, blank=True)
    date_avis = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avis de {self.user.noms} pour {self.service.nom}'

# Modèle pour les réalisations
class Realisation(models.Model):
    titre = models.CharField(max_length=255)
    detail_short = models.CharField(max_length=255)
    detail_long = models.TextField()
    image = models.ImageField(upload_to='realisations/images/', blank=True, null=True)
    video_short = models.FileField(upload_to='realisations/videos/', blank=True, null=True)
    video_long = models.FileField(upload_to='realisations/videos/', blank=True, null=True)
    date_real = models.DateField()
    lieu_real = models.CharField(max_length=255)
    nom_client = models.CharField(max_length=255)  # Correspond au nom du client servi

    def __str__(self):
        return self.titre

    # Fonction pour restreindre l'affichage des images ou vidéos selon l'admin
    def display_content(self):
        if self.image:
            return 'image'
        elif self.video_short or self.video_long:
            return 'video'
        return 'No content'

# Modèle pour les commentaires sur les réalisations
class Commentaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    realisation = models.ForeignKey(Realisation, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_com = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commentaire de {self.user.noms if self.user else "Utilisateur supprimé"} sur {self.realisation.titre}'