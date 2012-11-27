//////////////////////////////////////////////////////////////////////////////////////////////////
// VISUALIZZAZIONE EDIFICI
//////////////////////////////////////////////////////////////////////////////////////////////////     


// variabile per la generazione della mappa, step0
// serve a disabilitare/abilitare gli ascoltatori sugli edifici
// in caso di violazione generica da parte dell'utente
var infoWindowListenerEnabled = false;


// creazione dell'infobubble degli EDIFICI nell'INDEX + listener
function create_infoBubble(myLatlng, nome, versione, link, foto, piani, creazione, update) {
        
        var marker = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title:nome
        });
            
       var infoBubble = new InfoBubble({
                maxWidth: 300,
                minWidth: 100,
                maxHeight: 200,
                minHeight: 100,
                hideCloseButton: true
        });
            
        currentInfoBubble = infoBubble;
            
        
        var message_first = '<div style="text-align:center"><br>';

        message_first += '<img src='+ foto +' width=150 height=100><br><br>';
        message_first += '<a href="'+link+'">Link<\/a><br>';
        
        message_first += '</div>';
        
        
        var bold = "style='font-weight:bold;'";
        var message_second ="<ul>";
                         
        var data_creazione = new Date(creazione*1000);
        var data_update = new Date(update*1000);
        var indirizzo = reverseGeocoder(myLatlng);
        
        message_second ="<a "+bold+">Release: </a>"+versione+"<br>";
        message_second ="<a "+bold+">Address:</a> "+indirizzo+"<br>";
        message_second +="<a "+bold+">Floors: </a>"+piani+"<br>";
        message_second +="<a "+bold+">Created: </a>"+data_creazione.toDateString()+"<br>";
        message_second +="<a "+bold+">Last update: </a>"+data_update.toDateString();
            
        message_second +="</ul>";
        
        
        infoBubble.addTab(nome, message_first);
        infoBubble.addTab('Details', message_second);
     
        google.maps.event.addListener(marker, 'click', function() {
                currentInfoBubble.close();
                infoBubble.open(map,marker);
                currentInfoBubble = infoBubble;
                map.panTo(myLatlng);
                map.setZoom(17);
        });
        
        return infoBubble;
}


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



// Funzione per PARSARE EFFETTIVAMENTE il JSON di DJANGO delle POLYLINE in
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
//        color = '#'+Math.floor(Math.random() *16777215).toString(16)
        user_id = user_id * 70 - 15;
        color = '#'+Math.floor(16777215 - user_id ).toString(16);
        return color;
}



/*

// funzione per la creazione delle infowindow delle POLYLINE  durante la GENERAZIONE di un
// nuovo edificio
function generate_infoWindow(polygons, polygon, id_edificio, nome_utente) {
        
        var text = "";
        text += '<strong>' + "Signal an abuse!" + '</strong><br><br>';
        text += 'Building_id: '+id_edificio;
        text += '<br>User name: ' + nome_utente;
        
        polygon.infoWindow = new google.maps.InfoWindow({
                content: text,
        }); 
        
        polygon.infoWindow.setPosition(new google.maps.LatLng(0, 0));
        
        google.maps.event.addListener(polygon, 'click', function() {
                
                for(p in polygons) {
                        console.log(polygons[p]);
                        polygons[p].infoWindow.close();
                }
                
                if (infoWindowListenerEnabled)
                        polygon.infoWindow.open(map);
        });
        
        polygons.push(polygon);
        console.log(polygons);
        
        return polygons;
}


*/
