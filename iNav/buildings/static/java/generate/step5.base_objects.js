/////////////////////////////////////////////////////////////////////////////////////
// OGGETTI BASE //



////////////////////////////////////////////////////////////////////////////////////
// POINT //


// GESTORE DELLA LISTA DI PUNTI
function pointList() {

        // { id : point }
        list = {};
        
        
        // aggiungo un punto
        this.add = add;
        function add(rfid, x, y, floor_n, access, id) {
                list[id] = new point(rfid, x, y, floor_n, access, id);
                list[id].save();
        }
        
        // recupero un punto
        this.get = get;
        function get(id) {
                return list[id];
        }
        
        // aggiorno un punto
        this.update = update;
        function update(rfid, x, y, floor_n, access, id) {
                list[id].update(rfid, x, y, floor_n, access, id);
        }
        
        // cancello un punto, e sistemo anche i numeri incrementali
        this.del = del;
        function del(id) {
        
                // cancello il div
                list[id].delete_();
                
                // cancello l'elemento dalla lista
                delete list[id];
                
                // aggiorno i numeri incrementali dei "sopravvissuti"
                var counter = 0;
                for ( l in list) {
                        list[l].changeDivNumber(counter);
                        counter++;
                }
        }
        
        // carico tutti i div presenti
        this.load = load
        function load() {
                
                var n = new point().getTotal();
                
                if (n == null)
                        return;
                
                for (var i=0; i < n; i++) {
                
                        // carico il div corrispondente
                        p = new point().load(i);
                        list[p.id] = p;
                        
                        return list;
                }
        
        }
}        
        
        
// OGGETTO POINT 
function point(rfid, x, y, floor_n, access, id) {


        var self = this;
        
        // variabili
        this.rfid = rfid;
        this.x = x;
        this.y = y;
        this.floor_n = floor_n;
        this.access = access;
        this.id = id;
        
        
        // contenitore dei punti
        var point_div = document.getElementById('points');
        var input_point = point_div.getElementsByTagName('input');
        
        
        // contenitore dei dati
        var data = [rfid, x, y, floor_n, access, id];
        
        // contenitore dei div
        var div = {     
                        // numero totale di form di punti
                        'TOTAL'         : null,
        
                        // div di input
                        'RFID'          : null,
                        'x'             : null,
                        'y'             : null,
                        'piano'         : null,
                        'ingresso'      : null,
                        'id'            : null
                  }
        this.div=div;
        
        // carico gli elementi dalla form
        load_divs();
        function load_divs() {
        
                // scansiono tutti gli input
                for (ip in input_point) {
                        
                        var element = input_point[ip];
                        
                        // verifico se c'è corrispondenza tra gli elementi della pagina e quelli del dizionario
                        for (d in div)          
                                if (element.name.match(d) != null)
                                        div[d] = element;
                        
                        // verifico se posso terminare la scansione
                        var test = true;
                        for (d in div)
                                test = test && (div[d] != null);
                        
                        if (test)
                                break;         
                }
        }
        
        // funzione per resituire il numero di form totali
        // se la prima form è vuota restituisce NULL
        this.getTotal = getTotal
        function getTotal() {
        
                var n = parseInt(div['TOTAL'].value);
                
                if (div['RFID'].value == '')
                        return null;
                        
                return n;  
        }
        
        
        // funzione per il salvataggio dei dati
        this.save = save;
        function save() {
                
                // contatore per navigare l'array dei dati
                var counter = 0;
              
                // qui siamo nel caso in cui la prima form NON è vuota, 
                // quindi creo delle nuove form e le 'appendo' al div
                if (div['RFID'].value != '')   {    
                        for (d in div)      
                                if (d != 'TOTAL') {
                                        
                                        // costruisco un nuovo div con i nuovi parametri
                                        var new_div = document.createElement('input');
                                        new_div.type = 'hidden';
                                        new_div.name = div[d].name.replace('0', div['TOTAL'].value);
                                        new_div.id = div[d].id.replace('0', div['TOTAL'].value);
                                        new_div.value = data[counter];
                                        
                                        counter++;
                                        
                                        // lo 'attacco' al resto della form
                                        point_div.appendChild(new_div);
                                        
                                        // sostituisco il div nel dizionario
                                        div[d] = new_div;
                                }
                                
                        // incremento il total count
                        div['TOTAL'].value = parseInt(div['TOTAL'].value) + 1;                
                }
                // in questo caso riempiamo la prima form
                else 
                        for (d in div)             
                                if (d != 'TOTAL') {
                                        div[d].value = data[counter];
                                        counter++;
                                }
        }
       
        // funzione per la cancellazione dei dati
        this.delete_ = delete_
        function delete_() {
        
                if (parseInt(div['TOTAL'].value) > 1) {
                        // cancello l'elemento dalla form
                        for (d in div) 
                                if (d != 'TOTAL')
                                        div[d].remove();
                        
                        // decremento il total count
                        div['TOTAL'].value = parseInt(div['TOTAL'].value) - 1;
                }
                
                // DEVE restare almeno una form vuota, quindi cancello solo i dati dell'ultima
                else 
                        for (d in div) 
                                div[d].value = '';   
        }
        
        
        
        // funzione per l'update
        this.update = update;
        function update (rfid, x, y, floor_n, access, id) {

                // aggiorno le variabili e gli oggetti
                self.rfid = rfid;
                self.x = x;
                self.y = y;
                self.floor_n = floor_n;
                self.access = access;
                self.id = id;
                
                self.data = [self.rfid, self.x, self.y, self.floor_n, self.access, self.id];
                
                
                // aggiorno i dati nella form
                var counter = 0; 
                for (d in div)             
                        if (d != 'TOTAL') {
                                div[d].value = self.data[counter];
                                counter++;
                        }           
        }
        
        // funzione per modificare il numero identificativo del div
        this.changeDivNumber = changeDivNumber
        function changeDivNumber(n) {
                
                for (d in div) 
                        if (d != 'TOTAL') {
                                
                                // trovo il 'vecchio' numero
                                var old = div[d].id.split('-')[1];
                                
                                // lo rimpiazzo
                                div[d].id = div[d].id.replace(old, n);
                                div[d].name = div[d].name.replace(old,n);
                        }
        }
        
        
        // funzione per caricare il div dalla pagina dato il numero, restituisce sé stesso
        this.load = load;
        function load(n) {
                
                var counter = 0;
                
                for (d in div) 
                        if (d != 'TOTAL') {
                                
                                // creo il nuovo identificativo
                                var new_id = div[d].id.replace('0', n);
                                
                                var new_div = document.getElementById(new_id);
                                
                                // cambio il riferimento al div
                                div[d] = new_div;
                                
                                // aggiorno i dati
                                switch (counter) {
                                        
                                        case(0):
                                                self.rfid = new_div.value;
                                                break;
                                        case(1):
                                                self.x = parseInt(new_div.value);
                                                break;
                                        case(2):
                                                self.y = parseInt(new_div.value);
                                                break;        
                                        case(3):
                                                self.floor_n = parseInt(new_div.value);
                                                break;       
                                        case(4):
                                                self.access = (new_div.value == 'true');
                                                break;
                                        case(5):
                                                self.id = parseInt(new_div.value);
                                                break;
                                }
                                counter++;
                        }
                        
                self.data = [self.rfid, self.x, self.y, self.floor_n, self.access, self.id];
                return self;                
        }        
}

