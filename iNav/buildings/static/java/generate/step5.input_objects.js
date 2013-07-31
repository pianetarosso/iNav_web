////////////////////////////////////////////////////////////////////////////////////////////
// OGGETTI BASE DELLA FORM


// oggetto RFID ///////////////////////////////////////////////
function manageRFID() {
        
        var checkBox = document.getElementById("marker_RFID");
        
        var text = document.getElementById("RFID_text");
        var s_text = new showHide("RFID_input");
        
        // indica la validità del campo
        var isvalid = false;
        
        // usato se si è in modalità editing. 
        // indica che questo campo non è da verificare per la validità
        var esclude = undefined;
        
        
        
        // inizializzo l'oggetto
        initialize();
        function initialize() {
                
                // funzione per mostare o nascondere il campo text
                checkBox.onchange = function() {
                        if (checkBox.checked)  
                                s_text.show(); 
                        else 
                                clear();        
                           
                        validateText();
                }
                
                text.oninput = function() {
                        validateText();
                }
         }
         
         // validazione del testo dell'RFID
         function validateText() {
                var value = text.value;
                
                isvalid = (esclude == value) || ((value != '') && (rfid_l.indexOf(value) == -1) && (value.match(/\S/) != null));
                
                if (isvalid) 
                        text.style.background = "";
                else
                        text.style.background = "red";
                
         }
         
         
         // funzione per resettare l'RFID allo stato iniziale
         this.clear = clear;
         function clear() {
                checkBox.checked = false;
                text.value = '';
                esclude = undefined;
                s_text.hide();
                validateText();
         }
        
        // restituisce se il valore dell'RFID è valido o meno
        this.isValid = isValid;
        function isValid() {
                  return !checkBox.checked || isvalid;
        }
        
        // resituisce se l'oggetto è usato o no
        this.isChecked = isChecked;
        function isChecked() {
                return checkBox.checked;
        }
        
        // recupero il valore dell'RFID
        this.value = value;
        function value() {
                return text.value;
        }
        
        // metodo per riempire il campo
        this.edit = edit;
        function edit(value) {
        
                if (value != '') {
                        checkBox.checked = true;
                        s_text.show();
                        text.value = value;
                        esclude = value;
                        
                        validateText();
                }
        }
}


// oggetto ROOM ///////////////////////////////////////////////////////
function manageRoom() {
        
        var checkbox = document.getElementById("marker_room");
        
        var name = document.getElementById("room_name");
        
        var link = document.getElementById("room_link");
        
        var people = document.getElementById("room_people");
        
        var note = document.getElementById("room_notes");
        
        var container = new showHide("room_input");
        
        var isvalid = false;
        
        var esclude = undefined;
        
        
        this.initialize = initialize;
        function initialize(access, lift_o, stair_o) {
        
                checkbox.onchange = function() {
                
                        // abilito / disabilito gli altri checkbox
                        access.disabled = checkbox.checked;
                        lift_o.disable(checkbox.checked);
                        stair_o.disable(checkbox.checked);
                        
                        validate();
                        
                        // mostro / nascondo il contenitore
                        if (checkbox.checked)
                                container.show();
                        else
                                clear();
                }
                
                // verifico che il nome sia unico
                name.oninput = function() {
                        validate();
                }
        }
        
        // validazione dell'input
        function validate() {
        
                var value = name.value;
                
                isvalid = (value == esclude) || ((room_l.indexOf(value) == -1) && (value != '') && (value.match(/\S/) != null));
                
                if (isvalid) 
                        name.style.background = "";
                else
                        name.style.background = "red";            
        }
        
        // restituisco la validazione
        this.isValid = isValid;
        function isValid() {
                return !checkbox.checked || isvalid;
        }
        
        // disabilito il checkbox
        this.disable = disable;
        function disable(v) {
                checkbox.disabled = v;
        }
        
        // resituisco se l'oggetto è utilizzato
        this.isChecked = isChecked;
        function isChecked() {
                return checkbox.checked;
        }
        
        // metodo per pulire l'input
        this.clear = clear;
        function clear() {
                checkbox.disabled = false;
                checkbox.checked = false;
                name.value = '';
                link.value = '';
                people.value = '';
                note.value = '';
                
                esclude = undefined;
                
                validate();
               
                container.hide();
        }
        
        // metodo per restituire i valori
        this.value = value;
        function value() {
                return [name.value, link.value, people.value, note.value];
        }
        
        // metodo per riempire il campo
        this.edit = edit;
        function edit(nome, link, people, note) {
                
                if (nome != '') {
                        checkbox.checked = true;
                        name.value = nome;
                        link.value = link;
                        people.value = people;
                        note.value = notes;
                        
                        esclude = nome;
                        
                        validate();
                }
        }
}

