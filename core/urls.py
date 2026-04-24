from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.pet_list, name='pet_list'),
]

