from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def dvd_picker(request):
    return HttpResponse("There will be a randomiser button here.")


def add_dvd(request):
    return HttpResponse("This will be the add to database page.")


def film_info(request, name):
    return HttpResponse("This page will give information about a film")

