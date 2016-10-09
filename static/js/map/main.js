$(document).ready(function() {

	//development url
	var apiurl = 'http://127.0.0.1:8000/api/api/';


	//live url
	//var apiurl = 'https://pure-thicket-27964.herokuapp.com/api/api/';

	//when the document is loaded we get the country selected from the HTML.
	var country = $('#country').text();
	//look for a title
	var isTitle = $('#edit').text();
	//var delay=5000; //1 second
	///setTimeout(function() {
		getCountry(country, apiurl);
		countryDescription(country, apiurl);
		getRegions(country, apiurl);
		townsProcess(country, apiurl);	
		saveUpdate(country, apiurl);
		selectScroll();

		
	


		  
	//}, delay);


	

		
	
});// end of document ready







function mainLoad(country, isTitle){
	

	
}


function getCountry(country, apiurl){
		var lat;
    	var lng;
    	var co;
    	var map;
    	var zoom;
      $.getJSON(apiurl + 'country_' + country + '/?format=json', function(data){
        $.each(data, function(key, value){
          lat = value.latitude;
          lng = value.longitude;
          zoom = 4;

     

          initMap(lat,lng, zoom);
          
        });
      });
    }






//------------------------------------Country Description functions-----------------------------------------------------------

function getCountryDescription(value){
	desc = '<div id="thedesc" >' + value.description + '</div>';
	return desc;
}

function getAuthor(value){

	$('#credit').remove();
	author = '<div id="credit"><p id="authorTitle" style="text-decoration:underline;">Meet the author</p><p id="authorName">' + value.author + '</p><p id="authorWebsite">' + value.author_website + '</p><p id="authorUrl">' + value.author_url + '</p></div>'
	return author;
}

function appendCountryDescription(desc, author){
	$('#desc').append(desc);
	$('#author').append(author);
}

function loopCountryData(data, country){
	$.each(data, function(key, value) {
		var desc;
		var author;
		desc = getCountryDescription(value);
		author = getAuthor(value);
		appendCountryDescription(desc, author);
		displayCountryDesc(desc, author);
	});
}

function loadCountryfromAPI(country, apiurl){
	$.getJSON(apiurl + 'country_' + country + "/?format=json", function(data) {
		loopCountryData(data, country);
			
	});
}

function displayCountryDesc(desc, author) {
	//when country is clicked have it display the country description
	$('#country').click(function() {
		//remove element in the box
		$('#thedesc').remove();

		$('#credit').remove();

		var cDesc = '<div id="thedesc" >' + desc + '</div>';
		$('#desc').append(cDesc);
		$('#author').append(author);
	});// country click function end
}//end country display description function 

function countryDescription(country, apiurl){
	//load country description on loading
	loadCountryfromAPI(country, apiurl);
}// end countryDescription function
//------------------------------------End Country Description functions-------------------------------------------------------


//-----------------------------------start map url functions--------------------------------------------------------------





function appendMap(value){
	$m = '/static/' + value.maproute;
	$('#mainmap').attr("src", $m);
	$('.map').parent().css({position: 'relative'});
}

function loopCountryDataUrl(data){
	$.each(data, function(key, value) {

		appendMap(value);
	});
}

//-----------------------------------end map url functions--------------------------------------------------------------

//-----------------------------------start get regions functions--------------------------------------------------------------

function getRegions(country, apiurl){
	//We then use the country variable to get the regions from the API. 
	$.getJSON(apiurl + 'regions_' + country + "/?format=json", function(data) {
		//Arrays are created that will hold region ids, region names and the full region objects.
		var regionitems;
		//We the loop through all the region objects pushing region ids, region names and region objects to their variables 
		//created earlier.
		regionitems = loopRegionsData(data);
		//We the loop through all the region values and give them each an HTML id that is their region number and text that is 
		//their region name.
		loopRegionItems(regionitems);
	});
}

function loopRegionsData(data){
	//We the loop through all the region objects pushing region ids, region names and region objects to their variables 
	//created earlier.
	regionitems = [];
	$.each(data, function(key, value) {
		regionitems.push(value);
	});
	return regionitems;
}

