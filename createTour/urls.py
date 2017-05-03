from django.conf.urls import url
from . import views
from createTour import controllers

urlpatterns = [
    url(r'^$', controllers.tourController, name='selected details'),
    url(r'^itinerary_update_delete', controllers.itineraryUpdateDelete),
    url(r'^hotels/', views.hotels, name="hotels"),

]
