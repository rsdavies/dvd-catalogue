from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import datetime
from decimal import Decimal
from django.core.cache import cache
# Create your views here.
from .forms import DvDForm, PickerForm, HouseholdSetupForm, LocationSetupForm, LocationFormSet,  SemiRandomForm, SearchForm, ChooseForm
from .models import DvD, Director, Location, Actor, Genre, HouseHold, CustomUser
import omdb
from random import randint
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
            request.session['dvd_location'] = dvd_location.id
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
            dvd_location = request.session.get('dvd_location', None)

            # Director(s)
            director_list = [director for director in dvd_info['director'].split(',')]
            directors = []
            for director in director_list:
                director_obj, created = Director.objects.get_or_create(name=director)
                directors.append(director_obj)
                director_obj.save()
            
            # Actor
            actors = []
            # Don't get a list of actors, we get a string, split by commas. 
            actor_list = [actor for actor in dvd_info['actors'].split(', ') ]
            for actor in actor_list:
                act_obj, created = Actor.objects.get_or_create(name=actor)
                actors.append(act_obj)
                act_obj.save()
            # Genre
            genres = []
            genre_list = [genre for genre in dvd_info['genre'].split(', ')]
            for genre in genre_list:
                genre_obj, created = Genre.objects.get_or_create(name=genre)
                genres.append(genre_obj)
                genre_obj.save()

            # DVD
            dvd, created = DvD.objects.get_or_create(name = dvd_info['title'],
                      release_date = datetime.datetime.strptime(dvd_info['released'],'%d %b %Y'),
                      where_stored = Location(id=dvd_location),
                      runtime = int(dvd_info['runtime'].split()[0]),
                      imdb_rating = Decimal(dvd_info['imdb_rating']),
                      blurb = dvd_info['plot'],
                      poster_url = dvd_info['poster'],
                      director = directors[0])
            dvd.save()
            
            # this one was already in there!
            for actor in actors:
                dvd.actors.add(actor)
            for genre in genres:
                dvd.genres.add(genre)
                # TODO don't assume director is foreign key, what if its many to one?
                #for director in directors:
                #    dvd.director.add(director)
            dvd.save()

        return render(request, 'dvds/dvd_info.html', 
                      {'dvd' : dvd, 'just_added': True, 'count': DvD.users_dvds(request.user.id).count()})
    else:
        # TODO also have link to something se we can check its the right film?
        form = PickerForm(possibles=possible_dvds)

    return render(request, 'dvds/confirm_to_db.html', {'form': form})

def randomise(request, count_dvds):
    # How many dvds does this user have? 
    random_id = randint(0, int(count_dvds)-1)
    dvd_id = DvD.users_dvds(request.user.id)[random_id].id
    request.session['random_dvd'] = dvd_id
    name = DvD.users_dvds(request.user.id)[random_id].name
    return redirect('dvd_info', name=slugify(name), dvd_id=dvd_id)

def filtered_random(request):
    if request.method == "POST":
        form = SemiRandomForm(request.POST, user=request.user)
        if form.is_valid():
            # now the searching logic with the filters. 
            # Handle era
            filtered_query = DvD.users_dvds(request.user.id)
            if 'era' in form.changed_data:
                if form.cleaned_data['era'] == '2010':
                    # then we only have one end to the filter
                    filtered_query = filtered_query.filter(
                                        release_date__gte=datetime.date(int(form.cleaned_data['era']), 1 , 1))
                elif form.cleaned_data['era'] == '1960':
                    filtered_query = filtered_query.filter(
                                        release_date__lte=datetime.date(int(form.cleaned_data['era']), 1 , 1))
                
                else: 
                    # we have a start and an end
                    filtered_query = filtered_query.filter(
                                            release_date__gte=datetime.date(int(form.cleaned_data['era']), 1, 1)
                                        ).filter(
                                            release_date__lt=datetime.date(int(form.cleaned_data['era'])+10, 12, 31)
                                        )

            if 'max_duration' in form.changed_data:
                filtered_query = filtered_query.filter(
                                                    runtime__lte=int(form.cleaned_data['max_duration'])
                                                    )

            if 'rating' in form.changed_data:
                filtered_query = filtered_query.filter(
                                                    imdb_rating__gte=int(form.cleaned_data['rating'])-2
                                                ).filter(
                                                    imdb_rating__lte=int(form.cleaned_data['rating'])
                                                )  

            if 'director' in form.changed_data:
                filtered_query = filtered_query.filter(
                                                        director__name=form.cleaned_data['director']
                                                        )

            if 'actor' in form.changed_data:
                filtered_query = filtered_query.filter(
                                                        actors__name=form.cleaned_data['actor']
                                                        )

            if 'genre' in form.changed_data:
                filtered_query = filtered_query.filter(
                                                        genres__name=form.cleaned_data['genre'])

            result_objects = filtered_query
        if result_objects:
            cache.set('result_objects', result_objects)
            
            return render(request, 'dvds/search_results.html', {'results_list': result_objects})
        else:
            # no results version of filter random 
            return render(request, 'dvds/semi_random.html', {'form': form, 'no_results':True})
    else:
        form = SemiRandomForm(user=request.user)
        return render(request, 'dvds/semi_random.html', {'form': form, 'no_results': False})

def pick_dvd(request):
    count_dvds = DvD.users_dvds(request.user.id).count()
    return render(request, 'dvds/pick_dvd.html', {'count_dvds': count_dvds})    

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

def dvd_info(request, name, dvd_id):
    if request.method=="POST":
        form = ChooseForm(request.POST)
        dvd = DvD.objects.get(id=dvd_id)
        dvd.last_watched = datetime.datetime.today()
        dvd.save()
        return HttpResponse("Enjoy the show!")

    elif request.method=="GET":
        dvd = DvD.objects.get(id=dvd_id)
        form = ChooseForm()
        return render(request, 'dvds/dvd_info.html', {'dvd': dvd, 'just_added': False,'count':DvD.users_dvds(request.user.id).count(),'form':form})
        
    else:
        random_dvd = request.session.get('random_dvd')
        dvd = DvD.users_dvds(request.user.id).get(id=random_dvd)
        form = ChooseForm()
        return render(request, 'dvds/dvd_info.html', {'dvd': dvd, 'just_added': False,'count':DvD.users_dvds(request.user.id).count(),'form':form})

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if 'search_box' in form.changed_data:
            search_query = form.data["search_box"]
            result_objects = DvD.users_dvds(request.user.id).filter(name__icontains=search_query)
            if result_objects:
                # store the possibles in the cache
                cache.set('result_objects', result_objects)     
                return render(request, 'dvds/search_results.html', {'results_list': result_objects})
            else: 
                # reload search with a no results found message
                form = SearchForm()
                return render(request, 'dvds/search.html', {'form': form, 'no_results': True})
   
        else:
            return render(request, 'dvds/search.html', {'form': form, 'no_results': False})

    else:
        form = SearchForm()
        return render(request, 'dvds/search.html', {'form': form, 'no_results': False})


