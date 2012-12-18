from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.shortcuts import redirect
from buildings.models import *
from buildings.forms import *
from django.template import RequestContext
from django.shortcuts import redirect
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
#from django.core import serializers
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from PIL import Image
from django.template.response import TemplateResponse
from django.http import Http404
from django.db.models import Max

#import pdb;

############################################################################################
MAX_TEMPORARY_BUILDINGS = 3







############################################################################################
## PAGINE WEB


# INDEX, mostro tutti gli edifici (pronti) sulla mappa
def index(request):
        session = {}
        building_list = Building.objects.filter(pronto=True).order_by('id')
        session['buildings'] = building_list
        return render_to_response('buildings/index.html', session, context_instance = RequestContext(request))

# Dettaglio di un edificio selezionato nell'index
def detail(request, building_id):
        session = {}
        
        b = get_object_or_404(Building, pk=building_id)
        session['building'] = b
        
        session['floors'] = Floor.objects.filter(building=building_id).order_by('numero_di_piano')
        
        points = Point.objects.filter(building=building_id).order_by('piano')
        session['points'] = points
        
        temp_rooms = Room.objects.filter(building=building_id) 
        ordered_rooms = {}
        for r in temp_rooms:
        
                if not ordered_rooms.has_key(r.punto.piano.numero_di_piano):
                        ordered_rooms[r.punto.piano.numero_di_piano] = []   
                
                ordered_rooms[r.punto.piano.numero_di_piano].append(r)
                                
        session['rooms'] = ordered_rooms
        
        
        paths = Path.objects.filter(building=building_id)
        
        elevators = {}
        stairs = {}
        
        for p in paths:
                
                if not elevators.has_key(p.a.piano.numero_di_piano):
                        elevators[p.a.piano.numero_di_piano] = []
                        
                if not elevators.has_key(p.b.piano.numero_di_piano):
                        elevators[p.b.piano.numero_di_piano] = []
                        
                if not stairs.has_key(p.a.piano.numero_di_piano):
                        stairs[p.a.piano.numero_di_piano] = []
                        
                if not stairs.has_key(p.b.piano.numero_di_piano):
                        stairs[p.b.piano.numero_di_piano] = []
                        
                if p.ascensore != '':
                        elevators[p.a.piano.numero_di_piano].append(p.ascensore)
                        elevators[p.b.piano.numero_di_piano].append(p.ascensore)
                elif p.scala != '':
                        stairs[p.a.piano.numero_di_piano].append(p.scala)
                        stairs[p.b.piano.numero_di_piano].append(p.scala)
        
        session['elevators'] = elevators
        session['stairs'] = stairs
        
        return render_to_response('buildings/detail.html', session, context_instance = RequestContext(request))
    
@login_required
# lista degli edifici creati da un utente
def my_buildings(request):
        session = {}
        
        session['buildings'] = Building.objects.filter(utente=request.user)
        
        return render_to_response('buildings/my_buildings.html', session, context_instance = RequestContext(request))
        
        
# ??????????????????????????????????????????????????????????????????????????
# CHE E' STA' ROBA???????????????????????????????????????????
def profile(request):
        return render_to_response('buildings/profile.html', {'user': request.user}, context_instance = RequestContext(request))
 



# Generazione di un nuovo edificio


@login_required
# new_id e' l'id dell'edificio che viene instanziato all'apertura della pagina
def generate(request, new_id):
        session = {}
        
        try:
                b_id = int(new_id)
        except Exception: 
                raise Http404
        
        # verifico se l'utente e' abilitato a creare un nuovo edificio, o se ne ha gia' troppi
        # in "cantiere"
        if b_id == -1:
                
                other_buildings = Building.objects.filter(utente=request.user, pronto=False)

                if len(other_buildings) >= MAX_TEMPORARY_BUILDINGS:
                        return redirect('buildings.views.index')
                else:
                        now = datetime.datetime.now()
                        building = Building(utente=request.user, nome=str(request.user) + str(now), pronto=False, data_creazione=now, data_update=now, versione=1.0)
                        building.save()
                        
                        return redirect('buildings.views.generate', new_id=building.pk)
         
        # l'edificio esiste gia', ergo decido quali dati mandare a seconda del punto del wizard
        elif b_id >= 0:
        
                building = get_object_or_404(Building, pk=b_id)
                floors = Floor.objects.filter(building=building)
                
                # verifico se e' stato impostato il bearing agli edifici
                test_bearing = len(floors) > 0
                for f in floors:
                       test_bearing = test_bearing and (f.bearing != None)  
                
                # due casi "limite"
                if building.utente != request.user:
                        raise Http404
                elif building.pronto:
                        return redirect('buildings.views.detail', building_id=b_id)
                # se non e' stato impostato il bearing ci troviamo nel 3o step (JApplet)
                elif test_bearing:
                        session['building'] = building
                       # floors = get_list_or_404(Floor.objects.order_by('numero_di_piano'), building=b_id)
                        #data = []
                        
                        # costruisco un JSON con alcuni dati dei piani
                        #for f in floors:
                        #        data.append(parseFloor(f))
                        #session['floors'] = simplejson.dumps(data)
                       
                        return render_to_response('buildings/generate/generate-map.html', session, context_instance = RequestContext(request))
                     
                # verifico il nome dell'edificio, se e' lo stesso del momento della costruzione
                # allora mi trovo ancora nel primo step   
                elif building.nome == str(request.user) + str(building.data_creazione):
                        buildings= Building.objects.filter(pronto=True).order_by('utente')
                        session['buildings'] = buildings       
                session['building'] = building                        
        else:
                raise Http404
        
        return render_to_response('buildings/generate/generate-index.html', session, context_instance = RequestContext(request))


