#connects to Django User
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model): #stores role 
    ROLE_CHOICES = [
        ('ADOPTER', 'Adopter'),
        ('STAFF', 'Shelter Staff'),
        ('ADMIN', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
class Shelter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name