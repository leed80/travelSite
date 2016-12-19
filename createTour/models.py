from __future__ import unicode_literals

from django.db import models
from django_countries.fields import CountryField



class country(models.Model):
	countryid = models.IntegerField(default=0)
	name = CountryField(blank_label='(select country)')
	description = models.TextField(max_length=10000)

	def __unicode__(self):
		return '%s %s' % (self.name, self.description)

class destination(models.Model):
	destinationid = models.IntegerField(default=0)
	name = models.CharField(max_length=100)
	countryid = models.IntegerField(default=1)
	description = models.TextField(max_length=10000)

	def __unicode__(self):
		return '%s %s %s' % (self.name, self.countryid, self.description)

class hotel(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	description = models.TextField(max_length=10000)
	destinationid = models.IntegerField(default=1)
	rating = models.IntegerField(default=1)

	def __unicode__(self):
		return '%s %s %s %s %s' % (self.name, self.address, self.description, self.destinationid, self.rating)





