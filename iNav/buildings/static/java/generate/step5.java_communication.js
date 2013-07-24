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
        for (var j in json) 
                floors.push(parseInt(json[j].numero_di_piano));
             
            
        return json;
}
        
// abilita i campi delle options quando la JApplet ha caricato le immagini
function enableInputs() {
        form.loaded();
}
  
// "apro" la form per la creazione di un nuovo marker      
function createNewMarker() {
        form.new_marker();
}       

function saveNewMarker(RFID, access, elevator, stair, room_name, room_people, room_link, room_other) {
        mapGenerator.saveNewMarker(
            RFID,
            access,
            elevator,
            stair,
            room_name,
            room_people,
            room_link,
            room_other);

}

    
function cancelNewMarker(){
        mapGenerator.dismissNewMarker();
}   

function setMarkerData(marker) {
        console.log(marker)
        form.edit_marker(marker);
}


function saveEditMarker(RFID, access, elevator, stair, room_name, room_people, room_link, room_other) {
        mapGenerator.editMarker(
            RFID,
            access,
            elevator,
            stair,
            room_name,
            room_people,
            room_link,
            room_other);
}
   
function deleteMarker() {
        mapGenerator.deleteMarker();
}   



function getRoomList() {

        var out = []
        
        var json = JSON.parse(mapGenerator.getRoomNames());
        
        for (j in json) 
                out.push(json[j]);
        
        return out;
} 

function getRFIDList() {

        var out = []
        
        var json = JSON.parse(mapGenerator.getRFIDs());
        
        
        for (var j in json) 
                out.push(json[j]);
        
        return out;
}


function getLiftList() {

        return getLiftOrStairList(true);
}

function getStairList() {

        return getLiftOrStairList(false);
} 


function getLiftOrStairList(isLift) {

        var out = {}
        var json;
        
        for (f in floors) 
                out[floors[f]] = []
        
        if (isLift)
                json = JSON.parse(mapGenerator.getLifts());
        else
                json = JSON.parse(mapGenerator.getStairs());
       
        for (f in floors) 
                out[floors[f]] = json[f];
        
        return out;
}


 

// chiamata dall'applet al posto del System.out.println
function debug(value) {
        console.log("Applet:\n"+value+"\nEND!");
} 
//////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////
