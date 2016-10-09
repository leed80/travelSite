from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from models import Country_test
import os
from advr.settings import PROJECT_ROOT


def countryupdate(request):

      #Deletes the current table data
  Country_test.objects.all().delete()

    #assigns the correct file to the var 'file_'
  file_ = os.path.join('static/map/country.tsv')

    #opens the file
  f = open(file_, 'r')
    #loops everyline in the file
  for line in f:
    #splits each value with a ',' making it a list
    line = line.split(',')
    country = Country_test()
      #assigns each line to the name coumn in database
    country.country_id = line[0]
    country.name = line[1]
    country.maproute = line[2]
    country.description = line[3]
      #saves the data to the database
    country.save()

      #closes the file
    f.close()

    return HttpResponse('Country Updated')