// END OGGETTI BASE DELLA FORM
///////////////////////////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////////////////////////////////
// OGGETTI COMPLESSI

// oggetto comune per SCALE e ASCENSORI
function manageChangeFloor(checkbox_id, text_id, list_id, container_id, id_lista) {
                
        var checkbox = document.getElementById(checkbox_id);
        
        var text = document.getElementById(text_id);
        
        var list = document.getElementById(list_id);
        
        var container = new showHide(container_id);
        
        var lista_controllo;
        
        var esclude = undefined;
        
        var isvalid = false;
        
        
        function lista_controllo() {
                if (id_lista == 'stair')
                        return stair_l;
                else
                        return lift_l;
        }
        
        this.initialize = initialize;
        function initialize(access, b, c) {
             
                checkbox.onchange = function() {
                
                        
                        // abilito / disabilito gli altri checkbox
                        access.disabled = checkbox.checked;
                        b.disable(checkbox.checked);
                        c.disable(checkbox.checked);
                        
                        validate();
                        
                        // creo la lista di options da mostrare
                        buildList();
                        
                        // aggiungo l'onchange alla lista
                        list.onchange = function () {
                                
                                text.value = '';
                                text.disabled = (list.selectedIndex != 0); 
                                
                                validate();
                        }
                        
                        // mostro / nascondo il contenitore
                        if (checkbox.checked)
                                container.show();
                        else 
                                clear();
                                
                                
                }
                
                // verifico che il nome sia corretto
                text.oninput = function() {
                        validate();
                }
        }
        
        // genero dinamicamente la lista di scelte
        function buildList() {
                for(var l in lista_controllo()) {
                
                        // non considero il piano da escludere
                        if (l != selected_floor) {
                                array = lista_controllo()[l];  
                                for (a in array) {
                                        
                                        var newoption = document.createElement('option');
                                        newoption.value = array[a];
                                        newoption.text = array[a];
                                        list.appendChild(newoption);
                                } 
                        }
                }
        }
        
        
        // validazione dell'input
        function validate() {
        
                if (list.selectedIndex != 0)
                        value = list.value;
                else
                        value =  text.value;
                                
                        
                var array = lista_controllo()[selected_floor];
                
                if ((array.length == 0) && (list.selectedIndex == 0))
                        isvalid = (value != '') && (value.match(/\S/) != null);
                        
                else        
                        isvalid = (value == esclude) || ((array.indexOf(value) == -1) && (value != '') && (value.match(/\S/) != null));
                
                if (isvalid) 
                        text.style.background = "";
                else
                        text.style.background = "red";            
        }
        
        // restituisco la validazione
        this.isValid = isValid;
        function isValid() {
                return !checkbox.checked || isvalid;
        }
        
        // disabilito il checkbox
        this.disable = disable;
        function disable(value) {
                checkbox.disabled = value;
        }
        
        // resituisco se l'oggetto è utilizzato
        this.isChecked = isChecked;
        function isChecked() {
                return checkbox.checked;
        }
        
        // metodo per pulire l'input
        this.clear = clear;
        function clear() {
                checkbox.disabled = false;
                checkbox.checked = false;
                text.value = '';
                list.selectedIndex = 0;
                
                esclude = undefined;
                
                // elimino le options create
                var children = list.children;
                for (var i=1; i < children.length; i++)    
                        list.removeChild(children[i]);
                
                validate();
                
                container.hide();
        }
        
        // metodo per restituire i valori
        this.value = value;
        function value() {
                if (list.selectedIndex != 0)
                        return list.value;
                else
                        return text.value;
        }
        
        // metodo per riempire il campo
        this.edit = edit;
        function edit(value) {
                
                if (value != '') {
                        checkbox.checked = true;
                        text.value = value;
                        s_text.show(); 
                        esclude = value; 
                        
                        validate();      
                }
        }
}



