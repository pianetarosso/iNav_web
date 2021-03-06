///////////////////////////////////////////////////////////////////////////////////////////
// GEOCODING (& relativa grafica)
///////////////////////////////////////////////////////////////////////////////////////////


// Converto un indirizzo in coordinate
function codeAddress() {

        geocoder = new google.maps.Geocoder();
        var address = document.getElementById('address').value;
        
        geocoder.geocode({'address': address}, 
                function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                                map.setCenter(results[0].geometry.location);
                                map.setZoom(15);
                        } 
                        else 
                                alert('Geocode was not successful for the following reason: ' + status);
                }
        );
}

// converto una coordinata in indirizzo e lo passo alla funzione "funct" in input
function reverseGeocoder(latLng, funct) {
        geocoder = new google.maps.Geocoder();
        geocoder.geocode({'latLng': latLng}, 
                function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) 
                                funct(results);
                                //return results[0].formatted_address;
                        else 
                                return 'Geocode was not successful for the following reason: ' + status;
        });
}           
   
// modifico il colore del testo della casella di input e aggiungo blur   
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

