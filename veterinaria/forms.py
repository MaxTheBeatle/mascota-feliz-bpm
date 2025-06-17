from django import forms
from .models import (
    Mascota, Cita, CarritoItem, Pedido, Veterinario, User, Medicamento, RecetaMedica, ItemReceta, ReservaMedicamento, ItemReserva, CategoriaFarmacia,
    # Peluquería
    CitaPeluqueria, Peluquero, FotosAntesDepues
)
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'raza', 'color', 'especie', 'condicion', 'edad', 'sexo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control'}),
            'condicion': forms.Select(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
        }

class CitaForm(forms.ModelForm):
    # Opciones de duración predefinidas
    DURACION_CHOICES = [
        (30, '30 minutos'),
        (60, '1 hora'),
        (90, '1 hora 30 minutos'),
        (120, '2 horas'),
    ]
    
    duracion_minutos = forms.ChoiceField(
        choices=DURACION_CHOICES,
        initial=60,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Duración estimada'
    )
    
    class Meta:
        model = Cita
        fields = ['mascota', 'fecha', 'hora', 'duracion_minutos', 'motivo', 'veterinario']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'step': '900'}),  # Intervalos de 15 min
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'mascota': 'Mascota',
            'fecha': 'Fecha',
            'hora': 'Hora',
            'motivo': 'Motivo de la consulta',
            'veterinario': 'Veterinario (opcional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer veterinario opcional
        self.fields['veterinario'].required = False
        self.fields['veterinario'].empty_label = "Asignar automáticamente"
        
        # Mostrar solo veterinarios activos
        self.fields['veterinario'].queryset = Veterinario.objects.all()
        
        # Configurar horarios de atención (8:00 AM a 6:00 PM)
        self.fields['hora'].widget.attrs.update({
            'min': '08:00',
            'max': '18:00',
        })
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            from datetime import date
            if fecha < date.today():
                raise ValidationError("No puedes agendar citas en fechas pasadas.")
            
            # Verificar que no sea domingo (día 6)
            if fecha.weekday() == 6:
                raise ValidationError("No se pueden agendar citas los domingos.")
        
        return fecha
    
    def clean_hora(self):
        hora = self.cleaned_data.get('hora')
        if hora:
            # Verificar horario de atención (8:00 AM a 6:00 PM)
            hora_inicio = time(8, 0)  # 8:00 AM
            hora_fin = time(18, 0)    # 6:00 PM
            
            if hora < hora_inicio or hora > hora_fin:
                raise ValidationError("Las citas solo se pueden agendar entre 8:00 AM y 6:00 PM.")
            
            # Verificar que sea en intervalos de 15 minutos
            if hora.minute not in [0, 15, 30, 45]:
                raise ValidationError("Las citas deben agendarse en intervalos de 15 minutos (ej: 9:00, 9:15, 9:30, 9:45).")
        
        return hora
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        duracion_minutos = cleaned_data.get('duracion_minutos')
        
        if fecha and hora and duracion_minutos:
            # Verificar conflictos de horarios
            duracion = int(duracion_minutos)
            hora_fin = (datetime.combine(fecha, hora) + timedelta(minutes=duracion)).time()
            
            # Verificar que la cita no se extienda más allá del horario de atención
            if hora_fin > time(18, 0):
                raise ValidationError(
                    f"La cita se extendería hasta las {hora_fin.strftime('%H:%M')}, "
                    f"pero el horario de atención termina a las 18:00."
                )
            
            # Verificar conflictos con otras citas
            citas_conflicto = Cita.objects.filter(
                fecha=fecha,
                estado__in=['programada', 'confirmada', 'en_curso']
            )
            
            # Excluir la cita actual si estamos editando
            if self.instance and self.instance.pk:
                citas_conflicto = citas_conflicto.exclude(pk=self.instance.pk)
            
            for cita in citas_conflicto:
                cita_inicio = cita.hora
                cita_fin = (datetime.combine(fecha, cita.hora) + timedelta(minutes=cita.duracion_minutos)).time()
                
                # Verificar solapamiento
                if (hora < cita_fin and hora_fin > cita_inicio):
                    raise ValidationError(
                        f'Ya existe una cita programada de {cita_inicio.strftime("%H:%M")} a {cita_fin.strftime("%H:%M")} '
                        f'para {cita.mascota.nombre}. Por favor selecciona otro horario.'
                    )
        
        return cleaned_data

