from django.conf.urls import url
from . import views
from createTour import controllers

urlpatterns = [
    url(r'^$', controllers.tour_load_controller, name='selected details'),
    url(r'^itinerary_update_delete', controllers.itinerary_update_delete),
    url(r'^hotels/', views.hotels, name="hotels"),

]
