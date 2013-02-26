
var center;

// aggiorno i campi GEOMETRIA E PUNTO delle form di Django
function updateInputFields(path) {
        
        var geometria = document.getElementById('id_geometria');
        var posizione = document.getElementById('id_posizione');
        
        
        if (path == null) {
                geometria.value = '';
                posizione.value = '';
                return;
        }
        
        // imposto il valore della geometria
        geometria.value = buildPolygon(path);
        
        // calcolo il centro del poligono
        center = calculateCenter(path);
        
        // imposto il centro del poligono
        posizione.value = buildCenter(center);               
}

// funzione chiamata dal pulsante "next" della pagina per fare il reverse geocoding 
// al momento del salvataggio 
function setAddressInputFields() {
        // trovo la nazione e la città del centro del poligono
        reverseGeocoder(center, setAddress);   
}


// funzione per estrapolare i valori di città e nazione dal reverse geocoding e aggiorna i campi NAZIONE e CITTÀ
function setAddress(address) {
                
        var address_components =  address[0].address_components;
        
        var città = '';
        var nazione = '';
        
        for (l in address_components) {
                
                if (address_components[l].types.indexOf("country") > -1)
                        nazione = address_components[l].long_name;
                        
                if (address_components[l].types.indexOf("locality") > -1)
                        città = address_components[l].long_name;
        }

        // se non ho trovato la città, vuol dire che si trova sotto tag diversi, per cui
        // effettuo una nuova ricerca
        if (città == '') {
                
                for (l in address_components) {
                
                        if ((address_components[l].types.indexOf("administrative_area_level_1") > -1) ||
                            (address_components[l].types.indexOf("administrative_area_level_2") > -1) ||
                            (address_components[l].types.indexOf("administrative_area_level_3") > -1)) {  
                                
                                città = address_components[l].long_name;
                                break;
                        }
                }
        }
        
        
        // imposto i valori nei campi della pagina
        var nazioneF = document.getElementById('id_nazione');
        var cittàF = document.getElementById('id_citta')
        
        nazioneF.value = nazione;
        cittàF.value = città;
        
        //console.log("nazione: "+ nazione);
        //console.log("città: "+ città);
}


// produco la stringa de centro del poligono
function buildCenter(center) {

        //POINT(longitude latitude)
        message = "POINT (" + center.lng() + " " + center.lat() +")";

        return message;
}

// calcolo la stringa derivante dal poligono
function buildPolygon(path) {

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

        return message;
}

// calcolo il centro del poligono
function calculateCenter(path) {

        var bounds = new google.maps.LatLngBounds();
        var polygonCoords = [];
        for(var i=0; i < path.length; i++) 
                polygonCoords.push(path.getAt(i));

        for (i = 0; i < polygonCoords.length; i++) 
                bounds.extend(polygonCoords[i]);
        
        return bounds.getCenter()
}

