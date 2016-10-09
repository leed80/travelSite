$(document).ready(function(){



	var apiurl = 'http://127.0.0.1:8000/api/api/'
	var place = $('#place').text();
	

	$.getJSON(apiurl + 'place/?format=json', function(placedata){
		$.getJSON(apiurl + 'area/?format=json', function(areadata){
			$.getJSON(apiurl + 'attraction/?format=json', function(attractiondata){
				$.getJSON(apiurl + 'hotel/?format=json', function(hoteldata){

					loadplace(place, placedata);
					appendareas(place, apiurl, placedata, areadata, hoteldata, attractiondata);
					
					



				});
			});


			
			


		});
	});

	$('.navlink').click(function(){

		var state = $(this).attr('id');

		if(state == 'open'){
			$('#hey').css('display', 'block');
			$('.navlink').attr('id', 'close');


		} else {
			$('#hey').css('display', 'none');
			$('.navlink').attr('id', 'open');

		}
		

		
	});

	

	

});


function loadplace(place, placedata){
	var lat;
    	var lng;
    	var co;
    	var map;
    	var zoom;
     
        $.each(placedata, function(key, value){

			var currentplace = value.name;
			currentplace = currentplace.replace(/\s+/g,"-");

			if(place == currentplace){

				lat = value.latitude;
         	 	lng = value.longitude;
          		zoom = value.zoom;
          		var description = value.description;

          		$('#placedescription').append(description);



          		


          		
     

          		initMap(lat, lng, zoom);

          		$('#place').click(function(){
          			initMap(lat, lng, zoom);
          			$('#placedescription').empty();
          			$('#buttons').empty();


          			$('#placedescription').append(description);
          		});


			}



          
          
        });
      


}

function initMap(lat, lng, zoom) {

      	var latLng = new google.maps.LatLng(lat, lng);
        map = new google.maps.Map(document.getElementById('map'), {
          center: latLng,
          zoom: zoom
          
        });

        google.maps.event.addDomListener(window, "resize", function() {
   var center = map.getCenter();
   google.maps.event.trigger(map, "resize");
   map.setCenter(center); 
});
      }


function appendareas(place, apiurl, placedata, areadata, hoteldata, attractiondata){
	
	//loop through all the places to get the place selected by the user
	$.each(placedata, function(index, value){
		var currentplace = value.name;
		currentplace = currentplace.replace(/\s+/g,"-");

		//if the user selected place is equal to the looped place then get the place id from the database
		if(place == currentplace){

			var placeid = value.placeid;

			//loop through all the area data
			$.each(areadata, function(index, value){


				var areaplaceidurl = value.placeid;

				$.getJSON(areaplaceidurl, function(theplace){
					var areaplaceid = theplace.placeid;

					//if the place id from the last loop is equal to the looped place id then get the areaname and area number
				if(placeid == areaplaceid){
					
					var areaname = value.name;
					var areanumber = value.areaid;
					
					//remove the spaces from the areaname so it can be used in html id
					var areaid = areaname.replace(/\s+/g,"-");

					//create the area name element
					var area = '<p class="area" id="' + areaid + '">' + areaname + '</p>'
					//append area element
					$('.data').append(area);




					


					//when the areaname is clicked
					$('#' + areaid).click(function(){

						//remove current place name from unser map
						$('#placename').empty();

						
						
						var lat;
						var lng;
						var zoom;

						//we get the latitude, logitude and zoom from the api for that area
						lat = value.latitude;
						lng = value.longitude;
						zoom = value.zoom;

						//create the latitude and longitude value for google maps to use
						var latLng = new google.maps.LatLng(lat, lng);

						

						//center the map on the latitude and longitude and zoom correctly
						map.setCenter(latLng);
						map.setZoom(zoom);


						//Get the area description and append
						$('#placedescription').empty();
						$('#buttons').empty();
						var description = value.description;
						$('#placedescription').append(description)
						//add place name to above the buttons under map
						$('#placename').append('<h2 id="placename">' + areaname + '</h2>');

						//append hotel, attraction and description buttons
						$('#buttons').append('<div id="buttoncontainer"><p class="hotelbutton" id="hotelbutton' + areaid + '">Hotels</p><p class="attractionbutton" id="attractionbutton' + areaid + '">Attractions</p><p class="descriptionbutton" id="descriptionbutton' + areaid + '">Description</p></div>');

						$('#descriptionbutton' + areaid).click(function(){
							$('#placedescription').empty();
							$('#placedescription').append(description)

							$('html, body').animate({
       							 scrollTop: $("#placedescription").offset().top
   								 }, 1500);

						});

						//set the hotel feature for that area
						hotel(hoteldata, areanumber, placeid, areaid);
						attraction(attractiondata, areanumber, placeid, areaid);
						

							//scroll to map when button is clicked
    						$('html, body').animate({
       							 scrollTop: $("#map").offset().top
   								 }, 1500);



						



						

		    			
					});
				}

				});


				

			});
		}
	});
	
		
}


