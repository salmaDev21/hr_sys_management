from django.db import models
from django.conf import settings

class DPT(models.Model):
    name = models.CharField(max_length=100)
    hrbp = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'HRBP'})

    def __str__(self):
        return f"{self.name}"
    

class UEP(models.Model):
    name = models.CharField(max_length=100)
    dpt = models.ForeignKey(DPT, on_delete=models.CASCADE)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'NPLUS1'})

    def __str__(self):
        return f"{self.name}"
    
class Poste(models.Model):
    title = models.CharField(max_length=100)
    uep = models.ForeignKey(UEP, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
    
class Collaborateur(models.Model):
    first_name=models.CharField(max_length=50)
    family_name=models.CharField(max_length=50)
    corporate_id = models.CharField(max_length=50, unique=True) # Constant unique identifier
    matricule = models.CharField(max_length=50)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.family_name}-{self.corporate_id}"
    





class RepriseForm(models.Model):
    collaborateur = models.ForeignKey(Collaborateur, on_delete=models.CASCADE)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)

    date_absence_debut = models.DateField()
    date_absence_fin=models.DateField()

    ABSENCE_TYPES = [
        ('Maladie', 'Maladie'),
        ('Absence injustifiée', 'Absence injustifiée'),
    ]

    type_absence=models.CharField(max_length=50,choices=ABSENCE_TYPES)
    reason = models.TextField()
    is_repetitive=models.BooleanField(default=False)

    FREQUENCY_CHOICES = [
        ('2eme absence', '2eme absence'),
        ('3eme absence', '3eme absence'), 
        ('4eme absence', '4eme absence'),
        ('plus de 4 fois', 'plus de 4 fois'),
    ]

    frequency=models.CharField(max_length=30,choices=FREQUENCY_CHOICES,null=True,blank=True)

    cons_reorganization = models.BooleanField("Réorganisation de l'équipe",default=False)
    cons_recruitment = models.BooleanField("Recrutement",default=False)
    cons_departure = models.BooleanField("Départ de collaborateurs",default=False)
    cons_other = models.BooleanField("Autres (à préciser)",default=False)
    cons_other_details=models.TextField(null=True,blank=True)

    action_adjustment = models.BooleanField("Aménagement du temps de travail",default=False)
    action_training = models.BooleanField("Formation et tutorat",default=False)
    action_reassignment = models.BooleanField("Réaffectation à un autre poste",default=False)
    action_deskilling = models.BooleanField("Déshabilitation ses nouvelles opérations",default=False)
    new_missions = models.TextField(null=True, blank=True)



    medical_visit_required = models.BooleanField("Envoit pour une visite médicale de reprise",default=False)
    direct_return = models.BooleanField("Reprise de poste directement",default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)