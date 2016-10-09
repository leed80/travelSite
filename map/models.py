from django.db import models



class Country_test(models.Model):
	country_id = models.IntegerField(null=True, blank=True)
	name = models.CharField(max_length=200)
	maproute = models.CharField(max_length=500)
	description = models.CharField(max_length=10000)
	author = models.CharField(max_length=10000, default="nothing here")
	author_website = models.CharField(max_length=10000, default="nothing here")
	author_url = models.CharField(max_length=10000, default="nothing here")
	latitude = models.FloatField(default=1.0)
	longitude = models.FloatField(default=1.0)

	def __str__(self):
		return '%s %s %s %s' % (self.country_id, self.name, self.maproute, self.description)

class Regions_test(models.Model):
	region_id = models.IntegerField(null=True, blank=True)
	country_id = models.IntegerField()
	regionname = models.CharField(max_length=500)

	def __str__(self):
		return '%s %s %s' % (self.region_id, self.country_id, self.regionname)
		

	
		



class Towns_test(models.Model):
	region_id = models.IntegerField()
	townname = models.CharField(max_length=500)
	latitude = models.FloatField(default=1.0)
	longitude = models.FloatField(default=1.0)

	def __str__(self):
		return '%s %s %s %s' % (self.region_id, self.townname, self.latitude, self.longitude)

class Towns_test_desc(models.Model):
	townname = models.CharField(max_length=500)
	description = models.CharField(max_length=10000)
	author = models.CharField(max_length=10000)
	author_website = models.CharField(max_length=10000, default="nothing here")
	author_url = models.CharField(max_length=10000, default="nothing here")

	def __str__(self):
		return '%s %s' % (self.townname, self.description)
