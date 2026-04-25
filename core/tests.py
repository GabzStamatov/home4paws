from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Profile, Shelter, Pet, AdoptionApplication, Favourite


class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            role='ADOPTER'
        )

        self.shelter = Shelter.objects.create(
            name='Happy Paws Shelter',
            location='Dublin',
            contact_email='shelter@test.com',
            contact_phone='123456789',
            description='A local animal shelter.'
        )

        self.pet = Pet.objects.create(
            shelter=self.shelter,
            name='Daisy',
            pet_type='DOG',
            breed='Labrador',
            age=3,
            gender='Female',
            description='Friendly dog',
            vaccination_status=True,
            status='AVAILABLE'
        )

    def test_profile_string_returns_username(self):
        self.assertEqual(str(self.profile), 'testuser')

    def test_shelter_string_returns_name(self):
        self.assertEqual(str(self.shelter), 'Happy Paws Shelter')

    def test_pet_string_returns_name(self):
        self.assertEqual(str(self.pet), 'Daisy')

    def test_create_adoption_application(self):
        application = AdoptionApplication.objects.create(
            user=self.user,
            pet=self.pet,
            application_text='I would love to adopt Daisy.',
            housing_type='House',
            has_garden=True,
            near_park=True,
            has_other_pets=False,
            pet_experience='I have owned dogs before.',
            hours_alone=2,
            reason='I can provide a loving home.'
        )

        self.assertEqual(application.status, 'PENDING')
        self.assertEqual(str(application), 'testuser - Daisy')

    def test_create_favourite(self):
        favourite = Favourite.objects.create(
            user=self.user,
            pet=self.pet
        )

        self.assertEqual(str(favourite), 'testuser saved Daisy')


class ViewTests(TestCase):

    def setUp(self):
        self.adopter = User.objects.create_user(
            username='adopter',
            password='password'
        )

        self.staff = User.objects.create_user(
            username='staffuser',
            password='password'
        )

        Profile.objects.create(
            user=self.adopter,
            role='ADOPTER'
        )

        Profile.objects.create(
            user=self.staff,
            role='STAFF'
        )

        self.shelter = Shelter.objects.create(
            name='Happy Paws Shelter',
            location='Dublin',
            contact_email='shelter@test.com',
            contact_phone='123456789',
            description='A local animal shelter.'
        )

        self.pet = Pet.objects.create(
            shelter=self.shelter,
            name='Daisy',
            pet_type='DOG',
            breed='Labrador',
            age=3,
            gender='Female',
            description='Friendly dog',
            vaccination_status=True,
            status='AVAILABLE'
        )

        self.application = AdoptionApplication.objects.create(
            user=self.adopter,
            pet=self.pet,
            application_text='I want to adopt Daisy.',
            housing_type='House',
            has_garden=True,
            near_park=True,
            has_other_pets=False,
            pet_experience='Owned pets before.',
            hours_alone=2,
            reason='I can provide a safe home.'
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_pet_list_page_loads(self):
        response = self.client.get(reverse('pet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Daisy')

    def test_pet_detail_page_loads(self):
        response = self.client.get(reverse('pet_detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Daisy')

    def test_adopter_can_apply_for_pet(self):
        self.client.login(username='adopter', password='password')

        response = self.client.post(
            reverse('apply_for_pet', args=[self.pet.id]),
            {
                'application_text': 'I would like to adopt this pet.',
                'housing_type': 'House',
                'has_garden': 'on',
                'near_park': 'on',
                'has_other_pets': '',
                'pet_experience': 'I have experience with dogs.',
                'hours_alone': 3,
                'reason': 'I have a safe home.'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            AdoptionApplication.objects.filter(
                user=self.adopter,
                pet=self.pet
            ).exists()
        )

    def test_adopter_can_view_own_applications(self):
        self.client.login(username='adopter', password='password')

        response = self.client.get(reverse('my_applications'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Daisy')

    def test_adopter_can_add_favourite(self):
        self.client.login(username='adopter', password='password')

        response = self.client.get(reverse('toggle_favourite', args=[self.pet.id]))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Favourite.objects.filter(
                user=self.adopter,
                pet=self.pet
            ).exists()
        )

    def test_adopter_can_view_favourites(self):
        Favourite.objects.create(user=self.adopter, pet=self.pet)

        self.client.login(username='adopter', password='password')

        response = self.client.get(reverse('my_favourites'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Daisy')

    def test_staff_can_view_applications(self):
        self.client.login(username='staffuser', password='password')

        response = self.client.get(reverse('staff_applications'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Daisy')

    def test_adopter_cannot_view_staff_applications(self):
        self.client.login(username='adopter', password='password')

        response = self.client.get(reverse('staff_applications'))

        self.assertEqual(response.status_code, 403)

    def test_staff_can_approve_application(self):
        self.client.login(username='staffuser', password='password')

        response = self.client.get(
            reverse('approve_application', args=[self.application.id])
        )

        self.application.refresh_from_db()
        self.pet.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.application.status, 'APPROVED')
        self.assertEqual(self.pet.status, 'ADOPTED')

    def test_staff_can_reject_application(self):
        self.client.login(username='staffuser', password='password')

        response = self.client.get(
            reverse('reject_application', args=[self.application.id])
        )

        self.application.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.application.status, 'REJECTED')

    def test_staff_can_add_pet(self):
        self.client.login(username='staffuser', password='password')

        response = self.client.post(
            reverse('add_pet'),
            {
                'shelter': self.shelter.id,
                'name': 'Cleo',
                'pet_type': 'CAT',
                'breed': 'British Shorthair',
                'age': 2,
                'gender': 'Female',
                'description': 'Calm cat',
                'vaccination_status': 'on',
                'status': 'AVAILABLE'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pet.objects.filter(name='Cleo').exists())

    def test_staff_can_edit_pet(self):
        self.client.login(username='staffuser', password='password')

        response = self.client.post(
            reverse('edit_pet', args=[self.pet.id]),
            {
                'shelter': self.shelter.id,
                'name': 'Daisy Updated',
                'pet_type': 'DOG',
                'breed': 'Labrador',
                'age': 4,
                'gender': 'Female',
                'description': 'Updated description',
                'vaccination_status': 'on',
                'status': 'AVAILABLE'
            }
        )

        self.pet.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.pet.name, 'Daisy Updated')

    def test_staff_can_delete_pet(self):
        self.client.login(username='staffuser', password='password')

        response = self.client.post(reverse('delete_pet', args=[self.pet.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pet.objects.filter(id=self.pet.id).exists())