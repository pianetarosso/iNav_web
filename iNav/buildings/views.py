# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect

from django.template import RequestContext
from django.template.response import TemplateResponse

from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from django.utils import simplejson

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import datetime
from PIL import Image

from django.contrib.auth.models import User
from django.db.models import Max

from django.contrib.gis.measure import D
from django.contrib.gis.geos import *


from buildings.models import *
from buildings.forms import *






############################################################################################
MAX_TEMPORARY_BUILDINGS = 3







############################################################################################
## PAGINE WEB


# INDEX, mostro tutti gli edifici (pronti) sulla mappa
def index(request):
        session = {}
        building_list = Building.objects.filter(pronto=True).order_by('id')
        session['buildings'] = building_list
        user = request.user
        
       
        return render_to_response('buildings/index.html', session, context_instance = RequestContext(request))


# pagina che mostra le attività recenti sui building
def update_list(request):

        session ={}
        
        # recupero i 10 buildings con attività più recente
        updated_at = Building.objects.annotate(Max('data_update')) 
        
        # filtro gli edifici per tenere solo quelly "pronti" 
        i = 0
        session['recent'] = []
        for u in updated_at:
                if i == 9:
                        break 
                elif u.pronto:
                        session['recent'].append(u)
                        i+=1
        
        session['recent'].reverse()
       
        return render_to_response('buildings/update_list.html', session,  context_instance = RequestContext(request))
   

# lista degli edifici creati da un utente   
@login_required
def my_buildings(request):
        session = {}
        
        session['buildings'] = Building.objects.filter(utente=request.user, pronto=True)
        
        return render_to_response('buildings/my_buildings.html', session, context_instance = RequestContext(request))
         
   
   
   