function attraction(attractiondata, areanumber, placeid, areaid ){

	//when the attraction button is clicked have it loop through all the attractions, append the hotel to the map 
	//and append the details to the description box
	$('#attractionbutton' + areaid).click(function(){

		//clear the description area

			$('#placedescription').empty();

		

		
		var markers = [];


		$.each(attractiondata, function(key, value){

			$.getJSON(value.areaid, function(areadata){
				var loopareanumber = areadata.areaid;

			

				if(areanumber == loopareanumber){

					var attlng = value.longitude;
					var attlat = value.latitude;
					var attraction = value.name;
					var attid = attraction.replace(/\s+/g,"-");
					var address = value.address;
					var style = value.style;
					var budget = value.budget;
					var url = value.url;

					//combine lat and lng to make the google maps latlng variable

					var attlatlng = new google.maps.LatLng(attlat, attlng);

					var contentString = '<p>' + attraction + '</p>';
					var infowindow = new google.maps.InfoWindow({
						content: contentString
					});

					//append a marker on the map for the hotel
					var marker = new google.maps.Marker({
		    			position: attlatlng,
		    			map: map,
		    			id: marker
	  				});



					marker.addListener('mouseover', function(){
						infowindow.open(map, marker);
					});

					marker.addListener('mouseout', function(){
						infowindow.close(map, marker);
					});

					marker.addListener('click', function(){
						window.location.href = '#attraction' + attid;
					});

					markers.push(marker);
					// Sets the map on all markers in the array.
					function setMapOnAll(map) {
					  for (var i = 0; i < markers.length; i++) {
					    markers[i].setMap(map);
					  }
					}

				
				

				

					//appedn the hotel to the description area

					

					$('#placedescription').append('<div class="descitem" id="attraction' + attid + '"><h3 id="attractionname' + attid + '">' + attraction + '</h3><p id="attractionaddress' + attid + '">' + address + '</p><p id="attractionstyle' + attid + '">' + style + '</p><p id="attractionbudget' + attid + '">' + budget + '</p><p id="attractionurl' + attid + '"><a href="' + url + '" target="_blank">Visit Website</a></p></div>');
			
					//scroll to map when button is clicked
					$('html, body').animate({
							 scrollTop: $("#map").offset().top
							 }, 1500);

	    		

					$('#hotelbutton' + areaid).click(function(){
						function clearMarkers() {
			  				setMapOnAll(null, markers);
						}

					

		

					// Deletes all markers in the array by removing references to them.
			
			 		clearMarkers();
			  		markers = [];
		

					});

					$('#descriptionbutton' + areaid).click(function(){
						function clearMarkers() {
			  				setMapOnAll(null, markers);
						}

			

						// Deletes all markers in the array by removing references to them.
						
						clearMarkers();
						markers = [];
			

					});

					$('.area').click(function(){
								
								
								function clearMarkers() {
				  					setMapOnAll(null, markers);
								}

				

								// Deletes all markers in the array by removing references to them.
				
								  clearMarkers();
								  markers = [];
				

					});


				}
				

			});

			

		});
	
	});

}