// END POINT
//////////////////////////////////////////////////////////////////////////////////////////////      


/////////////////////////////////////////////////////////////////////////////////////////////
// ROOM //



// GESTORE DELLA LISTA DI STANZE
function roomList() {

        // { point_id : room }
        list = {};
        
        
        // aggiungo una stanza
        this.add = add;
        function add(point_id, nome, link, people, notes) {
                list[point_id] = new room_(point_id, nome, link, people, notes);
                list[point_id].save();
        }
        
        // recupero una stanza
        this.get = get;
        function get(id) {
                return list[id];
        }
        
        // aggiorno una stanza
        this.update = update;
        function update(point_id, nome, link, people, notes) {
                list[point_id].update(point_id, nome, link, people, notes);
        }
        
        // cancello una stanza, e sistemo anche i numeri incrementali
        this.del = del;
        function del(point_id) {
        
                // cancello il div
                list[point_id].delete_();
                
                // cancello l'elemento dalla lista
                delete list[point_id];
                
                // aggiorno i numeri incrementali dei "sopravvissuti"
                var counter = 0;
                for ( l in list) {
                        list[l].changeDivNumber(counter);
                        counter++;
                }
        }
        
        // carico tutti i div presenti
        this.load = load
        function load() {
                
                var n = new room_().getTotal();
                
                if (n == null)
                        return;
                
                for (var i=0; i < n; i++) {
                
                        // carico il div corrispondente
                        p = new room_().load(i);
                        list[p.point_id] = p;
                        
                        return list;
                }
        
        }
}        
      
        
// ROOM 
function room_(point_id, nome, link, people, notes) {


        var self = this;
        
        // variabili
        this.point_id = point_id;
        this.nome = nome;
        this.link = link;
        this.people = people;
        this.notes = notes;
        
        
        // contenitore dei punti
        var room_div = document.getElementById('rooms');
        var input_room = room_div.getElementsByTagName('input');
        
        
        // contenitore dei dati
        var data = [point_id, nome, link, people, notes];
        
        // contenitore dei div
        var div = {     
                        // numero totale di form di punti
                        'TOTAL'         : null,
        
                        // div di input
                        'punto'         : null,
                        'nome_stanza'   : null,
                        'link'          : null,
                        'persone'       : null,
                        'altro'         : null
                  }
        this.div=div;
        
        // carico gli elementi dalla form
        load_divs();
        function load_divs() {
        
                // scansiono tutti gli input
                for (ir in input_room) {
                        
                        var element = input_room[ir];
                        
                        // verifico se c'è corrispondenza tra gli elementi della pagina e quelli del dizionario
                        for (d in div)          
                                if (element.name.match(d) != null)
                                        div[d] = element;
                        
                        // verifico se posso terminare la scansione
                        var test = true;
                        for (d in div)
                                test = test && (div[d] != null);
                        
                        if (test)
                                break;         
                }
        }
        
        // funzione per resituire il numero di form totali
        // se la prima form è vuota restituisce NULL
        this.getTotal = getTotal
        function getTotal() {
        
                var n = parseInt(div['TOTAL'].value);
                
                if (div['punto'].value == '')
                        return null;
                        
                return n;  
        }
        
        
        // funzione per il salvataggio dei dati
        this.save = save;
        function save() {
                
                // contatore per navigare l'arralink dei dati
                var counter = 0;
              
                // qui siamo nel caso in cui la prima form NON è vuota, 
                // quindi creo delle nuove form e le 'appendo' al div
                if (div['punto'].value != '')   {    
                        for (d in div)      
                                if (d != 'TOTAL') {
                                        
                                        // costruisco un nuovo div con i nuovi parametri
                                        var new_div = document.createElement('input');
                                        new_div.type = 'hidden';
                                        new_div.name = div[d].name.replace('0', div['TOTAL'].value);
                                        new_div.id = div[d].id.replace('0', div['TOTAL'].value);
                                        new_div.value = data[counter];
                                        
                                        counter++;
                                        
                                        // lo 'attacco' al resto della form
                                        room_div.appendChild(new_div);
                                        
                                        // sostituisco il div nel dizionario
                                        div[d] = new_div;
                                }
                                
                        // incremento il total count
                        div['TOTAL'].value = parseInt(div['TOTAL'].value) + 1;                
                }
                // in questo caso riempiamo la prima form
                else 
                        for (d in div)             
                                if (d != 'TOTAL') {
                                        div[d].value = data[counter];
                                        counter++;
                                }
        }
       
        // funzione per la cancellazione dei dati
        this.delete_ = delete_
        function delete_() {
        
                if (parseInt(div['TOTAL'].value) > 1) {
                        // cancello l'elemento dalla form
                        for (d in div) 
                                if (d != 'TOTAL')
                                        div[d].remove();
                        
                        // decremento il total count
                        div['TOTAL'].value = parseInt(div['TOTAL'].value) - 1;
                }
                
                // DEVE restare almeno una form vuota, quindi cancello solo i dati dell'ultima
                else 
                        for (d in div) 
                                div[d].value = '';   
        }
        
        
        
        // funzione per l'update
        this.update = update;
        function update (point_id, nome, link, people, notes) {

                // aggiorno le variabili e gli oggetti
                self.point_id = point_id;
                self.nome = nome;
                self.link = link;
                self.people = people;
                self.notes = notes;
                
                self.data = [self.point_id, self.nome, self.link, self.people, self.notes];
                

                // aggiorno i dati nella form
                var counter = 0; 
                for (d in div)             
                        if (d != 'TOTAL') {
                                div[d].value = self.data[counter];
                                counter++;
                        }           
        }
        
        // funzione per modificare il numero identificativo del div
        this.changeDivNumber = changeDivNumber
        function changeDivNumber(n) {
                
                for (d in div) 
                        if (d != 'TOTAL') {
                                
                                // trovo il 'vecchio' numero
                                var old = div[d].id.split('-')[1];
                                
                                // lo rimpiazzo
                                div[d].id = div[d].id.replace(old, n);
                                div[d].name = div[d].name.replace(old,n);
                        }
        }
        
        
        // funzione per caricare il div dalla pagina dato il numero, restituisce sé stesso
        this.load = load;
        function load(n) {
                
                var counter = 0;
                
                for (d in div) 
                        if (d != 'TOTAL') {
                                
                                // creo il nuovo identificativo
                                var new_id = div[d].id.replace('0', n);
                                
                                var new_div = document.getElementByIdId(new_id);
                                
                                // cambio il riferimento al div
                                div[d] = new_div;
                                
                                // aggiorno i dati
                                switch (counter) {
                                        
                                        case(0):
                                                self.point_id = parseInt(new_div.value);
                                                break;
                                        case(1):
                                                self.nome = new_div.value;
                                                break;
                                        case(2):
                                                self.link = new_div.value;
                                                break;        
                                        case(3):
                                                self.people = new_div.value;
                                                break;       
                                        case(4):
                                                self.notes = new_div.value;
                                                break;
                                }
                                counter++;
                        }
                        
                self.data = [self.point_id, self.nome, self.link, self.people, self.notes];
                return self;                
        }       
}