# generazione di un nuovo edifici
@login_required
def generate_building(request, idb):

        # creo la variabile di sessione 
        session = {}
        
        # verifico se è possibile parsare il valore in input
        try:
                b_id = int(idb)
        except Exception: 
                raise Http404
   
        userAdditionaFields = request.user.useradditionalfields
        
        # verifico se l'utente ha già 3 edifici incompleti. in tal caso lo rispedisco alla Home
        if userAdditionaFields.incomplete_buildings == MAX_TEMPORARY_BUILDINGS:
                return redirect('buildings.views.index')                        
                       
        # se l'id in input è < 0 vuol dire che sto creando l'edificio ora
        if b_id < 0:
        
                now = datetime.datetime.now()
                
                building = Building(
                        utente = request.user, 
                        nome = str(request.user) + str(now), 
                        pronto = False, 
                        data_creazione = now, 
                        data_update = now, 
                        versione = 1
                )
                
                # salvo l'edificio temporaneo
                building.save()
                
                # aggiorno l'id
                b_id = building.pk
                
                # aggiorno gli edifici incompleti dell'utente
                userAdditionaFields.incomplete_buildings += 1
                userAdditionaFields.save()
                
                return redirect('buildings.views.generate_building', idb=b_id)
                
           
        else:
                # recupero l'edificio
                building = get_object_or_404(Building, pk=b_id)
                
                # verifico se l'edificio appartiene all'utente
                if building.utente != request.user:
                        raise Http404 
                  
                # verifico se "per caso" l'edificio è già pronto
                if building.pronto:
                        return redirect('buildings.views.detail', building_id=b_id)
                        
                
                # l'id dell'edificio (se presente) mi servirà per i link dei POST nelle varie form
                session['building'] = b_id
                        
                               
                # verifico il punto del wizard in cui mi trovo (da 1 a 5)
                
                # STEP 1: ################################################################################
                #
                # BUILDING
                #       - Nome edificio
                #       - Descrizione
                #       - Link
                #       - Foto di copertina
                if building.versione == 1:
                        
                        # caso di ritorno con i dati della form
                        if request.method == 'POST':
                        
                                # recupero i dati della form dal post
                                form = StepOneForm(request.POST, request.FILES, instance=building)
                                
                                if form.is_valid():
                
                                        building = form.save(commit=False)
                                       
                                        building.data_update = datetime.datetime.now()
                                        
                                        building.versione = 2
                                        
                                        # aggiorno l'edificio
                                        building.save()
                                        
                                        # richiamo la stessa pagina, la logica dietro farà tutto il resto
                                        return redirect('buildings.views.generate_building', idb=b_id)
                                      
                                else:
                                        # la form non è valida, per cui la rispedisco al mittente
                                        session['form'] = form
                                          
                        else:
                                # costruisco una form vuota e la passo all'utente
                                form = StepOneForm()
                                session['form'] = form 
                        
                        # restituisco il template
                        return render_to_response('buildings/generate_building/step1.html', session,  context_instance = RequestContext(request))
   
                # END STEP 1 #
                #########################################################################################
                
                
                # STEP 2: ################################################################################
                #
                # BUILDING
                #       - posizione
                #       - geometria
                #       - nazione
                #       - citta
                elif building.versione == 2:
                
                        # caso di ritorno con i dati della form
                        if request.method == 'POST':
                        
                                # recupero i dati della form dal post
                                form = StepTwoForm(request.POST, request.FILES, instance=building)
                                
                                if form.is_valid():
                
                                        building = form.save(commit=False)
                                       
                                        building.data_update = datetime.datetime.now()
                                        
                                        # scarico i dati del bearing dal server esterno
                                        building.base_bearing = retrieveDeclination(building.posizione.y, building.posizione.x)
                                        
                                        building.versione = 3
                                        
                                        # aggiorno l'edificio
                                        building.save()
                                        
                                        # richiamo la stessa pagina, la logica dietro farà tutto il resto
                                        return redirect('buildings.views.generate_building', idb=b_id)
                                      
                                else:
                                        # la form non è valida, per cui la rispedisco al mittente
                                        session['form'] = form
                                          
                        else:
                                # costruisco una form vuota e la passo all'utente
                                form = StepTwoForm()
                                
                                session['form'] = form 
                                
                        # aggiungo alla sessione tutti gli edifici pronti       
                        session['buildings'] = Building.objects.filter(pronto=True)
                        
                        # restituisco il template
                        return render_to_response('buildings/generate_building/step2.html', session,  context_instance = RequestContext(request))
                       
                # END STEP 2 #
                #########################################################################################
   
   
                # STEP 3: ################################################################################
                #
                # FLOOR
                #       - numero_di_piano
                #       - immagine
                elif building.versione == 3:
                
                        # costruisco la formset
                        FormSet = formset_factory(StepThreeForm, formset=StepThreeFormSet) 
                        
                        
                        # caso di ritorno con i dati della form
                        if request.method == 'POST':
                                
                                # recupero i dati della form dal post
                                form = FormSet(request.POST, request.FILES)
                                
                                if form.is_valid():
                
                                        for f in form.forms:
                                                
                                                floor = f.save(commit=False)
                                                floor.building = building 
                                        
                                                floor.save()                                         
                                       
                                        # aggiorno l'edificio
                                        building.data_update = datetime.datetime.now() 
                                        building.versione = 4
                                        building.save()
                                        
                                        # richiamo la stessa pagina, la logica dietro farà tutto il resto
                                        return redirect('buildings.views.generate_building', idb=b_id)
                                      
                                else:
                                        # la form non è valida, per cui la rispedisco al mittente
                                        session['formset'] = form
                                          
                        else:
                                # costruisco una formset vuota e la passo all'utente
                                form = FormSet()
                                
                                session['formset'] = form 
                                
                        # restituisco il template
                        return render_to_response('buildings/generate_building/step3.html', session,  context_instance = RequestContext(request))
                
                
                # END STEP 3 #
                #########################################################################################        
   
   
                # STEP 4: ################################################################################
                #
                # FLOOR
                #       - bearing
                #       - posizione_immagine
                #       - zoom_on_map
                elif building.versione == 4:
                
                
                        # recupero i piani
                        floors = Floor.objects.filter(building=building.pk).order_by('numero_di_piano')
                        
                        
                        # costruisco la formset
                        FormSet = formset_factory(StepFourForm, max_num=len(floors)) 
                        
                        
                        # caso di ritorno con i dati della form
                        if request.method == 'POST':
                                
                                # recupero i dati della form dal post
                                forms = FormSet(request.POST, request.FILES)
                                
                                if forms.is_valid():
                
                                        for f, old_floor in map(None, forms.forms, floors):
                                                
                                                floor = f.save(commit=False)
                                                
                                                old_floor.bearing               = floor.bearing
                                                old_floor.posizione_immagine    = floor.posizione_immagine
                                                old_floor.zoom_on_map           = floor.zoom_on_map
                                                old_floor.zoom_of_map           = floor.zoom_of_map
                                                
                                                old_floor.save()      
                                         
                                                                                   
                                        # aggiorno l'edificio
                                        building.data_update = datetime.datetime.now()
                                        building.versione = 5
                                        building.save()
                                        
                                        # richiamo la stessa pagina, la logica dietro farà tutto il resto
                                        return redirect('buildings.views.generate_building', idb=b_id)
                                      
                                else:
                                        # la form non è valida, per cui la rispedisco al mittente
                                        session['formset'] = forms
                                          
                        else:
                        
                                # genero i dati iniziali della form con:
                                #       - bearing => 0
                                #       - posizione_immagine => building.posizione
                                #       - zoom_on_map => 50%
                                #       - zoom_of_map => -1 (verrà modificato al caricamento)
                                data = []
                                for f in floors:
                                        data.append({'bearing': 0.0, 'posizione_immagine': str(building.posizione), 'zoom_on_map': 50.0, 'zoom_of_map' : -1},)
                                      
                                # costruisco la formset con i dati iniziali
                                forms = FormSet(initial=data)

                                session['formset'] = forms 
                                 
                        session['geometria'] = building.geometria  
                        session['declinazione'] = building.base_bearing
                        session['floors'] = floors
                                      
                        # restituisco il template
                        return render_to_response('buildings/generate_building/step4.html', session,  context_instance = RequestContext(request))
   
                # END STEP 4 #
                #########################################################################################
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   

   
# Dettaglio di un edificio selezionato nell'index
def detail(request, building_id):
        session = {}
        
        b = get_object_or_404(Building, pk=building_id)
        session['building'] = b
        
        session['floors'] = Floor.objects.filter(building=building_id).order_by('numero_di_piano')
       
        session['points'] = Point.objects.filter(building=building_id).order_by('piano')
        
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
    

        
# ??????????????????????????????????????????????????????????????????????????
# CHE è STà ROBA???????????????????????????????????????????
def profile(request):
        return render_to_response('buildings/profile.html', {'user': request.user}, context_instance = RequestContext(request))
 
