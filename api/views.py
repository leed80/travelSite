from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators import csrf 
from rest_framework.decorators import api_view
from rest_framework import viewsets, generics
from rest_framework import permissions
from serializers import countrySerializer, destinationSerializer, hotelSerializer, roomSerializer, tempItinerarySerializer, completeItinerarySerializer
from createTour.models import country, destination
from hotelManagement.models import hotel, room
from itinerary.models import tempItinerary, completeItinerary
import requests

# View for all country objects
class countryViewSet(generics.ListAPIView):
	serializer_class = countrySerializer

	def get_queryset(self):
		queryset = country.objects.all()
		countryid = self.request.query_params.get('countryid', None)
		if countryid is not None:
			queryset = country.objects.filter(countryid=countryid)
			return queryset
		else:
			return queryset

# View for destination objects with specific country
class destinationViewSet(generics.ListAPIView):
	serializer_class = destinationSerializer

	def get_queryset(self):
		queryset = destination.objects.all()
		countryid = self.request.query_params.get('countryid', None)
		name = self.request.query_params.get('name', None)
		if name is not None:
			queryset = queryset.filter(name=name)
			return queryset
		elif countryid is not None:
			queryset = queryset.filter(countryid=countryid)
			return queryset
		else:
			return queryset

# View for all hotel objects
class hotelViewSet(generics.ListAPIView):
	serializer_class = hotelSerializer

	def get_queryset(self):
		queryset = hotel.objects.all()
		destinationid = self.request.query_params.get('destinationid', None)
		if destinationid is not None:
			queryset = hotel.objects.filter(destinationid=destinationid)
			return queryset
		else:
			return queryset

class roomViewSet(generics.ListAPIView):
	serializer_class = roomSerializer

	def get_queryset(self):
		queryset = room.objects.all()
		hotelid = self.request.query_params.get('hotelid', None)
		if hotelid is not None:
			queryset = hotel.objects.filter(hotelid=hotelid)
			return queryset
		else:
			return queryset


class tempItineraryViewSet(generics.ListAPIView):
	serializer_class = tempItinerarySerializer

	def get_queryset(self):
		queryset = tempItinerary.objects.all()
		itineraryID = self.request.query_params.get('itineraryID', None)
		if itineraryID is not None:
			queryset = tempItinerary.objects.filter(itineraryID = itineraryID)
			return queryset
		else:
			return queryset

class updateTempItinerary(generics.UpdateAPIView):

	# update the database (the UpdateAPIView will update with the info passed in the url) 
	queryset = tempItinerary.objects.all()
	serializer_class = tempItinerarySerializer
	# set the permission so anyone can put
	permission_classes = (permissions.AllowAny,)

class deleteTempItinerary(generics.DestroyAPIView):
	queryset = tempItinerary.objects.all()
	serializer_class = tempItinerarySerializer
	permission_classes = (permissions.AllowAny,)

# Create a class to delete the temp itinerary

	

	# def get_queryset(self):
	# 	queryset = tempItinerary.objects.all()
	# 	itineraryID = self.request.query_params.get('itineraryID', None)
	# 	destinations = self.request.query_params.get('destinations', None)
	# 	hotels = self.request.query_params.get('hotels', None)
	# 	if itineraryID is not None:
	# 		queryset = tempItinerary.objects.filter(itineraryID=itineraryID)
	# 		if destinations is not None:
	# 			#update destinations here
	# 			return queryset
	# 		elif hotels is not None:
	# 			#update hotels here
	# 			return queryset
	# 		else:
	# 			return queryset

	

	
	

	

class completeItineraryViewSet(generics.ListAPIView):
	serializer_class = completeItinerarySerializer

	def get_queryset(self):
		queryset = completeItinerary.objects.all()
		itineraryID = self.request.query_params.get('itineraryID', None)
		if itineraryID is not None:
			queryset = completeItinerary.objects.filter(itineraryID = itineraryID)
			return queryset
		else:
			return queryset

	

    






