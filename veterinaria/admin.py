from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    User, Pet, Service, Veterinario, Farmaceutico, Mascota, Cita, Producto, Categoria, CarritoItem, Pedido, PedidoItem,
    # Farmacia
    CategoriaFarmacia, Medicamento, RecetaMedica, ItemReceta, ReservaMedicamento, ItemReserva,
    # Peluquería
    CategoriaServicioPeluqueria, ServicioPeluqueria, Peluquero, CitaPeluqueria, ServicioCitaPeluqueria, FotosAntesDepues
)

# ==================== CONFIGURACIÓN GENERAL ====================

admin.site.site_header = "🐾 Mascota Feliz - Panel de Administración"
admin.site.site_title = "Mascota Feliz Admin"
admin.site.index_title = "Sistema de Gestión Veterinaria"

# ==================== USUARIOS Y AUTENTICACIÓN ====================

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin', 'region', 'phone', 'date_joined')
    list_filter = ('is_admin', 'is_active', 'region', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('is_admin', 'region', 'phone')}),
    )
    readonly_fields = ('date_joined', 'last_login')

# ==================== MASCOTAS Y SERVICIOS ====================

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    readonly_fields = ('date',)

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'species', 'breed', 'condition', 'get_age')
    list_filter = ('species', 'condition', 'sex')
    search_fields = ('name', 'owner__username', 'breed', 'id')
    list_editable = ('condition',)
    inlines = [ServiceInline]
    ordering = ('id',)
    
    def get_age(self, obj):
        return f"{obj.age_years} años {obj.age_months} meses"
    get_age.short_description = 'Edad'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pet', 'service_type', 'reservation_type', 'date', 'get_owner')
    list_filter = ('service_type', 'reservation_type', 'date')
    search_fields = ('pet__name', 'pet__owner__username', 'service_type')
    date_hierarchy = 'date'
    readonly_fields = ('date',)
    
    def get_owner(self, obj):
        return obj.pet.owner.username
    get_owner.short_description = 'Propietario'

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'propietario', 'especie', 'raza', 'edad', 'condicion')
    list_filter = ('especie', 'condicion', 'sexo')
    search_fields = ('nombre', 'propietario__username', 'raza')
    list_editable = ('condicion',)
    ordering = ('id',)

# ==================== VETERINARIOS Y CITAS ====================

@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'especialidad', 'telefono')
    list_filter = ('especialidad',)
    search_fields = ('user__first_name', 'user__last_name', 'telefono', 'especialidad')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nombre Completo'

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'mascota', 'get_propietario', 'fecha', 'hora', 'estado', 'veterinario')
    list_filter = ('estado', 'fecha', 'veterinario')
    search_fields = ('mascota__nombre', 'mascota__propietario__username', 'motivo')
    date_hierarchy = 'fecha'
    list_editable = ('estado',)
    ordering = ('-fecha', '-hora')
    
    def get_propietario(self, obj):
        return obj.mascota.propietario.username
    get_propietario.short_description = 'Propietario'

# ==================== TIENDA Y PRODUCTOS ====================

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_productos_count')
    search_fields = ('nombre',)
    
    def get_productos_count(self, obj):
        return obj.producto_set.count()
    get_productos_count.short_description = 'Productos'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'es_destacado', 'get_imagen_preview')
    list_filter = ('categoria', 'es_destacado')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'es_destacado')
    ordering = ('categoria', 'nombre')
    
    def get_imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.imagen.url)
        return "Sin imagen"
    get_imagen_preview.short_description = 'Imagen'

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'metodo_pago', 'total', 'get_items_count')
    list_filter = ('metodo_pago', 'fecha_pedido')
    search_fields = ('usuario__username', 'direccion_envio')
    date_hierarchy = 'fecha_pedido'
    inlines = [PedidoItemInline]
    readonly_fields = ('fecha_pedido', 'total')
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Items'

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'get_subtotal')
    list_filter = ('producto__categoria',)
    search_fields = ('usuario__username', 'producto__nombre')
    
    def get_subtotal(self, obj):
        return f"${obj.subtotal():,.0f}"
    get_subtotal.short_description = 'Subtotal'

# ==================== FARMACIA ====================

@admin.register(CategoriaFarmacia)
class CategoriaFarmaciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_medicamentos_count')
    search_fields = ('nombre',)
    
    def get_medicamentos_count(self, obj):
        return obj.medicamento_set.count()
    get_medicamentos_count.short_description = 'Medicamentos'

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'requiere_receta', 'get_imagen_preview')
    list_filter = ('categoria', 'requiere_receta')
    search_fields = ('nombre', 'nombre_generico')
    list_editable = ('precio', 'stock', 'requiere_receta')
    
    def get_imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.imagen.url)
        return "Sin imagen"
    get_imagen_preview.short_description = 'Imagen'

