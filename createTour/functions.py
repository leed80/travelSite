def getFormData(request):
    country_id = str(request.GET['country'])
    date = request.GET['date']
    travelers = request.GET['travelers']
    travel_class = request.GET['class']

    return[country_id, date, travelers, travel_class]



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


def itinerary_data(countryID, itineraryID):
    # get the current itinerary destinations
    itinerary_object = itineraryCRUD()
    itinerary_destinations = itinerary_object.retieve_destinations(countryID, itineraryID)
    print(itinerary_destinations)
    return itinerary_destinations


def checkSessionId(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.modified = True
        request.session.save()
        return ["No", session_id]
    else:
        try:
            tempItinerary.objects.get(session=session_id)
            return ["Yes", session_id]
        except tempItinerary.DoesNotExist:
            return ["No", session_id]


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

def userCheck(request):
    if request.user.is_authenticated():
        current_user = request.user
    else:
        current_user = 'Guest'

    return current_user


class itineraryCRUD(object):

    def __init__(self, itineraryID='null'):
        self.itineraryID = itineraryID

    def create(self, country_id, date, travelers, travel_class, session_id, request):
        # code to create a new itinerary
        # Check if the current user is logged in or if they are a guest

        # setup the new itinerary
        saved = False
        while not saved:
            itinerary_id = createItineraryID(country_id)
            status = tempItinerarySetup(itinerary_id, current_user, date, travelers, travel_class, country_id,
                                        session_id)
            if not status:
                saved = True

        return itinerary_id

    def retieve_destinations(self, countryid):
        itinerary = tempItinerary.objects.get(itineraryID=self.itineraryID)
        destinations_id = itinerary.destinations
        destinations_ids = str(destinations_id).split(",")
        print "destinations is %s" % destinations_ids
        itinerary_destinations = []
        for item in destinations_ids:
            print "item is %s" % item
            if item != '0':
                destinations_query_set = destination.objects.get(countryid=countryid, destinationid=item)
                name = destinations_query_set.name
                parsedDestinations = {'destinationID': item, 'name': str(name)}
                itinerary_destinations.append(parsedDestinations)
            else:
                itinerary_destinations.append(item)


        return itinerary_destinations


    def update_destinations(self, newDestination):
        # Get the itinerary object
        itinerary = tempItinerary.objects.get(itineraryID=self.itineraryID)
        #Get the country from the itinerary object
        country_id = itinerary.country
        # Get the current destitnation from the object
        currentDestinations = itinerary.destinations
        # Check to see if the destination is currently in the itinerary
        status = destinationCheck(currentDestinations, newDestination)

        if status == 1:
            # If there is no duplicates
            newDestinations = '%s,%s' % (currentDestinations,newDestination)
            itinerary.destinations = newDestinations
            itinerary.save()
            return country_id
        else:
            return "no"



    def delete(self, itineraryID):
        # code to delete the itinerary
        print('hello')

def destinationCheck(currentDestinations, newDestination):
    currentDestinationsSplit = currentDestinations.split(',')
    for destination in currentDestinationsSplit:
        if destination == newDestination:
            return 0
    return 1





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


def itineraryUpdateDeleteController(request):
    operation = request.GET['operation']
    if operation == "update":
        destination = request.GET['destinations']
        itineraryID = request.GET['itineraryID']
        itineraryUpdate = itineraryCRUD(itineraryID)
        itineraryData = itineraryUpdate.update_destinations(destination)
        if itineraryData == 'no':
            return itineraryData
        else:
            itinerary_list = itineraryUpdate.retieve_destinations(itineraryData)
            return itinerary_list
    elif operation == "get":
        countryID = request.GET['countryID']
        itineraryID = request.GET['itineraryID']
        itineraryGet = itineraryCRUD(itineraryID)
        itineraryList = itineraryGet.retieve_destinations(countryID)
        return itineraryList


def createItineraryID(countryid):
    # type: (object) -> object
    # This function creates the itineraryID
    timestamp = str(time.time())
    itineraryID = hashlib.md5(timestamp + countryid).hexdigest()
    itineraryID = itineraryID[:8]
    return itineraryID


