from buildings.models import *
from django.forms import *
from django import forms
from django.forms.formsets import *
from PIL import Image
                

# FORM DELL'EDIFICIO
class BuildingForm(ModelForm):
        class Meta:
                model = Building
                exclude = ('versione', 'data_creazione', 'data_update', 'pronto', 'utente')
                widgets = {
                        'geometria' : HiddenInput(),
                        'posizione' : HiddenInput(),
                }  
        
        def clean_numero_di_piani(self):
                data = self.cleaned_data['numero_di_piani']
                if (data == None or data <= 0):
                        raise forms.ValidationError("The number of floors must be at least 1!!!")
                elif (data > 20):
                        raise forms.ValidationError("The number of floors exceed maximum (20)!!!")
                return data
       
        def clean_geometria(self):
                data = self.cleaned_data['geometria']
                if Building.objects.filter(geometria__intersects=data, pronto=True):
                        raise forms.ValidationError("You cannot draw over another Building!!!")
                        
                #if data.area.sq_m > 500000: # m^2
                #        raise forms.ValidationError("Your building is too big!!!")
                        
                #for l in data.length:
                #       if l.m > 1000: # m
                #                raise forms.ValidationError("Your building is too big!!!")
                return data
                
        def clean_nome(self):
                 
                nome = self.cleaned_data['nome']
                if nome == None or nome == '':
                        raise forms.ValidationError("Name missing or not valid!!!")
                return nome
                
##############################################################################################            

# FORM DEL PIANO, SEMPLICE      
class FloorForm(ModelForm):
        class Meta:
                model = Floor
                exclude = ('building', 'utente', 'bearing', 'zoom_on_map', 'posizione_immagine')
  
  
# RELATIVO FORMSET PER INSERIRE LE IMMAGINI              
class BaseFloorFormSet(BaseFormSet):

        def clean(self):
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
          
                numero_di_piani = []
      
                for i in range(0, self.total_form_count()):
                        form = self.forms[i]
          
                        numero_di_piano = form.cleaned_data.get('numero_di_piano',None)
           
                        if numero_di_piano in numero_di_piani:
                                raise forms.ValidationError("Floors must have different floor numbers.")
                                
                        numero_di_piani.append(numero_di_piano)
                return self
                
                
#############################################################################################
  
# FORM DEL PIANO, USATA PER IMPOSTARE IL BEARING E ALTRO  
class AlternateFloorForm(ModelForm):
        class Meta:
                model = Floor
                exclude = ('building', 'numero_di_piano', 'immagine', 'id', 'descrizione', 'utente')
                
                widgets = {
                        'bearing' : HiddenInput(),
                        'zoom_on_map' : HiddenInput(),
                        'posizione_immagine' : HiddenInput(),
                }  

              
# FORMSET SU QUELLA PRECEDENTE
class BaseAlternateFloorFormSet(BaseFormSet):

        def clean(self):
        
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
      
                for i in range(0, self.total_form_count()):
                        form = self.forms[i]
                        bearing = form.cleaned_data.get('bearing', None)
                        print bearing
                        if (bearing == None) or (bearing < 0) or (bearing > 360):
                                raise forms.ValidationError("Bearing is not correct!!!") 
                return self

#############################################################################################

# FORM DEL PUNTO
class PointForm(forms.ModelForm):
        
        # id del piano corrispondente
       # piano = forms.IntegerField(widget=forms.HiddenInput())
        
        class Meta:
                model = Point
                
                exclude = ('building')
                widgets = {
                       # 'RFID' : HiddenInput(),
                       # 'x' : HiddenInput(),
                        'y' : HiddenInput(),
                       # 'ingresso' : HiddenInput(),
                       # 'piano': HiddenInput()
                } 

        
        def clean(self):
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
      
                ingresso = self.cleaned_data['ingresso']
                ascensore = self.cleaned_data['ascensore']
                scala = self.cleaned_data['scala']
                
                # verifico che un marker non sia contemporaneamente ingresso, ascensore o scala
                if (ingresso and ascensore) or (ingresso and scala) or (ascensore and scala):
                        raise forms.ValidationError("A stair cannot be a elevator or an access!!!") 
                        
                x = self.cleaned_data['x']
                y = self.cleaned_data['y']
                temp_id = self.cleaned_data['id']
                piano = self.cleaned_data['piano']
                
                floor = Floor.objects.get(pk=floor_id)
                
                if floor == None:
                        raise forms.ValidationError("Incorrect floor!!!") 
               
                # verifico che i punti x e y siano all'interno dell'immagine
                image = Image.open(floor.immagine)
                
                if x < 0 or x > image.size[0] or y < 0 or y > image.size[1]:
                        raise forms.ValidationError("Incorrect marker position!!!") 
                
                if temp_id < 0:
                        raise forms.ValidationError("Incorrect values!!!") 
                        
                return self
        
        def save(self, commit=True):
                super(PointForm).save(commit=commit)
                
                
