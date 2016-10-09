from api import views
from rest_framework import routers
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()
router.register(r'tour', views.tourViewSet)
router.register(r'stop', views.stopViewSet)
router.register(r'activities', views.activitiesViewSet)
router.register(r'hotel', views.hotelViewSet)
router.register(r'hotelroom', views.hotelRoomViewSet)



urlpatterns = [
url(r'^api/', include(router.urls)), 
]

