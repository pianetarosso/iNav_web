/////////////////////////////////////////////////////////////////////////////////////
// OOGETTI BASE //


// POINT => {id_point : object}
function point(x, y, floor_n, access) {

        this.x = x;
        this.y = y;
        this.floor_n = floor_n;
        this.access = access;
        
        // metodi di scrittura, caricamento e aggiornamento
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