@login_required
# new_id e' l'id del nuovo edificio, si occupa l'oggetto soprastante di impostarlo
def step(request, new_id):
        
        session ={}
        
        b = get_object_or_404(Building, pk=new_id)
        
        if b.utente != request.user or b.pronto:
                raise Http404
         
               
        if b.nome == str(request.user) + str(b.data_creazione):
                step = 0
        else:
                if len(Floor.objects.filter(building=b.id)) == 0:
                        step = 1
                
                elif len(Floor.objects.filter(building=b.id).exclude(bearing=None)) == 0:
                        step = 2
                        
                elif len(Point.objects.filter(building=b.id)) == 0 and len(Path.objects.filter(building=b.id)) == 0:
                        step = 3
                else:
                        session['building'] = b        
                        return render_to_response('buildings/generate/redirect.html', session,  context_instance = RequestContext(request))
                        
                     #   b.pronto = True
                     #   b.save()
                     #   return redirect('index')
                        
        # Passo 0: 
        #    Creazione dell'oggetto Building
        #    Passo questo oggetto allo step successivo
        
        if step == 0:
                
                if request.method == 'POST':
                        form = BuildingForm(request.POST, request.FILES)
                        if form.is_valid():
        
                                data = form.save(commit=False)
                                now = datetime.datetime.now()
                                b.nome = data.nome
                                b.descrizione = data.descrizione
                                b.link = data.link
                                b.numero_di_piani = data.numero_di_piani
                                b.foto = data.foto
                                b.versione = 1.1
                                b.data_update = now
                                b.posizione = data.posizione
                                b.geometria = data.geometria
                                b.save()
                              
                                request.method = None
                                step += 1
                        else:
                                session['form'] = form
                else:   
                        form = BuildingForm(initial={'numero_di_piani' : 1})
                        session['form'] = form
                 
   
   # Passo 1:
   #    Creazione dei piani in base ai dati forniti in precedenza
   #    Salvataggio delle immagini (con auspicabile rinominazione)
       
        if step == 1:
                
                FloorFormSet = formset_factory(FloorForm, extra=b.numero_di_piani, formset=BaseFloorFormSet) 
                
                if request.method == 'POST':
                        form = FloorFormSet(request.POST, request.FILES)
                        
                        if b.numero_di_piani != form.total_form_count():
                                raise Http404
                                
                        if form.is_valid():
                                for f in form.forms:
                                        floor = f.save(commit=False)
                                        floor.building = b 
                                        floor.bearing = None
                                        floor.zoom_on_map = None
                                        floor.posizione_immagine = None
                                        floor.save() 
                                now = datetime.datetime.now()
                                b.data_update = now
                                b.versione = 1.4
                                b.save()
                                request.method = None
                                step += 1
                        else:
                                session['formset'] = form     
                else:
                        form = FloorFormSet()
                
                        session['formset'] = form 
    
    
   # Passo 2:
   # Utilizzo per l'ultima volta la mappa di google per effettuare la sovrapposizione dell'immagine 
   # del piano terra (o piu' vicino superiore) sull'immagine della mappa e ricavare il bearing
   
        if step == 2:
        
                floors = Floor.objects.filter(building=b.id).order_by("numero_di_piano")
                FloorFormSet = formset_factory(AlternateFloorForm, extra=b.numero_di_piani,  formset=BaseAlternateFloorFormSet)
                
                if request.method == 'POST':
                        
                        form = FloorFormSet(request.POST)
                        
                        if form.is_valid(): 
                               
                                if len(floors) != form.total_form_count():
                                        return Http404
                                        
                                allset = True
                                f_set = None
                                
                                for n_floor, c_floor in map(None, form.forms, floors):
                                        new_floor = n_floor.save(commit=False)
                                        
                                        c_floor.bearing = new_floor.bearing
                                        c_floor.zoom_on_map = new_floor.zoom_on_map
                                        c_floor.posizione_immagine = new_floor.posizione_immagine
                                        c_floor.save()
                                        
                                
                                now = datetime.datetime.now()
                                b.data_update = now
                                b.save()
                                request.method = None
                                
                                step += 1
                        else:
                                session['floorForm'] = form  
                                session['floors'] = floors
                else:
                        session['floorForm'] = FloorFormSet()
                        session['floors'] = floors
                        
                
                
   
   # Passo 3:
   #    Creazione dei punti e percorsi dei piani in base ai dati forniti in precedenza
   #    Salvataggio di TUTTO
        if step == 3:
                
                PointFSet = formset_factory(PointForm, formset=PointFormSet)
                PathFormSet = formset_factory(PathForm)
                RoomFormSet = formset_factory(RoomForm)
                
                if request.method == 'POST':
                        
                        
                        point_formset = PointFSet(request.POST, prefix='points')
                        path_formset = PathFormSet(request.POST, prefix='paths')
                        room_formset = RoomFormSet(request.POST, prefix='rooms')
                        
                        if not (point_formset.is_valid() and path_formset.is_valid()):
                              raise Http404
                              
                          
                        # salvo i punti nel db, e nel contempo creo un dizionario con il punto
                        # e l'id temporaneo usato all'interno della pagina
                        points = {}
                        for form in point_formset.forms:
                                temp_id = form.cleaned_data['temp_id']
                                temp_floor = form.cleaned_data['temp_piano']
                                floor = get_object_or_404(Floor, building=b, numero_di_piano=temp_floor)
                                
                                point = form.save(commit=False)
                                
                                # verifico che i punti x e y siano all'interno dell'immagine
                                image = Image.open(floor.immagine)
                                if point.x < 0 or point.x > image.size[0] or point.y < 0 or point.y > image.size[1]:
                                        raise Http404 
                                        
                                point.piano = floor
                                point.building = b
                                point.save()
                                
                                points[temp_id] = point
        
                        # salvo le path correggendo i riferimenti ai punti A e B grazie a points
                        for form in path_formset.forms:
                                temp_a = form.cleaned_data['temp_a']
                                temp_b = form.cleaned_data['temp_b']
                                
                                path = form.save(commit=False)
                                path.building = b
                                
                                if not (points.has_key(temp_a) and points.has_key(temp_b)):
                                        raise Http404
                                        
                                path.a = points[temp_a]
                                path.b = points[temp_b]
                                
                                path.save()
                                
                                
                        # innanzitutto verifico che esistano delle stanze. 
                        # Se ci sono, provveddo ad aggiornare il punto.
                        if room_formset.is_valid():
                        
                                for form in room_formset.forms:
                                        temp_punto = form.cleaned_data['punto']
                                        
                                        room = form.save(commit=False)
                                        room.building = b
                                        room.punto = points[temp_punto]
                                        
                                        room.save()
                        
                        now = datetime.datetime.now()
                        b.data_update = now
                        b.pronto = True
                        b.save()
                        request.method = None
                        
                        # Se tutto e' andato bene, porto l'utente nella pagina dei details del building appena creato, e gli comunico che ha terminato il wizard  
                        
                        session['building'] = b
                        print "redirect!" 
                        return render_to_response('buildings/generate/redirect.html', session)
        
        
        
        
        
        
                
       # pdb.set_trace()
        session['building'] = b
        session['step'] = step
        #print session
        
        return render_to_response('buildings/generate/step'+ str(step) +'.html', session,  context_instance = RequestContext(request))
     
     
     
