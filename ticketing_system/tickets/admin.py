from django.contrib import admin
from .models import Ticket, UserProfile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Ticket)
admin.site.register(UserProfile)

# Add the following to display additional user information in the admin interface
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)