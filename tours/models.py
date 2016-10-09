from __future__ import unicode_literals

from django.db import models
from django_countries.fields import CountryField



class tourTable(models.Model):
	refNumber = models.CharField(max_length=40)
	title = models.CharField(max_length=40)
	description = models.TextField(max_length=10000)
	country = models.CharField(max_length=40)
	travelClass = models.CharField(max_length=40)



	def __unicode__(self):
		return '%s %s %s %s %s' % (self.refNumber, self.title, self.description, self.country, self.travelClass)

class stopTable(models.Model):
	refNumber = models.CharField(max_length=40)
	tour = models.ForeignKey(tourTable)
	title = models.CharField(max_length=40)
	description = models.TextField(max_length=10000)
	lengthofstay = models.IntegerField()

	def __unicode__(self):
		return '%s %s %s %s %s' % (self.refNumber, self.tour, self.title, self.description, self.lengthofstay)


class activities(models.Model):
	refNumber = models.CharField(max_length=40)
	stop = models.ForeignKey(stopTable)
	title = models.CharField(max_length=40)
	description = models.TextField(max_length=10000)

	def __unicode__(self):
		return '%s %s %s %s' % (self.refNumber, self.stop, self.title, self.description)

