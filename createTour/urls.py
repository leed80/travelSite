from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.details, name='selected details'),
    url(r'^itinerarycrud', views.itineraryCRUD),
    url(r'^hotels/', views.hotels, name="hotels"),

]
