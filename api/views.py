from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import re
from django.template import RequestContext
import os
import sys
from django.views.decorators import csrf
from serializers import tourSerializer, stopSerializer, activitiesSerializer, hotelSerializer, hotelroomSerializer
from rest_framework import viewsets
from django.db.models import Q

from tours.models import tourTable, stopTable, activities
from hotel.models import hotelTable, hotelRoomTypes



class tourViewSet(viewsets.ModelViewSet):
    queryset = tourTable.objects.all()
    serializer_class = tourSerializer

class stopViewSet(viewsets.ModelViewSet):
    queryset = stopTable.objects.all()
    serializer_class = stopSerializer

class activitiesViewSet(viewsets.ModelViewSet):
    queryset = activities.objects.all()
    serializer_class = activitiesSerializer

class hotelViewSet(viewsets.ModelViewSet):
	queryset = hotelTable.objects.all()
	serializer_class = hotelSerializer

class hotelRoomViewSet(viewsets.ModelViewSet):
	queryset = hotelRoomTypes.objects.all()
	serializer_class = hotelroomSerializer




