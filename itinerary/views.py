from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def viewTempItinerary(request):
	return render_to_response('itinerary/tempItinerary.html', RequestContext(request))


def index(request):
    # Homepage view
    return render_to_response('homepage/home.html', RequestContext(request))


class homepage:
    def __init__(self, request):
        self.request = request

    def load(self):
        return render_to_response('homepage/home.html', RequestContext(self.request))

class create_itinerary(object):
    def __init__(self, request):
        self.request = request

    def load(self):
        return render_to_response('tours/createItinerary', RequestContext(self.request))


class itinerary_page_view:
    def __init__(self, template_data, request):
        self.template_data = template_data
        self.request = request

    def load(self):
        return render_to_response('tours/tour.html', self.template_data, RequestContext(self.request))


def hotels(request):
    # Hotel select page view
    if request.method == 'GET':
        args = mainHotelController(request)
    return render_to_response('tours/hotel.html', args, RequestContext(request))

import json

from django.http import HttpResponse


class itinerary_ajax_view(object):
    def __init__(self, itinerary_data):
        self.itinerary_data = itinerary_data
        self.response = None

    def load(self):
        self.response = json.dumps(self.itinerary_data)
        return HttpResponse(self.response)

def itinerary_deleted(request):

    return render_to_response('tours/itinerary_deleted.html', RequestContext(request))
