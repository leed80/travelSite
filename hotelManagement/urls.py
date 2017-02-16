from hotelManagement import views
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
url(r'^$', views.hotelManagement),
url(r'^addHotel/', views.addHotel),
url(r'^addRoom/', views.addRoom),

]
