from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def viewTempItinerary(request):
	return render_to_response('itinerary/tempItinerary.html', RequestContext(request))



