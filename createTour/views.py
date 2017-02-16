from __future__ import print_function
import hashlib
import time

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from createTour.models import country, destination
from hotelManagement.models import hotel, room
from itinerary.models import tempItinerary


def index(request):
    return render_to_response('homepage/home.html', RequestContext(request))


def details(request):
    if request.method == 'GET':
        if not request.session.session_key:
            request.session.modified = True
            request.session.save()

        session_id = request.session.session_key
        country_id = request.GET['country']
        date = request.GET['date']
        travelers = request.GET['travelers']
        travel_class = request.GET['class']

        itinerary_already_generated = checkSessionId(session_id)

        print('sessionID =  %s' % session_id)

        if itinerary_already_generated is "No":
            # Check if the current user is logged in or if they are a guest
            if request.user.is_authenticated():
                current_user = request.user
            else:
                current_user = 'Guest'

            # setup the new itinerary
            saved = False

            while not saved:
                itinerary_id = createItineraryID(country_id)
                status = tempItinerarySetup(itinerary_id, current_user, date, travelers, travel_class, country_id,
                                            session_id)
                if not status:
                    saved = True
        else:
            itinerary = tempItinerary.objects.get(session=session_id)
            itinerary_id = itinerary.itineraryID

        destinations_list = destinations_render_data(country_id)
        country_dictionary = country_render_data(country_id)
        itinerary_list = itinerary_data(country_id, itinerary_id)

        args = {"country": country_id, "date": date, "travelers": travelers, "class": travel_class,
                "destinationsList": destinations_list, "itineraryID": itinerary_id,
                "countryDictionary": country_dictionary, "itineraryList": itinerary_list}

        return render_to_response('tours/tour.html', args, RequestContext(request))
    else:
        # go back to the homepage
        return render_to_response('homepage/home.html', RequestContext(request))


def country_render_data(country_id):
    country_data = country.objects.filter(countryid=country_id)
    country_id = country_data[0].countryid
    country_name = country_data[0].name
    country_description = country_data[0].description
    country_lat = country_data[0].lat
    country_lng = country_data[0].lng
    country_zoom = country_data[0].zoom

    country_dictionary = {"name": str(country_name), "ID": country_id, "description": str(country_description),
                          "lat": country_lat, "lng": country_lng, "zoom": country_zoom}

    return country_dictionary


def destinations_render_data(countryid):
    destinations = destination.objects.filter(countryid=countryid)
    destinations_list = []

    count = 0
    while count < len(destinations):
        current_destination = destinations[count]
        destination_id = current_destination.destinationid
        destination_name = current_destination.name
        destination_description = current_destination.description
        destination_lat = current_destination.lat
        destination_lng = current_destination.lng
        destination_dictionary = {"destinationid": destination_id, "name": str(destination_name),
                                  "description": str(destination_description), "lat": destination_lat,
                                  "lng": destination_lng}
        destinations_list.append(destination_dictionary)

        count += 1
    return destinations_list


def itinerary_data(countryid, itineraryID):
    # get the current itinerary destinations
    itinerary = tempItinerary.objects.filter(itineraryID=itineraryID)

    # return current itinerary destinations as a list
    destinations_id = itinerary[0].destinations
    destinations_ids = str(destinations_id).split(",")

    destinations_query_set = destination.objects.filter(countryid=countryid)

    itinerary_destinations = []

    for item in destinations_ids:
        count = 0
        while count < len(destinations_query_set):
            name = destinations_query_set[count].name
            querySetDestinationID = destinations_query_set[count].destinationid
            if int(item) == querySetDestinationID:
                parsedDestinations = {}
                parsedDestinations['destinationID'] = querySetDestinationID
                parsedDestinations['name'] = str(name)
                itinerary_destinations.append(parsedDestinations)
            count = count + 1
    return itinerary_destinations


def checkSessionId(sessionID):
    try:
        sessionCheck = tempItinerary.objects.get(session=sessionID)
        return "Yes"
    except tempItinerary.DoesNotExist:
        return "No"


def tempItinerarySetup(itineraryID, currentUser, date, travelers, travelclass, countryid, sessionID):
    # setup the new itinerary

    try:
        checkItineraryID = tempItinerary.objects.get(itineraryID=itineraryID)
        print('duplicate')
        return "duplicate"
    except tempItinerary.DoesNotExist:
        makeTempItinerary = tempItinerary(itineraryID=itineraryID, user=currentUser, country=countryid,
                                          travelClass=travelclass, date=date, travelers=travelers, session=sessionID)
        makeTempItinerary.save()
        print('saved')


def createItineraryID(countryid):
    # This function creates the itineraryID
    timestamp = str(time.time())
    itineraryID = hashlib.md5(timestamp + countryid).hexdigest()
    itineraryID = itineraryID[:8]
    return itineraryID


def hotels(request):
    if request.method == 'GET':
        itineraryID = request.GET['itineraryID']

        # get itinerary Data
        itineraryData = tempItinerary.objects.filter(itineraryID=itineraryID)
        country = itineraryData[0].country
        finalMarkup = appendDestinations(itineraryData, country)
        args = {'finalMarkup': finalMarkup}

    return render_to_response('tours/hotel.html', args, RequestContext(request))


