$(document).ready(function() {


    country_data = get_country_data(country_data);
    initMap(country_data);
    get_itinerary_ajax(country_id, itinerary_id);

	destination_click(destinations_list, itinerary_id);
	delete_destination(itinerary_id);
	

});

// ****************** ALL DESTINATION FUNCTIONS *******************************************

// **** TO DO This File ******
// delete itinerary destination
// delete temp itinerary

function delete_destination(itinerary_id){
    //language=JQuery-CSS
    $('#itineraryContainer').on('click', '.delete', function(){
        var destination_to_delete_full = $(this).attr('id');
        var destination_to_delete;
        destination_to_delete = destination_to_delete_full.replace('delete', '');
        var updated_destinations = []

        // get destination itinerary list compile a destination list in that order
        for(x=0; x<itinerary_data.length; x++){
	        var current_itinerary_destination = itinerary_data[x];
	        var current_destination_id = current_itinerary_destination.destination_id;

	        if(current_destination_id !== destination_to_delete){
	            updated_destinations.push(current_destination_id);

	        }
        }


        // pass new list to the ajax function with itinerary_id and the operation as update

        var destinations_to_update = updated_destinations.toString();

        var operation = 'update';

        update_itinerary_ajax(destinations_to_update, itinerary_id, operation);



    });
}

function get_itinerary_ajax(country_id, itinerary_id) {




    // Ajax call to get itinerary
    $.ajax({
        url: '/createTour/itinerary_update_delete/',
        type: 'GET',
        data: {

            "country_id": country_id,
            "itinerary_id": itinerary_id,
            "operation": 'get'

        },
        success: function (result) {
            console.log('success');
            itinerary_data = jQuery.parseJSON(result);


            console.log(itinerary_data);

            append_itinerary();

        },

        error: function () {
            console.log('didnt work');
        },
        async: false
    });
}

function add_destination_itinerary(destination_id, itinerary_id){

	$('.addItinerary').on('click', function(){

        var operation = 'update';

		update_itinerary_ajax(destination_id, itinerary_id, operation);


	});
}


function destination_click(destination_dictionary, itinerary_id){
	gmarkers = [];
	$('.destinationTitle').on('click', function(){
		removeMarkers(gmarkers);
	
		// get the id of the clicked element to extract destination name
		var clicked_title = $(this).text();
		// use the name to get the description from the destination_dictionary
		for(i=0;i<destination_dictionary.length;i++){
			var destination_name = destination_dictionary[i].name;

			if(destination_name === clicked_title){
				var destination_description = destination_dictionary[i].description;
				var destination_id = destination_dictionary[i].destination_id;
				var lat = destination_dictionary[i].lat;
				var lng = destination_dictionary[i].lng;
				break;
			}
		}

		update_current_destination_markup(destination_id, destination_name, destination_description);

		add_destination_itinerary(destination_id, itinerary_id);

		var gmarker = destination_marker(lat, lng, destination_id);
		gmarkers.push(gmarker);
	});
}

function update_current_destination_markup(destination_id, destination_name, destination_description){

	var destination_title_id = 'titleDescription' + destination_id;
	$('.titleDescription').attr('id', destination_title_id);
	/*noinspection JSJQueryEfficiency*/
    $('.titleDescription').text(destination_name);
	$('.description').text(destination_description);

}

function append_itinerary(itinerary_data) {
    $('#itineraryContainer').empty();
	console.log(itinerary_data.length);
	for(x=0; x<itinerary_data.length; x++){
		var current_destination = itinerary_data[x];
		var name = current_destination.name;
		var destination_id = current_destination.destination_id;

		var itinerary_name_HTML = '<h3 id="itineraryDestination' + destination_id + '" class="itineraryDestination">' + name + '</h3>';
		var itinerary_delete_HTML = '<input id="delete' + destination_id + '" class="delete" type="button" value="delete">';
		$('#itineraryContainer').append(itinerary_name_HTML);
		$('#itineraryContainer').append(itinerary_delete_HTML);

	}

}

function get_country_data(country_dictionary){
	var country_id = country_dictionary.country_id;
	var lat = country_dictionary.lat;
	var lng = country_dictionary.lng;
	var zoom = country_dictionary.zoom

	var country_data = [Number(country_id), Number(lat), Number(lng), Number(zoom)];
	return country_data;
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

function update_itinerary_ajax(destinations_to_update, itinerary_id, operation){
	

	// Ajax call to insert new destination data
	$.ajax({
		url: '/createTour/itinerary_update_delete/',
		type: 'GET',
		data: {	
				
				"destinations": destinations_to_update,
				"itinerary_id": itinerary_id,
				"operation": operation,
				
			},
			success: function(result){

                var itineraryData;
                if (result !== 'N') {
                    itinerary_data = jQuery.parseJSON(result);
                    append_itinerary(itinerary_data);
                } else {
                    alert('This destination is already added');
                }
			},

			error: function(error){
				console.log('didnt work');
			},
        async: false

	});
}



// Google map function
function initMap(country_data) {
		var lat = country_data[1];
		var lng = country_data[2];
		var zoom = country_data[3];

		var country_location = {"lat": lat, "lng": lng};
  
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: zoom,
          center: country_location
        });
      }



function destination_marker(lat, lng, destination_id){
	//removeMarkers();
	//marker.setMap(null);	
	var destination_location = new google.maps.LatLng(lat, lng);
	marker = new google.maps.Marker({
          position: destination_location,
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




	


