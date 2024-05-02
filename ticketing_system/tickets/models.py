from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Ticket

class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('awaiting_response', 'Awaiting Response'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], default='new')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_tickets')
    company = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'description', 'company']
    template_name = 'tickets/ticket_form.html'
    success_url = '/tickets/list/'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)    