from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    # add custom user fields
    @property
    def is_setup(self):
        if HouseHold.objects.filter(members_id=self.pk).exists():
            return True
        return False

    def __str__(self):
        return self.email

class HouseHold(models.Model):
    name = models.CharField("Household name", max_length=30)
    members = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Location(models.Model):
    location_name = models.CharField("Name of storage location", max_length=30)
    location_description = models.CharField("Description of storage location", max_length=200)
    household = models.ForeignKey(HouseHold, on_delete=models.CASCADE)
    def __str__(self):
        return self.location_name


class Director(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class DvD(models.Model):
    name = models.CharField(max_length=200)
    release_date = models.DateField('date released')
    where_stored = models.ForeignKey(Location, on_delete=models.CASCADE)
    last_watched = models.DateField('last watched', null=True)
    runtime = models.PositiveSmallIntegerField(default=999)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=2, default=00.00)
    blurb = models.CharField(max_length=1000, default='none')
    poster_url = models.URLField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)

    @classmethod
    def users_dvds(self, user_id):
        return self.objects.filter(where_stored__household__members=user_id)

    def __str__(self):
        return self.name

