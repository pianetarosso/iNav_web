// gestione della form di input
        function form() {
              
                var loading = document.getElementById("loading");
                
                var operation = document.getElementById("operation_type");
                
                var floor_list = document.getElementById("floor_number");
                
                var commands = new showHide("commands_input");
                
                var marker = new showHide("marker_input");
               
                var marker_d = new marker_data();
                             
                var save_buttons = new saveButtons(marker_d);                         
                this.save_buttons = save_buttons;       
                
                // funzione chiamata al termine del caricamento della JApplet
                this.loaded = loaded;
                function loaded() {
                        
                        // nascondo il "loading..."
                        loading.hidden = true;
                        
                        // abilito il campo "operazioni" e imposto la funzione chiamata
                        operation.disabled = false;
                        operation.selectedIndex = 0;
                        operation.onchange = function() {
                                mapGenerator.setOperation(operation.value);
                        };
                        
                        // abilito e popolo il campo "numero di piani"
                        floor_list.disabled = false;
                        var first = true;
                        for (f in floors) {
                                var newoption = document.createElement('option');
                                newoption.value = floors[f];
                                newoption.text = 'Floor: ' + floors[f];
                                if (first) {
                                        newoption.selected = "selected";  
                                        selected_floor = floors[f];
                                }    
                                first = false;
                                floor_list.appendChild(newoption);        
                        }
                        // aggiungo l'ascoltatore per l'operazione
                        floor_list.onchange = function() {
                                mapGenerator.setFloor(floor_list.value);
                                selected_floor = floor_list.value;
                        }
                        
                        commands.show(); 
                }
                
                //////////////////////////////////////
                // NUOVO MARKER
                
                function cancel_new_marker() {
                
                        this.go = go;
                        function go() {
                                cancelNewMarker();
                                marker_d.clear();
                                marker.hide();
                        }         
                }
               
                function save_new_marker() {
                
                        this.go = go;
                        function go() {
                        
                                if (marker_d.isValid()) {
                                
                                        // recupero i dati
                                        var data = marker_d.value();
                                        
                                        // 
                                        var rfid = '';
                                        if (data['RFID'] != undefined)
                                                rfid = data['RFID'];
                                                
                                        var access = (data['access'] != undefined);
                                               
                                        var room_name = '';
                                        var room_people = '';
                                        var room_link = '';
                                        var room_other = ''; 
                                        // abbiamo una stanza per le mani
                                        if (data['room'] != undefined) {
                                                room = data['room'];
                                                room_name = room[0];
                                                room_link = room[1];
                                                room_people = room[2];
                                                room_other =  room[3];
                                        }
                                        
                                        // AGGIUNGERE SUPPORTO ASCENSORI E SCALE///
                                        var lift = '';
                                        if (data['lift'] != undefined) {
                                                lift = data['lift'];
                                        }
                                        
                                        var stair = '';
                                        if (data['stair'] != undefined) {
                                                stair = data['stair'];
                                        }
                                        /////////////////////////////////////////////
                                        
                                        saveNewMarker(rfid, access, lift, stair, room_name, room_people, room_link, room_other);
                                        marker_d.clear();
                                        marker.hide();
                                }
                                else
                                        alert("System error! Try to reload the page...");
                        }
                }
                ////////////////////////////////////////
                
                // EDIT MARKER
                
                
                this.save_edit_marker = save_edit_marker;
                function save_edit_marker() {
                
                        this.go = go;
                        function go() {
                        
                                if (marker_d.isValid()) {
                                
                                        // recupero i dati
                                        var data = marker_d.value();
                                        
                                        // 
                                        var rfid = '';
                                        if (data['RFID'] != undefined)
                                                rfid = data['RFID'];
                                                
                                        var access = (data['access'] != undefined);
                                               
                                        var room_name = '';
                                        var room_people = '';
                                        var room_link = '';
                                        var room_other = ''; 
                                        // abbiamo una stanza per le mani
                                        if (data['room'] != undefined) {
                                                room = data['room'];
                                                room_name = room[0];
                                                room_link = room[1];
                                                room_people = room[2];
                                                room_other =  room[3];
                                        }
                                        
                                        // AGGIUNGERE SUPPORTO ASCENSORI E SCALE///
                                        var lift = '';
                                        if (data['lift'] != undefined) {
                                                lift = data['lift'];
                                        }
                                        
                                        var stair = '';
                                        if (data['stair'] != undefined) {
                                                stair = data['stair'];
                                        }
                                        /////////////////////////////////////////////
                                        
                                        saveEditMarker(rfid, access, lift, stair, room_name, room_people, room_link, room_other);
                                        marker_d.clear();
                                        marker.hide();
                                }
                                else
                                        alert("System error! Try to reload the page...");
                        }
                
                }
                
                this.delete_marker = delete_marker;
                function delete_marker() {
                        this.go = go;
                        function go() {
                                deleteMarker();
                                marker_d.clear();
                                marker.hide();
                        } 
                }
                
                
                   
                
                ///////////////////////////////////////
                
                
                this.edit_marker = edit_marker;
                function edit_marker(data) {
                        
                        // pulisco l'input
                        marker_d.clear();
                        
                        // mostro l'input
                        marker.show();
                        
                        // popolo i campi
                        marker.edit(data[0], data[1], data[2], data[3], data[4], data[5], data[6]);
                        
                        save_buttons.edit_marker(new save_edit_marker(), new cancel_new_marker(), new delete_marker());
                }
                
                
                this.new_marker = new_marker;
                function new_marker() {
                
                        loadControlLists();
                      
                        // pulisco l'input
                        marker_d.clear();
                        
                        // mostro l'input
                        marker.show(); 
                        
                        // mostro i pulsanti "ok" e "cancel"
                        save_buttons.new_marker(new save_new_marker(), new cancel_new_marker()); 
                }
                
                
              
        }
       
        function saveButtons(marker_d) {
        
                // CONTENITORI:
                
                // contenitore pulsanti "save", "cancel", "delete"
                var buttons = new showHide("buttons_input");
                
                // contenitore pulsanti "are you sure?", "cancel"
                var question = new showHide("question_input");
               
                //////////////////////////////////////////////////////
                
                
                // PULSANTI:
                
                // save
                var save = document.getElementById("save");
                
                // cancel
                var cancel = document.getElementById("cancel");
                
                // delete
                var deletem = document.getElementById("delete");   
                
                // "are you sure?"
                var iAmSure = document.getElementById("proceed");
                
                // "no, I'm not sure"
                var goBack = document.getElementById("go_back");     
                
                /////////////////////////////////////////////////////
                
                // variabile di controllo cel check
                var check = true;
                
                // funzione per la validazione dell'input (e abilitare il pulsante "save")
                // verifico sia che i campi siano validi, sia che siano abilitati
                this.checkIfValid = checkIfValid;
                function checkIfValid() {
                        save.disabled = !marker_d.isValid();
                        setTimeout("form.save_buttons.checkIfValid()", 1000);
                }
                
                // funzione per resettare i campi e i pulsanti
                function reset() {
                        
                        // nascondo i campi
                        buttons.hide();
                        question.hide();
                        
                        // elimino gli ascoltatori onclick sui pulsanti
                        save.onclick = '';
                        cancel.onclick = '';
                        deletem.onclick = '';
                        iAmSure.onclick = '';
                        goBack.onclick = '';
                        
                        // reimposto alcuni valori
                        save.disabled = true;
                        save.hidden = false;
                        deletem.hidden = true;
                        
                        check = false;
                }
                
                // chiamata per la cancellazione di una path
                function delete_path() {
                
                        save.hidden = true;
                        buttons.show();
                
                        
                        cancel.onclick = function() {
                                // chiamo il metodo della form per 'pulire' tutto e abilitare l'applet
                                reset();
                        }
                        
                        deletem.onclick = function() {
                                
                                buttons.hide();
                                
                                // mostro la domanda
                                question.show();
                                
                                iAmSure.onclick = function() {
                                        
                                        // chiamo il metodo della form per cancellare la path
                                        // pulisco tutto
                                        // abilito l'applet
                                        reset();
                                };
                                
                                
                                goBack.onclick = function() {
                                        
                                        // resetto tutto e abilito la japplet
                                        reset();  
                                };
                        
                        };
                
                }
                
                
                
                // chiamata nella creazione di un nuovo marker
                // cancel => funzione di cancellazione
                // save => funzione salvataggio
                this.new_marker = new_marker;
                function new_marker(save_f, cancel_f) {
                        
                        buttons.show();
                        checkIfValid();
                        
                        cancel.onclick = function() {
                                cancel_f.go();
                                reset();
                        }
                        
                        save.onclick = function() {
                                save_f.go();
                                reset();
                        }
                }
                
                // chiamata per l'editing di un marker
                function edit_marker(save_f, cancel_f, delete_f) {
                        
                        loadControlLists();
                        
                        deletem.hidden = false;
                        buttons.show();
                        
                        save.onclick = function() {
                                save_f.go();
                                reset();
                        };
                
                        cancel.onclick = function() {
                        
                                // chiamo il metodo della form per 'pulire' tutto 
                                // NON cancello il punto, ma devo abilitare di nuovo la mappa
                                cancel_f.go();
                                reset();
                        };
                        
                        deletem.onclick = function() {
                                
                                buttons.hide();
                                
                                // mostro la domanda
                                question.show();
                                
                                iAmSure.onclick = function() {
                                        
                                        // chiamo il metodo della form per cancellare un marker
                                        // pulisco tutto
                                        // abilito l'applet
                                        delete_f.go();
                                        reset();
                                };
                                
                                
                                goBack.onclick = function() {
                                        
                                        question.hide();
                                        buttons.show();
                                        
                                        iAmSure.onclick = '';
                                        goBack.onclick = '';   
                                };
                        
                        };
                
                }
        
        }
        
        function loadControlLists() {
                        // carico le liste di controllo
                        rfid_l = getRFIDList();
                        room_l = getRoomList();
                        stair_l = getStairList();
                        lift_l = getLiftList();
}  
         
