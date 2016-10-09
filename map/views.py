from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import re
from django.template import RequestContext
import os
import sys
from forms import CountrySelect
from django.core.context_processors import csrf

from rest_framework import viewsets
from django.db.models import Q






#The view to select the country
@login_required
def main(request):
    return render_to_response ('map/premap.html', context_instance=RequestContext(request))
@login_required
def anglemap(request):
    return render_to_response ('map/map.html', RequestContext(request))
@login_required
#Main map page loading view
def map_page(request):
    if request.method == 'POST':
        place = request.POST['place']

   

        print 'place is %s' % (place)

        return render_to_response('map/map.html', {'place': place}, RequestContext(request))

   

  

    
      

