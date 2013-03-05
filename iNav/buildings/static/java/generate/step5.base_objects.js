/////////////////////////////////////////////////////////////////////////////////////
// OOGETTI BASE //


// gestore della lista di punti
function pointList() {

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
        function update((rfid, x, y, floor_n, access, id) {
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
        
        
// POINT 
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
                
                self.data = [rfid, x, y, floor_n, access, id];
                
                
                // aggiorno i dati nella form
                var counter = 0; 
                for (d in div)             
                        if (d != 'TOTAL') {
                                div[d].value = data[counter];
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


// PATH => {[id_point_a, id_point_b] : object}
function path(point_a, point_b, lift, stair) {

        this.point_a = point_a;
        this.point_b = point_b;
        
        this.lift = lift;
        this.stair = stair;
}

// ROOM => {id_point : object}
function room(point, nome, link, people, notes) {
        
        this.point = point;
        this.nome = nome;
        this.link = link;
        this.people = people;
        this.notes = notes;
        
}
