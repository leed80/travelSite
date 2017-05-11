from django.http import HttpResponse

from itinerary.views import homepage, itinerary_page_view, itinerary_ajax_view
from itinerary.functions import destination_check, destinations_render_data, country_render_data, create_itinerary_id, \
    check_session_id, get_form_data, user_check
from itinerary.models import Temp_Itinerary, Destination


def itinerary_load_controller(request):
    # Tour destination select page view
    if request.method == 'GET':
        itinerary_already_generated = check_session_id(request)
        session_id = itinerary_already_generated[1]
        form_data = get_form_data(request)
        user = user_check(request)
        itinerary = Itinerary(session_id, user)

        if itinerary_already_generated is "No":
            itinerary.new_itinerary(form_data)
        else:
            # get current itinerary using sessionid
            itinerary.get_itinerary()

        template_data = itinerary.compile_page_build_data()

        view = itinerary_page_view(template_data, request)
        return view.load()

    else:
        # go back to the homepage
        view = homepage(request)
        return view.load()


class Itinerary(object):
    def __init__(self, session_id=None, user=None, itinerary_id=None):
        self.country_id = None
        self.date = None
        self.travelers = None
        self.travel_class = None
        self.user = user
        self.session_id = session_id
        self.itinerary_id = itinerary_id
        self.destinations_data = None
        self.country_data = None
        self.template_data = None
        self.itinerary_data = None
        self.destination = None  # for use when updating itinerary
        self.country_data = None

    def new_itinerary(self, form_data):
        self.country_id = form_data[0]
        self.date = form_data[1]
        self.travelers = form_data[2]
        self.travel_class = form_data[3]
        self.itinerary_id = create_itinerary_id(self.country_id)
        Temp_Itinerary(itinerary_id=self.itinerary_id, user=self.user, country=self.country_id,
                       travel_class=self.travel_class, date=self.date, travelers=self.travelers, session=self.session_id)

    def get_itinerary(self):
        itinerary = Temp_Itinerary.objects.get(session=self.session_id)
        self.country_id = itinerary.country
        self.date = itinerary.date
        self.travelers = itinerary.travelers
        self.travel_class = itinerary.travel_class
        self.itinerary_id = itinerary.itinerary_id

    def compile_page_build_data(self):
        self.destinations_data = destinations_render_data(self.country_id)
        self.country_data = country_render_data(self.country_id)

        self.template_data = dict(country=self.country_id, date=self.date, travelers=self.travelers,
                                  travel_class=self.travel_class, destinations_data=self.destinations_data,
                                  itinerary_id=self.itinerary_id, country_data=self.country_data)

        return self.template_data

    def compile_itinerary_data(self):
        itinerary = Temp_Itinerary.objects.get(itinerary_id=self.itinerary_id)
        destinations = str(itinerary.destinations)
        self.country_id = itinerary.country
        destinations_id = destinations.split(",")
        self.itinerary_data = []
        for item in destinations_id:
            if item != '0':
                destinations_query = Destination.objects.get(country_id=self.country_id, destination_id=int(item))
                name = destinations_query.name
                parsedDestinations = {'destination_id': item, 'name': str(name)}
                self.itinerary_data.append(parsedDestinations)


        return self.itinerary_data

    def update_itinerary_destinations(self, request):
        self.destination = request.GET['destinations']
        self.itinerary_id = request.GET['itinerary_id']
        # Get the itinerary object
        itinerary = Temp_Itinerary.objects.get(itinerary_id=self.itinerary_id)
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

    def remove_itinerary_destination(self, request):
        self.destination = request.GET['destinations']
        self.itinerary_id = request.GET['itinerary_id']
        # Get the itinerary object
        itinerary = Temp_Itinerary.objects.get(itinerary_id=self.itinerary_id)
        current_destinations = itinerary.destinations
        destinations_id = current_destinations.split(",")
        new_destinations = []
        for item in destinations_id:
            if item != self.destination:
                new_destinations.append(item)

        itinerary.destinations = ",".join(str(x) for x in new_destinations)
        itinerary.save()



    def delete_itinerary(self):
        itinerary = Temp_Itinerary.objects.get(itinerary_id=self.itinerary_id)
        itinerary.delete()
        # Create a view to handle handle the deleted itinerary



        return "I'm an incomplete method, please finish me :("


def itinerary_update_delete(request):
    # View to update and delete itinerary
    if request.method == "GET":
        operation = request.GET['operation']
        if operation == "update":

            itinerary = Itinerary()
            itinerary_data = itinerary.update_itinerary_destinations(request)

            if itinerary_data == 'Y':
                # collect the itinerary display object and pass it to the view as json
                itinerary_data = itinerary.compile_itinerary_data()
                view = itinerary_ajax_view(itinerary_data)
                return view.load()

            else:
                return HttpResponse(itinerary_data)

        elif operation == "get":
            itinerary_id = request.GET['itinerary_id']
            itinerary = Itinerary(itinerary_id=itinerary_id)
            itinerary_data = itinerary.compile_itinerary_data()
            print(itinerary_data)
            view = itinerary_ajax_view(itinerary_data)
            return view.load()

        elif operation == "remove":
            itinerary = Itinerary()
            itinerary.remove_itinerary_destination(request)
            itinerary_data = itinerary.compile_itinerary_data()
            view = itinerary_ajax_view(itinerary_data)
            return view.load()

        elif operation == "delete":
            itinerary_id = request.GET['itinerary_id']
            itinerary = Itinerary()
            itinerary.itinerary_id = itinerary_id
            itinerary.delete_itinerary()






