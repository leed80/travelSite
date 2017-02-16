from api import views
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
url(r'^country/$(?P<countryid>)', views.countryViewSet.as_view() ),
url(r'^hotel/$(?P<destinationid>)', views.hotelViewSet.as_view() ),
url(r'^room/$(?P<hotelid>)', views.roomViewSet.as_view() ),
url(r'^destination/$(?P<countryid>)(?P<name>)', views.destinationViewSet.as_view()),
url(r'^tempItinerary/$(?P<itineraryID>)', views.tempItineraryViewSet.as_view()),
url(r'^Itinerary/$(?P<itineraryID>)', views.completeItineraryViewSet.as_view()),
url(r'^updatetempitinerary/(?P<pk>[0-9]+)/$', views.updateTempItinerary.as_view()),
url(r'^deletetempitinerary/(?P<pk>[0-9]+)/$', views.deleteTempItinerary.as_view()),
]

