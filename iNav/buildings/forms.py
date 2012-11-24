from buildings.models import *
from django.forms import *
from django.forms.formsets import *
                

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
                
                        
       
class FloorForm(ModelForm):
        class Meta:
                model = Floor
                exclude = ('id_edificio', 'utente', 'bearing', 'zoom_on_map', 'posizione_immagine')
                
                
class AlternateFloorForm(ModelForm):
        class Meta:
                model = Floor
                exclude = ('id_edificio', 'numero_di_piano', 'immagine', 'id', 'descrizione', 'utente')
                
                widgets = {
                        'bearing' : HiddenInput(),
                        'zoom_on_map' : HiddenInput(),
                        'posizione_immagine' : HiddenInput(),
                }  

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
          
          
          
          
          
          
