from django.contrib import admin

# Register your models here.
from .models import DvD, Location, Director, Actor

admin.site.register(DvD)
admin.site.register(Location)
admin.site.register(Director)
admin.site.register(Actor)