function loopRegionItems(regionitems){
	//We the loop through all the region values and give them each an HTML id that is their region number and text that is 
	//their region name.
	$.each(regionitems, function(i, v) {

		$p = ('<h3 class="region" id="' + v.region_id + '">' + v.regionname + '</h3>' );
		$('.data').append($p);
		
	});
}

function hidetowns(){
	$('.region').children().css('display', 'none');



	$('.region').click(function(){

		var hidden;
		hidden = $(this).children().css('display');

		if(hidden == 'none'){
			$(this).children().css('display', 'block');
		} else {
			$(this).children().css('display', 'none');
		}
		

	});

	$( ".town" ).click(function( event ) {
  event.stopPropagation();
  // Do something
});
}

//-----------------------------------end get regions functions--------------------------------------------------------------


//-----------------------------------start town process functions--------------------------------------------------------------
function getTowns(towndata){
	//We create an array that will hold the full town objects
	towns = [];
	//We loop through each town object and push the value to the towns array
	$.each(towndata, function(key, value) {
		towns.push(value);
	});	// each end
	return towns;
}

function getEachTown(towns){
	each_town = [];
	$.each(towns, function(index, value) {
		each_town.push(value);
	}); //each end
	return each_town;
}

function getRegionIdTown(v){
	townregion_id = v.region_id;
	return townregion_id;
}
function getTownNameTowns(v){
	townname = v.townname;
	return townname;
}

function appendTownMap(townname, townregion_id){
	var idtownname = townname.replace(/\s+/g,"-");
	$t = ('<p class="town" id="' + idtownname + '"> -' + townname + '<p>');
	var ident = ('#' + townregion_id );
	$(ident).append($t);
}

function appendEachTown(each_town){
	$.each(each_town, function(i, v) {
		var townregion_id;
		var townname;

		townregion_id = getRegionIdTown(v);
		townname = getTownNameTowns(v);
		appendTownMap(townname, townregion_id);
	}); // each end
}

function loopThroughSprites(){
	town_select = [];
	console.log('running loopThroughSprites');

	
	$.each($('.sprite'), function() {
		console.log('running each in loopThroughSprites');

		var pretown;
		var town;

		pretown = this.id;
		town = pretown.slice(0, -3);
		console.log('town is ' + town);
		town_select.push(town);
	});
	return town_select;
}

function loopTownSelect(town_select, townName){

	dup = loopTownSelectForDup(town_select, townName);
	return dup;	
}

function duplicateTowns(townName){
	var town_select;
	town_select = loopThroughSprites();
	
	dup = loopTownSelect(town_select, townName);
	return dup;
}//end duplicate towns function

function loopTownDescData(descdata, townName){
	$.each(descdata, function(key, value) {
		currenttown = value.townname;
		var newtownName = townName.split("-").join(" ");
		if (currenttown === newtownName) {
			var desc;
			var description;
			var author;
			description = value.description;

			console.log('description is ' + description);
			desc = '<div id="thedesc" >' + description + '</div>';
			$('#desc').append(desc);
			$('#credit').remove();
			author = '<div id="credit"><p id="authorTitle" style="text-decoration:underline;">Meet the author</p><p id="authorName">' + value.author + '</p><p id="authorWebsite">' + value.author_website + '</p><p id="authorUrl">' + value.author_url + '</p></div>'
			$('#author').append(author);

			
		}
	});
}

function addTownDescription(descdata, townName){
	var currenttown;
	//remove element in the box
	$('#thedesc').remove();

	loopTownDescData(descdata, townName);
}

function appendSpriteToMap(townName){
	//create an image that will be pinned on the map image
	var $c = ('<img src="/static/map/sprite.jpg" class="sprite" id="' + townName + 'img">');
	$('.map').append($c);
}

function setIdForSprite(townName){
	id = ('#' + townName + 'img');
	return id;
}







