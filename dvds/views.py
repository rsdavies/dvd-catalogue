from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
# Create your views here.
from .forms import DvDForm, PickerForm
import omdb
from .api_keys import api_key


def dvd_landing(request):
    # this in its most basic approach is a button that says "pick me a film" and it
    # generates a random dvd_id and takes you to the film info page.
    #  and it gives you an option to add a dvd
    return render(request, 'dvds/dvd_landing.html')


def add_dvd(request):
    # This is a form, with an input box or two.
    # Should trigger some omdb stuff and fill in the database
    if request.method == 'POST':
        form = DvDForm(request.POST)
        if form.is_valid():
            film_name = form.cleaned_data['film_name']
            film_year = form.cleaned_data['film_year']
            film_location = form.cleaned_data['film_location']
            type = form.cleaned_data['type']
            omdb.set_default('apikey', api_key)
            if type == 'film':
                possible_dvds = omdb.search_movie(film_name, year=film_year)
            else:
                possible_dvds = omdb.search_series(film_name, year=film_year)

            request.session['possible_dvds'] = possible_dvds
            # this is a list of dictionaries with films matching the search.
            # want to display the possibilities to the user.
            # user then picks which one is right, and a further call to the omdb api
            # gets the rest of the data.

        return redirect('confirm_dvd')
    else:
        # display the form
        form = DvDForm()

    return render(request, 'dvds/add_dvd.html', {'form': form})


def confirm_dvd(request):
    # display the list of possible films, years and links to posters?
    
    possible_dvds = request.session.get('possible_dvds')
    if request.method == 'POST':
        form = PickerForm(request.POST, possibles=possible_dvds)
        if form.is_valid():
            # TODO now put that data in the DB
            a = 1
        return redirect('dvd_added')
    else:
        # TODO also have link to something se we can check its the right film?
        form = PickerForm(possibles=possible_dvds)

    return render(request, 'dvds/confirm_to_db.html', {'form': form})

def dvd_added(request):
    return render(request, 'dvds/dvd_added.html')

def film_info(request, name):
    # TODO make this view actually show information about a film!
    return HttpResponse("This page will give information about a film")

