
///////////////////////////////////////////////////////////////////////////////////////////////
// VARIABILI GLOBALI
//////////////////////////////////////////////////////////////////////////////////////////////

var markers;
var path; 
var polygons;
var map








///////////////////////////////////////////////////////////////////////////////////////////
function convertPolygonToNewBuildingPolygon(polygons, user_id) {

        polygon = polygons.pop().getPath();
        
        path = new google.maps.MVCArray;
        
        for(var i=0; i < polygon.length; i++) 
                setUserPolygonPoints(polygon.getAt(i));

        polygon = setPolygonOnMap(polygons, user_id);
        
        this.polygons = polygons;
        
        return polygons;
}
///////////////////////////////////////////////////////////////////////////////////////









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

      




