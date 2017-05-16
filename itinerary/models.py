from django.db import models

class Temp_Itinerary(models.Model):
    itinerary_id = models.CharField(max_length=100, unique=True)
    user = models.IntegerField()
    country = models.IntegerField()
    destinations = models.CharField(max_length=100, default="0")
    hotels = models.CharField(max_length=100, default=0)
    travel_class = models.CharField(max_length=100)
    date = models.DateField()
    travelers = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s' % (self.pk, self.travelers, self.date, self.travel_class, self.hotels, self.destinations, self.country, self.itinerary_id, self.user, self.time)

class Complete_Itinerary(models.Model):
    itinerary_id = models.CharField(max_length=100, unique=True)
    user = models.IntegerField()
    country = models.IntegerField()
    destinations = models.CharField(max_length=100)
    hotels = models.CharField(max_length=100)
    travel_class = models.CharField(max_length=100)
    date = models.DateField()
    travelers = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s ' % (self.travelers, self.date, self.travel_class, self.hotels, self.destinations, self.country, self.itinerary_id, self.user)


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