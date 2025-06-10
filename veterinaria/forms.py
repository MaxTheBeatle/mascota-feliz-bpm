from django import forms
from .models import Mascota, Cita, CarritoItem, Pedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class MascotaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de Nacimiento'
    )

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'peso', 'foto']
        labels = {
            'nombre': 'Nombre de la Mascota',
            'especie': 'Especie',
            'raza': 'Raza',
            'peso': 'Peso (kg)',
            'foto': 'Foto de la Mascota'
        }

class CitaForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Fecha y Hora',
        required=True
    )

    class Meta:
        model = Cita
        fields = ['mascota', 'fecha', 'tipo_cita', 'motivo']
        labels = {
            'mascota': 'Seleccione su Mascota',
            'tipo_cita': 'Tipo de Cita',
            'motivo': 'Motivo de la Consulta'
        }

    def __init__(self, user=None, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['mascota'].queryset = Mascota.objects.filter(propietario=user)
            
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if not fecha:
            raise forms.ValidationError("La fecha y hora son obligatorias.")
        return fecha 

class CarritoItemForm(forms.ModelForm):
    class Meta:
        model = CarritoItem
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'})
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_envio', 'telefono', 'notas']
        widgets = {
            'direccion_envio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'notas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Instrucciones especiales para la entrega'})
        }
        labels = {
            'direccion_envio': 'Dirección de Envío',
            'telefono': 'Teléfono de Contacto',
            'notas': 'Notas Adicionales'
        } 