def appendDestinations(itineraryData, country):
    # Get destinations string from the itinerary and split into array
    itineraryDestinations = itineraryData[0].destinations.split(",")

    # For each destination create the HTML for page

    finalMarkup = ""

    count = 0
    while count < len(itineraryDestinations):
        # parse each destination in the itinerary
        parsedItineraryDestination = int(itineraryDestinations[count])
        # use the parsed destination to get the destination data from the database
        singleDestination = destination.objects.filter(destinationid=parsedItineraryDestination, countryid=country)

        destinationName = singleDestination[0].name

        destinationContainerStart = '<div id="destinationcontainer%s" class="destinationcontainer">' % (
        parsedItineraryDestination)
        destinationNameMarkup = '<h2 id="destination%s" class="destinationName">%s</h2>' % (
        parsedItineraryDestination, destinationName)
        destinationcontainerEnd = "</div>"
        # get the hotel html
        hotelMarkup = appendHotels(parsedItineraryDestination, country)
        destinationMarkup = "%s %s %s %s" % (
        destinationContainerStart, destinationNameMarkup, hotelMarkup, destinationcontainerEnd)
        finalMarkup = finalMarkup + destinationMarkup
        count = count + 1

    return finalMarkup


def appendHotels(parsedItineraryDestination, country):
    # get hotels from the database that match the ID
    hotels = hotel.objects.filter(countryid=country, destinationid=parsedItineraryDestination)
    # for each of them create html
    count = 0
    while count < len(hotels):
        thisHotel = hotels[count]
        hotelId = thisHotel.hotelid
        hotelName = thisHotel.name
        hotelAddress = thisHotel.address
        hotelDescription = thisHotel.description
        hotelRating = thisHotel.rating
        hotelCity = thisHotel.city
        hotelPostcode = thisHotel.postcode
        hotelCheckin = thisHotel.checkIn
        hotelCheckout = thisHotel.checkOut
        hotelPolicy = thisHotel.hotelPolicy
        roomInformation = thisHotel.roomInformation
        checkInInstructions = thisHotel.checkInInstructions

        hotelContainerStart = '<div id="hotel%s" class="hotelContainer">' % (hotelId)
        hotelContainerEnd = '</div>'

        hotelNameMarkup = '<h2 id="name%s" class="hotelName">%s</h2>' % (hotelId, hotelName)

        hotelAddressMarkup = '<p id="address%s" class="hotelAddress">%s, %s, %s</p>' % (
        hotelId, hotelAddress, hotelCity, hotelPostcode)

        hotelRatingMarkup = '<p id="rating%s" class="hotelRating">%s</p>' % (hotelId, hotelRating)

        hotelDescriptionMarkup = '<p id="description%s" class="hotelName">%s</p>' % (hotelId, hotelDescription)

        hotelCheckInOutMarkup = '<p id="InOut%s" class="hotelInOut">Checkin: %s Checkout: %s</p>' % (
        hotelId, hotelCheckin, hotelCheckout)

        hotelCheckInInstructionsMarkup = '<p id="checkInInstructions%s" class="hotelCheckin">%s</p>' % (
        hotelId, checkInInstructions)

        hotelPolicyMarkup = '<p id="policy%s" class="hotelPolicy">%s</p>' % (hotelId, hotelPolicy)

        roomInformationMarkup = '<p id="roomInformation%s" class="roomInformation">%s</p>' % (hotelId, roomInformation)

        # get the rooms
        roomMarkup = rooms(hotelId)

        finalHotelMarkup = '%s %s %s %s %s %s %s %s %s %s %s' % (
        hotelContainerStart, hotelNameMarkup, hotelAddressMarkup, hotelRatingMarkup, hotelDescriptionMarkup,
        hotelCheckInOutMarkup, hotelCheckInInstructionsMarkup, hotelPolicyMarkup, roomInformationMarkup, roomMarkup,
        hotelContainerEnd)
        return finalHotelMarkup
    # combine into a chunk of HTML 


def rooms(hotelId):
    rooms = room.objects.filter(hotelid=hotelId)

    count = 0

    while count < len(rooms):
        thisRoom = rooms[count]
        roomName = thisRoom.name
        roomTypeCode = thisRoom.roomTypeCode
        roomDescription = thisRoom.description

        roomContainerStart = '<div id="room%s" class="roomContainer>' % (roomTypeCode)
        roomContainerEnd = '</div>'

        roomNameMarkup = '<h3 id="name%s" class="roomName">%s</h3>' % (roomTypeCode, roomName)
        roomDescriptionMarkup = '<p id="description%s" class="roomDescription">%s</p>' % (roomTypeCode, roomDescription)

        # ratesMarkup = expediaRates(hotelId, roomTypeCode)
        ratesMarkup = 0

        finalRoomMarkup = '%s %s %s %s %s' % (
        roomContainerStart, roomNameMarkup, roomDescriptionMarkup, ratesMarkup, roomContainerEnd)
        return finalRoomMarkup


