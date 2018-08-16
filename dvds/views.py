from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
            info = form.save(commit=False)
        return render(request, 'dvds/add_dvd/confirm_to_db.html')
    else:
        # display the form
        form = DvDForm()

    return render(request, 'dvds/add_dvd.html', {'form': form})


def confirm_to_db(request):
    return HttpResponse("thankyou for adding a dvd")


def film_info(request, name):
    # TODO make this view actually show information about a film!
    return HttpResponse("This page will give information about a film")

