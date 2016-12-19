from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    activation_key = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=200)
    country = CountryField(blank_label='(select country)', default='gb')
    address = models.CharField(max_length=40, blank=True)
    postcode = models.CharField(max_length=40, blank=True)
   
      
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'

class billing(models.Model):
    userID = models.ForeignKey(User, unique=True)
    itineraryID = models.CharField(max_length=200)
    amount = models.FloatField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s %s %s" % (self.userID, self.itineraryID, self.amount, self.status)