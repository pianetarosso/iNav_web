//////////////////////////////////////////////////////////////////////////////////////////////////
// VISUALIZZAZIONE EDIFICI
//////////////////////////////////////////////////////////////////////////////////////////////////     




// Funzione per il PARSING delle POLYLINE ricavate dal db di django
// CHIAMATA: alert('{{b.geometria.geojson|safe}}');
// FORMATO JSON: { "type": "Polygon", "coordinates": [ [ [ lng, lat ], [ lng, lat ], ... ] ] }
function parseJSONPolyline(data, user_id, polygons, map) {

        var path = coord_to_path(data);
        
        polygon = new google.maps.Polygon({ 
                paths : new google.maps.MVCArray([path]), 
                strokeColor : "#B22222", 
                strokeOpacity : .5, 
                strokeWeight : 1, 
                fillColor : generate_color(user_id), 
                fillOpacity : .5,
                clickable: false
        });

        polygon.setVisible(true)
        polygon.setMap(map);   

        polygons.push(polygon);
        
        return polygons;
}

// Funzione per convertire il JSON di DJANGO delle POLYLINE in
// un ARRAY di COORDINATE
function coord_to_path(coords, path) {

        var path = new google.maps.MVCArray;
        
        data = coords.coordinates[0];
        
        for (var j = 0; j < data.length; j++) {
         
            var ll = new google.maps.LatLng(data[j][1], data[j][0]);
             path.insertAt(j, ll); 
        } 
    return path;       
}


// Semplice funzione per generare colori di riempimento delle POLYLINE diversi
// per ogni utente in base al loro ID
function generate_color(user_id) {

        user_id = user_id * 70 - 15;
        color = '#'+Math.floor(16777215 - user_id ).toString(16);
        return color;
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

// calcolo il pan e zoom ottimale per visualizzare un poligono 
function setOptimalPanEZoom(polygon, map) {

        path = polygon.getPaths().getAt(0);

        var bounds = new google.maps.LatLngBounds();
        for (i = 0; i < path.length; i++) 
                bounds.extend(path.getAt(i));
            
        map.fitBounds( bounds );
       
        return bounds;
}

// funzione per limitare il movimento dell'utente sulla mappa
function blockMapMovement(bounds) {
                
        var lastValidCenter = map.getCenter();

        google.maps.event.addListener(map, 'center_changed', function() {
                if (bounds.contains(map.getCenter())) {
                
                        // still within valid bounds, so save the last valid position
                        lastValidCenter = map.getCenter();
                        return; 
                }

                // not valid anymore => return to last valid position
                map.panTo(lastValidCenter);
        });
}
        
        

// funzione per centrare un poligono nella mappa ed eliminare la possibilità di movimento
// (consigliabile settare l'opzione "minZoom:16" della mappa per limitare la possibilità di zoom)
function setAndBlockPolygon(polygon, map) {

        var bounds = setOptimalPanEZoom(polygon, map);
        blockMapMovement(bounds);
}




// creazione dell'infobubble degli EDIFICI nell'INDEX + listener
function create_infoBubble(myLatlng, nome, link, foto, map, poligono) {
        
        var marker = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title:nome
        });
            
            
        var message_first = '<div style="text-align:center"><br>';
        
        message_first += '<a href="'+link+'">'+nome+'<\/a><br><br>'
        message_first += '<img src='+ foto +' height=100 >';
        message_first += '</div>';
        
        var infoBubble = new InfoBubble({
                maxWidth: 300,
                minWidth: 100,
                maxHeight: 200,
                minHeight: 100,
                hideCloseButton: false,
                content: message_first
        });
            
        currentInfoBubble = infoBubble;
        
        google.maps.event.addListener(marker, 'click', function() {
                currentInfoBubble.close();
                infoBubble.open(map,marker);
                currentInfoBubble = infoBubble;
                setOptimalPanEZoom(poligono, map);
        });
        
        return infoBubble;
}

