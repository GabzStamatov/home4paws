from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pet_id>/apply/', views.apply_for_pet, name='apply_for_pet'),
    path('my-applications/', views.my_applications, name='my_applications'),

    path('staff/applications/', views.staff_applications, name='staff_applications'),
    path('staff/applications/<int:app_id>/approve/', views.approve_application, name='approve_application'),
    path('staff/applications/<int:app_id>/reject/', views.reject_application, name='reject_application'),
    path('pets/<int:pet_id>/favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('my-favourites/', views.my_favourites, name='my_favourites'),

    path('pets/add/', views.add_pet, name='add_pet'),
    path('pets/<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),
    path('pets/<int:pet_id>/delete/', views.delete_pet, name='delete_pet'),
]