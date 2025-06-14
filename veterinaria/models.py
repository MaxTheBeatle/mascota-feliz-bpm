from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import RegexValidator
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    region = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.username
    
    @property
    def veterinario(self):
        """Verificar si el usuario es veterinario"""
        try:
            return self.veterinario_set.first()
        except:
            return None

class Veterinario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="El número debe estar en formato: '+999999999'")]
    )

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"

class Mascota(models.Model):
    ESPECIE_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
    ]
    
    CONDICION_CHOICES = [
        ('Normal', 'Normal'),
        ('Herido', 'Herido'),
        ('Vejez', 'Vejez'),
    ]
    
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]
    
    id = models.IntegerField(primary_key=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mascotas', null=True, blank=True)
    nombre = models.CharField(max_length=100, default='Sin nombre')
    raza = models.CharField(max_length=100, default='Mestizo')
    color = models.CharField(max_length=50, default='No especificado')
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES, default='Perro')
    condicion = models.CharField(max_length=10, choices=CONDICION_CHOICES, default='Normal')
    edad = models.CharField(max_length=50, default='0 años')
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, default='Macho')

    def __str__(self):
        return f"{self.nombre} - {self.especie} ({self.raza})"

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No Asistió'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(default='')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, blank=True)
    duracion_minutos = models.PositiveIntegerField(default=60, help_text="Duración estimada en minutos")
    notas_veterinario = models.TextField(blank=True, help_text="Notas del veterinario después de la consulta")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def clean(self):
        """Validar que no haya conflictos de horarios"""
        if self.fecha and self.hora:
            from datetime import datetime, timedelta, time
            
            # Asegurar que hora sea un objeto time
            if isinstance(self.hora, datetime):
                hora_obj = self.hora.time()
            else:
                hora_obj = self.hora
            
            # Calcular hora de inicio y fin de la cita
            hora_inicio = hora_obj
            hora_fin = (datetime.combine(self.fecha, hora_obj) + timedelta(minutes=self.duracion_minutos)).time()
            
            # Buscar citas que se solapen en la misma fecha
            citas_conflicto = Cita.objects.filter(
                fecha=self.fecha,
                estado__in=['programada', 'confirmada', 'en_curso']
            ).exclude(pk=self.pk if self.pk else None)
            
            for cita in citas_conflicto:
                # Asegurar que la hora de la cita existente sea un objeto time
                if isinstance(cita.hora, datetime):
                    cita_hora_obj = cita.hora.time()
                else:
                    cita_hora_obj = cita.hora
                
                cita_inicio = cita_hora_obj
                cita_fin = (datetime.combine(cita.fecha, cita_hora_obj) + timedelta(minutes=cita.duracion_minutos)).time()
                
                # Verificar si hay solapamiento
                if (hora_inicio < cita_fin and hora_fin > cita_inicio):
                    raise ValidationError(
                        f'Ya existe una cita programada de {cita_inicio.strftime("%H:%M")} a {cita_fin.strftime("%H:%M")} '
                        f'para {cita.mascota.nombre}. Por favor selecciona otro horario.'
                    )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def hora_fin(self):
        """Calcular hora de finalización de la cita"""
        from datetime import datetime, timedelta
        
        # Asegurar que hora sea un objeto time
        if isinstance(self.hora, datetime):
            hora_obj = self.hora.time()
        else:
            hora_obj = self.hora
            
        return (datetime.combine(self.fecha, hora_obj) + timedelta(minutes=self.duracion_minutos)).time()
    
    @property
    def duracion_formateada(self):
        """Formatear duración en horas y minutos"""
        horas = self.duracion_minutos // 60
        minutos = self.duracion_minutos % 60
        if horas > 0:
            return f"{horas}h {minutos}min" if minutos > 0 else f"{horas}h"
        return f"{minutos}min"
    
    @property
    def puede_cancelar(self):
        """Verificar si la cita se puede cancelar"""
        return self.estado in ['programada', 'confirmada']
    
    @property
    def puede_editar(self):
        """Verificar si la cita se puede editar"""
        return self.estado in ['programada', 'confirmada']

    def __str__(self):
        return f"Cita para {self.mascota.nombre} el {self.fecha} a las {self.hora} ({self.get_estado_display()})"

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-fecha', '-hora']

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    es_destacado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class CarritoItem(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad}x {self.producto}"

    class Meta:
        verbose_name = "Item de Carrito"
        verbose_name_plural = "Items de Carrito"

class Pedido(models.Model):
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
    ]
    
    direccion_envio = models.CharField(max_length=200, default='No especificada')
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default='Efectivo')
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.fecha_pedido.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} en Pedido #{self.pedido.id}"

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"

class Servicio(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    tipo_servicio = models.CharField(max_length=100, default='Consulta general')
    tipo_reserva = models.CharField(max_length=100, default='Presencial')
    region = models.CharField(max_length=100, default='No especificada')

    def __str__(self):
        return f"{self.tipo_servicio} para {self.mascota.nombre}"

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

class Pet(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    base_color = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    age_years = models.IntegerField()
    age_months = models.IntegerField()
    sex = models.CharField(max_length=10)
    service_history = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} - {self.species} ({self.owner.username})"

class Service(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(max_length=50)
    reservation_type = models.CharField(max_length=20)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.service_type} for {self.pet.name}"

# ==================== MODELOS DE FARMACIA ====================

class CategoriaFarmacia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, default='fas fa-pills')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría de Farmacia"
        verbose_name_plural = "Categorías de Farmacia"

