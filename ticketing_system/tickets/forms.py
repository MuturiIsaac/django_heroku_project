from django import forms
from .models import Ticket , Comment

class TicketStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']