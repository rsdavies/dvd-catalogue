from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_dvd', views.add_dvd, name='add_dvd')
]