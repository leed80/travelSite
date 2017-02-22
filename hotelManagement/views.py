from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.template import RequestContext
from createTour.models import country
from itinerary.models import tempItinerary
import time
import random
import hashlib
import md5
import urllib2
import json
from datetime import datetime
from hotelManagement.models import hotel, room

# Create your views here.

def hotelManagement(request):
	return render_to_response('hotelManagement/home.html', RequestContext(request))


def addHotel(request):
	if request.method == 'POST':
		hotelID = request.POST['hotelID']
		country = request.POST['country']
		destination = request.POST['destination']

		API = '5qihbibdm199m03leh63sin4jo'

		SK = '2ense2u0smh9a'

 		timestamp = str(int(time.time()))

		# Use md5 hash protocol to make a signature out of the expedia API, secretkey and the timestamp. reutnred in hexidecimal format
		sig = md5.new(API + SK + timestamp).hexdigest()

		eanurl = ('http://api.ean.com/ean-services/rs/hotel/v3/info?minorRev=30&cid=422852&sig=%s&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&hotelId=%s&options=0') % (sig, hotelID)
		response = urllib2.urlopen(eanurl)
		data = json.load(response)
		hotelSummary = data['HotelInformationResponse']['HotelSummary']

		name = hotelSummary['name']
		address = hotelSummary['address1']
		city = hotelSummary['city']
		postcode = hotelSummary['postalCode']
		latitude = hotelSummary['latitude']
		longitude = hotelSummary['longitude']
		
		hotelDetails = data['HotelInformationResponse']['HotelDetails']

		description = hotelDetails['propertyDescription']
		checkin = hotelDetails['checkInTime']
		checkout = hotelDetails['checkOutTime']
		hotelPolicy = hotelDetails['hotelPolicy']
		roomInformation = hotelDetails['roomInformation']
		checkInInstructions = hotelDetails['checkInInstructions']


		suppliers = data['HotelInformationResponse']['Suppliers']['Supplier']

		newHotel = hotel(hotelid=hotelID, name=name, address=address, description=description, destinationid=destination, rating=0, countryid=country, city=city, postcode=postcode, latitude=latitude, longitude=longitude, checkIn=checkin, checkOut=checkout, hotelPolicy=hotelPolicy, roomInformation=roomInformation, checkInInstructions=checkInInstructions, suppliers=suppliers)
		newHotel.save()

		args= {'saved' : "Hotel Saved"}




		return render(request, 'hotelManagement/addHotel.html', args)
	return render(request, 'hotelManagement/addHotel.html')

def addRoom(request):
	if request.method == 'POST':
		hotelID = request.POST['hotelID']
		
		API = '5qihbibdm199m03leh63sin4jo'

		SK = '2ense2u0smh9a'

 		timestamp = str(int(time.time()))

		# Use md5 hash protocol to make a signature out of the expedia API, secretkey and the timestamp. reutnred in hexidecimal format
		sig = md5.new(API + SK + timestamp).hexdigest()

		eanurl = ('http://api.ean.com/ean-services/rs/hotel/v3/info?minorRev=30&cid=422852&sig=%s&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&hotelId=%s&options=0') % (sig, hotelID)
		response = urllib2.urlopen(eanurl)
		data = json.load(response)
		roomType = data['HotelInformationResponse']['RoomTypes']['RoomType']
		# Get the number of different room types
		size = int(data['HotelInformationResponse']['RoomTypes']["@size"])
		count = 0
		while count < size:
			roomTypeCode = roomType[count]['@roomCode']
			name = roomType[count]['description']
			description = roomType[count]['descriptionLong']

			addRoom = room(hotelid=hotelID, roomTypeCode=roomTypeCode, name=name, description=description)
			addRoom.save()
			count = count + 1

		roomMessage = "%s room(s) saved" % (size)
		

		args= {'saved' : roomMessage}


		return render(request, 'hotelManagement/addRoom.html', args)
	return render(request, 'hotelManagement/addRoom.html')
