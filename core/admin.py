from django.contrib import admin
from .models import Profile, Shelter, Pet, AdoptionApplication, Favourite

admin.site.register(Profile)
admin.site.register(Shelter)
admin.site.register(Pet)
admin.site.register(AdoptionApplication)
admin.site.register(Favourite)