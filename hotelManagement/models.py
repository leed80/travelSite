from __future__ import unicode_literals

from django.db import models

class hotel(models.Model):
	hotelid = models.IntegerField(default=0)
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	description = models.TextField(max_length=10000)
	destinationid = models.IntegerField(default=1)
	rating = models.IntegerField(default=1)
	countryid = models.IntegerField(default=1)
	city = models.CharField(max_length=100)
	postcode = models.CharField(max_length=100)
	checkIn = models.CharField(max_length=100)
	checkOut = models.CharField(max_length=100)
	hotelPolicy = models.TextField(max_length=10000)
	roomInformation = models.TextField(max_length=10000)
	checkInInstructions = models.TextField(max_length=10000)
	suppliers = models.TextField(max_length=10000)


	def __unicode__(self):
		return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.hotelid, self.name, self.address, self.description, self.destinationid, self.rating, self.countryid, self.city, self.postcode, self.checkIn, self.checkOut, self.hotelPolicy, self.roomInformation, self.checkInInstructions, self.suppliers)

class room(models.Model):
	hotelid = models.IntegerField()
	roomTypeCode = models.IntegerField()
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=10000)

	def __unicode__(self):
		return '%s %s %s %s' % (self.hotelid, self.roomTypeCode, self.name, self.description)
