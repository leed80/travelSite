from django.conf.urls import url

import itinerary.views
from itinerary import controllers
from . import views

urlpatterns = [
    url(r'^$', controllers.itinerary_load_controller, name='selected details'),
    url(r'^itinerary_update_delete', controllers.itinerary_update_delete),
    url(r'^hotels/', itinerary.views.hotels, name="hotels"),

]
