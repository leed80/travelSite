from django.conf.urls import *
from map import views




urlpatterns = [
     url(r'^$', views.main, name='premap'),
     url(r'^get/', views.map_page, name='mappage'),
     
   
    

  ]