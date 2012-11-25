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
        fl = Floor.objects.filter(id_edificio=building_id).order_by('numero_di_piano')
        session['floors'] = fl
        session['building'] = b
        return render_to_response('buildings/detail.html', session, context_instance = RequestContext(request))
    
# ??????????????????????????????????????????????????????????????????????????
# CHE E' STA' ROBA???????????????????????????????????????????
def profile(request):
        return render_to_response('buildings/profile.html', {'user': request.user}, context_instance = RequestContext(request))
 



# Generazione di un nuovo edificio


@login_required
def generate(request, new_id):
        session = {}
        
        try:
                b_id = int(new_id)
        except Exception: 
                raise Http404
        
        if b_id == -1:
        
                other_buildings = Building.objects.filter(utente=request.user, pronto=False)
                
                if len(other_buildings) > MAX_TEMPORARY_BUILDINGS:
                        return redirect('buildings.views.index')
                else:
                        now = datetime.datetime.now()
                        building = Building(utente=request.user, nome=str(request.user) + str(now), pronto=False, data_creazione=now, data_update=now, versione=1.0)
                        building.save()
                        
                        return redirect('buildings.views.generate', new_id=building.pk)
         
        elif b_id >=0:
        
                building = get_object_or_404(Building, pk=b_id)
                floors = Floor.objects.filter(utente=request.user, id_edificio=building)
                
                test_bearing = len(floors) > 0
                
                for f in floors:
                       test_bearing = test_bearing and (f.bearing != None)  
                
                
                if building.utente != request.user:
                        raise Http404
                elif building.pronto:
                        return redirect('buildings.views.detail', building_id=b_id)
                elif test_bearing:
                        session['building'] = building
                        floors = get_list_or_404(Floor.objects.order_by('numero_di_piano'), id_edificio=b_id)
                        data = []
                        for f in floors:
                                data.append(parseFloor(f))
                        session['floors'] = simplejson.dumps(data)
                        
                        return render_to_response('buildings/generate/generate-map.html', session, context_instance = RequestContext(request))
                        
                elif building.nome == str(request.user) + str(building.data_creazione):
                        buildings= Building.objects.filter(pronto=True).order_by('utente')
                        session['buildings'] = buildings
                        
                session['building'] = building                        
        else:
                raise Http404
        
        return render_to_response('buildings/generate/generate-index.html', session, context_instance = RequestContext(request))


@login_required
def step(request, new_id):
        

        session ={}
        
        b = get_object_or_404(Building, pk=new_id)
        
        if b.utente != request.user or b.pronto:
                raise Http404
                
        if b.nome == str(request.user) + str(b.data_creazione):
        
                step = 0
                
        else:
        
                if len(Floor.objects.filter(id_edificio=b.id)) == 0:
                        step = 1
                
                elif len(Floor.objects.filter(id_edificio=b.id).exclude(bearing=None)) == 0:
                        step = 2
                        
                elif len(Point.objects.filter(id_edificio=b.id)) == 0 and len(Path.objects.filter(id_edificio=b.id)) == 0:
                        step = 3
                else:
                        step = 4
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
                                        floor.id_edificio = b 
                                        floor.utente = request.user
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
                        print form
                        session['formset'] = form 
    
    
   # Passo 2:
   # Utilizzo per l'ultima volta la mappa di google per effettuare la sovrapposizione dell'immagine 
   # del piano terra (o piu' vicino superiore) sull'immagine della mappa e ricavare il bearing
   
        if step == 2:
        
                floors = Floor.objects.filter(id_edificio=b.id).order_by("numero_di_piano")
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
     
                floors = Floor.objects.filter(id_edificio=b.id).order_by('numero_di_piano')
                
                points = []
                paths = []
     
                
                        
                        # aggiungere il centraggio automatico sul building appena creato nell'index
                        # (basta controllare 
                return redirect('buildings/index.html')
        
        
        #print str(request.session.items())
       # pdb.set_trace()
        session['building'] = b
        session['step'] = step
        #print session
        return render_to_response('buildings/generate/step'+ str(step) +'.html', session,  context_instance = RequestContext(request))
     
     
     
        
   

   