// DATI DEL MARKER //////////////////////////////////////////////////////////////////////////
function marker_data() {
        
        var rfid = new manageRFID();
        var access = document.getElementById("marker_access");
        var room_o = new manageRoom();
        var lift_o = new manageChangeFloor("marker_elevator", "elevator_new_id", "elevator_options", "elevator_input", 'lift');
        var stair_o = new manageChangeFloor("marker_stair", "stair_new_id", "stair_options", "stair_input", 'stair');
        
        initialize();
        function initialize() {
                
                // imposto l'ascoltatore per disabilitare / abilitare gli altri checkbox della lista
                access.onchange = function() {
                
                        room_o.disable(access.checked);
                        lift_o.disable(access.checked);
                        stair_o.disable(access.checked);
                }
                
                // passo a tutti gli oggetti i riferimenti a tutti gli altri della form
                // per poter disabilitare i checkbox in caso di necessità
                room_o.initialize(access, lift_o, stair_o);
                lift_o.initialize(access, room_o, stair_o);
                stair_o.initialize(access, room_o, lift_o);
        }
        
        
        // funzione per "pulire" le parti della form
        this.clear = clear
        function clear() {
                access.checked = false;
                access.disabled = false;
                rfid.clear();
                room_o.clear();
                lift_o.clear();
                stair_o.clear();
        }
        
        // restituisce la validità
        this.isValid = isValid;
        function isValid() {
                
                // questa condizione è FALSA solo quando l'oggetto
                // è selezionato ma non è valido 
                var r = !room_o.isChecked() || room_o.isValid();
                var l = !lift_o.isChecked() || lift_o.isValid();
                var s = !stair_o.isChecked() || stair_o.isValid();
                
                return (rfid.isValid() & r & l & s ) && (access.checked || rfid.isChecked() || room_o.isChecked() || lift_o.isChecked() || stair_o.isChecked());        
        }
        
        // recupero i dati
        this.value = value
        function value() {
                
                var value = {};
                
                if (rfid.isChecked())
                        value['RFID'] = rfid.value();
                
                if (access.checked)
                        value['access'] = access.checked;
                
                if (room_o.isChecked())
                        value['room'] = room_o.value();
                
                if (lift_o.isChecked())
                        value['lift'] = lift_o.value();
                
                if (stair_o.isChecked()) 
                        value['stair'] = stair_o.value();         
                
                return value;
        }
        
        // imposto i valori dei campi per consentire l'editing
        this.edit = edit;
        function edit(RFID, access_, stair, lift, room_name, room_people, room_link, room_other) {
                rfid.edit(RFID);
                lift_o.edit(lift);
                stair_o.edit(stair);
                room_o.edit(room_name, room_link, room_people, room_other);
                
                if (access_ == "true")
                        access.click();
        }
}


// END OGGETTI COMPLESSI

/////////////////////////////////////////////////////////////////////////////////////
// OGGETTI GRAFICI

// gestione degli effetti di showing
function showHide(identifier) {
        
        var id = identifier;
        
        this.hided = hided;
        var hided = true;
        
        DELAY = 2200;
        
        // nascondo l'oggetto
        // NEXT è il successivo oggetto da mostrare / nascondere;
        this.hide = hide
        function hide(next) {
                if (hided)
                        if (next != undefined)
                                next;
                        else        
                                return;
                hided = true;
                slide(next);   
        }
        
        // mostro l'oggetto
        this.show = show;
        function show(next) {
                if (!hided)
                        if (next != undefined)
                                next;
                        else        
                                return;
                hided = false;
                slide(next);
        }
        
        function slide(next) {
                if (next != undefined) 
                        $("#" + id).slideToggle(DELAY, function() { next; });
                else 
                        $("#" + id).slideToggle(); 
        }
}

// END OGGETTI GRAFICI
////////////////////////////////////////////////////////////////////////////////////
