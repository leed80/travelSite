$(window).on('load', function() {

	

	initMap(countryData);



});

// Google map function
function initMap2(countryData) {
		console.log(countryData)
		lat = countryData[2];
		lng = countryData[3];
		zoom = countryData[4];
        countryLocation = {lat: lat, lng: lng};
        map = new google.maps.Map(document.getElementById('map2'), {
          zoom: zoom,
          center: countryLocation
        });
      }

// Get the Parameters from the backend from the URL
function getUrlParameters() {
	// empty array to house the parameters
	parameters = []
	// Get the page URL
	url = document.URL
	// Split the URL at "?" to get the parameters seperated from the address and take the index 1 parameter	
	urlsplit = url.split('?')[1];
	// Split each parameter at the &
	paramSplit = urlsplit.split('&');
	// Parse each parameters and split at the '=' push the second index (the value) to the parameters array
    for(var i=0; i<paramSplit.length; i++){
    	var value = paramSplit[i].split('=');
    	parameters[value[0]] = value[1];
    }
    return parameters;    
}