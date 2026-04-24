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
    
class Shelter(models.Model): #animal shelter
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Pet(models.Model):#all of the pets
    PET_TYPE_CHOICES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ADOPTED', 'Adopted'),
    ]

    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    description = models.TextField()
    vaccination_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    application_text = models.TextField()
    housing_type = models.CharField(max_length=50, blank=True)
    has_garden = models.BooleanField(default=False)
    near_park = models.BooleanField(default=False)
    has_other_pets = models.BooleanField(default=False)
    pet_experience = models.TextField(blank=True)
    hours_alone = models.IntegerField(default=0)
    reason = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pet')

    def __str__(self):
        return f"{self.user.username} saved {self.pet.name}"