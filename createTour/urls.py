from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.details, name='selected details'),
    url(r'^itinerary_update_delete', views.itineraryUpdateDeleteView),
    url(r'^hotels/', views.hotels, name="hotels"),

]
