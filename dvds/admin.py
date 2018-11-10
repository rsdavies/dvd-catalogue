from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# user stuff
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# DvD stuff models here.
from .models import DvD, Location, Director, Actor, Genre, HouseHold

admin.site.register(DvD)
admin.site.register(Location)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Genre)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(HouseHold)