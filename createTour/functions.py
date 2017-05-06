from createTour.models import Country, Destination
from itinerary.models import Temp_Itinerary


def get_form_data(request):
    country_id = str(request.GET['country'])
    date = request.GET['date']
    travelers = request.GET['travelers']
    travel_class = request.GET['class']

    return [country_id, date, travelers, travel_class]


def country_render_data(country_id):
    country_data = Country.objects.get(countryid=country_id)
    country_dictionary = {"name": str(country_data.name), "countryID": country_data.countryid,
                          "description": str(country_data.description), "lat": country_data.lat,
                          "lng": country_data.lng, "zoom": country_data.zoom}
    return country_dictionary


def destinations_render_data(country_id):
    destinations = destinations_list(country_id)
    destinations_data = destinations.destination_data
    return destinations_data


def check_session_id(request):
    # Get the session id
    session_id = request.session.session_key
    # if not populated then create one
    if not session_id:
        request.session.modified = True
        session_id = request.session.save()

    # Check the database for duplicate session id and return Yes or No
    try:
        Temp_Itinerary.objects.get(session=session_id)
        return ["Yes", session_id]
    except Temp_Itinerary.DoesNotExist:
        return ["No", session_id]



def user_check(request):
    if request.user.is_authenticated():
        current_user = request.user
    else:
        current_user = 'Guest'

    return current_user


def destination_check(current_destinations, new_destination):
    current_destinations_split = current_destinations.split(',')
    for destination in current_destinations_split:
        if destination == new_destination:
            return 0
    return 1


def create_itinerary_id(country_id):
    # type: (object) -> object
    # This function creates the itinerary_id
    timestamp = str(time.time())
    itinerary_id = hashlib.md5(timestamp + country_id).hexdigest()
    itinerary_id = itinerary_id[:8]
    return itinerary_id