function townsProcess(country, apiurl){	
//Again use the country variable to get the towns JSON data
	$.getJSON(apiurl + 'towns_' + country + "/?format=json", function(towndata) {
		$.getJSON(apiurl + 'towns_' + country + "_desc/?format=json", function(descdata) {
			$.getJSON(apiurl + 'towns_' + country + "_attractions/?format=json", function(attrdata) {
				$.getJSON(apiurl + 'Route_Stop_' + country + '/?format=json', function(stopdata){
					$.getJSON(apiurl + 'Transport_Company_' + country + '/?format=json', function(transcodata){
						$.getJSON(apiurl + 'Major_Hub_' + country + '/?format=json', function(hubdata){
							$.getJSON(apiurl + 'Transport_Company_Route_' + country + '/?format=json', function(transroutedata){

								var towns;
								var each_town;

								towns = getTowns(towndata);
								each_town = getEachTown(towns);
								appendEachTown(each_town);
								hidetowns();
								townClickedGoog(towndata, each_town, descdata, attrdata, stopdata, transcodata, hubdata, transroutedata);

							});

						});


					});

				});

				
				
			});
			
		});
	});

}

function addattractions(attrdata, townName){
	
	$.each(attrdata, function(index, value){
		
		currenttown = value.townname;
		var newtownName = townName.split("-").join(" ");
		if (currenttown === newtownName) {
			var attr;
			var attraction;
			
			attraction = value.attraction;

			
			attr = '<div id="theattr" >' + attraction + '</div>';
			$('#attractions').append(attr);
			

			
		}
	
		

	});



}

function townClickedGoog(towndata, each_town, descdata, attrdata, stopdata, transcodata, hubdata, transroutedata){
	$('.town').click(function() {
		$('.addtown').remove();
		var nextElementClass;

		
		var townName;

		

		//get the towns id
		townName = this.id;
		
		
		



		
			appendAddButton(townName);
			addTownDescription(descdata, townName);
			addattractions(attrdata, townName);
			addtransport(townName, stopdata, transroutedata, transcodata, hubdata);
			centerTown(towndata, townName);
			addTownClicked(townName, each_town, towndata, descdata);



		
	});
}

function addtransport(townName, stopdata, transroutedata, transcodata, hubdata){

	$('.trans').remove();
	//get the towns stop data
	var newtownName = townName.split("-").join(" ");
	$.each(stopdata, function(index, value){
		var stoptown = value.stoptown;
		if(stoptown == newtownName){
		 	var routeid = value.routeid;
		 	var stopid = value.stopid;
		 	var beforetownid = stopid - 1;
		 	var aftertownid = stopid + 1;

		 	$.each(hubdata, function(index, value){
				var hub = value.hubname;
		 		$.each(stopdata, function(index, value){
					var hubstopid = value.stoptown;

					if(hub == hubstopid){
						var hubroute = value.routeid;

						if(hubroute == routeid){

							$.each(transroutedata, function(index, value){
			 					var currentrouteid = value.routeid;

			 					if(currentrouteid == routeid){
			 						var companyid = value.companyid;
			 						var routename = value.routename;

						 			//loop through the company tabel to get the company name
						 			$.each(transcodata, function(index, value){
						 				var currentcompanyid = value.companyid;

						 				if(currentcompanyid == companyid){
						 					var companyname = value.companyname;
						 					var transtype = value.trans_type;

											var trans = '<p class="trans" id="' + routename + '">Get to ' + newtownName + ' from ' + hub + ' by ' + transtype +  ' with ' + companyname + '</p>';
						 					$('#transport').append(trans);
						 				}
						 			});	
						 		}
						 	});
						}
					}
				});
			});		
						 				
			$.each(stopdata, function(index, value){
	

				var prevstopid = value.stopid;
		 		if(prevstopid == beforetownid || prevstopid == aftertownid){
		 		 	var beforetown = value.stoptown;

			 		//loop through roite table to get the company id and route name
				 	$.each(transroutedata, function(index, value){
				 		var currentrouteid = value.routeid;




				 		if(currentrouteid == routeid){
				 			var companyid = value.companyid;
				 			var routename = value.routename;

				 			//loop through the company tabel to get the company name
				 			$.each(transcodata, function(index, value){
				 				var currentcompanyid = value.companyid;

				 				if(currentcompanyid == companyid){
				 					var companyname = value.companyname;
				 					var transtype = value.trans_type;


				 					var trans = '<p class="trans" id="' + routename + '">Get to ' + newtownName + ' from ' + beforetown + ' by ' + transtype +  ' with ' + companyname + '</p>';
				 					$('#transport').append(trans);

				 				}
			 				});
		 				}	
	 				});	
				}		 
			
			});
		}
	});

}
		