function hotelloop(hoteldata, areanumber, placeid, areaid, markers){

	//when the hotel button is clicked have it loop through all the hotels, append the hotel to the map 
	//and append the details to the description box
	
			




		$.each(hoteldata, function(key, value){

			$.getJSON(value.areaid, function(areadata){

				var r = $.Deferred();
				var loopareanumber = areadata.areaid;

				

				if(areanumber == loopareanumber){

					var hotellng = value.longitude;
					var hotellat = value.latitude;
					var hotel = value.name;
					var hotelid = hotel.replace(/\s+/g,"-");
					var address = value.address;
					var style = value.style;
					var budget = value.budget;
					var url = value.url;

					//combine lat and lng to make the google maps latlng variable

					var hotellatlng = new google.maps.LatLng(hotellat, hotellng);

					var contentString = '<p>' + hotel + '</p>';
					var infowindow = new google.maps.InfoWindow({
						content: contentString
					});

					//append a marker on the map for the hotel
					var marker = new google.maps.Marker({
			    			position: hotellatlng,
			    			map: map
		  				});

					marker.addListener('mouseover', function(){
						infowindow.open(map, marker);
					});

					marker.addListener('mouseout', function(){
						infowindow.close(map, marker);
					});

					marker.addListener('click', function(){
						window.location.href = '#hotel' + hotelid;
					});

					markers.push(marker);



				

					 // Sets the map on all markers in the array.
					function setMapOnAll(map) {
					  for (var i = 0; i < markers.length; i++) {
					    markers[i].setMap(map);
					  }
					}





				

					//appedn the hotel to the description area

					$('#placedescription').append('<div class="descitem" id="hotel' + hotelid + '"><h3 id="hotelname' + hotelid + '">' + hotel + '</h3><p id="hotelstyle' + hotelid + '">' + style + '</p><p id="hotelbudget' + hotelid + '"></p><p id="hoteladdress' + hotelid + '">' + address + '</p><p id="hotelurl' + hotelid + '"><a href="' + url + '" target="_blank">Visit Website</a></p></div>');
					
					for(i=0; i < budget; i++){
						$('#hotelbudget' + hotelid).append('<img src="/static/img/star.png" >');
					}


					//scroll to map when button is clicked
					$('html, body').animate({
							 scrollTop: $("#map").offset().top
					}, 1500);

					

					

					
				


					$('#attractionbutton' + areaid).click(function(){
						
					// Sets the map on all markers in the array.
					function clearMarkers() {
		  				setMapOnAll(null, markers);
		  			}
						// Deletes all markers in the array by removing references to them.
		
					clearMarkers();
		  			markers = [];
		

					});

					$('#descriptionbutton' + areaid).click(function(){
						function clearMarkers() {
		 			 		setMapOnAll(null, markers);
						}

		

						// Deletes all markers in the array by removing references to them.
		
		  				clearMarkers();
		 				 markers = [];
		

					});


					$('.area').click(function(){
						
						function clearMarkers() {
		  					setMapOnAll(null, markers);
						}

		

						// Deletes all markers in the array by removing references to them.
		
						  clearMarkers();
						  markers = [];
		

					});
				}

				return r;

			});

		});

	
		

}




function hotel(hoteldata, areanumber, placeid, areaid, markers){

	$('#hotelbutton' + areaid).click(function(){

		//clear the description area

		$('#placedescription').empty();

		var markers = [];

		var function1 = hotelloop(hoteldata, areanumber, placeid, areaid, markers);

		var function2 = loader();

		hotelloop().done(loader());

	});

	

	

}

function loader(){

	alert('loaderbeing run');

	$('#loadMore').remove();

	$('#placedescription').append('<button id="loadMore">Load more</button>');
	var max_items_page = 1;

	$('#placedescription div:lt('+max_items_page+')').show();
	var shown = null;
	var items = $("#placedescription").find('div').length;

	alert('loader items ' + items);

	$('#loadMore').on('click',function(e){
	    shown = $('#placedescription div:visible').length+max_items_page;
	    if(shown<items) {
	        $('#placedescription div:lt('+shown+')').show();
	    }else {
	        $('#myList li:lt('+items+')').show();
	        $('#loadMore').hide();
	    }
	});
}



	

	