
var MAX_FLOORS = 2;

// imposto il numero massimo di piani
function setMaxFloors(f) {
        this.MAX_FLOORS = f;
}


// funzione per abilitare / disabitlitare il pulsante per aggiungere edifici
function enableAdd() {

        var form = document.getElementById("form");
        var fieldWrapper = form.getElementsByClassName('fieldWrapper');

        document.getElementById("add_floor").disabled = ((fieldWrapper.length / 2) >= MAX_FLOORS);              
}

// funzione per abilitare / disabilitare il pulsante delete
        function enableDelete() {
                var form = document.getElementById("form");
                var fieldWrapper = form.getElementsByClassName('fieldWrapper');
                
                fieldWrapper[1].getElementsByTagName("input")[1].disabled = (fieldWrapper.length < 3);
        }
        
        
        // funzione per verificare che i numeri di identificazione delle form siano corretti
        function testFormIds() {
                
                var form = document.getElementById("form");
                var fieldWrapper = form.getElementsByClassName('fieldWrapper');
                
                for (i=0; i < fieldWrapper.length; i++) {
                        
                        value = Math.floor(i / 2);
                        
                        fw = fieldWrapper[i];
                        
                        innerHTML = fw.innerHTML;
                        
                        current_id = parseInt(innerHTML.charAt(innerHTML.search(/-.-/) + 1));
                        
                        if (current_id != value) {
                        
                                // sostituisco l'id
                                id_s = innerHTML.search('id="') + 4;
                                id_f = innerHTML.substr(id_s).search('"');
                                
                                id = innerHTML.substring(id_s, id_f + id_s);
                                
                                np = document.getElementById(id);
                                
                                np.setAttribute("id", id.replace(current_id, value));
                                
                                // sostituisco il nome
                                name_s = innerHTML.search('name="') + 6;
                                name_f = innerHTML.substr(name_s).search('"');
                                
                                nome = innerHTML.substring(name_s, name_f + name_s);
                                
                                np.setAttribute("name", nome.replace(current_id, value)); 
                        }
                }
        
        }
        
        // funzione per aumentare il numero di piani "on demand"
        function addFloor() {
                var form = document.getElementById("form");
                var fieldWrapper = form.getElementsByClassName('fieldWrapper');
                
                var newID = (fieldWrapper.length / 2);
                
                for (i=0; i < 2; i++) {
                        var temp_object = fieldWrapper[i];
                        var new_object = document.createElement("div");
                        new_object.setAttribute("class", "fieldWrapper")
                        
                        new_object.innerHTML = temp_object.innerHTML.replace(/0/g, newID);
                        
                        // condizione perché il pulsante "delete" sia abilitato sempre quando si aggiunge
                        if (i == 1) 
                                new_object.getElementsByTagName("input")[1].disabled = false;
                        
                        form.appendChild(new_object)
                }
                
                testFormIds();
                enableDelete();
                enableAdd();
                addOnChange();
        }
        
        // funzione per cancellare un piano
        function deleteFloor(input) {
                
                var form = document.getElementById("form");
                var fieldWrapper = form.getElementsByClassName('fieldWrapper');
                
                if (fieldWrapper.length > 2) {
                        predecessor = input.previousElementSibling;
                        
                        input.remove();
                        predecessor.remove();
                        
                        testFormIds();
                        enableDelete();
                        enableAdd();
                }
        }
