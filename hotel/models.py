from __future__ import unicode_literals

from django.db import models




class hotelTable(models.Model):
	refNumber = models.CharField(max_length=40)
	title = models.CharField(max_length=40)
	description = models.TextField(max_length=10000)
	stop = models.CharField(max_length=40)
	travelClass = models.CharField(max_length=40)
	eanhotelid = models.IntegerField()
	address = models.CharField(max_length=40)
	location = models.CharField(max_length=40)
	amenities = models.TextField(max_length=10000)
	policies = models.TextField(max_length=10000)
	roomtypecode = models.IntegerField()
	ratecode = models.IntegerField()




	def __unicode__(self):
		return '%s %s %s %s %s %s %s %s %s %s %s %s' % (self.refNumber, self.title, self.description, self.stop, self.travelClass, self.eanhotelid, self.address, self.location, self.amenities, self.policies, self.roomtypecode, self.ratecode)

class hotelRoomTypes(models.Model):
	refNumber = models.CharField(max_length=40)
	hotel = models.ForeignKey(hotelTable)
	title = models.CharField(max_length=100)
	beds = models.CharField(max_length=100)
	amenities = models.TextField(max_length=10000)

	def __unicode__(self):
		return '%s %s %s %s' % (self.hotel, self.title, self.beds, self.amenities)
