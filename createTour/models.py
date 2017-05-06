from __future__ import unicode_literals

from django.db import models
from django_countries.fields import CountryField


class Country(models.Model):
    country_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="unknown")
    description = models.TextField(max_length=10000)
    lat = models.FloatField(max_length=10000, default=11.111)
    lng = models.FloatField(max_length=10000, default=111.111)
    zoom = models.IntegerField(max_length=100, default=4)

    def __unicode__(self):
        return '%s %s %s %s %s %s' % (self.country_id, self.name, self.description, self.lat, self.lng, self.zoom)


class Destination(models.Model):
    destination_id = models.IntegerField()
    name = models.CharField(max_length=100)
    country_id = models.IntegerField(default=1)
    description = models.TextField(max_length=10000)
    lat = models.FloatField(max_length=10000, default=11.111)
    lng = models.FloatField(max_length=10000, default=111.111)

    def __unicode__(self):
        return '%s %s %s %s %s' % (self.name, self.country_id, self.description, self.lat, self.lng)
