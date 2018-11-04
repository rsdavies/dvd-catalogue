from django.db import models

# Create your models here.


class Location(models.Model):
    location_name = models.CharField(max_length=30)

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

    def __str__(self):
        return self.name


