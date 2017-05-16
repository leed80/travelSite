from itinerary import views, controllers
from django.conf.urls import include, url


urlpatterns = [
url(r'^$', controllers.itinerary_load_controller, name='selected details'),
    url(r'^create_itinerary', controllers.itinerary_create_form),
    url(r'^new_itinerary_generator', controllers.new_itinerary_controller),
    url(r'^load_itinerary', controllers.itinerary_load_controller),
    url(r'^itinerary_update_delete', controllers.itinerary_update_delete),
    url(r'^hotels/', views.hotels, name="hotels"),
    url(r'itinerary_deleted', views.itinerary_deleted, name="deleted")
]