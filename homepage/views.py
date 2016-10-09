from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.template import RequestContext


def index(request):	
	return render_to_response ('homepage/home.html', RequestContext(request))
 
