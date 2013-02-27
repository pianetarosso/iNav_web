
// numero massimo di piani
var MAX_FLOORS = 2;


// imposto il numero massimo di piani
function setMaxFloors(f) {
        this.MAX_FLOORS = f;
}

// funzioni comuni per la gestione della validazione
function group() {

        testFormIds();
        enableDelete();
        enableAdd();
        testFloorNumber();
}

// funzione per abilitare / disabilitare il pulsante per aggiungere edifici
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

// funzione per aumentare o diminuire il numero di form totali nel "form management"
function setTotalForms(add) {
        
        var store = document.getElementById("id_form-TOTAL_FORMS");
        var value = parseInt(store.value);
        
        if (add)
                store.value = value + 1;
        else
                store.value = value - 1;
}

// funzione per verificare che i numeri di identificazione delle form siano corretti 
// ovverosia una sequenza crescente
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

// funzione per aumentare il numero di form piani "on demand"
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

        setTotalForms(true);
        group();
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

                setTotalForms(false);
                group();
        }
}


// funzione per aggiungere ad ogni campo di input di testo un ascoltatore sull'editing
// per effettuare le validazioni
function addOnChange() {
        input = document.getElementById("form").getElementsByTagName("input");

        for (i=0; i < input.length -1; i++) {
                if (input[i].getAttribute("type") == 'text') {
                        input[i].oninput = function() {
                                testFloorNumber();
                        };
                        
                        testFloorNumber();
                }
        }
}

// funzione che ha il compito di testare il numero di piano immesso
// ovverosia verifico che ci sia, che sia un numero e che non ci siano doppioni
// in uno dei casi soprastanti disabilito il pulsante "next" e bordo in rosso il textfield
function testFloorNumber() {

        button_next = document.getElementById("next");

        input = document.getElementById("form").getElementsByTagName("input");

        test = true;

        for (var i=0; i < input.length - 1; i++) {
                if (input[i].getAttribute("type") == 'text') {
                        
                        var out = isValid(input[i]);

                        if (out)
                                input[i].style.borderColor = "";   
                        else
                                input[i].style.borderColor = "#ff0000";
                                  
                        test = test && out;
                }
        }
        button_next.disabled = !out;   
}       

// funzione per testare se l'input del piano immesso è valido: scansiono ogni volta tutti gli
// input della form
function isValid(element) {

        // piani massimo e minimo
        max = 50;
        min = -10;


        value = parseInt(element.value);

        if (isNaN(value))
                return false;

        if ((value > max) || (value < min))
                return false;

        input = document.getElementById("form").getElementsByTagName("input");

        // contatore, visto che passiamo anche lui stesso
        errors = 0;

        for (var i=0; i < input.length -1; i++) {
                if (input[i].getAttribute("type") == 'text') {
                        t_value = parseInt(input[i].value); 

                if ((!isNaN(t_value)) && (t_value == value))
                        errors++;

                if (errors > 1)
                        return false;
                }
        }
        return true;
}
