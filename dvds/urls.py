from django.urls import path, include
from . import views

urlpatterns = [
    # dvds/
    path('', views.dvd_landing, name='dvd_landing'),
    # dvds/add_dvd
    path('add_dvd/', views.add_dvd, name='add_dvd'),
    # dvds/add_dvd/confirm_dvd
    path('confirm_dvd/', views.confirm_dvd, name='confirm_dvd'),
    # dvds/add_dvd/dvd_added
    path('added/', views.dvd_added, name='dvd_added'),
    # dvds/film_name/info
    path('<slug:name>/info', views.film_info, name='film_info')
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]