
//--------------- TO DO LIST ---------------------------------

// Get current hotel rates to show up the total calculated price for the trip

// Get room images from expedia

// When a hotel is selected for that stop lock it in

//-------------------------------------------------------------

//--------------- EXPEDIA INTEGRATION --------------------

// ******* To get room images from expedia ********* 

// "https://book.api.ean.com/ean-services/rs/hotel/v3/roomImages?cid=422852&minorRev=99&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&sig=7ff7583aa61db4782e61be058f8fe382&xml=%3CRoomImageRequest%3E%0A%20%20%20%20%3ChotelId%3E444276%3C%2FhotelId%3E%0A%3C%2FRoomImageRequest%3E"

// where 444276 is the hotel id and sig is generated using apikey, secret and UNIX timestam using MD5 hash

// ******* To get room rate and availability ********

// https://book.api.ean.com/ean-services/rs/hotel/v3/avail?cid=422852&minorRev=99&apiKey=5qihbibdm199m03leh63sin4jo&locale=en_US&currencyCode=USD&sig=0a30163c6465cc44d139f0701c8feecd&xml=%3CHotelRoomAvailabilityRequest%3E%0A%20%20%20%20%3ChotelId%3E106347%3C%2FhotelId%3E%0A%20%20%20%20%3CarrivalDate%3E9%2F30%2F2016%3C%2FarrivalDate%3E%0A%20%20%20%20%3CdepartureDate%3E10%2F2%2F2016%3C%2FdepartureDate%3E%0A%20%20%20%20%3CincludeDetails%3Etrue%3C%2FincludeDetails%3E%0A%20%20%20%20%3CRoomGroup%3E%0A%20%20%20%20%20%20%20%20%3CRoom%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3CnumberOfAdults%3E2%3C%2FnumberOfAdults%3E%0A%20%20%20%20%20%20%20%20%3C%2FRoom%3E%0A%20%20%20%20%3C%2FRoomGroup%3E%0A%3C%2FHotelRoomAvailabilityRequest%3E

// I need hotel id, arrivedate departure date and no of guests

// Use the RATECODE and ROOMTYPECODE stored under rooms for the hotel to cycle throuhg 
// data to get the results. Get SUPPLIERTYPE, CHARGEAGABLERATE (Carry over the value of total from the ChargeableRateInfo object returned in the room response.), 
// RATEKEY and RATETYPE to be used in the next bit.

// ******* To Book hotel **********

// Following info to be posted to expedia:

/* <HotelRoomReservationRequest>
    <hotelId>106347</hotelId>
    <arrivalDate>9/30/2016</arrivalDate>
    <departureDate>10/2/2016</departureDate>
    <supplierType>E</supplierType>
    <rateKey>af00b688-acf4-409e-8bdc-fcfc3d1cb80c</rateKey>
    <roomTypeCode>198058</roomTypeCode> 
    <rateCode>484072</rateCode>
    <chargeableRate>231.18</chargeableRate>
    <RoomGroup>
        <Room>
            <numberOfAdults>2</numberOfAdults>
            <firstName>test</firstName>
            <lastName>tester</lastName>
            <bedTypeId>23</bedTypeId>
            <smokingPreference>NS</smokingPreference>
        </Room>
    </RoomGroup>
    <ReservationInfo>
        <email>test@travelnow.com</email>
        <firstName>test</firstName>
        <lastName>tester</lastName>
        <homePhone>2145370159</homePhone>
        <workPhone>2145370159</workPhone>
        <creditCardType>CA</creditCardType>
        <creditCardNumber>5401999999999999</creditCardNumber>
        <creditCardIdentifier>123</creditCardIdentifier>
        <creditCardExpirationMonth>11</creditCardExpirationMonth>
        <creditCardExpirationYear>2018</creditCardExpirationYear>
    </ReservationInfo>
    <AddressInfo>
        <address1>travelnow</address1>
        <city>Seattle</city>
        <stateProvinceCode>WA</stateProvinceCode>
        <countryCode>US</countryCode>
        <postalCode>98004</postalCode>
    </AddressInfo>
</HotelRoomReservationRequest>



---------------------- What i want to happen --------------------

// User will select the itinerary they want

// All itinerarys will come with stops and pre selected hotels and rooms

// If room is not available on the trip then we show it as not available

// If use likes the itinerary and selects it then the system will book all rooms via expedia


*/ 