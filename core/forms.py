from django import forms
from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'shelter',
            'name',
            'pet_type',
            'breed',
            'age',
            'gender',
            'description',
            'vaccination_status',
            'status',
            'image',
        ]