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
                        
                if data.area.sq_m > 500000: # m^2
                        raise forms.ValidationError("Your building is too big!!!")
                        
                for l in data.length:
                       if l.m > 1000: # m
                                raise forms.ValidationError("Your building is too big!!!")
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
                return self.cleaned_data

#############################################################################################

# FORM DEL PUNTO
class PointForm(forms.ModelForm):
        
        temp_id = forms.IntegerField(widget=forms.HiddenInput());
        temp_piano = forms.IntegerField(widget=forms.HiddenInput());
        
        class Meta:
                model = Point
                
                exclude = ('building', 'id', 'piano')
                widgets = {
                        'RFID' : HiddenInput(),
                        'x' : HiddenInput(),
                        'y' : HiddenInput(),
                        'ingresso' : HiddenInput(),
                } 

        
        def clean(self):
                
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
                
                ingresso = self.cleaned_data['ingresso']
                        
                x = self.cleaned_data['x']
                y = self.cleaned_data['y']
                temp_id = self.cleaned_data['temp_id']
                temp_piano = self.cleaned_data['temp_piano']
           
                
                return self.cleaned_data
        
        
                
                
# POINT FORM SET                
class PointFormSet(BaseFormSet):
        def clean(self):
                
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
      
                floors = {}
                ids = []
                rfid = []
                
                #old_building = None
                
                for i in range(0, self.total_form_count()):
                
                        form = self.forms[i]
                       
                        f_id = form.cleaned_data.get('temp_piano')
                        temp_id = form.cleaned_data.get('temp_id')
                        
                        x = form.cleaned_data.get('x')
                        y = form.cleaned_data.get('y')
                        
                        RFID = form.cleaned_data.get('RFID')
                         
                        # verifico che non ci siano duplicazioni di id
                        if temp_id in ids:
                                raise forms.ValidationError("Incorrect ids!!!")
                        ids.append(temp_id) 
                        
                        # verifico che non ci siano duplicazioni di RFID
                        if RFID in rfid:
                               raise forms.ValidationError("Duplicated RFID!!!") 
                        if RFID != '':
                                rfid.append(RFID)
                       
                        # verifico che non esistano marker con le stesse coordinate 
                        # sullo stesso piano
                        if floors.has_key(f_id):
                                lista = floors[f_id]
                                
                                if (x, y) in lista:
                                        raise forms.ValidationError("Markers overlap!!!") 
                                
                                floors[f_id].append((x, y))
                               
                        else:
                                floors[f_id] = [(x, y)]
                               
             
                return self.cleaned_data
        
 #################################################################################################     
          
          
# FORM DELLA PATH
class PathForm(forms.ModelForm):

        # faccio l'override per avere dei valori integer al posto degli oggetti piano
        temp_a = forms.IntegerField(widget=forms.HiddenInput())
        temp_b = forms.IntegerField(widget=forms.HiddenInput())
        
        class Meta:
                model = Path
                
                exclude = ('building', 'id', 'a', 'b')
                widgets = {
                        'ascensore' : HiddenInput(),  
                        'scala' : HiddenInput()
                } 
 
        
        def clean(self):
                
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
      
                a = self.cleaned_data['temp_a']
                b = self.cleaned_data['temp_b']
                
                ascensore = self.cleaned_data['ascensore']
                scala= self.cleaned_data['scala']
                
                # verifico che i due punti non siano uguali, se non sono una scala o un ascensore
                if (ascensore == '' and scala == '' and a == b):
                        raise forms.ValidationError("Points not correct!!!")
                
                return self.cleaned_data
        
 #################################################################################################     
     
     
# FORM DELLA STANZA
class RoomForm(forms.ModelForm):
        
        # faccio l'override per avere un valore integer al posto dell'oggetto point
        punto = forms.IntegerField(widget=forms.HiddenInput())    
                
        class Meta:
                model = Room
                
                exclude = ('building', 'id', 'punto')
                widgets = {
                        'nome_stanza' : HiddenInput(),
                        'persone' : HiddenInput(),  
                        'altro' : HiddenInput(),
                        'link' : HiddenInput()
                }   
                
