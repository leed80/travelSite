from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime
from django_countries.fields import CountryField


class User_Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    activation_key = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200)
    country = CountryField(blank_label='(select country)', default='gb')
      
    def __str__(self):
        return '%s, %s, %s, %s' % (self.user, self.activation_key, self.status, self.country)
