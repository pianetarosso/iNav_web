///////////////////////////////////////////////////////////////////////////////////////////
// GEOCODING (& relativa grafica)
///////////////////////////////////////////////////////////////////////////////////////////


// Converto un indirizzo in coordinata
function codeAddress() {

        geocoder = new google.maps.Geocoder();
        var address = document.getElementById('address').value;
        
        geocoder.geocode({'address': address}, 
                function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                                map.setCenter(results[0].geometry.location);
                                map.setZoom(14);
                        } 
                        else 
                                alert('Geocode was not successful for the following reason: ' + status);
                }
        );
}

// converto una coordinata in indirizzo
function reverseGeocoder(latLng) {
        geocoder = new google.maps.Geocoder();
        geocoder.geocode({'latLng': latLng}, 
                function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) 
                                return results[0].formatted_address;
                        else 
                                return 'Geocode was not successful for the following reason: ' + status;
        });
}           
   
// modifico il colore del testo della casella di input e aggiunglo blur   
function inputFocus(i){
        
        if(i.value==i.defaultValue) { 
                i.value=""; 
                i.style.color="#000"; 
        }
}
        
function inputBlur(i) {
          
        if(i.value=="") { 
                i.value=i.defaultValue; 
                i.style.color="#888"; 
        }
}
   
//////////////////////////////////////////////////////////////////////////////////////////////////