class CarritoItemForm(forms.ModelForm):
    class Meta:
        model = CarritoItem
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_envio', 'metodo_pago']
        widgets = {
            'direccion_envio': forms.TextInput(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }

class VeterinarioRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    especialidad = forms.CharField(max_length=100, required=True, label='Especialidad')
    telefono = forms.CharField(max_length=20, required=True, label='Teléfono')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Personalizar labels y help texts
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['email'].help_text = 'Correo electrónico profesional'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Crear perfil de veterinario
            Veterinario.objects.create(
                user=user,
                especialidad=self.cleaned_data['especialidad'],
                telefono=self.cleaned_data['telefono']
            )
        return user

class VeterinarioProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = Veterinario
        fields = ['especialidad', 'telefono']
        widgets = {
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'especialidad': 'Especialidad',
            'telefono': 'Teléfono',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        
        # Agregar clases CSS
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        veterinario = super().save(commit=False)
        if commit:
            # Actualizar datos del usuario
            user = veterinario.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            veterinario.save()
        return veterinario

# ==================== FORMULARIOS DE FARMACIA ====================

class RecetaMedicaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = ['fecha_vencimiento', 'diagnostico', 'observaciones']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'diagnostico': 'Diagnóstico',
            'observaciones': 'Observaciones Adicionales',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha mínima (hoy + 30 días por defecto)
        from datetime import date, timedelta
        fecha_minima = date.today() + timedelta(days=1)
        fecha_default = date.today() + timedelta(days=30)
        
        self.fields['fecha_vencimiento'].widget.attrs.update({
            'min': fecha_minima.strftime('%Y-%m-%d'),
            'value': fecha_default.strftime('%Y-%m-%d')
        })

class ItemRecetaForm(forms.ModelForm):
    class Meta:
        model = ItemReceta
        fields = ['medicamento', 'cantidad', 'dosis', 'duracion', 'instrucciones']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'dosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1 tableta cada 8 horas'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 7 días'}),
            'instrucciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Instrucciones especiales (opcional)'}),
        }
        labels = {
            'medicamento': 'Medicamento',
            'cantidad': 'Cantidad',
            'dosis': 'Dosis',
            'duracion': 'Duración del Tratamiento',
            'instrucciones': 'Instrucciones Especiales',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo medicamentos activos y con stock
        self.fields['medicamento'].queryset = Medicamento.objects.filter(activo=True, stock__gt=0)
        self.fields['instrucciones'].required = False

class ReservaMedicamentoForm(forms.ModelForm):
    class Meta:
        model = ReservaMedicamento
        fields = ['fecha_retiro', 'telefono_contacto', 'notas']
        widgets = {
            'fecha_retiro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 XXXX XXXX'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionales (opcional)'}),
        }
        labels = {
            'fecha_retiro': 'Fecha de Retiro',
            'telefono_contacto': 'Teléfono de Contacto',
            'notas': 'Notas Adicionales',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha mínima (mañana)
        from datetime import date, timedelta
        fecha_minima = date.today() + timedelta(days=1)
        
        self.fields['fecha_retiro'].widget.attrs.update({
            'min': fecha_minima.strftime('%Y-%m-%d'),
            'value': fecha_minima.strftime('%Y-%m-%d')
        })
        self.fields['notas'].required = False

class ItemReservaForm(forms.ModelForm):
    class Meta:
        model = ItemReserva
        fields = ['medicamento', 'cantidad']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'medicamento': 'Medicamento',
            'cantidad': 'Cantidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo medicamentos de venta libre con stock
        self.fields['medicamento'].queryset = Medicamento.objects.filter(
            activo=True, 
            stock__gt=0, 
            requiere_receta=False
        )

class BuscarMedicamentoForm(forms.Form):
    busqueda = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar medicamento...',
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=CategoriaFarmacia.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipo = forms.ChoiceField(
        choices=[('', 'Todos los tipos')] + Medicamento.TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    requiere_receta = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('True', 'Con receta'),
            ('False', 'Venta libre'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de venta'
    )
    disponible = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Solo disponibles'
    )

# ==================== FORMULARIOS DE PELUQUERÍA ====================

class CitaPeluqueriaForm(forms.ModelForm):
    class Meta:
        model = CitaPeluqueria
        fields = ['mascota', 'fecha', 'hora', 'observaciones_cliente', 'telefono_contacto']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'step': '900'}),
            'observaciones_cliente': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones especiales para el peluquero...'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 XXXX XXXX'}),
        }
        labels = {
            'mascota': 'Mascota',
            'fecha': 'Fecha',
            'hora': 'Hora',
            'observaciones_cliente': 'Observaciones Especiales',
            'telefono_contacto': 'Teléfono de Contacto',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar horarios de atención (9:00 AM a 6:00 PM)
        self.fields['hora'].widget.attrs.update({
            'min': '09:00',
            'max': '18:00',
        })
        self.fields['observaciones_cliente'].required = False
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            from datetime import date
            if fecha < date.today():
                raise ValidationError("No puedes agendar citas en fechas pasadas.")
            
            # Verificar que no sea domingo (día 6)
            if fecha.weekday() == 6:
                raise ValidationError("No se pueden agendar citas de peluquería los domingos.")
        
        return fecha
    
    def clean_hora(self):
        hora = self.cleaned_data.get('hora')
        if hora:
            # Verificar horario de atención (9:00 AM a 6:00 PM)
            hora_inicio = time(9, 0)  # 9:00 AM
            hora_fin = time(18, 0)    # 6:00 PM
            
            if hora < hora_inicio or hora > hora_fin:
                raise ValidationError("Las citas de peluquería solo se pueden agendar entre 9:00 AM y 6:00 PM.")
            
            # Verificar que sea en intervalos de 15 minutos
            if hora.minute not in [0, 15, 30, 45]:
                raise ValidationError("Las citas deben agendarse en intervalos de 15 minutos (ej: 9:00, 9:15, 9:30, 9:45).")
        
        return hora

class PeluqueroRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    telefono = forms.CharField(max_length=20, required=True, label='Teléfono')
    experiencia_años = forms.IntegerField(min_value=0, required=True, label='Años de Experiencia')
    certificaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Certificaciones y Cursos',
        help_text='Describe tus certificaciones, cursos y experiencia relevante'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Personalizar labels y help texts
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['email'].help_text = 'Correo electrónico profesional'
    
    def save(self, commit=True):
        from .models import Peluquero
        
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Crear perfil de peluquero
            Peluquero.objects.create(
                user=user,
                telefono=self.cleaned_data['telefono'],
                experiencia_años=self.cleaned_data['experiencia_años'],
                certificaciones=self.cleaned_data['certificaciones']
            )
        return user

class PeluqueroProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = Peluquero
        fields = ['telefono', 'experiencia_años', 'certificaciones', 'horario_inicio', 'horario_fin', 'especialidades']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'experiencia_años': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'certificaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'horario_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'horario_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'especialidades': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'telefono': 'Teléfono',
            'experiencia_años': 'Años de Experiencia',
            'certificaciones': 'Certificaciones y Cursos',
            'horario_inicio': 'Horario de Inicio',
            'horario_fin': 'Horario de Fin',
            'especialidades': 'Especialidades',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        
        # Agregar clases CSS
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        peluquero = super().save(commit=False)
        if commit:
            # Actualizar datos del usuario
            user = peluquero.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            peluquero.save()
        return peluquero

class FotosAntesDepuesForm(forms.ModelForm):
    class Meta:
        model = FotosAntesDepues
        fields = ['foto_antes', 'foto_despues', 'descripcion']
        widgets = {
            'foto_antes': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'foto_despues': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe el trabajo realizado...'}),
        }
        labels = {
            'foto_antes': 'Foto Antes',
            'foto_despues': 'Foto Después',
            'descripcion': 'Descripción del Trabajo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].required = False 