# vetrina dell'applicazione
def show(request):
        return

# Cancellazione di un edificio 
@login_required
def delete(request, b_id):
        
        building = get_object_or_404(Building, pk=b_id)
        
        if building.utente != request.user:
                raise Http404
        
        else:
               deleteBuilding(building)
               # aggiungere un return che faccia senso
        

# Generazione di un nuovo edificio


@login_required
# new_id è l'id dell'edificio che viene instanziato all'apertura della pagina
def generate(request, new_id):
        session = {}
        
        try:
                b_id = int(new_id)
        except Exception: 
                raise Http404
        
        # verifico se l'utente è abilitato a creare un nuovo edificio, o se ne ha già troppi
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
         
        # l'edificio esiste già, ergo decido quali dati mandare a seconda del punto del wizard
        elif b_id >= 0:
        
                building = get_object_or_404(Building, pk=b_id)
                floors = Floor.objects.filter(building=building)
                
                # verifico se è stato impostato il bearing agli edifici
                test_bearing = len(floors) > 0
                for f in floors:
                       test_bearing = test_bearing and (f.bearing != None)  
                
                # due casi "limite"
                if building.utente != request.user:
                        raise Http404
                elif building.pronto:
                        return redirect('buildings.views.detail', building_id=b_id)
                # se non è stato impostato il bearing ci troviamo nel 3o step (JApplet)
                elif test_bearing:
                        session['building'] = building
                       # floors = get_list_or_404(Floor.objects.order_by('numero_di_piano'), building=b_id)
                        #data = []
                        
                        # costruisco un JSON con alcuni dati dei piani
                        #for f in floors:
                        #        data.append(parseFloor(f))
                        #session['floors'] = simplejson.dumps(data)
                       
                        return render_to_response('buildings/generate/generate-map.html', session, context_instance = RequestContext(request))
                     
                # verifico il nome dell'edificio, se è lo stesso del momento della costruzione
                # allora mi trovo ancora nel primo step   
                elif building.nome == str(request.user) + str(building.data_creazione):
                        buildings= Building.objects.filter(pronto=True).order_by('utente')
                        session['buildings'] = buildings       
                session['building'] = building                        
        else:
                raise Http404
        
        return render_to_response('buildings/generate/generate-index.html', session, context_instance = RequestContext(request))