def itineraryCRUD(request):
    if request.method == "GET":
        operation = request.GET['operation']
        if operation == "update":
            itinerary_id = request.GET['itineraryID']
            destination = request.GET['destinations']

            itinerary = tempItinerary.objects.filter(itineraryID=itinerary_id)
            destinations = itinerary[0].destinations
            countryID = itinerary[0].country
            newDestinations = '%s%s' % (destinations, destination)
            itinerary.destinations = newDestinations
            itinerary.update()


            print('%s & %s' % (countryID, itinerary_id))

            itinerary_list = itinerary_data(countryID, itinerary_id)

            print(itinerary_list)

            return HttpResponse(itinerary_list)



            # def expediaRates(hotelId, roomTypeCode, arrivalDate, leaveDate):

            # 	API = '5qihbibdm199m03leh63sin4jo'

            # 	SK = '2ense2u0smh9a'

            # 		timestamp = str(int(time.time()))

            # 	# Use md5 hash protocol to make a signature out of the expedia API, secretkey and the timestamp. reutnred in hexidecimal format
            # 	sig = md5.new(API + SK + timestamp).hexdigest()
            # 	eanurl = ('http://api.ean.com/ean-services/rs/hotel/v3/info?minorRev=30&cid=422852&sig=%s&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&hotelId=%s&options=0') % (sig, hotelID)
            # 	response = urllib2.urlopen(eanurl)
            # 	data = json.load(response)


            # def rates(request):
            # 	# get the info from the frontend
            # 	if request.method == 'GET':
            # 		hotelid = request.GET['hotelid']
            # 		eanArriveDate = request.GET['eanArriveDate']
            # 		eanLeaveDate = request.GET['eanLeaveDate']
            # 		guests = request.GET['guests']
            # 		country = request.GET['country']
            # 		tour = request.GET['tour']
            # 		hotelref = request.GET['hotelref']


            # 		API = '5qihbibdm199m03leh63sin4jo'

            # 		SK = '2ense2u0smh9a'

            # 		timestamp = str(int(time.time()))

            # 		# Use md5 hash protocol to make a signature out of the expedia API, secretkey and the timestamp. reutnred in hexidecimal format
            # 		sig = md5.new(API + SK + timestamp).hexdigest()

            # 		print sig

            # 		print hotelref

            # 		hotel = hotelTable.objects.get(refNumber=hotelref)
            # 		roomtypecode = hotel.roomtypecode
            # 		ratecode = hotel.ratecode

            # 		print roomtypecode
            # 		print ratecode



            # 		eanurl = ('http://api.ean.com/ean-services/rs/hotel/v3/avail?minorRev=30&cid=422852&sig=%s&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&hotelId=%s&arrivalDate=%s&departureDate=%s&room1=2&rateCode=%s&roomTypeCode=%s') % (sig, hotelid, eanArriveDate, eanLeaveDate, ratecode, roomtypecode)

            # 		response = urllib2.urlopen(eanurl)
            # 		data = json.load(response)
            # 		data = data['HotelRoomAvailabilityResponse']

            # 		print 'printing data %s' % (data)




            # 		finalRate = data['HotelRoomResponse']['RateInfos']['RateInfo']['ChargeableRateInfo']['@total']
            # 		rateType = data['HotelRoomResponse']['RateInfos']['RateInfo']['rateType']
            # 		supplierType = data['HotelRoomResponse']['supplierType']
            # 		rateKey = data['HotelRoomResponse']['RateInfos']['RateInfo']['RoomGroup']['Room']['rateKey']

            # 		print('finalRate is %s' % (finalRate))
            # 		print('rateType is %s' % (rateType))
            # 		print('supplierType is %s' % (supplierType))
            # 		print('rateKey is %s' % (rateKey))

            # 		args = {"finalRate": finalRate, "rateType": rateType, "supplierType": supplierType, "rateKey": rateKey, "roomTypeCode": roomtypecode, "rateCode": ratecode}
            # 		return HttpResponse(args)


            # def tourselect(request):
            # 	if request.method == 'GET':
            # 		country = request.GET['country']
            # 		date = request.GET['date']
            # 		travelers = request.GET['travelers']
            # 		travelclass = request.GET['class']
            # 		tour = request.GET['tourtitle']

            # 		# Get the signature

            # 		API = '5qihbibdm199m03leh63sin4jo'

            # 		SK = '2ense2u0smh9a'

            # 		timestamp = str(time.time())

            # 		SIG = md5.new(API + SK + timestamp).hexdigest()

            # 		print SIG

            # 		args = { 'country': country,
            # 				 'date': date,
            # 				 'travelers': travelers,
            # 				 'class': travelclass,
            # 				 'tour': tour,
            # 				 'sig': SIG

            # 		}

            # 		return render_to_response('tours/tourselect.html', args, RequestContext(request))

            # #def bookhotels(request):
            # 	#if request.method == 'GET':

            # 	#We then take the package peramieters sent back by the title or each hotel along with the above information and send it too the backend for booking.

            # 	# The backend then interacts with the zumata api
            # 	# too book all the selected hotels and displays 
            # 	# all the information needed on a later page.
