from django.db import models

# Create your models here.


class Location(models.Model):
    location_name = models.CharField(max_length=30)

    def __str__(self):
        return self.location_name


class DvD(models.Model):
    name = models.CharField(max_length=200)
    release_date = models.DateTimeField('date released')
    where_stored = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=30)
    film = models.ForeignKey(DvD, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=30)
    film = models.ForeignKey(DvD, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Genre(models.Models):
    name = models.CharField(max_length=30)
    film = models.ForeignKey(DvD, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