@login_required
# new_id è l'id del nuovo edificio, si occupa l'oggetto soprastante di impostarlo
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
   # del piano terra (o più vicino superiore) sull'immagine della mappa e ricavare il bearing
   
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
                        
                        # Se tutto è andato bene, porto l'utente nella pagina dei details del building appena creato, e gli comunico che ha terminato il wizard  
                        
                        session['building'] = b
                        print "redirect!" 
                        return render_to_response('buildings/generate/redirect.html', session)
        
        
        
        
        
        
                
       # pdb.set_trace()
        session['building'] = b
        session['step'] = step
        #print session
        
        return render_to_response('buildings/generate/step'+ str(step) +'.html', session,  context_instance = RequestContext(request))
     
     
     


   
############################################################################################        



############################################################################################
## RESTITUZIONE DEI DATI TRAMITE JSON PER JAPPLET O ANDROID
   
# posso scegliere se l'edificio è recuperato tramite id, oppure
# dando delle coordinate e un raggio in centinaia di m
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
                
	# caso in cui faccio la ricerca in base alla distanza
        elif int(radius) > 0:

		# costruisco il punto che sarà il centro della ricerca
		pnt = fromstr('POINT(' + str(longitude) + ' ' + str(latitude) +')', srid=4326)

		# effettuo l'interrogazione basandomi sulla distanza passata
		buildings = Building.objects.filter(posizione__distance_lte=(pnt, D(m = int(radius) * 100)))

		print str(pnt)
		print str(buildings)
                
                # elimino gli edifici che non sono pronti
		out = {}
		out['lista'] = []
                for b in buildings:
			if b.pronto:
                        	out['lista'].append(parseBuilding(b)['building'])
                
                return HttpResponse(simplejson.dumps(out), mimetype="application/json")
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
       
# funzione per convertire un oggetto Path in una lista        
def parsePath(p):
        
        path = {
                'a' : p.a.pk,
                'b' : p.b.pk,
                'ascensore' : p.ascensore,
                'scala' : p.scala
        } 
        
        return path 

# funzione per convertire un oggetto Point in una lista        
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

# funzione per cancellare completamente un edificio (manca la cancellazione delle immagini)
def deleteBuilding(building):

        for path in Path.objects.filter(building = building.id): 
                path.delete()
                
        for room in Room.objects.filter(building = building.id): 
                room.delete()
                        
        for point in Point.objects.filter(building = building.id): 
                point.delete()
                        
        for floor in Floor.objects.filter(building = building.id): 
                floor.delete()
                        
        building.delete()






# funzione che restituisce un'immagine ridimensionata di un piano.
# utilizzata quando viene eseguito il calcolo del bearing nella creazione
# di un nuovo building
# width => nuova larghezzasetBearing
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

# FUNZIONE PER RECUPERARE LA DECLINAZIONE MAGNETICA DELLA LOCALITÀ

import urllib2 
from xml.dom.minidom import parseString

# costruisco l'url
def buildUrl(latitude, longitude):
        return settings.MAGNETIC_URL + '?' + 'lat1=' + str(latitude) + '&' + 'lon1=' + str(longitude) + '&' + 'resultFormat=xml'
        
        
# recupero la pagina dall'indirizzo       
def retrieveWeb(address):
        
        try:                 
                web_handle = urllib2.urlopen(address)
                         
        except urllib2.HTTPError, e: 
                error_desc = BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0] 
                print "Cannot retrieve URL: HTTP Error Code", e.code, "Error: ", error_desc 
                sys.exit(1)         
        except urllib2.URLError, e: 
                print "Cannot retrieve URL: " + e.reason[1] 
                sys.exit(1)         
        except:                 
                print "Cannot retrieve URL: unknown error"                 
                sys.exit(1) 
                
        return web_handle  


# funzione principale per il recupero della declinazione
def retrieveDeclination(lat, lng):

        # costruisco l'indirizzo
        address = buildUrl(lat, lng) 
       
        # recupero la pagina
        page = retrieveWeb(address)
        
        # recupero l'xml
        xml = page.read()  
        
        page.close()
        
        # inizio il parsin
        dom = parseString(xml)
        
        #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
        xmlTag = dom.getElementsByTagName('declination')[0].toxml()
        
        #strip off the tag (<tag>data</tag>  --->   data):
        xmlData=xmlTag.replace('<declination>','').replace('</declination>','')
        
        print "DECLINATION: " + xmlData
        
        return float(xmlData)
      
############################################################################################

############################################################################################

############################################################################################

