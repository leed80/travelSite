from django.db import models

class tempItinerary(models.Model):
    itineraryID = models.CharField(max_length=100, unique=True)
    user = models.CharField(max_length=100)
    country = models.IntegerField()
    destinations = models.CharField(max_length=100, default="0")
    hotels = models.CharField(max_length=100, default=0)
    travelClass = models.CharField(max_length=100)
    date = models.DateField()
    travelers = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now=True)
    session = models.CharField(max_length=1000)

    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s' % (self.pk, self.travelers, self.date, self.travelClass, self.hotels, self.destinations, self.country, self.itineraryID, self.user, self.time, self.session)

class completeItinerary(models.Model):
    itineraryID = models.CharField(max_length=100, unique=True)
    user = models.CharField(max_length=100)
    country = models.IntegerField()
    destinations = models.CharField(max_length=100)
    hotels = models.CharField(max_length=100)
    travelClass = models.CharField(max_length=100)
    date = models.DateField()
    travelers = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s ' % (self.travelers, self.date, self.travelClass, self.hotels, self.destinations, self.country, self.itineraryID, self.user)