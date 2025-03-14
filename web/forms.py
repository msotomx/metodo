from django import forms

class DateInput(forms.DateInput):
    input_type='date'

class ClienteForm(forms.Form):
    SEXO_CHOICES = (
        ('M','Masculino'),
        ('F','Femenino')
    )

    rfc = forms.CharField(label='RFC',max_length=13)
    nombre = forms.CharField(label='Nombres',max_length=200,required=True)
    apellidos = forms.CharField(label='Apellidos',max_length=200)
    sexo = forms.ChoiceField(label='Sexo',choices=SEXO_CHOICES)
    telefono = forms.CharField(label='Telefono',max_length=20)
    email = forms.EmailField(label='Email',required=True)
    fecha_nacimiento = forms.DateField(label='Fecha Nacimiento',input_formats=['%Y-%m-%d'],widget=DateInput())
    direccion = forms.CharField(label='Direccion Fiscal',widget=forms.Textarea)
    codigo_postal = forms.CharField(label='Codigo Postal',max_length=5)
    ciudad = forms.CharField(label='Ciudad',max_length=100)       
    direccion_entrega = forms.CharField(label='Direccion de Entrega',widget=forms.Textarea)
    codigo_postal_entrega = forms.CharField(label='Codigo Postal',max_length=5)
    ciudad_entrega = forms.CharField(label='Ciudad de Entrega',max_length=100)
    campo_libre = forms.CharField(label='Campo Libre',widget=forms.Textarea)
    comentarios = forms.CharField(label='Comentarios',widget=forms.Textarea)
