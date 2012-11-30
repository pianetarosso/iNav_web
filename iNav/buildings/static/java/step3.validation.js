/////////////////////////////////////////////////////////////////////////////////////////////////////
// FUNZIONI PER LA VALIDAZIONE DEI CAMPI DI INPUT NELLO STEP3

        // dizionario per contenere i campi validi
        var valid_input = {};
        function validateFields(input) {
                var test = true;
                if (input.name == "RFID") {
                        for (var i in markers) 
                                test = test && (input.value != markers[i].RFID);
                } 
                        
                if (input.name == "room") {
                        for (var i in markers) 
                                test = test && (input.value != markers[i].nome_stanza);
                } 
                                
                if ((!input.validity) || (input.value == "") || (!test)) {
                        input.style.background = "red";
                        valid_input[input.name] = false;
                }
                else {
                        input.style.background = "";
                        valid_input[input.name] = true;
                }
                
                validateSaveButton();
        }

        // fa i test per abilitare o no il savebutton
        function validateSaveButton() {
                var test = true;
                var counter = 0;
                
                for (var p in valid_input) {
                        test = test && valid_input[p];
                        counter++
                }
                test = test && (counter > 0);
                disableSaveButton(!test);
        }
        
        // funzione specifica per la gestione della validazione dell'ingresso
        function validateAccess(input) {
                valid_input[input.name] = input.checked;
                validateSaveButton();
        }
        
        // funzione chiamata quando viene eliminata una form
        function removeValidation(input, value) {
                if (!input.checked)
                        delete(valid_input[value]);
                validateSaveButton();
        }

        // nelle option, alla voce Ascensore o Scala,
        // abilito o disabilito il campo "new_id" a seconda del valore selezionato
        // nel menu a tendina (aggiunta validazione)
        function enableNewId(value) {
                
                test = document.getElementById(createOptionId(value)).selectedIndex != 0;
                if (test) {
                        document.getElementById(createOptionNewidId(value)).value = "";
                        document.getElementById(createOptionNewidId(value)).style.background = "";
                        valid_input[value] = true;
                }
                else
                        valid_input[value] = false;
                document.getElementById(createOptionNewidId(value)).disabled = test;
                
                validateSaveButton();
        }
        
        // test di validazione per i campi immissione in Ascensore/Scala
        function testIfText(input, value) {
                if (input != null) {
                        duplicates_on_same_floor = (!testDuplicates(input.id, input.value));
                        if ((input.value != "") && duplicates_on_same_floor)
                                input.style.background = "";
                        else
                                input.style.background = "red"; 
                        valid_input[value] = (input.value != "") && duplicates_on_same_floor;
                        validateSaveButton();
                }
        }
        
        // funzione per lanciare la validazione sui dati ogni volta che viene mostrata una form
        function verify(id) {
                document.getElementById(id).oninput();
        }
