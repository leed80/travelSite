$(document).ready(function() {

	var country = $('#country').text();
	var travelClass = $('#class').text();
	var tour = $('#tour').text();

	$.getJSON("http://127.0.0.1:8000/api/api/stop/?format=json", function(stopdata){
		$.each(stopdata, function(key, value){
			var toururl = value.tour;

			$.getJSON(toururl, function(tourdata){
				
				var loopTour = tourdata.refNumber;

				if (loopTour == tour){
					console.log('yes!');

					var stop = value.refNumber;
					var title = value.title;
					var description = value.description;


					$('#tourstopbody').append('<div id="stop' + stop + '" class="stop"><h2 id="stoptitle' + stop + '" class="stoptitle">' + title + '</h2><p id="stopdescription' + stop + '" class="stopdescription">' + description + '</p></div>');
					$('#stop' + stop).append('<div id="hotels' + stop + '" class="hotels"><p><-------------This is where i need to add hotels for selection-------------></p></div>');

					// Get hotels for that stop

					$.getJSON('http://127.0.0.1:8000/api/api/hotel/?format=json', function(hotelstop){
						$.each(hotelstop, function(hotelkey, hotelvalue){

							var loopstop = hotelvalue.stop;

							if (loopstop == stop){



								// Create a new hotel div

								var refNumber = hotelvalue.refNumber;

								$('#stop' + stop).append('<div id="' + refNumber + 'stop" class="hotel"></div>');

								

								// Show hotel name for that stop

								var hotelname = hotelvalue.title;

								$('#' + refNumber + 'stop').append('<h3 id="' + refNumber + 'name" class="hotelname">' + hotelname + '</h3>');



							

								// Show main hotel image for that stop

								$('#' + refNumber + 'stop').append('<img src="#"" alt="hotelphoto" id="' + refNumber + 'photo" class="hotelphoto">');

								// Show hotel description

								var hotelDescription = hotelvalue.description;

								$('#' + refNumber + 'stop').append('<p id="' + refNumber + 'description" class="hoteldescription">' + hotelDescription + '</p>');


								// Calcukate leaving date

									// Get arrive date

									var arriveDate = $('#date').text();

									console.log('arrive date is ' + arriveDate);

									// Get length of stay

									var lengthStay = parseInt(value.lengthofstay);

									console.log("length of stay is " + lengthStay);

									// Get the day of arrival

									var arriveday = parseInt(arriveDate.slice(-2));

									console.log("arrive day is " + arriveday);

									// Get the month

									var arrivemonth = parseInt(arriveDate.slice(5, 7));

									console.log("arrive month is " + arrivemonth);


									// Get arrival year

									var arriveyear = parseInt(arriveDate.slice(0, 4));

									console.log("arrive year is " + arriveyear);

									var leavedate = leavedatefunc(arriveday, arrivemonth, arriveyear, lengthStay);

									console.log('leavedate[7] is ' + leavedate[7]);

									

									console.log('leavedate length is ' + leavedate.length);

									

									var eanArriveDate = arrivemonth + '/' + arriveday + '/' + arriveyear;
									//slice the leave date up tp add in 0s in the correct positions infornt of day and month

									if (leavedate.length < 9){
										
										var part1 = leavedate.slice(0, 5);
										var part2 = leavedate.slice(5);
										leavedate = part1 + '0' + part2;
										var part3 = leavedate.slice(0,8);
										var part4 = leavedate.slice(8);
										leavedate = part3 + '0' + part4;

										console.log('part1 is ' + part1 + 'part2 is ' + part2);
									} else if ((leavedate.length < 10) && (leavedate[5] == '0' || leavedate[5] == '1')) {
										console.log('running leavedate[5]');
										var part1 = leavedate.slice(0,8);
										var part2 = leavedate.slice(8);
										leavedate =  part1 + '0' + part2;
									} else if ((leavedate.length < 10) && (leavedate[7] == '0' || leavedate[7] == '1' || leavedate[7] == '2' || leavedate[7] == '3')){
										console.log('running leavedate[7]');
										var part1 = leavedate.slice(0,5);
										var part2 = leavedate.slice(5);
										leavedate = part1 + '0' + part2;
									}
									console.log('leavedate is ' + leavedate);

									$('#' + refNumber + 'stop').append('<p id="' + refNumber + 'leavedate" class="leavedate">' + leavedate + '</p>');

									var leaveday = parseInt(leavedate.slice(-2));
									var leavemonth = parseInt(leavedate.slice(5, 7));
									var leaveyear = parseInt(leavedate.slice(0, 4));

									var eanLeaveDate = leavemonth + '/' + leaveday + '/' + leaveyear;

									// Work out month

									//** Create a function that will store the leave date value **

									function leavedatefunc(arriveday, arrivemonth, arriveyear, lengthStay){
										if( arrivemonth == 09 || arrivemonth == 04 || arrivemonth == 05 || arrivemonth == 11){
										// if this is true then the month has 30 days

										var daysinmonth = 30;

										console.log("the month has " + daysinmonth + " days");

										// if the date plus the length of stay > the number of days in the month then month =++
										var leaveday = arriveday + lengthStay;
										console.log("leaveday is " + leaveday);

										if(leaveday > daysinmonth){
											console.log("leaveday is > daysinmonth");
											var leavemonth = arrivemonth + 1;
											var leaveday = leaveday - 30;

											console.log("post calc leaveday is " + leaveday);



											var leavedate = arriveyear + '-' + leavemonth + '-' + leaveday;

											console.log("leavedate before function ends is " + leavedate);



											return leavedate;
										} else {
											var leavedate = arriveyear + '-' + arrivemonth + '-' + leaveday;
											return leavedate;
										}
										// minus the no of days in the month from the date plus lngth of stay to give you the date in the new month

									} else if(arrivemonth == 01 || arrivemonth == 03 || arrivemonth == 06 || arrivemonth == 07 || arrivemonth == 08 || arrivemonth == 10) {
										// if this is true then the month has 31 days
										var daysinmonth = 31;
										console.log("the month has " + daysinmonth + " days")
										// if the date plus the length of stay > the number of days in the month then month =++
										var leaveday = (arriveday + lengthStay);

										if(leaveday > daysinmonth){
											var leavemonth = arrivemonth + 1;
											var leaveday = leaveday - 31;

											var leavedate = arriveyear + '-' + leavemonth + '-' + leaveday

											return leavedate;
										} else {
											var leavedate = arriveyear + '-' + arrivemonth + '-' + leaveday
											return leavedate;
										}
										// minus the no of days in the month from the date plus lngth of stay to give you the date in the new month

									} else if (arrivemonth == 02){

										// if this is true then is it a leap year?

										if(arriveyear == 2020 || arriveyear == 2024 || arriveyear == 2028 || arriveyear == 2032){
											// if this is true then the month has 28 days
											var daysinmonth = 29;
											console.log("the month has " + daysinmonth + " days")
											// if the date plus the length of stay > the number of days in the month then month =++
											var leaveday = arriveday + lengthStay;

											if(leaveday > daysinmonth){
												var leavemonth = arrivemonth + 1;
												var leaveday = leaveday - 29;

												var leavedate = arriveyear + '-' + leavemonth + '-' + leaveday

												return leavedate;
											} else {
											var leavedate = arriveyear + '-' + arrivemonth + '-' + leaveday
											return leavedate;
											}
										// minus the no of days in the month from the date plus lngth of stay to give you the date in the new month

										} else {

											// if this is true then the month has 28 days
											var daysinmonth = 28;
											console.log("the month has " + daysinmonth + " days")
											// if the date plus the length of stay > the number of days in the month then month =++
											var leaveday = arriveday + lengthStay;

											if(leaveday > daysinmonth){
												var leavemonth = arrivemonth + 1;
												var leaveday = leaveday - 28;

												var leavedate = arriveyear + '-' + leavemonth + '-' + leaveday

												return leavedate;
											} else {
											var leavedate = arriveyear + '-' + arrivemonth + '-' + leaveday
											return leavedate;
											}
						
										}

									} else if(arrivemonth == 12){
										// Work it out for the change of the year if it goes over december 31st
										// if this is true then the month has 28 days
											var daysinmonth = 31;
											console.log("the month has " + daysinmonth + " days")
											// if the date plus the length of stay > the number of days in the month then month =++
											var leaveday = arriveday + lengthStay;

											if(leaveday > daysinmonth){
												var leavemonth = 01;
												var leaveday = leaveday - 31;
												var leaveyear = arriveyear + 1;

												var leavedate = leaveyear + '-' + leavemonth + '-' + leaveday

												return leavedate;
											} else {
											var leavedate = arriveyear + '-' + arrivemonth + '-' + leaveday
											return leavedate;
											}
									}


									}

									




								// Show room types, images, availability and rates 

								// Shpw hotel amenities

								var hotelamenities = hotelvalue.amenities;

								$('#' + refNumber + 'stop').append('<p id="' + refNumber + 'amenities" class="hotelamenities">' + hotelamenities + '</p>');

								// Get room availbility and rates

									// get sig

									var sig = $('#sig').text();
									//var sig = '0' + sig;


									console.log('sig is ' + sig);


									// get hotelid

									var hotelid = hotelvalue.eanhotelid;

									console.log('hotelid is ' + hotelid);

									//get no guests

									var guests = $('#travelers').text();

									console.log('guests is ' + guests);

									$.ajax({
									    url: '/tour/rates/',
									    type: 'get',
									    data: {
									    	'hotelid' : hotelid,
									    	'hotelref': refNumber,
									    	'eanArriveDate' : eanArriveDate,
									    	'eanLeaveDate' : eanLeaveDate,
									    	'guests' : guests,
									    	'country': country,
									    	'tour': tour
									    },
									    success: function(data) {
									        alert(data);
									    },
									    failure: function(data) { 
									        alert('Got an error dude');
									    }
									}); 

									//$.getJSON('http://api.ean.com/ean-services/rs/hotel/v3/avail?minorRev=30&cid=422852&sig=' + sig + '&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&hotelId=' + hotelid + '&arrivalDate=' + eanArriveDate + '&departureDate=' + eanLeaveDate + '&room1=2', function(hotelinfo){
										//console.log(hotelinfo);
									//});








							}
						});
					});

						

				}
				
			});
		});
	});


});