function centerTown(towndata, townName){
	$.each(towndata, function(key, value){
		var loopTown = value.townname;
		var newtownName = townName.split("-").join(" ");
		if(newtownName == loopTown){
			lat = value.latitude;
			lng = value.longitude
			

			var latLng = new google.maps.LatLng(lat, lng);
			map.setCenter(latLng);
			map.setZoom(14);


		}
	});
}





     
      function initMap(lat,lng, zoom) {
 
      	var latLng = new google.maps.LatLng(lat, lng);
        map = new google.maps.Map(document.getElementById('map'), {
          center: latLng,
          zoom: zoom
          
        });
      }



function loopTownSelectForDup(town_select, townName){
	var dup;
	$.each(town_select, function(index, value){
		var alreadyPicked; 
		alreadyPicked = value;
		if(alreadyPicked === townName){
			dup = 1;
			return dup;
		}
		return dup;

	});
	return dup;
}

function appendAddButton(townName){
	
	var idtownName = townName.replace
	$('#' + townName).append('<input type="submit" class="addtown" id="add' + townName + '" value="Add">');
}

function addTownClicked(townName, each_town, towndata, descdata){
	$('.addtown').click(function(){


		
		$('.addtown').remove();
		
		dupSelectedTowns(townName, towndata, descdata);
		

		
		

			
			
		
	});
}


function markerClick(marker, descdata){
	marker.addListener('click', function(){
		var id = marker.id;
		addTownDescription(descdata, id)

		$('#delete').remove();
		$('.addtown').remove();


		$('#' + id).append('<input type="submit" class="delete" id="delete" value="Delete">');

		$('#' + id).css('display', 'block');

		$("body").scrollTop($("#" + id).offset().top);

		deleteMarker(marker, id);


	});
}

function deleteMarker(marker, id){
	$('#delete').click(function(){
		marker.setMap(null);
		$('#delete').remove();

		var deleteid = id.replace(/\s+/g,"-");;

		$('#addedtown' + deleteid).remove();


	});
}

function dupSelectedTowns(townName, towndata, descdata){
	var dup;
	$.each($('.addedtown'), function(){
		pretown = this.id;

		id = pretown.slice(9);



		if(id == townName){
			
			dup = 1;
			return;
		} 
		

		
		
	});

	if(dup !== 1){
		completeTownAdd(towndata, townName, descdata);
	} else {
		alert('you have already selected' + townName);
	}
	
}

function completeTownAdd(towndata, townName, descdata){
	$.each(towndata, function(key, value){


				var towncycle = value.townname;

				var newtownName = townName.split("-").join(" ");

				if(towncycle == newtownName){

					var idtowncycle = towncycle.replace(/\s+/g,"-");

					$('#addedtowns').append('<p class="addedtown" id="addedtown'  + idtowncycle + '">' + towncycle + '</p>');

					lat = value.latitude;
					lng = value.longitude;

					var newtownName = townName.replace(/\s+/g,"-");

					var markerid = '' + newtownName;
	          
	        		

	        		var latLng = new google.maps.LatLng(lat, lng);


					var marker = new google.maps.Marker({
	   				position: latLng,
	    			map: map,
	    			id: markerid
	    		});

					markerClick(marker, descdata);
					addedTownsClick(towndata);

					
				}
			});
}

function addedTownsClick(towndata){
	$('.addedtown').click(function(){

		var addTownClicked;
		var preaddTownClicked = this.id;
		var newaddTownClicked = preaddTownClicked.split("-").join(" ");
		addTownClicked = newpreaddTownClicked.slice(9);
		$.each(towndata, function(key, value){

			var currenttown = value.townname;

			if(currenttown == addTownClicked){
				lat = value.latitude;
				lng = value.longitude;

				var latLng = new google.maps.LatLng(lat, lng);
				map.setCenter(latLng);
				map.setZoom(14);

			}

		});
	});
}
//-----------------------------------end town process functions--------------------------------------------------------------

function selectScroll(){
	$(window).scroll(function(){
  $(".ads").css({"margin-top": ($(window).scrollTop()) + "px", "margin-left":($(window).scrollLeft()) + "px"});
});
}




    


	

	




	






				
				
				

			
		
		
		

	


	
