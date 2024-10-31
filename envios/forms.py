from django import forms
from .models import *

class ShopeeForm(forms.ModelForm):
    class Meta:
        model = Shopee
        fields = ['quantidade', 'documento', 'nome', 'assinatura']
        
class MercadoLivreForm(forms.ModelForm):
    class Meta:
        model = MercadoLivre
        fields = ['quantidade', 'documento', 'nome', 'assinatura']

