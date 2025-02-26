from django.contrib.auth.models import User
from django.db import models


class ProfilUtilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100,)
    matieres = models.TextField( choices=[
        ('Sciences' , 'Sciences'), ('Lettres','Lettres'), ('Sciences et lettres', 'Sciences et lettres'),
    ])
    class Meta: 
        abstract = True
        
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class Apprenants(ProfilUtilisateur):
    niveau = models.CharField(max_length=100,)
    modalites = models.CharField(max_length=50, null=True)
    objectifs = models.TextField(blank=True, null=True)
    ecole = models.TextField(max_length=255, null=True)
    moyenne = models.TextField(max_length=50, null= True)
    
    
class Enseignants(ProfilUtilisateur):
    contacts = models.CharField(max_length=15, null=True)
    experiences = models.TextField(max_length=25,)
    niveau = models.TextField(max_length=25, null=True)
    quartier = models.TextField(max_length=50, null=True)
    
    
class Message_apprenants(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Apprenants, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient.nom}"
    
class Message_enseignants(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Enseignants, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.sender} to {self.recipient.nom}"

from django.db import models

from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    file = models.FileField(upload_to='documents/', verbose_name="Fichier")
    page_count = models.IntegerField(default=0, verbose_name="Nombre de pages")
    popularity = models.IntegerField(default=0, verbose_name="Popularité")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"