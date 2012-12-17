
///////////////////////////////////////////////////////////////////////////////////////////////
// VARIABILI GLOBALI
//////////////////////////////////////////////////////////////////////////////////////////////

var markers;
var path; 
var polygons;

max_length = 1000; // m
max_area = 500000; // m^2
        
////////////////////////////////////////////////////////////////////////////////////////////
     

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
                setUserPolygonPoints(event.latLng, true);
        });        
        setPolygonOnMap(polygons, user_id);
        
        return polygons;
}

// disegno tutti i poligoni sulla mappa, generando il colore in base al user_id
function setPolygonOnMap(polygons, user_id) {

        color = generate_color(user_id);
        
        poly = new google.maps.Polygon({
                strokeWeight: 3,
                fillColor: color,
                clickable:false
        });
        
        poly.setMap(map);
        
        poly.setPaths(new google.maps.MVCArray([path]));
        
        polygons.push(poly);
        
        return polygons;
}
///////////////////////////////////////////////////////////////////////////////////////////
function convertPolygonToNewBuildingPolygon(polygons, user_id) {

        polygon = polygons.pop().getPath();
        
        path = new google.maps.MVCArray;
        
        for(var i=0; i < polygon.length; i++) 
                setUserPolygonPoints(polygon.getAt(i), false);

        polygon = setPolygonOnMap(polygons, user_id);
        
        this.polygons = polygons;
        
        return polygons;
}
///////////////////////////////////////////////////////////////////////////////////////

// Crea dinamicamente il poligoni dell'utente, verificando nel contempo che le dimensioni
// dell'edificio non superino le massime consentite
function setUserPolygonPoints(latLng, markerClickableDraggable) {
        
        var marker_map;
        
        if (markerClickableDraggable)
                marker_map = map;
        else
                marker_map = null;
                
                
        path.insertAt(path.length, latLng);
                
        if (!testMeasures(path)) 
                path.removeAt(path.length-1);
        else { 
                updateGeometrie(path);
                var marker = new google.maps.Marker({
                        position: latLng,
                        map: marker_map,
                        draggable: markerClickableDraggable  
                });
              
                markers.push(marker);
                                
                marker.setTitle("#" + path.length);
                
                if (markerClickableDraggable) {
                
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
                                updateGeometrie(path);
                        });

                        google.maps.event.addListener(marker, 'dragend', function(event) {
                                
                                for (var i = 0, I = markers.length; i < I && markers[i] != marker; ++i);
                                
                                var old = path.getAt(i);
                                
                                path.setAt(i, event.latLng);  
                             
                                
                                if (!testMeasures(path)) {
                                        path.setAt(i, old);  
                                        markers[i].setPosition(old);   
                                }  
                                  
                                updateGeometrie(path);
                        });    
                }     
        }        
}



function bloccaDisegno() {
        for(var i=0; i<markers.length; i++) 
                markers[i].setMap(null)
        google.maps.event.clearListeners(map, "click") ;
}

// aggiorno i campi GEOMETRIA E PUNTO delle form di Django
function updateGeometrie(path) {
        
        //POLYGON((longitude latitude, ..))
        var message = "POLYGON ((";
        separator = ", ";
        ending = "))";
        
        for(var i=0; i < path.length; i++) {
                current = path.getAt(i);
                message += current.lng() + " " + current.lat(); 
                message += separator;
        }
        current = path.getAt(0);
        message += current.lng() + " " + current.lat(); 
        message += ending;
        
        var $currentIFrame = $('#the_iframe'); 
        $currentIFrame.contents().find("body #id_geometria").val(message);
        
        var bounds = new google.maps.LatLngBounds();
        var polygonCoords = [];
        for(var i=0; i < path.length; i++) 
                polygonCoords.push(path.getAt(i));

        for (i = 0; i < polygonCoords.length; i++) 
                bounds.extend(polygonCoords[i]);

        //POINT(longitude latitude)
        message = "POINT (" + bounds.getCenter().lng() + " " + bounds.getCenter().lat() +")";
        $currentIFrame.contents().find("body #id_posizione").val(message);
}

// Verifico se le misure di distanza e area tra i vari punti sono al di sotto
// di un valore massimo che identifico

function testMeasures(path) {

        message_too_long = "The line you have drawed is too long!!! Max length is " + max_length+"m";
        message_too_big = "The area of the building is too big!!! Max area is " +max_area+"m^2";
        
        for (var i=0; i< path.length; i++) {
        
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
        }
        
        area_m = google.maps.geometry.spherical.computeArea(path);
        //console.log(area_m);
        if (area_m >= max_area) {
                alert(message_too_big);
                return false;  
        }
        return true;
}


function measureCalc() {

    // Use the Google Maps geometry library to measure the length of the line
    var length = google.maps.geometry.spherical.computeLength(measure.line.getPath());
    jQuery("#span-length").text(length.toFixed(1))

    // If we have a polygon (>2 vertexes in the mvcPolygon MVCArray)
    if (measure.mvcPolygon.getLength() > 2) {
        // Use the Google Maps geometry library to measure the area of the polygon
        var area = google.maps.geometry.spherical.computeArea(measure.polygon.getPath());
        jQuery("#span-area").text(area.toFixed(1));
    }

}


