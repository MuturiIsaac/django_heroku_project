from django.urls import path
from . import views

urlpatterns = [
    path('register/client/', views.client_register, name='client_register'),
    path('register/staff/', views.staff_register, name='staff_register'),
    path('tickets/create/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/list/', views.TicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<int:pk>/update-status/', views.TicketStatusUpdateView.as_view(), name='ticket_status_update'),

]