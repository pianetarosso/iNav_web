// FUNZIONE PER PASSARE ALLO STEP SUCCESSIVO

function nextStep() {
        if (oldValue == 0)
                return;
        var pathsFromJApplet = window.top.getPaths();

        var roomsFromMarkers = [];
        var pathsFromMarkers = [];

        var points = [];
        var paths = [];
        var rooms = [];

        // converto i markers in Points, mettendo da parte gli oggetti Room e path
        for (var m in markers) {

                marker = markers[m];

                if (marker.nome_stanza != "") 
                        roomsFromMarkers.push(marker);

                if ((marker.ascensore!="") || (marker.scala != ""))
                        pathsFromMarkers.push(marker);

                points.push(new Point(marker.id, 
                        marker.piano, 
                        marker.RFID, 
                        marker.x, 
                        marker.y, 
                        marker.ingresso
                ));
        }

        // scansiono le path dalla JAPPLET per vedere se devo creare altri POINT
        // questi avranno id negativo per non rischiare di utilizzare id già presenti
        var id = -2; 
        for (var piano in pathsFromJApplet) {
                pathsFJ = pathsFromJApplet[piano];
                newPaths = [];
        
                for (var p = 0; p < pathsFJ.length; p++) {
                        var path = pathsFJ[p];

                        //struttura:id_marker_1,x1,y1,id_marker_2,x2,y2
                        // se il marker.id == -1, allora non esiste

                        if (path[0] == -1) {
                                var new_id = findPath(id, newPaths, path[1], path[2]);

                                if (new_id == id) {
                                        point = new Point(
                                                id, 
                                                piano, 
                                                "", 
                                                path[1], 
                                                path[2], 
                                                false
                                        );
                                        points.push(point); 
                                        newPaths.push(point); 
                                        id -= 1;
                                }
                                path[0] = new_id;                                        
                        }

                        if (path[3] == -1) {
                                var new_id = findPath(id, newPaths, path[4], path[5]);
                                
                                if (new_id == id) {
                                        point = new Point(
                                                new_id, 
                                                piano, 
                                                "", 
                                                path[4], 
                                                path[5], 
                                                false
                                        ); 
                                        points.push(point); 
                                        newPaths.push(point);
                                        id -= 1;
                                }
                                path[3] = new_id;
                        }

                }
        }

        // a questo punto dispongo di tutti i punti necessari, quindi con un ciclo 
        // provvedo a costuirli
        addInput(points, 0);


        // ora preparo le stanze
        for (var r in roomsFromMarkers) {
                room = roomsFromMarkers[r];

                rooms.push(new Room(
                        room.id,
                        room.nome_stanza,
                        room.persone,
                        room.altro,
                        room.link
                ));
        }

        // costruisco le stanze
        addInput(rooms, 2);

        // preparo le path dai marker dividendo gli ascensori dalle scale, e costruendo
        // un dizionario con gli id
        var ascensore = {};
        var scala = {};

        for (var p in pathsFromMarkers) {
                path = pathsFromMarkers[p];

                if (path.ascensore != "") {
                        if (ascensore[path.ascensore] == null)
                                ascensore[path.ascensore] = [];
                        ascensore[path.ascensore].push(path);
                        }
                        else {
                                if (scala[path.scala] == null)
                                        scala[path.scala] = [];
                                scala[path.scala].push(path);
                }
        }

        // aggiungo gli ascensori, inserendo una sola path dal piano più basso al più alto
        // es [0,1,2,3] => 0->1; 1->2; 2->3;
        for (var a in ascensore) {
                asc = ascensore[a];
                asc.sort(sortMByFloor);

                for (var p in asc) {
                        var next = parseInt(p) + 1;
                        if (next < asc.length) 
                                paths.push(new Path(
                                        asc[p].id,
                                        asc[next+""].id,
                                        asc[p].ascensore,
                                        '' 
                                ));
                }
        }

        // aggiungo le scale
        for (var s in scala) {
                asc = scala[s];
                asc.sort(sortMByFloor);

                for (var p in asc) {
                        var next = parseInt(p) + 1;
                        if (next < asc.length) 
                                paths.push(new Path(
                                        asc[p].id,
                                        asc[next+""].id,
                                        '',
                                        asc[p].scala 
                                ));
                }
        }

        // aggiungo le path dalla JApplet
        for (piano in pathsFromJApplet) {
                for (path in pathsFromJApplet[piano]) {
                        pathOfPiano = pathsFromJApplet[piano][path];
                        paths.push(new Path(
                                pathOfPiano[0],
                                pathOfPiano[3],
                                '',
                                '' 
                        ));
                }
        }

        // costruisco le path
        addInput(paths, 1);
        
        // lancio il submit della form
        document.forms["myform"].submit();
}

