from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import TicketStatusUpdateForm
from .models import Ticket, Comment
from .forms import CommentForm
from .mixins import ClientRequiredMixin,StaffRequiredMixin,UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def client_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, is_staff=False)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def staff_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, is_staff=True)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        if self.request.user.profile.is_staff:
            return Ticket.objects.all()
        else:
            return Ticket.objects.filter(client=self.request.user)
 
class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'      
    
class TicketStatusUpdateView(LoginRequiredMixin, StaffRequiredMixin,  UserPassesTestMixin, UpdateView):
    model = Ticket
    form_class = TicketStatusUpdateForm
    template_name = 'tickets/ticket_status_update.html'
    success_url = reverse_lazy('ticket_list')

    def test_func(self):
        ticket = self.get_object()
        return self.request.user.profile.is_staff or ticket.client == self.request.user

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user if self.request.user.profile.is_staff else None
        return super().form_valid(form)
    
class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(ticket=self.object)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            return self.get(request, *args, **kwargs)
    
class TicketCreateView(LoginRequiredMixin, ClientRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'description', 'company']
    template_name = 'tickets/ticket_form.html'
    success_url = '/tickets/list/'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)