from django import forms

class DateInput(forms.DateInput):
    input_type='date'

# PARA PAYPAL
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'ciudad']