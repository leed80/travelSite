$(document).ready(function() {

	var itineraryID = $('#itineraryID').text();
	$.getJSON('http://127.0.0.1:8000/api/tempItinerary/?itineraryID=' + itineraryID + '&format=json', function(itinerarydata){
		var country;
		$.each(itinerarydata, function(key, value){
			country = value.country;
		});
		$.getJSON('http://127.0.0.1:8000/api/destination/?countryid=' + country + '&format=json', function(destinationdata){
			appendDestinations(itinerarydata, destinationdata);
			appendHotels(itinerarydata);
		});
	});
});

function appendDestinations(itinerarydata, destinationdata){
	var itineraryDestinations = [];
	$.each(itinerarydata, function(key, value){
		itineraryDestinations = value.destinations;
		return itineraryDestinations;
	});
	
	var itineraryDestinationsSplit = itineraryDestinations.split(',');
	console.log(itineraryDestinationsSplit);
	console.log(itineraryDestinationsSplit.length);
	var i = 0;
	while(i<itineraryDestinationsSplit.length){
		var parsedItineraryDestination = itineraryDestinationsSplit[i];
		$.each(destinationdata, function(key, value){
			var parsedDestinationID = value.destinationid;
			console.log(parsedItineraryDestination + ' = ' + parsedDestinationID);
			if(parsedItineraryDestination == parsedDestinationID){
				var destinationName = value.name;
				var destinationContainer = "<div id='destinationcontainer" + parsedDestinationID + "' class='destinationcontainer'></div>"
				var destinationTitleAppend = "<h1 id='title" + parsedDestinationID + "' class='destination'>" + destinationName + "</h1>";
				$('#destinationSelect').append(destinationContainer);
				$('#destinationcontainer' + parsedDestinationID).append(destinationTitleAppend);
			}
		});
		i++;
	}
}

function appendHotels(itinerarydata){
	var itineraryDestinations = [];
	$.each(itinerarydata, function(key, value){
		itineraryDestinations = value.destinations;
		return itineraryDestinations;
	});

	var itineraryDestinationsSplit = itineraryDestinations.split(',');
	console.log(itineraryDestinationsSplit);
	$.getJSON("http://127.0.0.1:8000/api/hotel/?format=json", function(hoteldata){
		var i=0;
		while(i<itineraryDestinationsSplit.length){
			var parsedItineraryDestination = itineraryDestinationsSplit[i];
			$.each(hoteldata, function(key, value){
				var parsedHotelDestination = value.destinationid;

				if(parsedItineraryDestination == parsedHotelDestination){
					var hotelID = value.hotelid;
					var hotelName = value.name;//get hotel name 
					var hotelAddress = value.address;// get hotel address
	        		var hotelDescription = value.description;// get hotel description
	        		var hotelrating = value.rating;// get hotel rating
	        		var destinationid = value.destinationid;
	        		console.log('destinationid is ' + destinationid);

	        		
        			//create new hotel div
	        		console.log('destinationcontainer' + parsedItineraryDestination);
	        		var newHotelContainer = '<div id="hotel' + hotelID + '" class="hotelContainer"></div>';
	        		$('#destinationcontainer' + parsedItineraryDestination).append(newHotelContainer);
	        		//append the name
	        		var hotelname = '<h2 id="name' + parsedItineraryDestination + '" class="hotelname">' + hotelName + '</h2>';
	        		$('#hotel' + hotelID).append(hotelname);
	        		//append the address
	        		var hoteladdress = '<p id="address' + parsedItineraryDestination + '" class="hoteladdress">' + hotelAddress + '</p>';
	        		$('#hotel' + hotelID).append(hoteladdress);
	        		//append the rating
					var hotelrating = '<p id="rating' + parsedItineraryDestination + '" class="hotelrating">' + hotelrating + '</p>';
	        		$('#hotel' + hotelID).append(hotelrating);
	        		//append the description
	        		var hotelDescription = '<p id="description' + parsedItineraryDestination + '" class="hoteldescription">' + hotelDescription + '</p>';
	        		$('#hotel' + hotelID).append(hotelDescription);
	        		//append select hotel button
	        		var days = '<input type="number" id="days' + parsedItineraryDestination + '" class="days" value="0">';
	        		$('#hotel' + hotelID).append(days);
	        		var hotelselect = '<input id="select' + parsedItineraryDestination + '" class="hotelselect" type="button" value="Select For Destination">';
	        		$('#hotel' + hotelID).append(hotelselect);
				}
			});
			i++;
		}	
	});
}

// get hotel vailability
//function hotelAvailability(){
	// get cid from database
	// get api key from database
	// get shared secret from database
	// get timestamp
	// Use md5 hash protocol to make a signature out of the expedia API, secretkey and the timestamp. reutnred in hexidecimal format
	// get hotel id
	// get arrival date
	// get departure date
	// number of adults
	// get hotel availability from expedia 
	// [http://api.ean.com/ean-services/rs/hotel/v3/avail?minorRev=30
	// &cid=54321
	// &sig=5432112345
	// &apiKey=[xxx-yourOwnKey-xxx]
	// &customerUserAgent=[xxx]
	// &customerIpAddress=[xxx]
	// &customerSessionId=[xxx]
	// &locale=en_US
	// &currencyCode=USD
	// &hotelId=127092
	// &arrivalDate=09/03/2015
	// &departureDate=09/04/2015
	// &includeDetails=true
	// &includeRoomImages=true
	// &room1=2,5,7]
	// filter hotels based on the availabilty
	// response = see http://developer.ean.com/docs/room-avail/examples/rest-room-availability/
//}






