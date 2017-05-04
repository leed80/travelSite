from createTour.functions import destination_check, destinations_render_data, country_render_data, create_itinerary_id, \
    checkSessionId, get_form_data, user_check
from createTour.models import Destination
from createTour.views import itinerary_ajax_view
from createTour.views import itinerary_page_view, homepage
from itinerary.models import Temp_Itinerary


def tour_load_controller(request):
    # Tour destination select page view
    if request.method == 'GET':
        itinerary_already_generated = checkSessionId(request)
        session_id = itinerary_already_generated[1]
        form_data = get_form_data(request)
        user = user_check(request)
        itinerary = Tour(session_id, user)

        if itinerary_already_generated is "No":
            itinerary.new_tour(form_data)
        else:
            # get current itinerary using sessionid
            itinerary.get_tour()

        template_data = itinerary.compile_tour_data()

        view = itinerary_page_view(template_data, request)
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
        self.itinerary_id = itinerary_id
        self.destinations_list = None
        self.country_dictionary = None
        self.template_data = None
        self.itinerary_data = None
        self.destination = None  # for use when updating itinerary
        self.country_dictionary = None

    def new_tour(self, form_data):
        self.country_id = form_data[0]
        self.date = form_data[1]
        self.travelers = form_data[2]
        self.travel_class = form_data[3]
        self.itinerary_id = create_itinerary_id(self.country_id)
        Temp_Itinerary(itinerary_id=self.itinerary_id, user=self.user, country=self.country_id,
                       travel_class=self.travel_class, date=self.date, travelers=self.travelers, session=self.session_id)

    def get_tour(self):
        itinerary = Temp_Itinerary.objects.get(session=self.session_id)
        self.country_id = itinerary.country
        self.date = itinerary.date
        self.travelers = itinerary.travelers
        self.travel_class = itinerary.travel_class
        self.itinerary_id = itinerary.itinerary_id

    def compile_tour_data(self):
        self.destinations_list = destinations_render_data(self.country_id)
        self.country_dictionary = country_render_data(self.country_id)

        self.template_data = {"country": self.country_id, "date": self.date, "travelers": self.travelers,
                              "class": self.travel_class,
                              "destinations_list": self.destinations_list, "itinerary_id": self.itinerary_id,
                              "country_dictionary": self.country_dictionary}

        return self.template_data

    def compile_itinerary_data(self):
        itinerary = Temp_Itinerary.objects.get(itinerary_id=self.itinerary_id)
        destinations_id = str(itinerary.destinations).split(",")
        self.itinerary_data = []
        for item in destinations_id:
            if item != '0':
                destinations_query_set = Destination.objects.get(country_id=self.country_id, destination_id=item)
                name = destinations_query_set.name
                parsedDestinations = {'destinationID': item, 'name': str(name)}
                self.itinerary_data.append(parsedDestinations)
            else:
                self.itinerary_data.append(item)

        return self.itinerary_data

    def update_itinerary_destinations(self, request):
        self.destination = request.GET['destinations']
        self.itinerary_id = request.GET['itinerary_ID']
        # Get the itinerary object
        itinerary = Temp_Itinerary.objects.get(itineraryID=self.itinerary_id)
        # Get the current destination from the object
        current_destinations = itinerary.destinations
        # Check to see if the destination is currently in the itinerary
        status = destination_check(current_destinations, self.destination)

        if status == 1:
            # If there is no duplicates
            new_destinations = '%s,%s' % (current_destinations, self.destination)
            itinerary.destinations = new_destinations
            itinerary.save()
            return "Y"
        else:
            return "N"

    def delete_itinerary(self):
        return "I'm an incomplete method, please finish me :("


def itinerary_update_delete(request):
    # View to update and delete itinerary
    if request.method == "GET":
        operation = request.GET['operation']
        if operation == "update":

            itinerary = Tour(session_id=None, user=None)
            itinerary_data = itinerary.update_itinerary_destinations(request)

            if itinerary_data == 'Y':
                # collect the itinerary display object and pass it to the view as json
                itinerary_data = itinerary.compile_itinerary_data()
                view = itinerary_ajax_view(itinerary_data)
                return view.load()

            else:
                return itinerary_data

        elif operation == "get":
            itinerary_id = request.GET['itinerary_id']
            itinerary = Tour(itinerary_id=itinerary_id)
            itinerary_data = itinerary.compile_itinerary_data()
            view = itinerary_ajax_view(itinerary_data)
            return view.load()
