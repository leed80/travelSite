from django.db import models

class Temp_Itinerary(models.Model):
    itinerary_id = models.CharField(max_length=100, unique=True)
    user = models.CharField(max_length=100)
    country = models.IntegerField()
    destinations = models.CharField(max_length=100, default="0")
    hotels = models.CharField(max_length=100, default=0)
    travel_class = models.CharField(max_length=100)
    date = models.DateField()
    travelers = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now=True)
    session = models.CharField(max_length=1000)

    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s' % (self.pk, self.travelers, self.date, self.travel_class, self.hotels, self.destinations, self.country, self.itinerary_id, self.user, self.time, self.session)

class Complete_Itinerary(models.Model):
    itinerary_id = models.CharField(max_length=100, unique=True)
    user = models.CharField(max_length=100)
    country = models.IntegerField()
    destinations = models.CharField(max_length=100)
    hotels = models.CharField(max_length=100)
    travel_class = models.CharField(max_length=100)
    date = models.DateField()
    travelers = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s ' % (self.travelers, self.date, self.travel_class, self.hotels, self.destinations, self.country, self.itinerary_id, self.user)