from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'Superadmin'),
        ('HRBP', 'HRBP'),
        ('NPLUS1', 'Manager (N+1)'),
    )
    

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='NPLUS1')
    corporate_id = models.CharField(max_length=50, unique=True, null=True) 


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"