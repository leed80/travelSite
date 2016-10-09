from rest_framework import serializers
from django.contrib.auth.models import User
from tours.models import tourTable, stopTable, activities
from hotel.models import hotelTable, hotelRoomTypes

class tourSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tourTable
		fields = ('refNumber', 'title', 'description', 'country', 'travelClass')

class stopSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = stopTable
		fields = ('refNumber', 'tour', 'title', 'description', 'lengthofstay')

class activitiesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = activities
		fields = ('refNumber', 'stop', 'title', 'description')


class hotelSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hotelTable
		fields = ('refNumber', 'title', 'description', 'stop', 'travelClass', 'eanhotelid', 'address', 'location', 'amenities', 'policies', 'roomtypecode', 'ratecode')

class hotelroomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hotelRoomTypes
		fields = ('refNumber', 'hotel', 'title', 'beds', 'amenities')






