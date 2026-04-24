from django.shortcuts import render
from .models import Pet

def home(request):
    return render(request, 'core/home.html')

def pet_list(request):
    pets = Pet.objects.all()
    return render(request, 'core/pet_list.html', {'pets': pets})