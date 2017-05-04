from createTour.functions import destinationCheck, destinations_render_data, country_render_data, createItineraryID, \
    checkSessionId, getFormData, userCheck
from createTour.models import destination
from createTour.views import itineraryAjaxView
from createTour.views import itineraryPageView, homepage
from itinerary.models import tempItinerary


def tourController(request):
    # Tour destination select page view
    if request.method == 'GET':
        itinerary_already_generated = checkSessionId(request)
        session_id = itinerary_already_generated[1]
        formData = getFormData(request)
        user = userCheck(request)
        itinerary = Tour(session_id, user)

        if itinerary_already_generated is "No":
            itinerary.newTour(formData)
        else:
            # get current itinerary using sessionid
            itinerary.getTour()

        templateData = itinerary.compileTourData()

        view = itineraryPageView(templateData, request)
        return view.load()

    else:
        # go back to the homepage
        view = homepage(request)
        return view.load()

class Tour:

    def __init__(self, session_id=None, user=None, itinerary_id=None):
        self.country_id = None
        self.date = None
        self.travelers = None
        self.travel_class = None
        self.user = user
        self.session_id = session_id
        self.itineraryID = itinerary_id
        self.destinations_list = None
        self.countryDictionary = None
        self.templateData = None
        self.itineraryData = None
        self.destination = None #for use when updating itinerary
        self.country_dictionary = None

    def newTour(self, form_data):
        self.country_id = form_data[0]
        self.date = form_data[1]
        self.travelers = form_data[2]
        self.travel_class = form_data[3]
        self.itineraryID = createItineraryID(self.country_id)
        tempItinerary(itineraryID=self.itineraryID, user=self.user, country=self.country_id,
                              travelClass=self.travel_class, date=self.date, travelers=self.travelers, session=self.session_id)


    def getTour(self):
        itinerary = tempItinerary.objects.get(session=self.session_id)
        self.country_id = itinerary.country
        self.date = itinerary.date
        self.travelers = itinerary.travelers
        self.travel_class = itinerary.travelClass
        self.itineraryID = itinerary.itineraryID


    def compileTourData(self):
        self.destinations_list = destinations_render_data(self.country_id)
        self.country_dictionary = country_render_data(self.country_id)

        self.templateData = {"country": self.country_id, "date": self.date, "travelers": self.travelers, "class": self.travel_class,
                "destinationsList": self.destinations_list, "itineraryID": self.itineraryID,
                "countryDictionary": self.country_dictionary}

        return self.templateData

    def compileItineraryData(self):
        itinerary = tempItinerary.objects.get(itineraryID=self.itineraryID)
        destinations_id = str(itinerary.destinations).split(",")
        self.itineraryData = []
        for item in destinations_id:
            if item != '0':
                destinations_query_set = destination.objects.get(countryid=self.country_id, destinationid=item)
                name = destinations_query_set.name
                parsedDestinations = {'destinationID': item, 'name': str(name)}
                self.itineraryData.append(parsedDestinations)
            else:
                self.itineraryData.append(item)

        return self.itineraryData


    def updateItineraryDestinations(self, request):
        self.destination = request.GET['destinations']
        self.itineraryID = request.GET['itineraryID']
        # Get the itinerary object
        itinerary = tempItinerary.objects.get(itineraryID=self.itineraryID)
        # Get the current destination from the object
        currentDestinations = itinerary.destinations
        # Check to see if the destination is currently in the itinerary
        status = destinationCheck(currentDestinations, self.destination)

        if status == 1:
            # If there is no duplicates
            newDestinations = '%s,%s' % (currentDestinations, self.destination)
            itinerary.destinations = newDestinations
            itinerary.save()
            return "Y"
        else:
            return "N"


    def deleteItinerary(self):
        return "I'm an incomplete method, please finish me :("


def itineraryUpdateDelete(request):
    # View to update and delete itinerary
    if request.method == "GET":
        operation = request.GET['operation']
        if operation == "update":

            itinerary = Tour(session_id=None, user=None)
            itineraryData = itinerary.updateItineraryDestinations(request)

            if itineraryData == 'Y':
                # collect the itinerary display object and pass it to the view as json
                itineraryData = itinerary.compileItineraryData()
                view = itineraryAjaxView(itineraryData)
                return view.load()

            else:
                return itineraryData

        elif operation == "get":
            itineraryID = request.GET['itineraryID']
            itinerary = Tour(itinerary_id=itineraryID)
            itineraryData = itinerary.compileItineraryData()
            view = itineraryAjaxView(itineraryData)
            return view.load()




