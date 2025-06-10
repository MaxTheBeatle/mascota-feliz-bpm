from django.contrib import admin
from .models import Veterinario, Mascota, Cita, Categoria, Producto, Pedido, PedidoItem, CarritoItem

@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidad', 'telefono')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'especialidad')

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'propietario', 'especie', 'raza', 'fecha_nacimiento', 'peso')
    list_filter = ('especie',)
    search_fields = ('nombre', 'propietario__username', 'raza')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'fecha', 'tipo_cita', 'estado')
    list_filter = ('estado', 'tipo_cita', 'fecha')
    search_fields = ('mascota__nombre', 'veterinario__user__username', 'motivo')
    date_hierarchy = 'fecha'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'es_destacado')
    list_filter = ('categoria', 'es_destacado')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'es_destacado')

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'estado', 'total')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__username', 'direccion_envio')
    inlines = [PedidoItemInline]

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'fecha_agregado')
    list_filter = ('fecha_agregado',)
    search_fields = ('usuario__username', 'producto__nombre')
