
// OGGETTI BASE /////////////////////////////////////////////////////////////

// Gestione della posizione
        function Posizione(numero) {
               
                // identificativo della posizione nella form
                ID = 'id_form-0-posizione_immagine';
                
                // formato della stringa 
                POINT = "POINT (y x)";
                
                // costruisco l'id della form
                var id = ID.replace('0', numero); 
                
                // funzione per leggere il valore
                this.read = read;
                function read() {
                        
                        var t = document.getElementById(id).value;
                        
                        t = t.substring(t.indexOf('(') + 1, t.indexOf(')') + 1);
                        
                        var y = parseFloat(t.substring(0, t.indexOf(' ')));
                        var x = parseFloat(t.substr(t.indexOf(' ') + 1));
                        
                        return new google.maps.LatLng(x,y);
                }
               
                // funzione per scriverlo
                this.write = write;
                function write(latLng) {        
                        document.getElementById(id).value = POINT.replace('x', latLng.lat()).replace('y', latLng.lng());
                }
        }
        
        
        function Zoom(numero) {
               
                // identificativo dello zoom nella form
                ID = 'id_form-0-zoom_on_map';
                
                // identificativo dello zoom della mappa
                ID_map = 'id_form-0-zoom_of_map';
                
                // valore di incremento / decremento dello zoom
                ZOOM = 2;
                
                // zoom massimo / minimo
                ZOOM_MAX = 200;
                ZOOM_MIN = 0.5;
                
                // costruisco gli id delle form
                var id = ID.replace('0', numero); 
                var id_map = ID_map.replace('0', numero);
                
                // zoom della mappa al momento del caricamento
                var map_zoom = parseInt(document.getElementById(id_map).value);
                
                // metodo per impostare lo zoom di base della mappa, casomai non sia impostato
                // viene chiamato una sola volta quando la mappa ha terminato il caricamento
                google.maps.event.addListenerOnce(map, 'idle', function() {
                        if (map_zoom < 0) {
                                map_zoom = map.zoom;
                                document.getElementById(id_map).value = map_zoom;
                        }
                });

                // funzione per calcolare il valore dello zoom in base allo zoom della mappa
                // se lo zoom della mappa cambia, viene scalato anche quello dell'immagine
                this.get = get;
                function get() {
                        
                        var difference = 0;
                        
                        if (map_zoom > 0) 
                                difference = map_zoom - map.zoom;
                                
                        var new_value = read() / Math.pow(2, difference);
                        
                        return new_value / 100;
                }
                
                // funzione per leggere il valore
                this.read = read;
                function read() {
                        
                        var t = parseFloat(document.getElementById(id).value);
                        
                        if (isNaN(t)) {
                                t = 50.0;
                                write(t);
                        }
                        
                        return t;
                }
                
                // funzione per scriverlo
                this.write = write;
                function write(value) {
                        
                        document.getElementById(id).value = value;
                }
        }
        
        
        function Bearing(numero) {
                
                // identificativo del bearing nella form
                ID = 'id_form-0-bearing';
        
                // valore di incremento / decremento del bearing
                BEARING = 0.1;
                
                // bearing massimo / minimo
                BEARING_MAX = 360;
                BEARING_MIN = 0;
                
                // identificativo della form
                var id = ID.replace('0', numero);
                
                // funzione per aggiungere i listener per la scrittura
                this.addListener = addListener;
                function addListener(o) {
                        var t = document.getElementById(id);
                        t.oninput = function() {
                                o.changeBearing();
                        };
                }
                
                
                // funzione per leggere il valore
                this.read = read;
                function read() {
                        
                        var t = parseFloat(document.getElementById(id).value);
                        
                        if (isNaN(t)) {
                                t = 0;
                                write(declinazione);
                        }
                                
                        return (t + declinazione) % 360;
                }
                
                // funzione per scriverlo
                this.write = write;
                function write(value) {
                        document.getElementById(id).value = (value - declinazione) % 360;
                }
        }
        
        
        ///////////////////////////////////////////////////////////////////////////////////////////////////
        
        
        
        // OGGETTO PIANO!!!! /////////////////////////////////////////////////////////////////////////////
        
         // creazione di un piano (numero è il numero all'interno dell'array + il link all'immagine)
        function piano(numero, link) {
                
                var posizione = new Posizione(numero);
                this.posizione = posizione;
                
                var bearing = new Bearing(numero);
                this.bearing = bearing;
                
                var zoom =  new Zoom(numero);
                this.zoom = zoom;
                
                var marker = createRichMarker();
                this.marker = marker;
                
                var immagine = loadImage(link, marker);
                this.immagine = immagine
                
                // variabile che indica se il marker (leggi immagine) è stato caricato
                var marker_ready = false;
                this.marker_ready = marker_ready;
                
                var self = this;
                
                // funzione chiamata in caso di modifiche manuali sul bearing
                this.changeBearing = changeBearing;
                function changeBearing() {
                        
                        marker.setContent(prepareImage()); 
                }
                
                function addZoomListener() {
                
                        // aggiungo l'ascoltatore sullo zoom della mappa 
                        // questo chiama la funzione per aggiornare la dimenzione del marker (ritardandolo)
                        google.maps.event.addListener(map, 'zoom_changed', function(event) {
                                if (marker.visible)
                                        setTimeout(function() {
                                                        update_marker();
                                                }, 700);
                        });
                }
                
                // funzione per forzare l'aggiornamento del marker
                this.update_marker = update_marker;
                function update_marker() {
                        marker.setContent(prepareImage());
                }
                
                // funzione per la prima creazione del richmarker
                function createRichMarker() {
                        
                        var marker = new RichMarker({
                                position    : posizione.read(),
                                map         : map,
                                draggable   : true,
                                flat        : true,
                                anchor      : RichMarkerPosition.MIDDLE,
                                visible     : false,
                        });
                        
                        // aggiungo l'ascoltatore sul trascinamento, per tracciare la posizione
                        google.maps.event.addListener(marker, 'dragend', function(event) {
                                     
                                if (document.getElementById("checkbox").checked) {
                                        for (f in floors) {
                                                floors[f].marker.position = marker.position;
                                                floors[f].posizione.write(marker.position);  
                                        }
                                }
                                
                                else
                                      posizione.write(marker.position);  
                        });
                
                        return marker;
                }
                
                function prepareImage() {
                
                        // content element of a rich marker
                        var div    = document.createElement('div');

                        // imposto colore 
                        immagine.style.opacity = document.getElementById('alpha_range').value;

                        var imageContainer = document.createElement('div');
                        
                        // imposto la rotazione e zoom
                        var deg = bearing.read();
                        var scale =  zoom.get(); 
                        
                        // stili per rotazione e ridimensionamento
                        var styles =    'display:block;' +
                                        '-ms-transform:      rotate(' + deg + 'deg) ' + 'scale(' + scale + ');' +
                                        '-o-transform:       rotate(' + deg + 'deg) ' + 'scale(' + scale + ');' +
                                        '-moz-transform:     rotate(' + deg + 'deg) ' + 'scale(' + scale + ');' +
                                        '-webkit-transform:  rotate(' + deg + 'deg) ' + 'scale(' + scale + ');';
                        
                
                        // append rotation container into the richMarker content element
                        imageContainer.setAttribute('style', styles);
                        imageContainer.appendChild(immagine);
                        
                        div.appendChild(imageContainer);
              
                        return div.innerHTML;
                }
                
                
                // carico l'immagine 
                function loadImage(link, marker) {
                
                        var immagine = new Image();
                
                        immagine.src = link;
                
                        immagine.onload = function() {
                                
                                // inizializzo il div del marker
                                marker.setContent(prepareImage());
                                
                                // aggiungo l'ascoltatore sul campo bearing
                                bearing.addListener(self);
                                
                                // aggiungo l'ascoltatore sull0 zoom della mappa
                                addZoomListener();
                                
                                // il marker è pronto quindi cambio la variabile
                                self.marker_ready = true;
                                
                                // verifico se anche gli altri piani hanno terminato il caricamento
                                // di marker
                                var test = true;
                                for (f in floors) 
                                        test = test && floors[f].marker_ready;
                                
                                var radio = document.getElementsByName("floor_list");
                                
                                // se è così abilito i radiobutton (e il pulsante di "NEXT")
                                // e faccio un "click" sul primo
                                if (test) {
                                        for (r in radio) 
                                                radio[r].disabled = false;
                                        radio[0].click(); 
                                        document.getElementById('submit').disabled = false;
                                        
                                }     
                        };  
                        
                        return immagine;
                 }
        }
        
        
        /////////////////////////////////////////////////////////////////////////////////////////////////////
        
        
        
