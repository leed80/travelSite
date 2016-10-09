$(document).ready(function(){
	//development url
	var apiurl = 'http://127.0.0.1:8000/api/api/';


	//live url
	//var apiurl = 'https://pure-thicket-27964.herokuapp.com/api/api/';

	//get the username
	var user = $('.user').text();

	$.getJSON(apiurl + 'itinerary/?format=json', function(data) {
		$.each(data, function(key, value){

			var userItinerarys = value.user_id;
			console.log('user id is' + userItinerarys);

			if(userItinerarys === user){
				console.log('titles are ' + value.title);
				var title = value.title;
				var description = value.description;
				var country = value.country;
				var titleId = title.replace(/\s+/g, "");
				
				$('.itinerarys').append('<h3 class="madeItineraries" id="' + titleId + '">' + title + '</h3>');
				$('#' + titleId).append('<p class="description" id="desc' + titleId + '">' + description + '</p>');
				$('#desc' + titleId ).append('<p class="country" id="country' + titleId + '">Country:' + country + '</p>' );

				$('#' + titleId).click(function(){
					

					$('#getTitle').remove();
					$('#delete').remove();

					//var title = $(this).text();
					//var country = $('#country' + title).text();
					//console.log('country is ' + country);

				
					$('#' + titleId).append('<form id="getTitle" class="getTitle" action="/itinerary/processing/" method="get"><input type="text" name="title" class="title" ><input type="text" name="country" class="country"><input type="submit" value="edit" id="submit"></form><form id="delete" class="deleteItinerary" action="/itinerary/delete/" method="get"><input type="text" name="title" class="title" ><input type="submit" value="delete" id="delete"></form>');
					var titleSend = title.replace(/\s+/g,".|_|.");
					$('.title').val(titleSend).css({'display':'none'});
					$('.country').val(country).css({'display':'none'});
				});//end click function

			}//end of if

			
		});//end of each


		


	});//end get JSON


});// end document ready