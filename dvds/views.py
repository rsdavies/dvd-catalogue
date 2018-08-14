from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the dvd catalogue page.")


def add_page(request):
    return HttpResponse("This will be the add to database page.")
