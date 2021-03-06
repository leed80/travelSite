from rest_framework import serializers
from django.contrib.auth.models import User
from itinerary.models import Temp_Itinerary, Complete_Itinerary, Country, Destination
from hotelManagement.models import hotel, room

class countrySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Country
		fields = ('countryid', 'name', 'description', 'lat', 'lng', 'zoom')

class destinationSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Destination
		fields = ('destinationid', 'name', 'countryid', 'description', 'lat', 'lng')

class hotelSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hotel
		fields = ('hotelid', 'name', 'address', 'description', 'destinationid', 'rating', 'countryid', 'city', 'postcode', 'checkIn', 'checkOut', 'hotelPolicy', 'roomInformation', 'checkInInstructions', 'suppliers')

class roomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = room
		fields = ('hotelid', 'roomTypeCode', 'name', 'description')

class tempItinerarySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Temp_Itinerary
		fields = ('pk','travelers', 'date', 'travelClass', 'hotels', 'destinations', 'country', 'itineraryID', 'user','time', 'session')

class completeItinerarySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Complete_Itinerary
		fields = ('travelers', 'date', 'travelClass', 'hotels', 'destinations', 'country', 'itineraryID', 'user')









