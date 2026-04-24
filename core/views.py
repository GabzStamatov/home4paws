from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from .models import Pet, AdoptionApplication


def home(request):
    return render(request, 'core/home.html')


def pet_list(request):
    pets = Pet.objects.all()
    return render(request, 'core/pet_list.html', {'pets': pets})


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'core/pet_detail.html', {'pet': pet})


def is_staff_user(user):
    return hasattr(user, 'profile') and user.profile.role in ['STAFF', 'ADMIN']


@login_required
def apply_for_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        application_text = request.POST.get('application_text')

        AdoptionApplication.objects.create(
            user=request.user,
            pet=pet,
            application_text=application_text
        )

        return redirect('pet_list')

    return render(request, 'core/apply_for_pet.html', {'pet': pet})


@login_required
def my_applications(request):
    applications = AdoptionApplication.objects.filter(user=request.user)
    return render(request, 'core/my_applications.html', {'applications': applications})

@login_required
def staff_applications(request):
    if not is_staff_user(request.user):
        return HttpResponseForbidden("You are not allowed to access this page.")

    applications = AdoptionApplication.objects.all()
    return render(request, 'core/staff_applications.html', {'applications': applications})


@login_required
def approve_application(request, app_id):
    if not is_staff_user(request.user):
        return HttpResponseForbidden("You are not allowed to access this page.")

    app = get_object_or_404(AdoptionApplication, id=app_id)
    app.status = 'APPROVED'
    app.pet.status = 'ADOPTED'
    app.pet.save()
    app.save()
    return redirect('staff_applications')


@login_required
def reject_application(request, app_id):
    if not is_staff_user(request.user):
        return HttpResponseForbidden("You are not allowed to access this page.")

    app = get_object_or_404(AdoptionApplication, id=app_id)
    app.status = 'REJECTED'
    app.save()
    return redirect('staff_applications')