############################################################################################
   
############################################################################################
## RESTITUZIONE DEI DATI TRAMITE JSON PER JAPPLET O ANDROID
   
# posso scegliere se l'edificio e' recuperato tramite id, oppure
# dando delle coordinate e un raggio in km
#@csrf_exempt
#def getBuildings(request, id_="-1", latitude="0", longitude="0", radius="-1"):
#        if id_!="-1":
#                building = get_object_or_404(Building, pk=id_, ready=True)
 #               b = parseBuilding(building)
  #              return HttpResponse(simplejson.dumps(bp), mimetype="application/json") 
   #     elif latitude!="0" and longitude!="0" and int(radius) > 0:
    #            building = get_list_or_404(Building, ready=True )
     #           data=[]
      #          for b in building:
       #                 if(testNear(b, latitude, longitude, radius)):
        #                        data.append(parseBuilding(b))
         #       return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        #raise Http404  
       
# recupero i piani di un determinato edificio
#@csrf_exempt
@login_required
def getFloors(request, building_id="-1"):
         
        building = get_object_or_404(Building, pk=building_id )
        user = get_object_or_404(User, pk=request.user.pk)
                
        if building.utente != user or building.pronto:
                raise Http404
                    
        floors = get_list_or_404(Floor.objects.order_by('numero_di_piano'), id_edificio=building_id)
                
        data = []
        for f in floors:
                data.append(parseFloor(f))
                
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")

       


############################################################################################

############################################################################################
## FUNZIONI VARIE DI CALCOLO E CONVERSIONE                
                
                
# funzione per calcolare se un edificio si trova in un raggio di tot km da un punto
def testNear(building, latitude, longitude, radius):
###### DA RIEMPIRE
        return True


# funzione per convertire un oggetto Building in una lista        
def parseBuilding(b):
        building = {
                'nome' : b.nome,
                'versione' : b.versione,
                'latitudine' : b.latitudine,
                'longitudine' : b.longitudine,
                'indirizzo' : b.indirizzo,
                'numero_di_piani' : b.numero_di_piani,
                'foto' : b.foto.url
        } 
        return building  
   
        
# funzione per convertire un oggetto Floor in una lista        
def parseFloor(f):
        
        floor = {
                'numero_di_piano' : f.numero_di_piano,
                'bearing' : str(f.bearing),
                'link' : f.immagine.url
        } 
        return floor 
        
# funzione per convertire una lista ricavata da un POST in una Path
def parsePathPost(request, building):
        p = Path() 
        p.id_edificio = building  
        p.x = element["x"] 
        p.y = element["y"]
        p.x1 = element["x1"] 
        p.y1 = element["y1"]
        p.numero_di_piano = element["numero_di_piano"] 
        
        return p          


# funzione per convertire un oggetto Point in una lista        
def parsePoint(p):
        point = {
                'RFID' : p.RFID,
                'x' : p.x,
                'y' : p.y, 
                'numero_di_piano' : p.numero_di_piano,
                'ingresso' : p.ingresso,
                'ascensore' : p.ascensore,
                'scala' : p.scala,
                'stanza' : p.stanza
        } 
        return point 

# funzione per convertire una lista ricavata da un POST in un Point
def parsePointPost(request, building):
        p = Point() 
        p.id_edificio = building
        p.RFID = element["RFID"]      
        p.x = element["x"] 
        p.y= element["y"]
        p.numero_di_piano = element["numero_di_piano"] 
        p.ingresso = (element["ingresso"] == 'true')
        p.ascensore = element["ascensore"]
        p.scala = element["scala"]
        p.stanza = element["stanza"]
        
        return p
                  
# funzione per convertire un oggetto Path in una lista        
def parsePath(p):
        path = {
                'x' : p.x,
                'y' : p.y, 
                'x1' : p.x1,
                'y1' : p.y1,
                'numero_di_piano' : p.numero_di_piano,
        } 
        return path
        







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