class Medicamento(models.Model):
    TIPO_CHOICES = [
        ('antibiotico', 'Antibiótico'),
        ('analgesico', 'Analgésico'),
        ('antiinflamatorio', 'Antiinflamatorio'),
        ('antiparasitario', 'Antiparasitario'),
        ('vitamina', 'Vitamina/Suplemento'),
        ('vacuna', 'Vacuna'),
        ('desparasitante', 'Desparasitante'),
        ('dermatologico', 'Dermatológico'),
        ('cardiaco', 'Cardíaco'),
        ('digestivo', 'Digestivo'),
        ('respiratorio', 'Respiratorio'),
        ('oftalmico', 'Oftálmico'),
        ('otro', 'Otro'),
    ]
    
    PRESENTACION_CHOICES = [
        ('tableta', 'Tableta'),
        ('capsula', 'Cápsula'),
        ('jarabe', 'Jarabe'),
        ('suspension', 'Suspensión'),
        ('inyectable', 'Inyectable'),
        ('crema', 'Crema'),
        ('pomada', 'Pomada'),
        ('gotas', 'Gotas'),
        ('spray', 'Spray'),
        ('polvo', 'Polvo'),
    ]
    
    nombre = models.CharField(max_length=200)
    nombre_generico = models.CharField(max_length=200, blank=True)
    categoria = models.ForeignKey(CategoriaFarmacia, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    presentacion = models.CharField(max_length=20, choices=PRESENTACION_CHOICES)
    concentracion = models.CharField(max_length=100, help_text="Ej: 250mg, 10ml, etc.")
    laboratorio = models.CharField(max_length=100)
    descripcion = models.TextField()
    indicaciones = models.TextField(help_text="Para qué se usa")
    contraindicaciones = models.TextField(blank=True, help_text="Cuándo no usar")
    efectos_secundarios = models.TextField(blank=True)
    dosis_recomendada = models.TextField(help_text="Dosis general recomendada")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    requiere_receta = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='medicamentos/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo
    
    @property
    def disponible(self):
        return self.activo and self.stock > 0
    
    def __str__(self):
        return f"{self.nombre} - {self.concentracion}"
    
    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ['nombre']

class RecetaMedica(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('parcialmente_dispensada', 'Parcialmente Dispensada'),
        ('dispensada', 'Completamente Dispensada'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]
    
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='recetas')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(help_text="Fecha límite para usar la receta")
    diagnostico = models.TextField()
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=25, choices=ESTADO_CHOICES, default='activa')
    
    @property
    def esta_vencida(self):
        from datetime import date
        return date.today() > self.fecha_vencimiento
    
    @property
    def total_medicamentos(self):
        return self.items.count()
    
    @property
    def total_precio(self):
        return sum(item.subtotal for item in self.items.all())
    
    def __str__(self):
        return f"Receta #{self.id} - {self.mascota.nombre} ({self.fecha_emision.strftime('%d/%m/%Y')})"
    
    class Meta:
        verbose_name = "Receta Médica"
        verbose_name_plural = "Recetas Médicas"
        ordering = ['-fecha_emision']

class ItemReceta(models.Model):
    receta = models.ForeignKey(RecetaMedica, on_delete=models.CASCADE, related_name='items')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    dosis = models.CharField(max_length=200, help_text="Ej: 1 tableta cada 8 horas")
    duracion = models.CharField(max_length=100, help_text="Ej: 7 días, 2 semanas")
    instrucciones = models.TextField(blank=True, help_text="Instrucciones especiales")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.precio_unitario = self.medicamento.precio
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.medicamento.nombre} x{self.cantidad}"
    
    class Meta:
        verbose_name = "Item de Receta"
        verbose_name_plural = "Items de Receta"

class ReservaMedicamento(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('lista', 'Lista para Recoger'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]
    
    TIPO_CHOICES = [
        ('receta', 'Con Receta Médica'),
        ('libre', 'Venta Libre'),
    ]
    
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    receta = models.ForeignKey(RecetaMedica, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_retiro = models.DateField(help_text="Fecha estimada de retiro")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True)
    telefono_contacto = models.CharField(max_length=20)
    
    @property
    def numero_reserva(self):
        return f"RES-{self.id:06d}"
    
    def __str__(self):
        return f"Reserva {self.numero_reserva} - {self.cliente.get_full_name()}"
    
    class Meta:
        verbose_name = "Reserva de Medicamento"
        verbose_name_plural = "Reservas de Medicamentos"
        ordering = ['-fecha_reserva']

class ItemReserva(models.Model):
    reserva = models.ForeignKey(ReservaMedicamento, on_delete=models.CASCADE, related_name='items')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.precio_unitario = self.medicamento.precio
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)
        
        # Actualizar total de la reserva
        self.reserva.total = sum(item.subtotal for item in self.reserva.items.all())
        self.reserva.save()
    
    def __str__(self):
        return f"{self.medicamento.nombre} x{self.cantidad}"
    
    class Meta:
        verbose_name = "Item de Reserva"
        verbose_name_plural = "Items de Reserva"
