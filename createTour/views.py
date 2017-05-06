from __future__ import print_function

import json

from django.http import HttpResponse


class itinerary_ajax_view:
    def __init__(self, itinerary_data):
        self.itinerary_data = itinerary_data
        self.response = None

    def load(self):
        self.response = json.dumps(self.itinerary_data)
        return HttpResponse(self.response)



        # def expediaRates(hotelId, roomTypeCode, arrivalDate, leaveDate):

        # 	API = '5qihbibdm199m03leh63sin4jo'

        # 	SK = '2ense2u0smh9a'

        # 		timestamp = str(int(time.time()))

        # 	# Use md5 hash protocol to make a signature out of the expedia API, secretkey and the timestamp. reutnred in hexidecimal format
        # 	sig = md5.new(API + SK + timestamp).hexdigest()
        # 	eanurl = ('http://api.ean.com/ean-services/rs/hotel/v3/info?minorRev=30&cid=422852&sig=%s&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&hotelId=%s&options=0') % (sig, hotelID)
        # 	response = urllib2.urlopen(eanurl)
        # 	data = json.load(response)


        # def rates(request):
        # 	# get the info from the frontend
        # 	if request.method == 'GET':
        # 		hotelid = request.GET['hotelid']
        # 		eanArriveDate = request.GET['eanArriveDate']
        # 		eanLeaveDate = request.GET['eanLeaveDate']
        # 		guests = request.GET['guests']
        # 		country = request.GET['country']
        # 		tour = request.GET['tour']
        # 		hotelref = request.GET['hotelref']


        # 		API = '5qihbibdm199m03leh63sin4jo'

        # 		SK = '2ense2u0smh9a'

        # 		timestamp = str(int(time.time()))

        # 		# Use md5 hash protocol to make a signature out of the expedia API, secretkey and the timestamp. reutnred in hexidecimal format
        # 		sig = md5.new(API + SK + timestamp).hexdigest()

        # 		print sig

        # 		print hotelref

        # 		hotel = hotelTable.objects.get(refNumber=hotelref)
        # 		roomtypecode = hotel.roomtypecode
        # 		ratecode = hotel.ratecode

        # 		print roomtypecode
        # 		print ratecode



        # 		eanurl = ('http://api.ean.com/ean-services/rs/hotel/v3/avail?minorRev=30&cid=422852&sig=%s&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&hotelId=%s&arrivalDate=%s&departureDate=%s&room1=2&rateCode=%s&roomTypeCode=%s') % (sig, hotelid, eanArriveDate, eanLeaveDate, ratecode, roomtypecode)

        # 		response = urllib2.urlopen(eanurl)
        # 		data = json.load(response)
        # 		data = data['HotelRoomAvailabilityResponse']

        # 		print 'printing data %s' % (data)




        # 		finalRate = data['HotelRoomResponse']['RateInfos']['RateInfo']['ChargeableRateInfo']['@total']
        # 		rateType = data['HotelRoomResponse']['RateInfos']['RateInfo']['rateType']
        # 		supplierType = data['HotelRoomResponse']['supplierType']
        # 		rateKey = data['HotelRoomResponse']['RateInfos']['RateInfo']['RoomGroup']['Room']['rateKey']

        # 		print('finalRate is %s' % (finalRate))
        # 		print('rateType is %s' % (rateType))
        # 		print('supplierType is %s' % (supplierType))
        # 		print('rateKey is %s' % (rateKey))

        # 		args = {"finalRate": finalRate, "rateType": rateType, "supplierType": supplierType, "rateKey": rateKey, "roomTypeCode": roomtypecode, "rateCode": ratecode}
        # 		return HttpResponse(args)


        # def tourselect(request):
        # 	if request.method == 'GET':
        # 		country = request.GET['country']
        # 		date = request.GET['date']
        # 		travelers = request.GET['travelers']
        # 		travelclass = request.GET['class']
        # 		tour = request.GET['tourtitle']

        # 		# Get the signature

        # 		API = '5qihbibdm199m03leh63sin4jo'

        # 		SK = '2ense2u0smh9a'

        # 		timestamp = str(time.time())

        # 		SIG = md5.new(API + SK + timestamp).hexdigest()

        # 		print SIG

        # 		args = { 'country': country,
        # 				 'date': date,
        # 				 'travelers': travelers,
        # 				 'class': travelclass,
        # 				 'tour': tour,
        # 				 'sig': SIG

        # 		}

        # 		return render_to_response('tours/tourselect.html', args, RequestContext(request))

        # #def bookhotels(request):
        # 	#if request.method == 'GET':

        # 	#We then take the package peramieters sent back by the title or each hotel along with the above information and send it too the backend for booking.

        # 	# The backend then interacts with the zumata api
        # 	# too book all the selected hotels and displays
        # 	# all the information needed on a later page.
