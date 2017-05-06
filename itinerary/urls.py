from itinerary import views, controllers
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
url(r'^$', controllers.itinerary_load_controller, name='selected details'),
    url(r'^itinerary_update_delete', controllers.itinerary_update_delete),
    url(r'^hotels/', views.hotels, name="hotels"),
]