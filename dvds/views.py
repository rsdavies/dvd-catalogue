from django.shortcuts import render
from django.http import HttpResponse
from django import forms
# Create your views here.
from .forms import DvDForm

def dvd_picker(request):
    # this in its most basic approach is a button that says "pick me a film" and it
    # generates a random dvd_id and takes you to the film info page.
    return HttpResponse("There will be a randomiser button here.")


def add_dvd(request):
    # This is a form, with an input box or two.
    # Should trigger some omdb stuff and fill in the database
    if request.method == 'POST':
        form = DvDForm(request.POST)
        if form.is_valid():
            # do stuff
            a = 1
        return HttpResponse("film details entered")
    else:
        # display the form
        form = DvDForm()

    return render(request, 'dvds/add_dvd.html', {'form': form})


def film_info(request, name):
    # TODO make this view actually show information about a film!
    return HttpResponse("This page will give information about a film")

