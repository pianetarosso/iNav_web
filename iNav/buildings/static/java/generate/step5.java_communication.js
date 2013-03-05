//////////////////////////////////////////////////////////////////////////////////////////////////////
// COMUNICAZIONE CON JAPPLET
        
// funzione chiamata dall'applet Java per caricare i piani
function getFloors() {

        var xmlHttp = null;

        xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", GET_FLOORS, false );
        xmlHttp.send(null);
        var json = JSON.parse(xmlHttp.responseText);
        
        // costruisco l'array globale dei piani
        for (var j in json) {
                floors.push(parseInt(json[j].numero_di_piano));
                lift[parseInt(json[j].numero_di_piano)] = [];
                stair[parseInt(json[j].numero_di_piano)] = [];
        }
        
        return json;
}
        
// abilita i campi delle options quando la JApplet ha caricato le immagini
function enableInputs() {
        form.loaded();
}
        
// Creazione di un nuovo marker
function createNewMarker(id, x, y, piano) {
 
        this.id = parseInt(id);
        this.x = parseInt(x);
        this.y = parseInt(y);
        this.piano = parseInt(piano)
        form.new_marker();
}
        
        
//////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////
