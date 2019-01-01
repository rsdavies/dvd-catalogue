from django.urls import path, include
from . import views

urlpatterns = [
    # dvds/
    path('', views.dvd_landing, name='dvd_landing'),
    # dvds/add_dvd
    path('add_dvd/', views.add_dvd, name='add_dvd'),
    # dvds/pick_dvd
    path('pick_dvd', views.pick_dvd, name='pick_dvd'),
    # dvds/randomise
    path('randomise_<slug:count_dvds>', views.randomise, name='randomise'),
    # dvds/filtered_random
    path('filtered_random/', views.filtered_random, name='filtered_random'),
    # dvds/add_dvd/confirm_dvd
    path('confirm_dvd/', views.confirm_dvd, name='confirm_dvd'),
    # dvds/add_dvd/dvd_added
    path('added/', views.dvd_added, name='dvd_added'),
    # dvds/dvd_info
    path('<slug:dvd_id>_<slug:name>/info/', views.dvd_info, name='dvd_info'),
    # dvds/search
    path('search/', views.search, name='search'),
   
    # dvds/user_home
    path('user_home/', views.user_home, name='user_home'),
    # dvds/user_home/setup_household
    path('setup_household', views.setup_household, name='setup_household'),
    # dvds/user_home/manage_household
    path('manage_household/', views.manage_household, name='manage_household'),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]