function setOptimalPanEZoom(polygon) {
        path = polygon.getPaths().getAt(0);

        var bounds = new google.maps.LatLngBounds();
        for (i = 0; i < path.length; i++) 
                bounds.extend(path.getAt(i));
                
        map.fitBounds( bounds );
       
        return bounds;
}

// funzione di calcolo della dimensione (in pixel) dei bounds sulla mappa, restituisce un array
// [width, height]
function transformBoundsToPixels(bounds) {

        var SW = bounds.getSouthWest(); 
        var NE = bounds.getNorthEast();

        var proj = map.getProjection(); 
        
        var swPx = proj.fromLatLngToPoint(SW); 
        var nePx = proj.fromLatLngToPoint(NE); 
        
        var pixelWidth = Math.abs(nePx.x - swPx.x)* Math.pow(2, map.getZoom()); 
        var pixelHeight = Math.abs(nePx.y - swPx.y)* Math.pow(2, map.getZoom()); 

        //console.log(pixelWidth);
        //console.log(pixelHeight);
        
        return pixelWidth;
}


/////////////////////////////////////////////////////////////////////////////////////////////////////
// generazione dell'immagine sulla mappa

function prepareImage(directionDeg, image, width) {
          // content element of a rich marker
var richMarkerContent    = document.createElement('div');

image.style.opacity = 0.75;
image.style.width = width+"px";
image.style.height = 'auto';

// rotation in degree
//var directionDeg         = 144 ;

// create a container for the arrow
var rotationElement      = document.createElement('div');
var rotationStyles       = 'display:block;' +
                           '-ms-transform:      rotate(%rotationdeg);' +
                           '-o-transform:       rotate(%rotationdeg);' +
                           '-moz-transform:     rotate(%rotationdeg);' +
                           '-webkit-transform:  rotate(%rotationdeg);' ;

// replace %rotation with the value of directionDeg
rotationStyles           = rotationStyles.split('%rotation').join(directionDeg);

rotationElement.setAttribute('style', rotationStyles);
rotationElement.setAttribute('alt',   'arrow');

// append image into the rotation container element
rotationElement.appendChild(image);

// append rotation container into the richMarker content element
richMarkerContent.appendChild(rotationElement);

        return richMarkerContent.innerHTML;
}

function generateImageMarker(map, bounds, image) {
        var marker;
        var center = bounds.getCenter();
        
  /*      
        i_div = '<div class="my-marker">';
        i_div += '<div>This is a nice image</div>';
        //i_div += '<div><img src="'+image+'/></div>';
        i_div += '<div><img src="http://farm4.static.flickr.com/3212/3012579547_' +
            '097e27ced9_m.jpg/></div>';
        i_div += '<div>You should drag it!</div></div>';
        
        var image_div = document.createElement('DIV');
        image_div.innerHTML = image_div;
            
            console.log(image);
          console.log(center);
          console.log(map);
          console.log(image_div);
          
        marker = new RichMarker({
          position: new google.maps.LatLng(0, 0),
          map: map,
          draggable: true,
          content: i_div
          });
          
    */    
    
    // arrow image
var width = transformBoundsToPixels(bounds);  


        marker = new RichMarker(
    {
        position    : center,
        map         : map,
        draggable   : true,
        flat        : true,
        anchor      : RichMarkerPosition.MIDDLE,
        content     : prepareImage(0, image, width)
    }
);
          
          
       
//console.log(marker);
   /*     var div = document.createElement('DIV');
        div.innerHTML = '<div class="my-other-marker">I am flat marker!</div>';

        marker2 = new RichMarker({
          map: map,
          position: new google.maps.LatLng(30, 50),
          draggable: true,
          flat: true,
          anchor: RichMarkerPosition.MIDDLE,
          content: div
        });

        google.maps.event.addListener(marker, 'position_changed', function() {
          log('Marker position: ' + marker.getPosition());
        });
/*
        google.maps.event.addDomListener(document.getElementById('set-content'),
          'click', function() {
          setMarkerContent();
        });

        google.maps.event.addDomListener(document.getElementById('toggle-map'),
          'click', function() {
          toggleMap();
        });

        google.maps.event.addDomListener(document.getElementById('toggle-anchor'),
          'click', function() {
          toggleAnchor();
        });

        google.maps.event.addDomListener(document.getElementById('toggle-flat'),
          'click', function() {
          toggleFlat();
        });
        google.maps.event.addDomListener(document.getElementById('toggle-visible'),
          'click', function() {
          toggleVisible();
        });

        google.maps.event.addDomListener(document.getElementById('toggle-draggable'),
          'click', function() {
          marker.setDraggable(!marker.getDraggable());
        });
  */   
  
  return marker;
  }


      

      




