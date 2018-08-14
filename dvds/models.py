from django.db import models

# Create your models here.


class dvd(models.Model):
    name = models.CharField(max_length=200)
    release_date = models.DateTimeField('date released')
    where_stored = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def where(self):
        return self.where_stored

    def released(self):
        return self.release_date