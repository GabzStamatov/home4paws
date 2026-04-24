from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden


from .models import Pet, AdoptionApplication, Favourite
from .forms import PetForm
from django.contrib.auth import logout


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
    if request.user.profile.role != 'ADOPTER':
        return HttpResponseForbidden("Only adopters can apply for pets.")

    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        application_text = request.POST.get('application_text')

        AdoptionApplication.objects.create(
            user=request.user,
            pet=pet,
            application_text=application_text
        )

        return redirect('my_applications')

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


@login_required
def toggle_favourite(request, pet_id):
    if request.user.profile.role != 'ADOPTER':
        return HttpResponseForbidden("Only adopters can favourite pets.")

    pet = get_object_or_404(Pet, id=pet_id)

    favourite, created = Favourite.objects.get_or_create(
        user=request.user,
        pet=pet
    )

    if not created:
        favourite.delete()

    return redirect('pet_list')


@login_required
def my_favourites(request):
    if request.user.profile.role != 'ADOPTER':
        return HttpResponseForbidden("Only adopters can view favourites.")

    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'core/my_favourites.html', {'favourites': favourites})


@login_required
def add_pet(request):
    if not is_staff_user(request.user):
        return HttpResponseForbidden("You are not allowed to access this page.")

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('pet_list')
    else:
        form = PetForm()

    return render(request, 'core/pet_form.html', {
        'form': form,
        'title': 'Add Pet'
    })


@login_required
def edit_pet(request, pet_id):
    if not is_staff_user(request.user):
        return HttpResponseForbidden("You are not allowed to access this page.")

    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)

        if form.is_valid():
            form.save()
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PetForm(instance=pet)

    return render(request, 'core/pet_form.html', {
        'form': form,
        'title': 'Edit Pet'
    })


@login_required
def apply_for_pet(request, pet_id):
    if request.user.profile.role != 'ADOPTER':
        return HttpResponseForbidden("Only adopters can apply for pets.")

    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        AdoptionApplication.objects.create(
            user=request.user,
            pet=pet,
            application_text=request.POST.get('application_text'),
            housing_type=request.POST.get('housing_type'),
            has_garden=request.POST.get('has_garden') == 'on',
            near_park=request.POST.get('near_park') == 'on',
            has_other_pets=request.POST.get('has_other_pets') == 'on',
            pet_experience=request.POST.get('pet_experience'),
            hours_alone=request.POST.get('hours_alone') or 0,
            reason=request.POST.get('reason'),
        )

        return redirect('my_applications')

    return render(request, 'core/apply_for_pet.html', {'pet': pet})

@login_required
def delete_pet(request, pet_id):
    if not is_staff_user(request.user):
        return HttpResponseForbidden("You are not allowed to access this page.")

    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        pet.delete()
        return redirect('pet_list')

    return render(request, 'core/delete_pet.html', {'pet': pet})

def logout_view(request):
    logout(request)
    return redirect('home')