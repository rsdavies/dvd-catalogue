from django.urls import path

from . import views

urlpatterns = [
    # dvds/
    path('', views.dvd_picker, name='dvd_picker'),
    # dvds/add_dvd
    path('add_dvd', views.add_dvd, name='add_dvd'),
    # dvds/add_dvd/confirm_dvd
    path('dvds/add_dvd/confirm', views.confirm_to_db, name="confirm_dvd"),
    # dvds/film_name/info
    path('<slug:name>/info', views.film_info, name='film_info')
]