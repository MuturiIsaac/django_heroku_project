from django.urls import path
from . import views

urlpatterns = [
    path('register/client/', views.client_register, name='client_register'),
    path('register/staff/', views.staff_register, name='staff_register'),
]