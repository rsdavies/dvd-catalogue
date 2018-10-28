from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
# Create your views here.
from .forms import DvDForm
import omdb
from .api_keys import api_key


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
            film_name = form.cleaned_data['film_name']
            film_year = form.cleaned_data['film_year']
            film_location = form.cleaned_data['film_location']
            omdb.set_default('apikey', api_key)
            # todo handle the possible lack of year
            possible_films = omdb.get(search=film_name, year=film_year)
            # todo the possible films needs to be a class so I can . access the
            # attributes in the next view
            request.session['possible_films'] = possible_films
            # this is a dictionary with films matching the search.
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
    possible_films = request.session.get('possible_films')
    return render(request, 'dvds/confirm_to_db.html', {'possible_films': possible_films})


def film_info(request, name):
    # TODO make this view actually show information about a film!
    return HttpResponse("This page will give information about a film")

