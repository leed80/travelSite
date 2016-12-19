from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^$', views.details, name='selected details'),
     url(r'^destinations/', views.destinations, name="destinations"),
     url(r'^hotels/', views.hotels, name="hotels"),
     
]