from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^$', views.details, name='selected details'),
     url(r'^tourselect/', views.tourselect, name="tour select"),
     url(r'^rates/', views.rates, name="room rates"),
]