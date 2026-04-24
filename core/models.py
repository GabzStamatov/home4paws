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