$(document).ready(function() {

	var map;
	var marker;
	var gmarkers;
	var csrftoken;
	
	var countryData = getCountryData(countryDictionary);
    initMap(countryData);
	getItineraryAjax(countryID, itineraryID);

	destinationClick(destinationsList, itineraryID);
	deleteDestination(itineraryID);
	

});

// ****************** ALL DESTINATION FUNCTIONS *******************************************

// **** TO DO This File ******
// delete itinerary destination
// delete temp itinerary

function deleteDestination(itineraryID){
    $('#itineraryContainer').on('click', '.delete', function(){
        console.log('clicked');
        var destinationToDeleteFull = $(this).attr('id');
        var destinationToDelete = destinationToDeleteFull.replace('delete', '');
        var updatedDestinations = []

        // get destination itinerary list compile a destination list in that order
        for(x=0;x<itineraryList.length;x++){
	        var currentItineraryDestination = itineraryList[x];
	        var currentDestinationid = currentItineraryDestination.destinationID;

	        if(currentDestinationid != destinationToDelete){
	            updatedDestinations.push(currentDestinationid);

	        }
        }


        // pass new list to the ajax function with itineraryID and the operation as update

        var destinationsToUpdate = updatedDestinations.toString();

        if(destinationsToUpdate == ""){
            destinationsToUpdate = "0";
        }
        var operation = "update";

        updateItineraryAjaxCall(destinationsToUpdate, itineraryID, operation);



    });
}

function getItineraryAjax(countryID, itineraryID) {




    // Ajax call to get itinerary
    $.ajax({
        url: '/createTour/itinerary_update_delete/',
        type: 'GET',
        data: {

            "countryID": countryID,
            "itineraryID": itineraryID,
            "operation": 'get',

        },
        success: function (result) {
            console.log('success');
            itineraryList = jQuery.parseJSON(result);


            console.log(itineraryList);

            appendItinerary(itineraryList);

        },

        error: function (error) {
            console.log('didnt work');
        },
        async: false
    });
}

function addDestinationItinerary(destinationid, itineraryID){
	$('.addItinerary').on('click', function(){

		operation = 'update';


		updateItineraryAjaxCall(destinationid, itineraryID, operation);


	});
}


function destinationClick(destinationDictionary, itineraryID){
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
    $('#itineraryContainer').empty();
	console.log(itineraryList.length);
	for(x=0;x<itineraryList.length;x++){
		var currentDestination = itineraryList[x];
		var name = currentDestination.name;
		var destinationID = currentDestination.destinationID;

		var itineraryNameHTML = '<h3 id="itineraryDestination' + destinationID + '" class="itineraryDestination">' + name + '</h3>';
		var itineraryDeleteHTML = '<input id="delete' + destinationID + '" class="delete" type="button" value="delete">';
		$('#itineraryContainer').append(itineraryNameHTML);
		$('#itineraryContainer').append(itineraryDeleteHTML);

	}

}

function getCountryData(countryDictionary){
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
		url: '/createTour/itinerary_update_delete/',
		type: 'GET',
		data: {	
				
				"destinations": destinationsToUpdate, 
				"itineraryID": itineraryID,
				"operation": operation,
				
			},
			success: function(result){

				if(result == 'NO'){
					alert('This destination is already added');
				} else{
					itineraryList = jQuery.parseJSON(result);
					appendItinerary(itineraryList);
				}
			},

			error: function(error){
				console.log('didnt work');
			},
        async: false

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




	


