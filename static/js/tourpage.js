$(document).ready(function() {


    country_data = get_country_data(country_data);
    initMap(country_data);
    get_itinerary_ajax(country_id, itinerary_id);

	destination_click(destinations_data, itinerary_id);
	delete_destination(itinerary_id);
	

});

// ****************** ALL DESTINATION FUNCTIONS *******************************************

// **** TO DO This File ******
// delete itinerary destination
// delete temp itinerary

function delete_itinerary(itinerary_id){
	$('#delete').click(function(){
		var operation = "delete";
		update_itinerary_ajax("None", itinerary_id, operation);


	});

}


function delete_destination(itinerary_id){
    //language=JQuery-CSS
    $('#itineraryContainer').on('click', '.delete', function(){
        var destination_to_delete_full = $(this).attr('id');
        var destination_to_delete;
        destination_to_delete = destination_to_delete_full.replace('delete', '');
        var operation = "remove";
        update_itinerary_ajax(destination_to_delete, itinerary_id, operation);




        // // get destination itinerary list compile a destination list in that order
        // for(x=0; x<itinerary_data.length; x++){
	     //    var current_itinerary_destination = itinerary_data[x];
	     //    var current_destination_id = current_itinerary_destination.destination_id;
        //
	     //    if(current_destination_id !== destination_to_delete){
	     //        updated_destinations.push(current_destination_id);
        //
	     //    }
        // }
        //
        //
        // // pass new list to the ajax function with itinerary_id and the operation as update
        //
        // var destinations_to_update = updated_destinations.toString();
        //
        // var operation = 'update';
        //
        // update_itinerary_ajax(destinations_to_update, itinerary_id, operation);



    });
}



function get_itinerary_ajax(country_id, itinerary_id) {




    // Ajax call to get itinerary
    $.ajax({
        url: '/itinerary/itinerary_update_delete/',
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

            append_itinerary(itinerary_data);

        },

        error: function () {
            console.log('didnt work');
        },
        async: false
    });
}

function add_destination_itinerary(destination_id, itinerary_id){

	$('.addItinerary').unbind('click').on('click', function(){

        var operation = 'update';

		update_itinerary_ajax(destination_id, itinerary_id, operation);

		return;


	});
}


function destination_click(destinations_data, itinerary_id){
	gmarkers = [];
	$('.destinationTitle').on('click', function(){
		removeMarkers(gmarkers);
	
		// get the id of the clicked element to extract destination name
		var clicked_title = $(this).text();
		// use the name to get the description from the destinations_data
		for(i=0;i<destinations_data.length;i++){
			var destination_name = destinations_data[i].name;

			if(destination_name === clicked_title){
				var destination_description = destinations_data[i].description;
				var destination_id = destinations_data[i].destination_id;
				var lat = destinations_data[i].lat;
				var lng = destinations_data[i].lng;
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

function get_country_data(country_data){
	var country_id = country_data.country_id;
	var lat = country_data.lat;
	var lng = country_data.lng;
	var zoom = country_data.zoom

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

function update_itinerary_ajax(destination_to_action, itinerary_id, operation){
	

	// Ajax call to insert new destination data
	$.ajax({
		url: '/itinerary/itinerary_update_delete/',
		type: 'GET',
		data: {	
				
				"destinations": destination_to_action,
				"itinerary_id": itinerary_id,
				"operation": operation,
				
			},
			success: function(result){

                var itinerary_data;
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




	


