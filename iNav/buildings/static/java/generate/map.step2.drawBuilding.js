///////////////////////////////////////////////////////////////////////////////////////////////
// VARIABILI GLOBALI
//////////////////////////////////////////////////////////////////////////////////////////////

var markers;
var path; 
var polygons;
var map

// valori limite per il disegno di un edificio
var max_length; // m
var min_length;

var max_area; // m^2
var min_area;  
      
////////////////////////////////////////////////////////////////////////////////////////////
     
// funzione per impostare le dimensioni massime e minime di un edificio
function initializeGeometryLimits(max_area, min_area, max_length, min_length) {

        this.max_length = max_length;
        this.min_length = min_length;
        
        this.max_area = max_area;
        this.min_area = min_area;
}

// inizializzo le variabili globali all'avvio    
function initializeJS(map, polygons) {
        map = this.map;
        markers = [];
        path = new google.maps.MVCArray;
        polygons = this.polygons;
} 


// funzione per abilitare il disegno dell'edificio da parte dell'utente
function disegna_edificio(polygons, user_id) {
         
        google.maps.event.addListener(map, 'click', function(event) {
                setUserPolygonPoints(event.latLng);
        });        
        setPolygonOnMap(polygons, user_id);
        
        return polygons;
}

// funzione per eliminare il building disegnato dall'utente
function clearUserPolygon() {
        
        for(m in markers)
                markers[m].setMap(null);
                
        markers = [];
        
        path.clear();
        updateInputFields(null);
        
        enableNextButton();
}

// funzione per abilitare o meno il pulsante "next" e il "canc"
function enableNextButton() {
        
        next = document.getElementById('submit');
        delete_b = document.getElementById('delete');
        
        next.disabled = path.length <= 2; 
        delete_b.hidden = path.length < 1; 
}


// Crea dinamicamente il poligoni dell'utente, verificando nel contempo che le dimensioni
// dell'edificio non superino le massime consentite
function setUserPolygonPoints(latLng) {
        
        if (path.length == 0) {
                map.panTo(latLng);
                map.setZoom(17);
        }
       
        testPoint(latLng);
        
        path.insertAt(path.length, latLng);
        
       
        if (!testMeasures(path)) 
                path.removeAt(path.length-1);
        else { 
                
                enableNextButton();
                
                updateInputFields(path);
                
                var marker = new google.maps.Marker({
                        position: latLng,
                        map: map,
                        draggable: true  
                });
              
                
                markers.push(marker);
                                
                marker.setTitle("#" + path.length);
                
                google.maps.event.addListener(marker, 'click', function(event) {
                                       
                        for (var i = 0, I = markers.length; i < I && markers[i] != marker; ++i);
                                
                        old = path.getAt(i);
                        path.removeAt(i);  
                                 
                        if (!testMeasures(path)) 
                                path.insertAt(i, old);
                        else {
                                marker.setMap(null);
                                markers.splice(i, 1);    
                        }   
                                
                        updateInputFields(path);
                        enableNextButton();
                });

                google.maps.event.addListener(marker, 'dragend', function(event) {
                        
                        for (var i = 0, I = markers.length; i < I && markers[i] != marker; ++i);
                                
                        var old = path.getAt(i);
                                
                        path.setAt(i, event.latLng);  
                             
                                
                        if (!testMeasures(path)) {
                                path.setAt(i, old);  
                                markers[i].setPosition(old);   
                        }  
                                  
                        updateInputFields(path);
                 });       
        }        
}

// verifico se il punto 
testPoint(latLng)

// Verifico se le misure di distanza e area tra i vari punti sono al di sotto
// di un valore massimo che identifico
function testMeasures(path) {

        message_too_long = "The line you have drawed is too long!!! Max length is " + max_length+"m";
        message_too_big = "The area of the building is too big!!! Max area is " +max_area+"m^2";
        
        if (path.length > 1) {
                for (var i=0; (i< path.length); i++) {
                
                        var test = new google.maps.MVCArray;
                        
                        test.insertAt(0, path.getAt(i));
                        
                        if (i+1 >= path.length)
                               test.insertAt(1, path.getAt(0)); 
                        else
                                test.insertAt(1, path.getAt(i+1));
                                
                        length_m = google.maps.geometry.spherical.computeLength(test);
                
                        
                        if (length_m >= max_length) {
                                alert(message_too_long);
                                return false; 
                        }
                        
                        if (length_m < min_length) 
                                return false;        
                }
        }
        
        if (path.length > 2) {
                area_m = google.maps.geometry.spherical.computeArea(path);
                
                if (area_m >= max_area) {
                        alert(message_too_big);
                        return false;  
                }
        }
        
        return true;
}

