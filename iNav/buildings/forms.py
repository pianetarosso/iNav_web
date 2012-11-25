from buildings.models import *
from django.forms import *
from django import forms
from django.forms.formsets import *
                

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
                exclude = ('id_edificio', 'utente', 'bearing', 'zoom_on_map', 'posizione_immagine')
  
  
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
                exclude = ('id_edificio', 'numero_di_piano', 'immagine', 'id', 'descrizione', 'utente')
                
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

        # id temporaneo, impostato dalla JApplet, server per poter costruire la 
        # path corrispondente in modo corretto
        temp_id = forms.IntegerField()
        
        # id del piano corrispondente
        floor_id = forms.IntegerField()
        
        
        class Meta:
                model = Point
                
                exclude = ('id_edificio')
                widgets = {
                        'RFID' : HiddenInput(),
                        'x' : HiddenInput(),
                        'y' : HiddenInput(),
                        'ingresso' : HiddenInput(),  
                        'temp_id' : HiddenInput(),
                        'floor_id' : HiddenInput(),
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
                temp_id = self.cleaned_data['temp_id']
                floor_id = self.cleaned_data['floor_id']
                
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
                # do something with self.cleaned_data['temp_id']
                super(PointForm).save(commit=commit)
                
# POINT FORM SET                
class PointFormSet(BaseFormSet):
        def clean(self):
        
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
      
                floors = {}
                ids = []
                
                for i in range(0, self.total_form_count()):
                        form = self.forms[i]
                        
                        f_id = form.cleaned_data.get('floor_id')
                        temp_id = form.cleaned_data.get('temp_id')
                        
                        x = form.cleaned_data.get('x')
                        y = form.cleaned_data.get('y')
                        
                        # verifico che non ci siano duplicazioni di id
                        if temp_id in ids:
                                raise forms.ValidationError("Incorrect ids!!!")
                        
                        ids[len(ids)] = temp_id 
                        
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
          
          