# POINT FORM SET                
class PointFormSet(BaseFormSet):
        def clean(self):
        
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
      
                floors = {}
                ids = []
                rfid = []
                
                old_building = None
                
                for i in range(0, self.total_form_count()):
                        form = self.forms[i]
                        
                        f_id = form.cleaned_data.get('floor_id')
                        temp_id = form.cleaned_data.get('temp_id')
                        
                        x = form.cleaned_data.get('x')
                        y = form.cleaned_data.get('y')
                        
                        RFID = form.cleaned_data.get('RFID')
                        
                        # verifico che tutti i piani appartengano allo stesso building
                        if old_Building == None:
                                old_Building = Floor.object.get(pk=f_id).building
                        new_Building = Floor.object.get(pk=f_id).building
                        
                        if old_Building != new_Building:
                                raise forms.ValidationError("Incorrect Floors!!!")
                                
                        # verifico che non ci siano duplicazioni di id
                        if temp_id in ids:
                                raise forms.ValidationError("Incorrect ids!!!")
                        
                        ids[len(ids)] = temp_id 
                        
                        # verifico che non ci siano duplicazioni di RFID
                        if RFID != None and RFID in rfid:
                               raise forms.ValidationError("Duplicated RFID!!!") 
                        rfid[len(rfdi)] = RFID
                        
                        # verifico che non esistano marker con le stesse coordinate 
                        # sullo stesso piano
                        if floors.has_key(f_id):
                                lista = floors[f_id]
                                
                                if (x, y) in lista:
                                        raise forms.ValidationError("Markers overlap!!!") 
                                
                                lista[len(lista)] = (x, y)
                                floors[f_id] = lista
                                
                        else:
                                floors[f_id] = [(x, y)]
                                
                return self
        
 #################################################################################################     
          
          
# FORM DEL PUNTO
class PathForm(forms.ModelForm):

        # faccio l'override per avere dei valori integer al posto degli oggetti piano
        a = forms.IntegerField()
        b = forms.IntegerField()
        
        class Meta:
                model = Path
                
                exclude = ('building', 'id')
                widgets = {
                       # 'a' : HiddenInput(),
                       # 'b' : HiddenInput(),
                       # 'ascensore' : HiddenInput(),  
                       # 'scala' : HiddenInput()
                } 
 
        
        def clean(self):
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
      
                a = self.cleaned_data['a']
                b = self.cleaned_data['b']
                
                ascensore = self.cleaned_data['ascensore']
                scala= self.cleaned_data['scala']
                
                # verifico che i punti siano differenti
                if a == b:
                        raise forms.ValidationError("Points not correct!!!")
                
                point_a = Point.objects.get(pk=a)
                point_b = Point.objects.get(pk=b)
                
                # verifico che i punti a cui fa capo la path siano dello stesso edificio
                if point_a.building != point_b.building :
                        raise forms.ValidationError("Points not correct!!!")
                      
                # verifico che se la path e' un ascensore o una scala, i due punti non si trovino
                # sullo stesso piano  
                if (ascensore != None or scala != None) and (point_a.piano == point_b.piano):
                        raise forms.ValidationError("Points not correct!!!")
                        
                return self
        
 #################################################################################################     
     
     
# FORM DELLA STANZA
class RoomForm(forms.ModelForm):
        
        # faccio l'override per avere un valore integer al posto dell'oggetto point
        punto = forms.IntegerField()    
                
        class Meta:
                model = Room
                
                exclude = ('building', 'id')
                widgets = {
                       # 'punto' : HiddenInput(),
                       # 'nome_stanza' : HiddenInput(),
                       # 'persone' : HiddenInput(),  
                       # 'altro' : HiddenInput(),
                       # 'link' : HiddenInput()
                }   
                