// END ROOM
////////////////////////////////////////////////////////////////////////////////////////////////




/////////////////////////////////////////////////////////////////////////////////////////////
// PATH //



// OGGETTO PATH 
function path(point_a, point_b, lift, stair) {


        var self = this;
        
        // variabili
        this.point_a = point_a;
        this.point_b = point_b;
        this.lift = lift;
        this.stair = stair;
        
        
        
        // contenitore delle path
        var path_div = document.getElementById('paths');
        var input_path = path_div.getElementsByTagName('input');
        
        
        // contenitore dei dati
        var data = [point_a, point_b, lift, stair];
        
        // contenitore dei div
        var div = {     
                        // numero totale di form di punti
                        'TOTAL'         : null,
        
                        // div di input
                        'temp_a'          : null,
                        'temp_b'             : null,
                        'ascensore'             : null,
                        'scala'         : null
                  }
        this.div=div;
        
        // carico gli elementi dalla form
        load_divs();
        function load_divs() {
        
                // scansiono tutti gli input
                for (ip in input_path) {
                        
                        var element = input_path[ip];
                        
                        // verifico se c'è corrispondenza tra gli elementi della pagina e quelli del dizionario
                        for (d in div)          
                                if (element.name.match(d) != null)
                                        div[d] = element;
                        
                        // verifico se posso terminare la scansione
                        var test = true;
                        for (d in div)
                                test = test && (div[d] != null);
                        
                        if (test)
                                break;         
                }
        }
        
        // funzione per resituire il numero di form totali
        // se la prima form è vuota restituisce NULL
        this.getTotal = getTotal
        function getTotal() {
        
                var n = parseInt(div['TOTAL'].value);
                
                if (div['temp_a'].value == '')
                        return null;
                        
                return n;  
        }
        
        
        // funzione per il salvataggio dei dati
        this.save = save;
        function save() {
                
                // contatore per navigare l'arralift dei dati
                var counter = 0;
              
                // qui siamo nel caso in cui la prima form NON è vuota, 
                // quindi creo delle nuove form e le 'appendo' al div
                if (div['temp_a'].value != '')   {    
                        for (d in div)      
                                if (d != 'TOTAL') {
                                        
                                        // costruisco un nuovo div con i nuovi parametri
                                        var new_div = document.createElement('input');
                                        new_div.type = 'hidden';
                                        new_div.name = div[d].name.replace('0', div['TOTAL'].value);
                                        new_div.id = div[d].id.replace('0', div['TOTAL'].value);
                                        new_div.value = data[counter];
                                        
                                        counter++;
                                        
                                        // lo 'attacco' al resto della form
                                        path_div.appendChild(new_div);
                                        
                                        // sostituisco il div nel dizionario
                                        div[d] = new_div;
                                }
                                
                        // incremento il total count
                        div['TOTAL'].value = parseInt(div['TOTAL'].value) + 1;                
                }
                // in questo caso riempiamo la prima form
                else 
                        for (d in div)             
                                if (d != 'TOTAL') {
                                        div[d].value = data[counter];
                                        counter++;
                                }
        }
       
        // funzione per la cancellazione dei dati
        this.delete_ = delete_
        function delete_() {
        
                if (parseInt(div['TOTAL'].value) > 1) {
                        // cancello l'elemento dalla form
                        for (d in div) 
                                if (d != 'TOTAL')
                                        div[d].remove();
                        
                        // decremento il total count
                        div['TOTAL'].value = parseInt(div['TOTAL'].value) - 1;
                }
                
                // DEVE restare almeno una form vuota, quindi cancello solo i dati dell'ultima
                else 
                        for (d in div) 
                                div[d].value = '';   
        }
        
        
        
        // funzione per l'update
        this.update = update;
        function update (point_a, point_b, lift, stair) {

                // aggiorno le variabili e gli oggetti
                self.point_a = point_a;
                self.point_b = point_b;
                self.lift = lift;
                self.stair = stair;
                
                self.data = [self.point_a, self.point_b, self.lift, self.stair];
                
                
                // aggiorno i dati nella form
                var counter = 0; 
                for (d in div)             
                        if (d != 'TOTAL') {
                                div[d].value = self.data[counter];
                                counter++;
                        }           
        }
        
        // funzione per modificare il numero identificativo del div
        this.changeDivNumber = changeDivNumber
        function changeDivNumber(n) {
                
                for (d in div) 
                        if (d != 'TOTAL') {
                                
                                // trovo il 'vecchio' numero
                                var old = div[d].id.split('-')[1];
                                
                                // lo rimpiazzo
                                div[d].id = div[d].id.replace(old, n);
                                div[d].name = div[d].name.replace(old,n);
                        }
        }
        
        
        // funzione per caricare il div dalla pagina dato il numero, restituisce sé stesso
        this.load = load;
        function load(n) {
                
                var counter = 0;
                
                for (d in div) 
                        if (d != 'TOTAL') {
                                
                                // creo il nuovo identificativo
                                var new_id = div[d].id.replace('0', n);
                                
                                var new_div = document.getElementById(new_id);
                                
                                // cambio il riferimento al div
                                div[d] = new_div;
                                
                                // aggiorno i dati
                                switch (counter) {
                                        
                                        case(0):
                                                self.point_a = parseInt(new_div.value);
                                                break;
                                        case(1):
                                                self.point_b = parseInt(new_div.value);
                                                break;
                                        case(2):
                                                self.lift = new_div.value;
                                                break;        
                                        case(3):
                                                self.stair = new_div.value;
                                                break;       
                                }
                                counter++;
                        }
                        
                self.data = [self.point_a, self.point_b, self.lift, self.stair];
                return self;                
        }        
}
 




// END PATH 
////////////////////////////////////////////////////////////////////////////////////////////





