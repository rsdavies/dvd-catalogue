from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime
from decimal import Decimal
# Create your views here.
from .forms import DvDForm, PickerForm, HouseholdSetupForm, LocationSetupForm, LocationFormSet
from .models import DvD, Director, Location, Actor, Genre, HouseHold, CustomUser
import omdb
from .api_keys import api_key


def dvd_landing(request):
    # this in its most basic approach is a button that says "pick me a film" and it
    # generates a random dvd_id and takes you to the film info page.
    #  and it gives you an option to add a dvd
    return render(request, 'dvds/dvd_landing.html')

@login_required
def add_dvd(request):
    # This is a form, with an input box or two.
    # Should trigger some omdb stuff and fill in the database
    if request.method == 'POST':
        form = DvDForm(request.POST, user=request.user)
        if form.is_valid():
            name = form.cleaned_data['name']
            year = form.cleaned_data['year']
            dvd_location = form.cleaned_data['location']
            type = form.cleaned_data['type']
            omdb.set_default('apikey', api_key)
            if type == 'film':
                possible_dvds = omdb.search_movie(name, year=year)
            else:
                possible_dvds = omdb.search_series(name, year=year)

            request.session['possible_dvds'] = possible_dvds
            request.session['dvd_location'] = dvd_location
            # this is a list of dictionaries with films matching the search.
            # want to display the possibilities to the user.
            # user then picks which one is right, and a further call to the omdb api
            # gets the rest of the data.

        return redirect('confirm_dvd')
    else:
        # display the form
        form = DvDForm(user=request.user)

    return render(request, 'dvds/add_dvd.html', {'form': form})

@login_required
def confirm_dvd(request):
    # display the list of possible films, years and links to posters?
    
    possible_dvds = request.session.get('possible_dvds')
    if request.method == 'POST':
        form = PickerForm(request.POST, possibles=possible_dvds)
        if form.is_valid():
            omdb.set_default('apikey', api_key)
            # TODO now put that data in the DB, needs to be done in order so I can get the IDs 
            dvd_id = form.cleaned_data['picked']
            dvd_info = omdb.imdbid(dvd_id)

            # location
            dvd_location = request.session.get('dvd_location')
            # TODO handle location so I'm selecting it from a dropdown in the form. 
            location, created = Location.objects.get_or_create(location_name=dvd_location)
            location.save()

            # Director
            director, created = Director.objects.get_or_create(name=dvd_info['director'])
            director.save()
            
            # Actor
            actors = []
            for actor in dvd_info['actors']:
                act_obj, created = Actor.objects.get_or_create(name=actor)
                actors.append(act_obj)
                act_obj.save()
            # Genre
            genres = []
            for genre in dvd_info['genre']:
                genre_obj, created = Genre.objects.get_or_create(name=genre)
                genres.append(genre_obj)
                genre_obj.save()

            # DVD
            dvd, created = DvD.objects.get_or_create(name = dvd_info['title'],
                      release_date = datetime.strptime(dvd_info['released'],'%d %b %Y'),
                      where_stored = location,
                      runtime = int(dvd_info['runtime'].split()[0]),
                      imdb_rating = Decimal(dvd_info['imdb_rating']),
                      blurb = dvd_info['plot'],
                      poster_url = dvd_info['poster'],
                      director = director)
            dvd.save()
            if not created:
                # this one was already in there!
                for actor in actors:
                    dvd.actors.add(actor)
                for genre in genres:
                    dvd.genres.add(genre)
                dvd.save()

        return render(request, 'dvds/dvd_added.html', {'dvd_info' : dvd_info})
    else:
        # TODO also have link to something se we can check its the right film?
        form = PickerForm(possibles=possible_dvds)

    return render(request, 'dvds/confirm_to_db.html', {'form': form})


def pick_dvd(request):
    return render(request, 'dvds/pick_dvd.html')

@login_required
def user_home(request):
    return render(request, 'dvds/user_home.html')

@login_required
def setup_household(request):
    if request.method == 'GET':
        house_form = HouseholdSetupForm(request.GET or None)
        loc_formset = LocationFormSet(request.GET or None)
    elif request.method == 'POST':
        house_form = HouseholdSetupForm(request.POST)
        loc_formset = LocationFormSet(request.POST)
        if house_form.is_valid() and loc_formset.is_valid():
            # save the household name
            house_name = house_form.cleaned_data.get('household_name')

            hh = HouseHold(name=house_name, members=request.user)
            hh.save()
            for form in loc_formset:
                # save the dvd name and location to DB.
                loc_name = form.cleaned_data.get('location_name')
                loc_desc = form.cleaned_data.get('location_desc')
                if loc_name:
                    loc = Location.objects.create(location_name=loc_name, 
                                                  location_description=loc_desc, 
                                                  household=hh)
                    loc.save()
            # redirect to a page which informs you you've set up household?  
            return render(request, 'dvds/manage_household.html')
    return render(request, 'dvds/setup_household.html', 
                  {'location_form': loc_formset, 
                   'household_form': house_form})

@login_required
def manage_household(request):
    # this will be where a user adds a dvd to their collection, 
    # moves it to a different storage location, or removes it entirely
    # they can also invite someone else to join their household?

    # get the household name and the list of locations associated with this user
    hh_name= HouseHold.objects.get(members=request.user)
    storage_locs = Location.objects.filter(household=hh_name)

    return render(request, 'dvds/manage_household.html', {'hh':hh_name, 'storage':storage_locs})

def dvd_added(request):
   return render(request, 'dvds/dvd_added.html')

def film_info(request, name):
    # TODO make this view actually show information about a film!
    return HttpResponse("This page will give information about a film")

