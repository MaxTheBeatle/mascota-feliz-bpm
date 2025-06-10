from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from decimal import Decimal
from django.core.validators import MinValueValidator

class Veterinario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('otro', 'Otro'),
    ]
    
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES)
    raza = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    foto = models.ImageField(upload_to='mascotas/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_especie_display()} de {self.propietario.get_full_name()}"

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    TIPO_CITA_CHOICES = [
        ('consulta', 'Consulta General'),
        ('vacunacion', 'Vacunación'),
        ('emergencia', 'Emergencia'),
        ('control', 'Control'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField()
    tipo_cita = models.CharField(max_length=20, choices=TIPO_CITA_CHOICES)
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cita de {self.mascota.nombre} con {self.veterinario} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-fecha']

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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre} x {self.cantidad}"

    class Meta:
        verbose_name = "Item de Carrito"
        verbose_name_plural = "Items de Carrito"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    direccion_envio = models.TextField()
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="El número debe estar en formato: '+999999999'")]
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

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