# pagina dell'iframe che mostra le attivita' recenti sui building
def iframe(request):

        session ={}
        
        # recupero i 10 buildings con attivita' piu' recente
        updated_at = Building.objects.annotate(Max('data_update')) 
        session['recent'] = updated_at[:9]
                                
        return render_to_response('buildings/iframe.html', session,  context_instance = RequestContext(request))
   

   
############################################################################################        



############################################################################################
## RESTITUZIONE DEI DATI TRAMITE JSON PER JAPPLET O ANDROID
   
# posso scegliere se l'edificio e' recuperato tramite id, oppure
# dando delle coordinate e un raggio in km
@csrf_exempt
def getBuildings(request, id_, latitude, longitude, radius):
        if int(id_) != -1:
        
                # recupero il building
                building = get_object_or_404(Building, pk=id_, pronto=True)
                floors = get_list_or_404(Floor, building=building)
                points = get_list_or_404(Point, building=building)
                paths = get_list_or_404(Path, building=building)
                rooms = get_list_or_404(Room, building=building)
                
                # parso i vari componenti
                out = parseBuilding(building)
                
                out['piani'] = []
                out['stanze'] = []
                out['punti'] = []
                out['paths'] = []
                
                for f in floors:
                        out['piani'].append(parseFloor(f))
                        
                for p in points:
                        out['punti'].append(parsePoint(p))
                        
                for p in paths:
                        out['paths'].append(parsePath(p))
                        
                for r in rooms:
                        out['stanze'].append(parseRoom(r))
                
                return HttpResponse(simplejson.dumps(out), mimetype="application/json") 
                
        elif int(radius) > 0:
                building = get_list_or_404(Building, ready=True )
                
                # filtrare i buildings in base alla distanza
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        raise Http404  
       
       
# recupero i piani di un determinato edificio
@login_required
def getFloors(request, building_id="-1"):
         
        building = get_object_or_404(Building, pk=building_id )
        user = get_object_or_404(User, pk=request.user.pk)
                
        if building.utente != user or building.pronto:
                raise Http404
                    
        floors = get_list_or_404(Floor.objects.order_by('numero_di_piano'), building=building_id)
                
        data = []
        for f in floors:
                data.append(parseFloor(f))
                
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")

       


