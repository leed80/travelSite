$(document).ready(function() {

	var map;
	var marker;
	var gmarkers;
	var csrftoken;
	
	var countryData = getCountryData();
    initMap(countryData);
	appendItinerary(itineraryList);
	destinationClick(destinationsList, itineraryID);
	

});





// ****************** ALL DESTINATION FUNCTIONS *******************************************

// **** TO DO This File ******
	// Add an on click event to add new itinerary destination, save and reload on the page
	// Add an on click event to delete an itinerary, update and return the new code
	// Add an on click evennt for the country to display description

function addDestinationItinerary(destinationid, itineraryID){
	$('.addItinerary').on('click', function(){
		var operation = "update";
		updateItineraryAjaxCall(destinationid, itineraryID, operation);
		

	});
}



function destinationClick(destinationDictionary){
	gmarkers = [];
	$('.destinationTitle').on('click', function(){
		removeMarkers(gmarkers)
	
		// get the id of the clicked element to extract destination name
		var clickedTitle = $(this).text();
		// use the name to get the description from the destinationDictionary
		for(i=0;i<destinationDictionary.length;i++){
			var destinationName = destinationDictionary[i].name;

			if(destinationName == clickedTitle){
				var destinationDescription = destinationDictionary[i].description;
				var destinationID = destinationDictionary[i].destinationid;
				var lat = destinationDictionary[i].lat;
				var lng = destinationDictionary[i].lng;
				break;
			}
		}



		updateCurrentDestinationMarkup(destinationID, destinationName, destinationDescription);

		addDestinationItinerary(destinationID, itineraryID);

		var gmarker = destinationMarker(lat, lng, destinationID);	
		gmarkers.push(gmarker);
	});
}

function updateCurrentDestinationMarkup(destinationID, destinationName, destinationDescription){

	var destinationTitleId = 'titleDescription' + destinationID;
	$('.titleDescription').attr('id', destinationTitleId);
	$('.titleDescription').text(destinationName);
	$('.description').text(destinationDescription);

}

function appendItinerary(itineraryList){
	var x=0;
	while(x<itineraryList.length){
		var currentDestination = itineraryList[x];
		var name = currentDestination.name;
		var destinationID = currentDestination.destinationID;

		var itineraryNameHTML = '<h3 id="itineraryDestination' + destinationID + '" class="itineraryDestination">' + name + '</h3>';
		var itineraryDeleteHTML = '<input id="delete' + destinationID + '" class="delete" type="button" value="delete">';
		$('#itineraryContainer').append(itineraryNameHTML);
		$('#itineraryContainer').append(itineraryDeleteHTML);
		x++;
	}

}

function getCountryData(){
	var countryID = countryDictionary.countryid;
	var lat = countryDictionary.lat;
	var lng = countryDictionary.lng;
	var zoom = countryDictionary.zoom

	var countryData = [Number(countryID), Number(lat), Number(lng), Number(zoom)];
	return countryData;
}

function csrfSetup(csrftoken){
	//setup csrf token
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
 			}
		}  
	});
}

function updateItineraryAjaxCall(destinationsToUpdate, itineraryID, operation){
	

	// Ajax call to insert new destination data
	$.ajax({
		url: '/createTour/itinerarycrud/',
		type: 'GET',
		data: {	
				
				"destinations": destinationsToUpdate, 
				"itineraryID": itineraryID,
				"operation": operation,
				
			},
			success: function(result){
				console.log('success');
				console.log(result);
				var itineraryList = result;
				console.log(itineraryList);
				appendItinerary(itineraryList);
			},
			error: function(error){
				console.log('didnt work');
			}
	});
}



// Google map function
function initMap(countryData) {
		var lat = countryData[1];
		var lng = countryData[2];
		var zoom = countryData[3];

		var countryLocation = {"lat": lat, "lng": lng};
  
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: zoom,
          center: countryLocation
        });
      }





function destinationMarker(lat, lng, destinationID){
	//removeMarkers();
	//marker.setMap(null);	
	var destinationLocation = new google.maps.LatLng(lat, lng);
	marker = new google.maps.Marker({
          position: destinationLocation,
          title: 'marker',
          map: map
        });
	return marker;	
}

function removeMarkers(gmarkers){
	for(i=0;i<gmarkers.length;i++){
		gmarkers[i].setMap(null);
	}
}




	


