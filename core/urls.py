from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
]

