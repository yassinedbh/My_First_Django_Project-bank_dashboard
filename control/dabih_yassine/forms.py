from django import forms

from .models import *
class ClientForm(forms.ModelForm):
    class Meta:
        model= Client
        fields= ('nom','prenom')
        widgets= {
            'nom': forms.TextInput(attrs={'class':'form-control','placeholder':'saisissez votre nom'}), ## -> class='form-control' bootstrap
            'prenom': forms.TextInput(attrs={'class': 'form-control','placeholder':'saisissez votre prenom'}),
        }


class CompteForm(forms.ModelForm):
    class Meta:
        model= Compte
        fields = ('numero', 'dateCreation','solde','client')
        widgets = {
            'numero': forms.NumberInput(attrs={'class':'form-control','placeholder':'saisissez un numero'}),  ## -> class='form-control' bootstrap
            'dateCreation': forms.DateInput(attrs={'class':'form-control','type': 'date'}),
            'solde': forms.NumberInput(attrs={'class':'form-control','placeholder':'saisissez un solde'}),
            'client': forms.Select(attrs={'class':'form-control',}),
        }

class OperationForm(forms.ModelForm):
    class Meta:
        model= Operation
        fields = ('dateOperation','montant','type','compte')
        widgets = {
            ## -> class='form-control' bootstrap
            'dateOperation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'saisissez un solde'}),
            'type': forms.Select(attrs={'class': 'form-control', }),
            'compte': forms.Select(attrs={'class': 'form-control', }),
        }

class RechercheForm(forms.Form):
    date_debut=forms.DateField(widget=forms.DateInput( attrs={'type': "date",'class': 'form-control'}))
    date_fin = forms.DateField(widget=forms.DateInput( attrs={'type': "date",'class': 'form-control'}))