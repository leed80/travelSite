from createTour.models import country, destination
from hotelManagement.models import hotel, room
from itinerary.models import tempItinerary
import hashlib
import time


# --------------------------- Create Itinerary Controller functions ------------------------------


def createTourMainController(request):
    if not request.session.session_key:
        request.session.modified = True
        request.session.save()

    session_id = request.session.session_key
    country_id = request.GET['country']
    date = request.GET['date']
    travelers = request.GET['travelers']
    travel_class = request.GET['class']
    itinerary_already_generated = checkSessionId(session_id)

    if itinerary_already_generated is "No":
        # create a new itinerary
        newItinerary = itineraryCRUDController()
        newItinerary.create(country_id=country_id, date=date, travelers=travelers, travel_class=travel_class,
                            session_id=session_id, request=request)
        itinerary = tempItinerary.objects.get(session=session_id)
        itinerary_id = itinerary.itineraryID
    else:
        # get current itinerary using sessionid
        itinerary = tempItinerary.objects.get(session=session_id)
        itinerary_id = itinerary.itineraryID
    # get the following objects to populate the page
    destinations_list = destinations_render_data(country_id)
    country_dictionary = country_render_data(country_id)
    itinerary_list = itinerary_data(country_id, itinerary_id)
    # add the objects into a dictionary to be passed to the view
    args = {"country": country_id, "date": date, "travelers": travelers, "class": travel_class,
            "destinationsList": destinations_list, "itineraryID": itinerary_id,
            "countryDictionary": country_dictionary, "itineraryList": itinerary_list}

    return args


def country_render_data(country_id):
    country_data = country.objects.get(countryid=country_id)
    country_dictionary = {"name": str(country_data.name), "countryID": country_data.countryid,
                          "description": str(country_data.description), "lat": country_data.lat,
                          "lng": country_data.lng, "zoom": country_data.zoom}
    return country_dictionary


def destinations_render_data(countryid):
    destinations = destinations_list_object(countryid)
    destinations_list = destinations.destination_data
    return destinations_list


def itinerary_data(countryid, itineraryID):
    # get the current itinerary destinations
    itinerary = tempItinerary.objects.get(itineraryID=itineraryID)
    itinerary_object = itinerary_destinations_class(countryid, itinerary)
    itinerary_destinations = itinerary_object.compile_itinerary_data
    return itinerary_destinations


def checkSessionId(sessionID):
    try:
        sessionCheck = tempItinerary.objects.get(session=sessionID)
        return "Yes"
    except tempItinerary.DoesNotExist:
        return "No"


class destinations_list_object(object):
    def __init__(self, countryid):
        self.countryid = countryid

    def destination_data(self):
        destinations = destination.objects.filter(countryid=self.countryid)
        destinations_list = []
        for item in destinations:
            country_destination = {"destinationid": item.destinationid, "name": str(item.name),
                                   "description": str(item.description),
                                   "lat": item.lat, "lng": item.lng}

            destinations_list.append(country_destination)
        return destinations_list


class itinerary_destinations_class(object):
    def __init__(self, countryid, itinerary):
        self.itinerary = itinerary
        self.countryid = countryid

    def compile_itinerary_data(self):
        destinations_id = self.itinerary.destinations
        destinations_ids = str(destinations_id).split(",")
        itinerary_destinations = []
        for item in destinations_ids:
            try:
                destinations_query_set = destination.objects.get(countryid=self.countryid, destinationid=item)
                name = destinations_query_set.name
                parsedDestinations = {'destinationID': item, 'name': str(name)}
                itinerary_destinations.append(parsedDestinations)
            except destination.DoesNotExist:
                return {'destinationID': 0, 'name': "You have not added any destinations to your itinerary yet"}

        return itinerary_destinations


class itineraryCRUDController(object):
    def create(self, country_id, date, travelers, travel_class, session_id, request):
        # code to create a new itinerary
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

        return itinerary_id

    def update(self, itineraryID, updateType, updateData):
        # code to update the itinerary
        print('hello')

    def delete(self, itineraryID):
        # code to delete the itinerary
        print('hello')


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


# ----------------------- Hotel controller functions -----------------------------------------


def mainHotelController(request):
    # this will be the main controller for the hotels page
    return "test"


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


def itineraryUpdateDeleteController(request):
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

        return itinerary_list
