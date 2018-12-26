from django.urls import path, include
from . import views

urlpatterns = [
    # dvds/
    path('', views.dvd_landing, name='dvd_landing'),
    # dvds/add_dvd
    path('add_dvd/', views.add_dvd, name='add_dvd'),
    # dvds/pick_dvd
    path('pick_dvd', views.pick_dvd, name='pick_dvd'),
    # dvds/add_dvd/confirm_dvd
    path('confirm_dvd/', views.confirm_dvd, name='confirm_dvd'),
    # dvds/add_dvd/dvd_added
    path('added/', views.dvd_added, name='dvd_added'),
    # dvds/film_name/info
    path('<slug:name>/info', views.film_info, name='film_info'),

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