// funzione per scoprire se il punto di una path corrisponde ad una appena creata
function findPath(id, newPaths, x, y) {
        for (var p in newPaths) {
                var path = newPaths[p];
                if ((path.x.value == x) && (path.y.value == y))
                        return path.id.value;
        }
        return id;
}

// funzione per fare il sort dei marker in base al piano in ordine crescente
function sortMByFloor(m1, m2) {

        if (m1.piano > m2.piano)
                return 1;
        else if (m1.piano == m2.piano)
                return 0;
        else
                return -1;
} 




function couples(name, value) {
        this.name = name;
        this.value = value;
}
 
function Point(id, piano, RFID, x, y, ingresso) {
 
        this.id = new couples("temp_id", id);
        this.piano = new couples("temp_piano", piano);
        this.RFID = new couples("RFID", RFID);
        this.x = new couples("x", x);
        this.y = new couples("y", y);

        if (ingresso)
                this.ingresso = new couples("ingresso", "True");
        else
                this.ingresso = new couples("ingresso", "False");
         
        this.array = array;
        function array() {
                return [this.id, this.piano, this.RFID, this.x, this.y, this.ingresso]; 
        }
}
 
function Path(a, b, ascensore, scala) {
 
        this.a = new couples("temp_a", a);
        this.b = new couples("temp_b", b);
        this.ascensore = new couples("ascensore", ascensore);
        this.scala = new couples("scala", scala);
         
        this.array = array;

        function array() {
                return [this.a, this.b, this.ascensore, this.scala]; 
        }
}
 
function Room(punto, nome_stanza, persone, altro, link) {
 
        this.punto = new couples("punto", punto);
        this.nome_stanza = new couples("nome_stanza", nome_stanza);
        this.persone = new couples("persone", persone);
        this.altro = new couples("altro", altro);
        this.link = new couples("link", link);
         
        this.array = array;

        function array() {
                return [this.punto, this.nome_stanza, this.persone, this.altro, this.link]; 
        }
}

form_types = ["points", "paths", "rooms"];

function addInput(element, type) {
        
        ID = "id_";

        var minimum_length = 1;
        
        if (element.length == 0) 
                switch(type) {
                        case 0:
                                element.push(new Point('','','','','',''));
                                break;
                        case 1:
                                element.push(new Path('','','',''));
                                break;
                        case 2:
                                element.push(new Room('','','','',''));
                                break;
                }
              

        var form = document.getElementById("myform");

        // INTESTAZIONE
        var newform = document.createElement('input');
        newform.type = "hidden";
        newform.name = form_types[type] + "-" + "TOTAL_FORMS";
        newform.id = ID + form_types[type] + "-" + "TOTAL_FORMS";
        newform.value = element.length;
        form.appendChild(newform);
        
        // ROBA DI CONTROLLO
        var newform = document.createElement('input');
        newform.type = "hidden";
        newform.name = form_types[type] + "-" + "INITIAL_FORMS";
        newform.id = ID + form_types[type] + "-" + "INITIAL_FORMS";
        newform.value = minimum_length;
        form.appendChild(newform);
        
        var newform = document.createElement('input');
        newform.type = "hidden";
        newform.name = form_types[type] + "-" + "MAX_NUM_FORMS";
        newform.id = ID + form_types[type] + "-" + "MAX_NUM_FORMS";
        form.appendChild(newform);
        ////////////////////////////
        
        // ELEMENTI
        var number = 0;
        for (e in element) {
                var elements = element[e].array();

                for (var i in elements) {
                        var newform = document.createElement('input');
                        newform.type = "hidden";
                        newform.id = ID + form_types[type] + "-" + number + "-" + elements[i].name;
                        newform.name = form_types[type] + "-" + number + "-" + elements[i].name;
                        newform.value = elements[i].value;
                        form.appendChild(newform);
                        console.log(newform);
                }
                number++;
        }
}
 
//////////////////////////////////////////////////////////////////////////////////////////////
