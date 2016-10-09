$(document).ready(function() {

	var country = $('#country').text();
	var travelClass = $('#class').text();
	var date = $('#date').text();
	var travelers = $('#travelers').text();

	$.getJSON('http://127.0.0.1:8000/api/api/tour/?format=json', function(tourdata){

		$.each(tourdata, function(key, value){
			var tourCountry = value.country;
			var tourTravelClass = value.travelClass;


			console.log('tourCountry is ' + tourCountry + ' and county is ' + country);
			console.log('travelclass is ' + travelClass + ' and tour is ' + tourTravelClass);

			if (tourCountry == country && travelClass == tourTravelClass){
				console.log('we get here');
				var tourname = value.title;
				var tourdesc = value.description;
				var refno = value.refNumber;



				$('#tourbody').append("<div id='tour'" + refno + "' class='tour'><h3 id='title" + refno + "' class='title'>" + tourname + "</h3><p id='class" + refno + "' class='class'>" + tourTravelClass + "</p><p id='desc" + refno + "' class='desc'>" + tourdesc + "</p></div>");
				$('#tourbody').append('<form action="/tour/tourselect/" class="form" id="form" method="get"><input id="country" name="country" value="' + country + '"><input type="date" id="date" name="date" value="' + date + '"><input type="number" id="travelers" name="travelers" value="' + travelers + '"><input id="class" name="class" value="' + travelClass + '"><input id="tourtitle" name="tourtitle" value="' + refno + '"><button value="select tour"></form>');
			}
		});
	});



});