############################################################################################

############################################################################################
## FUNZIONI VARIE DI CALCOLO E CONVERSIONE                


# funzione per convertire un oggetto Building in una lista        
def parseBuilding(b):
        building = {
                'nome' : b.nome,
                'descrizione' : b.descrizione,
                'link' : b.link,
                'id' : b.pk,
                
                'numero_di_piani' : b.numero_di_piani,
                'foto' : "",
                
                'versione' : b.versione,
                'data_creazione' : str(b.data_creazione),
                'data_update' : str(b.data_update),
                
                'posizione' : b.posizione.coords,
                'geometria' : b.geometria.coords
        }

        if b.foto != '':
                building['foto'] = b.foto.url
        
        
        return {'building' : building}  
   
        
# funzione per convertire un oggetto Floor in una lista        
def parseFloor(f):
        
        floor = {
                'numero_di_piano' : f.numero_di_piano,
                'bearing' : str(f.bearing),
                'id' : f.pk,
                'immagine' : f.immagine.url,
                'descrizione' : f.descrizione
        } 
        
        return floor 
        
# funzione per convertire un oggetto Room in una lista        
def parseRoom(r):
        
        room = {
                'punto' : r.punto.pk,
                'nome_stanza' : r.nome_stanza,
                'persone' : r.persone,
                'altro' : r.altro,
                'link' : r.link
        } 
        
        return room 
       
# funzione per convertire un oggetto Room in una lista        
def parsePath(p):
        
        path = {
                'a' : p.a.pk,
                'b' : p.b.pk,
                'ascensore' : p.ascensore,
                'scala' : p.scala
        } 
        
        return path 

# funzione per convertire un oggetto Room in una lista        
def parsePoint(p):
        
        point = {
                'id' : p.pk,
                'piano' : p.piano.numero_di_piano,
                'RFID' : p.RFID,
                'x' : p.x,
                'y' : p.y,
                'ingresso' : p.ingresso
        } 
        
        return point 

 






# funzione che restituisce un'immagine ridimensionata di un piano.
# utilizzata quando viene eseguito il calcolo del bearing nella creazione
# di un nuovo building
# width => nuova larghezza
# idf   => id del floor interessato
# id_b  => id del building interessato
@login_required
def setBearingimage(request, width, idf, id_b):
        
        building = get_object_or_404(Building, utente=request.user, pk=id_b)
          
        floor = get_object_or_404(Floor, pk=idf, id_edificio=building)
      
        # carico l'immagine
        image = Image.open(floor.link)
        
        i_width = image.size[0]
        i_heigt = image.size[1]
        
        if (int(width) < i_width):

                factor = float(width) / i_width
                new_h = i_heigt * factor 
                print str(new_h)
                print str (i_width)
                image = image.resize((int(width), int(new_h)), Image.ANTIALIAS)
        
        # serialize to HTTP response
        response = HttpResponse(mimetype="image/png")
        image.save(response, "PNG")
        
        return response
         
############################################################################################

############################################################################################

############################################################################################

############################################################################################

