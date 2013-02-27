// STEP 3, GENERAZIONE DEI PUNTI E LINEE DELLA MAPPA
// FUNZIONI PER GLI EFFETTI GRAFICI

// funzione per l'animazione alla comparsa/scomparsa delle varie liste
// la variabile "displayed_list" viene riempita man mano
var displayed_list = {};
var busy = false;
function resize(name_t) {

        if (busy)
                setTimeout(function() {resize(name_t); },500);
        else {
                busy = true;
               
                name = createInputId(name_t);
                
                heigth = $("#"+name).height(); 
                console.log(heigth);
                console.log(name);
                console.log($("#"+name));
                
                if (displayed_list[name] == null)
                        displayed_list[name] = false;

                if (displayed_list[name]) {
                        $("#"+name).slideToggle();
                        window.top.resizeIframe(-1 * heigth);
                        displayed_list[name] = false;
                        clearChildren(document.getElementById(name));
                }
                else {
                        console.log(displayed_list);
                        window.top.resizeIframe(heigth);
                        $("#"+name).slideToggle();
                        displayed_list[name] = true;
                }
                
                setTimeout(function() {busy = false;},500);
        }
}
        
// funzione per disabilitare i checkBox esclusivi alla selezione di uno di questi
checkBox = ['room', 'elevator', 'stair', 'access']
function disableCheckBoxes(value_t) {
        
        value = createCheckBoxId(value_t);
        boolean = document.getElementById(value).checked;

        for(var i in checkBox) {
                if (checkBox[i] != value_t)
                        document.getElementById(createCheckBoxId(checkBox[i])).disabled = boolean;
        }
}



// "Pulizia" dei valori delle form, quando queste vengono collassate
function clearChildren(element) {
        
        for (var i = 0; i < element.childNodes.length; i++) {
                var e = element.childNodes[i];
                        
                if (e.tagName) 
                        switch (e.tagName.toLowerCase()) {
                                case 'input':
                                        switch (e.type) {
                                                case "radio":
                                                
                                                case "checkbox": 
                                                        if (e.checked) 
                                                                e.click(); 
                                                        break;
                                                        
                                                case "button":
                                                
                                                case "submit":
                                                
                                                case "image": 
                                                        break;
                                                        
                                                default: 
                                                        e.value = ''; 
                                                        e.style.background = "";
                                                        break;
                                        }
                                        break;
                                        
                                case 'select': 
                                        if (e.name != "commands") {
                                                e.selectedIndex = 0; 
                                                enableNewId(e.name);
                                        } 
                                        break;
                                        
                                case 'textarea': 
                                        e.innerHTML = ''; 
                                        e.style.background = "";
                                        break;
                                        
                                default: clearChildren(e);
                        }
        }
        // disabilito anche il pulsante di salvataggio
        disableSaveButton(true);
}


