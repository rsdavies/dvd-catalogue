from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.add_page, name='add_page')
]