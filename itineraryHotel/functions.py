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