@admin.register(Farmaceutico)
class FarmaceuticoAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'telefono', 'numero_registro', 'experiencia_años')
    list_filter = ('experiencia_años', 'activo')
    search_fields = ('user__first_name', 'user__last_name', 'numero_registro')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nombre Completo'

class ItemRecetaInline(admin.TabularInline):
    model = ItemReceta
    extra = 0

@admin.register(RecetaMedica)
class RecetaMedicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'mascota', 'veterinario', 'fecha_emision', 'estado', 'get_items_count')
    list_filter = ('estado', 'fecha_emision', 'veterinario')
    search_fields = ('mascota__nombre', 'diagnostico')
    date_hierarchy = 'fecha_emision'
    inlines = [ItemRecetaInline]
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Medicamentos'

class ItemReservaInline(admin.TabularInline):
    model = ItemReserva
    extra = 0

@admin.register(ReservaMedicamento)
class ReservaMedicamentoAdmin(admin.ModelAdmin):
    list_display = ('numero_reserva', 'cliente', 'fecha_reserva', 'tipo', 'estado', 'total')
    list_filter = ('tipo', 'estado', 'fecha_reserva')
    search_fields = ('cliente__username', 'numero_reserva')
    date_hierarchy = 'fecha_reserva'
    inlines = [ItemReservaInline]
    readonly_fields = ('numero_reserva', 'fecha_reserva')

# ==================== PELUQUERÍA ====================

class ServicioCitaPeluqueriaInline(admin.TabularInline):
    model = ServicioCitaPeluqueria
    extra = 0
    readonly_fields = ('precio',)

class FotosAntesDepuesInline(admin.TabularInline):
    model = FotosAntesDepues
    extra = 0
    readonly_fields = ('fecha_subida',)

@admin.register(CategoriaServicioPeluqueria)
class CategoriaServicioPeluqueriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'get_servicios_count')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    
    def get_servicios_count(self, obj):
        return obj.serviciopeluqueria_set.count()
    get_servicios_count.short_description = 'Servicios'

@admin.register(ServicioPeluqueria)
class ServicioPeluqueriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'duracion_formateada', 'tipo_mascota', 'activo', 'get_imagen_preview')
    list_filter = ('categoria', 'tipo_mascota', 'tamaño_mascota', 'activo')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio_base', 'activo')
    
    def get_imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.imagen.url)
        return "Sin imagen"
    get_imagen_preview.short_description = 'Imagen'

@admin.register(Peluquero)
class PeluqueroAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'telefono', 'experiencia_años', 'activo', 'get_especialidades')
    list_filter = ('activo', 'especialidades', 'experiencia_años')
    search_fields = ('user__first_name', 'user__last_name', 'telefono')
    filter_horizontal = ('especialidades',)
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nombre Completo'
    
    def get_especialidades(self, obj):
        return ", ".join([esp.nombre for esp in obj.especialidades.all()[:3]])
    get_especialidades.short_description = 'Especialidades'

@admin.register(CitaPeluqueria)
class CitaPeluqueriaAdmin(admin.ModelAdmin):
    list_display = ('numero_cita', 'mascota', 'cliente', 'peluquero', 'fecha', 'hora', 'estado', 'total')
    list_filter = ('estado', 'fecha', 'peluquero')
    search_fields = ('mascota__nombre', 'cliente__first_name', 'cliente__last_name')
    date_hierarchy = 'fecha'
    inlines = [ServicioCitaPeluqueriaInline, FotosAntesDepuesInline]
    readonly_fields = ('numero_cita', 'total', 'created_at', 'updated_at')
    list_editable = ('estado',)

@admin.register(ServicioCitaPeluqueria)
class ServicioCitaPeluqueriaAdmin(admin.ModelAdmin):
    list_display = ('cita', 'servicio', 'precio', 'completado')
    list_filter = ('completado', 'servicio__categoria')
    search_fields = ('cita__mascota__nombre', 'servicio__nombre')
    list_editable = ('completado',)

@admin.register(FotosAntesDepues)
class FotosAntesDepuesAdmin(admin.ModelAdmin):
    list_display = ('cita', 'get_mascota', 'fecha_subida', 'get_foto_antes_preview', 'get_foto_despues_preview')
    list_filter = ('fecha_subida',)
    search_fields = ('cita__mascota__nombre',)
    readonly_fields = ('fecha_subida',)
    
    def get_mascota(self, obj):
        return obj.cita.mascota.nombre
    get_mascota.short_description = 'Mascota'
    
    def get_foto_antes_preview(self, obj):
        if obj.foto_antes:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.foto_antes.url)
        return "Sin foto"
    get_foto_antes_preview.short_description = 'Antes'
    
    def get_foto_despues_preview(self, obj):
        if obj.foto_despues:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.foto_despues.url)
        return "Sin foto"
    get_foto_despues_preview.short_description = 'Después'

# ==================== REGISTRO DE MODELOS ====================

admin.site.register(User, CustomUserAdmin)
admin.site.register(PedidoItem)
admin.site.register(ItemReceta)
admin.site.register(ItemReserva) 