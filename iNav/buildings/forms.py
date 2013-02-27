# -*- coding: utf-8 -*-

from buildings.models import *
from buildings.context_processors import constants

from django.forms import *
from django import forms
from django.forms.formsets import *

from PIL import Image
from django.conf import settings

from django.contrib.gis.geos import LineString




# Form per la generazione dell'edificio: ######################################################################à


# STEP 1
#       - Nome edificio
#       - Descrizione
#       - Link
#       - Foto di copertina 
class StepOneForm(ModelForm):
        class Meta:
        
                model = Building
                
                exclude = (
                        'versione', 
                        'data_creazione', 
                        'data_update', 
                        'pronto', 
                        'utente',
                        'posizione',
                        'geometria',
                        'nazione',
                        'citta'
                )
                
        # verifico che il nome sia effettivamente unico
        def clean_nome(self):
                
                nome = self.cleaned_data['nome']
                if nome == None or nome == '':
                        raise forms.ValidationError("Name missing or not valid!!!")
                return nome                 

        # verifico che l'immagine sia leggibile e la sua dimensione non superi i 3 Mb                
        def clean_foto(self):
                        
                image = self.cleaned_data['foto']
                        
                if image:
                        if image._size > MAX_IMAGE_SIZE:
                                raise ValidationError("Image file too large ( maximum 3 Mb )")
                        return image
                else:
                        raise ValidationError("Couldn't read uploaded image")
        

# STEP 2
#       - posizione
#       - geometria
#       - nazione
#       - città 
class StepTwoForm(ModelForm):
        class Meta:
        
                model = Building
                
                exclude = (
                        'versione', 
                        'data_creazione', 
                        'data_update', 
                        'pronto', 
                        'utente',
                        'nome',
                        'descrizione',
                        'link',
                        'foto'
                )
                
                widgets = {
                        'geometria'     : HiddenInput(),
                        'posizione'     : HiddenInput(),
                        'nazione'       : HiddenInput(),
                        'citta'         : HiddenInput()
                }  
                
        # verifico alcuni campi della geometria 
        def clean_geometria(self):
        
                data = self.cleaned_data.get('geometria')
                
                # verifico che la geometria non sia sovrapposta ad altre
                if Building.objects.filter(geometria__intersects=data, pronto=True):
                        raise forms.ValidationError("You cannot draw over another Building!!!")
               
                # converto il valore dell'area in un altro leggibile (m^2), tramite la proiezione EPSG
                # (3003 vale per l'Italia, e dà risultati abbastanza buoni...)
                new_geom = data.clone()
                new_geom.transform(3003)
                area = new_geom.area
               
                print str(area)
                # verifico che l'area sia inferiore al valore massimo (in m^2)        
                if area > settings.MAX_GEOMETRY_AREA: # m^2
                        raise forms.ValidationError("Your building is too big!!!")
                     
                # verifico che l'area sia maggiore del valore minimo (in m^2)        
                if area < settings.MIN_GEOMETRY_AREA: # m^2
                        raise forms.ValidationError("Your building is too small!!!")
                        
                
                   
                # verifico che la lunghezza di ogni lato della geometria sia compatibile con
                # i valori massimi e minimi (in metri)
                old = None
                lines = []
                
                for p in new_geom[0]:
                        
                        if old != None:
                                lines.append(LineString(old, p))
                                
                        old = p
                
                for l in lines:
                        
                        if l.length > settings.MAX_GEOMETRY_LENGTH: 
                                raise forms.ValidationError("Your building is too big!!!")
                                
                        if l.length < settings.MIN_GEOMETRY_LENGTH: 
                                raise forms.ValidationError("Your building is too small!!!")
                               
                return data
                
        
        # verifico che la "posizione" sia all'interno della "geometria"
        def clean(self):
                
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
                        
                cleaned_data = super(StepTwoForm, self).clean()
                
                data = cleaned_data.get('posizione')
                data_g = cleaned_data.get('geometria')
                
                if data and data_g:
                        if not data_g.contains(data):
                                raise forms.ValidationError("Point is not inside geometry!!!")   
                
                return cleaned_data 



# STEP 3
#       - immagine
#       - numero_di_piano

class StepThreeForm(ModelForm):
        class Meta:
        
                model = Floor
                
                exclude = (
                        'building', 
                        'bearing', 
                        'zoom_on_map', 
                        'posizione_immagine', 
                )
                
# FromSet per verificare le immagini e i numeri di piano             
class StepThreeFormSet(BaseFormSet):

        def clean(self):
                if any(self.errors):
                        # Don't bother validating the formset unless each form is valid on its own
                        return
          
                numero_di_piani = []
      
               # for i in range(0, self.total_form_count()):
                #        form = self.forms[i]
          
                 #       numero_di_piano = form.cleaned_data.get('numero_di_piano',None)
           
                  #      if numero_di_piano in numero_di_piani:
                   #             raise forms.ValidationError("Floors must have different floor numbers.")
                                
                    #    numero_di_piani.append(numero_di_piano)
                return self             


#########################################################################################################


























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
                        
            #    if data.area.sq_m > 500000: # m^2
            #            raise forms.ValidationError("Your building is too big!!!")
                        
            #    for l in data.length:
            #           if l.m > 1000: # m
            #                    raise forms.ValidationError("Your building is too big!!!")
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
                
