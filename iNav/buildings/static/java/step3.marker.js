// STEP3 GESTIONE DELLA CREAZIONE E GESTIONE DEI MARKER E DELLE PATH


// lista di markers ordinati in base ad un id generato dalla JApplet
var markers = {};
        
// lista di ascensori e scale indicizzate per piano
var elevator_list = {};
var stair_list = {};
        
// valore temporaneo per un nuovo marker, in attesa che venga salvato dall'utente
var new_marker = null;

// valore temporaneo per l'editing di un marker
var edit_marker = null;

// oggetto marker di base
function Marker(id, piano, x, y) {
 
        // id temporaneo
        this.id = id;
        this.piano = piano;
        this.x = x;
        this.y = y;
        
        this.RFID = "";
         
        this.ascensore = "";
        this.scala = "";
        this.ingresso = false;
        
        this.nome_stanza = "";
        this.persone = "";
        this.altro = "";
        this.link = "";
        
}

// aggiorno le coordinate del marker
function updateMarkerPosition(id, x, y) {
        var m = markers[id];
        m.x = x;
        m.y = y;
        markers[id] = m;
}

// funzione per editare un marker
function editMarker(id) {

        //removeMarker(true);
        valid_input = {};
        
        // copio il marker nella variabile temporanea, e lo elimino dalla lista
        edit_marker = markers[id];
        delete(markers[id]);
        
         // creo le options
        setOptionsElevator(elevator_list, edit_marker.piano);
        setOptionsStair(stair_list, edit_marker.piano);
        
        resize('marker');
        resize('commands');
        
        toEditButton();
        
        showMarkerData(edit_marker);
}

// funzione chiamata dalla JAPPLET al momento delle creazione di un marker, 
// gli viene passato un id interno del marker, il piano e le coordinate del punto 
function addMarker(id, x, y, piano) {
        
        // elimino eventuali altri marker presenti in editing o creazione
        //removeMarker(true);
        
        valid_input = {};
        
        new_marker = new Marker(id, piano, x, y, null);
        
        // creo le options
        setOptionsElevator(elevator_list, piano);
        setOptionsStair(stair_list, piano);
        
        toSaveButton();
        
        resize('marker');
        resize('commands');
}

// funzione per il salvataggio di un nuovo marker
function saveMarker() {

        if (new_marker != null)
                marker = new_marker;
        else
                marker = edit_marker;
                
        marker.RFID = getRFID();
        
        var room = getRoom();
        marker.nome_stanza = room[0];
        marker.link = room[1];
        marker.persone = room[2];
        marker.altro = room[3];
        
        marker.ascensore = getElevator();
        marker.scala = getStair();
        
        marker.ingresso = getAccess();
         
        // salvo il marker nella lista
        markers[marker.id] = marker;
        console.log(markers);
        // aggiorno la lista delle scale e degli ascensori
        updateElevatorAndStairList(marker)
        
        removeOptions(marker.piano);
               
        test = marker.ingresso;
        test = test || (marker.ascensore != "");
        test = test || (marker.scala != "");
        
        // abilitazione al movimento della JAPPLET
        // primo valore: "SALVATO?"
        // secondo valore: ID
        // terzo valore: tipo (marker/path)
        // quarto valore: booleano che indica se è un ingresso/ascensore/scala
        operationComplete(true, marker.id, "marker", test);
        
        new_marker = null;
        edit_marker = null;
        
        resize('marker');
        resize('commands');
        console.log(markers);
        console.log(valid_input);
        console.log("MARKER SAVED!");
}

// aggiorno le liste delle scale e degli ascensori
function updateElevatorAndStairList(marker) {
        console.log(marker);
        // se l'array per il piano non esiste, lo creo
        if (elevator_list[marker.piano] == null)
                elevator_list[marker.piano] = [];
               
        if (stair_list[marker.piano] == null)
                stair_list[marker.piano] = [];   
        
        // testo se l'id dell'ascensore è già presente da qualche parte
        var test_e = true;
        for(var e in elevator_list) 
                test_e = test_e && (elevator_list[e].indexOf(marker.ascensore) < 0);
        
         // testo se l'id della scala è già presente da qualche parte
        var test_s = true;
        for(var s in stair_list) 
                test_s = test_s && (stair_list[s].indexOf(marker.scala) < 0);
        
        console.log(test_e);
        console.log(test_s);
        // verifico e, in caso, aggiungo i valori alle liste
        if ((marker.ascensore != "") && test_e) {
                list = elevator_list[marker.piano];
                list[list.length] = marker.ascensore;
                elevator_list[marker.piano] = list;
        }
        
        if ((marker.scala != "") && test_s) {
                list = stair_list[marker.piano];
                list[list.length] = marker.scala;
                stair_list[marker.piano] = list;
        }
}

// funzione per verificare che il valore di scala o ascensore immesso 
// non sia già presente sullo stesso piano
function testDuplicates(type, value) {
       
       console.log(type);
       console.log(value);
       console.log(elevator_list);
       console.log(new_marker);
        if (new_marker != null)
                marker = new_marker;
        else
                marker = edit_marker;
              console.log(marker);  
        if (marker != null) {
                if (type == "elevator_new_id") 
                        list = elevator_list[marker.piano];
                if (type == "stair_new_id")
                        list = stair_list[marker.piano];
                if (list != null)
                        return (list.indexOf(value) >= 0);
        }
        
        return false
}


// funzione per la rimozione dei parametri di un marker dalla form, 
// a seconda che sia stato appena creato (cancellazione) o editato (dismiss delle modifiche)
function removeMarker(value) {

        if (new_marker != null) {
                if (value) {
                        removeMarkerParam(new_marker.piano);
                        
                         // eliminazione del marker sulla JAPPLET
                         operationComplete(false, new_marker.id, "marker", false);
                        new_marker = null;
                        showQuestion(false);
                        resize('marker');
                        resize('commands');
                }
                else
                        showQuestion(true);
        }
        
        if (edit_marker != null) {
                if (value) {
                        markers[edit_marker.id] = edit_marker;
                        removeMarkerParam(edit_marker.piano);
                        operationComplete(false, edit_marker.id, "marker", false);
                        edit_marker = null;
                        showQuestion(false);
                        resize('marker');
                        resize('commands');
                }
                else {
                        removeMarkerParam(edit_marker.piano);
                        operationComplete(false, edit_marker.id, "marker", false);   
                        edit_marker = null;
                        resize('marker');
                        resize('commands');
                }
        } 
}

var question_showed = false;
function showQuestion(value) {
 
        if (( value && !question_showed ) || ( !value && question_showed )) {
                resize("buttons");
                resize("question");
                
                if (question_showed)
                        question_showed = false;
                else
                        question_showed = true;
        }
}

// rimuovo tutti i parametri del marker dalla form
function removeMarkerParam(piano) {
        removeOptions(piano);
        
        // azzero le validazioni
        valid_input = {};
}

// elimino i campi options creati ad-hoc
function removeOptions(piano) {
        removeOptionsElevator(elevator_list, piano);
        removeOptionsStair(stair_list, piano);
}

// funzione deputata all'aggiornamento della posizione di un marker
function updatePosition(id, x, y) {
        marker = markers[id];
        marker.x = x;
        marker.y = y;
        markers[id] = marker;
        console.log(marker);
}









