$(document).ready(function(){
var country;
country = $('#country').text();




getCountry(country);


    


});



function townClickedGoog(towndata, each_town, descdata){
	$('.select_container').on('click', '.town', function() {
		$('.addtown').remove();
		var nextElementClass;

		
		var townName;
		console.log('townClicked is being run');
		

		//get the towns id
		townName = this.id;
		console.log('townName is ' + townName);
		



		
			appendAddButton(townName);
			addTownDescription(descdata, townName);
			centerTown(towndata, townName);

		}
	});
}

function centerTown(towndata, townName){
	$.each(towndata, function(key, value){
		var loopTown = value.townname;

		if(townName == loopTown){
			lat = value.latitude;
			lng = value.longitude
			initMap(lat,lng);

		}
	});
}


function getCountry(country){
		var lat;
    	var lng;
    	var co;
    	var map;
      $.getJSON('http://127.0.0.1:8000/map/api/country_' + country + '/?format=json', function(data){
        $.each(data, function(key, value){
          lat = value.latitude;
          lng = value.longitude;
          alert('lat is ' + lat +' and lng is ' + lng);

          initMap(lat,lng);
          
        });
      });
    }


     
      function initMap(lat,lng) {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: lat, lng: lng},
          zoom: 5
        });
      }

