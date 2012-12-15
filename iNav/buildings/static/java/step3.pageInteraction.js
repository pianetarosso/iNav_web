// LETTURA / SCRITTURA DATI SULLA PAGINA


//////////////////////////////////////////////////////////////////////////////////////////////////
// FUNZIONI PER IMPOSTARE UN MARKER NELLA FORM

// carico nella form i dati di un marker già presente
function showMarkerData(marker) {

        // RFID
        if (marker.RFID != "") {
                resize('RFID');
                document.getElementById(createCheckBoxId('RFID')).checked = true; 
                document.getElementById('RFID_text').value = marker.RFID;
        }
    
        // INGRESSO
        if (marker.ingresso) {
                document.getElementById(createCheckBoxId('access')).checked = marker.ingresso;
                disableCheckBoxes('access');
        }
    
        // STANZA
        else if (marker.nome_stanza != "") {
                resize('room');
                document.getElementById(createCheckBoxId('room')).checked = true;
                disableCheckBoxes('room');
                document.getElementById("room_name").value = marker.nome_stanza;
                document.getElementById("room_link").value = marker.link;
                document.getElementById("room_people").value = marker.persone;
                document.getElementById("room_notes").value = marker.altro;
        }
    
        // ASCENSORE
        else if (marker.ascensore != "") 
                setElevatorOrStair(marker.ascensore, 'elevator');
    
        // SCALA
        else if (marker.scala != "")
                setElevatorOrStair(marker.scala, 'stair');

        disableSaveButton(false);        
}
 
// imposto i valori del menu a tendina o del testo per gli ascensori o le scale
function setElevatorOrStair(value, type) {
        resize(type);
        document.getElementById(createCheckBoxId(type)).checked = true;  
        disableCheckBoxes(type);
        childs =  document.getElementById(createOptionId(type)).children;
        var t = -1;
        for(i=0; i < childs.length; i++) 
                if (childs.text == value) {
                        t = i;
                        break;
                }    
        if (t > 0) 
                document.getElementById(createOptionId(type)).selectedIndex = t;
        else
                document.getElementById(createOptionNewidId(type)).value = value;
}
        
//////////////////////////////////////////////////////////////////////////////////////////////////
// FUNZIONI PER IMPOSTARE I VALORI DELLE OPTIONS DI ASCENSORI E SCALE

function setOptions(list, exclude_floor, name, add) {
    
        if (add) {
                for(var l in list) {
                        // non considero il piano da escludere
                        if (l != exclude_floor) {
        
                                array = list[l];  
                                for (a in array) {
                                        var newoption = document.createElement('option');
                                        newoption.value = array[a];
                                        newoption.text = array[a];
                                        document.getElementById(createOptionId(name)).appendChild(newoption);
                                } 
                        }
                }
        }
        else {
                child =  document.getElementById(createOptionId(name)).children;
                for (var i=1; i < child.length; i++)    
                        document.getElementById(createOptionId(name)).removeChild(child[i]);
        }
}
        
function setOptionsElevator(list, exclude_floor) {
        setOptions(list, exclude_floor, 'elevator', true);
}
        
function setOptionsStair(list, exclude_floor) {
        setOptions(list, exclude_floor, 'stair', true);
}
        
function removeOptionsElevator(list, exclude_floor) {
        setOptions(list, exclude_floor, 'elevator', false);
}
        
function removeOptionsStair(list, exclude_floor) {
        setOptions(list, exclude_floor, 'stair', false);
}


//////////////////////////////////////////////////////////////////////////////////////////////////
// FUNZIONI PER ESTRARRE I DATI DAI CAMPI

function getRFID() {
        
        checkbox = document.getElementById(createCheckBoxId("RFID"));
        text = document.getElementById("RFID_text");
        
        if (checkbox.checked)
                return text.value;
        return "";       
}
        
function getRoom() {
        checkbox = document.getElementById(createCheckBoxId("room"));
        nome = document.getElementById("room_name");
        link = document.getElementById("room_link");
        persone = document.getElementById("room_people");
        altro = document.getElementById("room_notes");
    
        if (checkbox.checked)
                return [nome.value, link.value, persone.value, altro.value]
        return ["", "", "", ""]; 
}
        
function getAccess() {
        var access = document.getElementById(createCheckBoxId('access')).checked;
        return access;
}

function getElevatorOrStair(value) {
        checkbox = document.getElementById(createCheckBoxId(value));
        option = document.getElementById(createOptionId(value)); 
        text = document.getElementById(createOptionNewidId(value));
        console.log("GET");
        console.log(value);
        console.log(text.value);
        if (checkbox.checked) {
                if (option.selectedIndex == 0)
                        return text.value;
                else
                        return option.value;
        }
        return "";
}
        
function getElevator() {
        return getElevatorOrStair("elevator");
}
        
function getStair() {
        return getElevatorOrStair("stair");
}

/////////////////////////////////////////////////////////////////////////////////////////////////////
// FUNZIONI PER ASTRARRE LA CREAZIONE DI ID HTML E L'ABILITAZIONE DEI PULSANTI DALLE ALTRE FUNZIONI

// funzione per abilitare/disabilitare il pulsante di salvataggio       
function disableSaveButton(value) {
        document.getElementById("saveMarker").disabled = value;
} 
        
// funzione per convertire il salvataggio in Edit       
function toEditButton() {
        disableSaveButton(false);
        document.getElementById("saveMarker").text = "Edit";
        hideDeleteButton(false);
}   
        
// funzione per convertire il salvataggio in save
function toSaveButton() {
        disableSaveButton(true);
        document.getElementById("saveMarker").text = "Save";
        hideDeleteButton(true);
}
        
// funzione per mostrare o disabilitare il pulsante DELETE
function hideDeleteButton(value) {
        document.getElementById("deleteMarker").disabled = value;
        document.getElementById("deleteMarker").hidden = value; 
}    

// funzione per la costruzione dell'id dei campi input in base al valore passato
function createInputId(name) {
        return name + "_input";
}

// funzione per la costruzione dell'id dei checkBox in base al valore passato
function createCheckBoxId(name) {
        return "marker_" + name;
}

// funzione per la costruzione dell'id delle Options in base al valore passato
function createOptionId(name) {
        return name + "_options";
}

// funzione per la costruzione dell'id dei campi testo delle Options in base al valore passato
function createOptionNewidId(name) {
        return name + "_new_id";
}

