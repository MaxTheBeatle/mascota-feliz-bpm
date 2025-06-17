from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Pet, Service, Veterinario, Farmaceutico, Mascota, Cita, Producto, Categoria, CarritoItem, Pedido, PedidoItem,
    # Farmacia
    CategoriaFarmacia, Medicamento, RecetaMedica, ItemReceta, ReservaMedicamento, ItemReserva,
    # Peluquería
    CategoriaServicioPeluqueria, ServicioPeluqueria, Peluquero, CitaPeluqueria, ServicioCitaPeluqueria, FotosAntesDepues
)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin', 'region', 'phone')
    list_filter = ('is_admin', 'region')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('is_admin', 'region', 'phone')}),
    )

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'species', 'breed', 'condition', 'get_age')
    list_filter = ('species', 'condition', 'sex')
    search_fields = ('name', 'owner__username', 'breed')
    inlines = [ServiceInline]

    def get_age(self, obj):
        return f"{obj.age_years} años {obj.age_months} meses"
    get_age.short_description = 'Edad'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pet', 'service_type', 'reservation_type', 'date')
    list_filter = ('service_type', 'reservation_type', 'date')
    search_fields = ('pet__name', 'service_type')
    date_hierarchy = 'date'

admin.site.register(User, CustomUserAdmin)
admin.site.register(Veterinario)
admin.site.register(Farmaceutico)
admin.site.register(Mascota)
admin.site.register(Cita)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(CarritoItem)
admin.site.register(Pedido)
admin.site.register(PedidoItem)

# ==================== ADMIN FARMACIA ====================
admin.site.register(CategoriaFarmacia)
admin.site.register(Medicamento)
admin.site.register(RecetaMedica)
admin.site.register(ItemReceta)
admin.site.register(ReservaMedicamento)
admin.site.register(ItemReserva)

# ==================== ADMIN PELUQUERÍA ====================

class ServicioCitaPeluqueriaInline(admin.TabularInline):
    model = ServicioCitaPeluqueria
    extra = 1

class FotosAntesDepuesInline(admin.TabularInline):
    model = FotosAntesDepues
    extra = 1

@admin.register(CategoriaServicioPeluqueria)
class CategoriaServicioPeluqueriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)

@admin.register(ServicioPeluqueria)
class ServicioPeluqueriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'duracion_formateada', 'tipo_mascota', 'activo')
    list_filter = ('categoria', 'tipo_mascota', 'tamaño_mascota', 'activo')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio_base', 'activo')

@admin.register(Peluquero)
class PeluqueroAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'experiencia_años', 'activo')
    list_filter = ('activo', 'especialidades')
    search_fields = ('user__first_name', 'user__last_name', 'telefono')
    filter_horizontal = ('especialidades',)

@admin.register(CitaPeluqueria)
class CitaPeluqueriaAdmin(admin.ModelAdmin):
    list_display = ('numero_cita', 'mascota', 'cliente', 'fecha', 'hora', 'estado', 'total')
    list_filter = ('estado', 'fecha', 'peluquero')
    search_fields = ('mascota__nombre', 'cliente__first_name', 'cliente__last_name')
    date_hierarchy = 'fecha'
    inlines = [ServicioCitaPeluqueriaInline, FotosAntesDepuesInline]
    readonly_fields = ('numero_cita', 'total')

@admin.register(ServicioCitaPeluqueria)
class ServicioCitaPeluqueriaAdmin(admin.ModelAdmin):
    list_display = ('cita', 'servicio', 'precio', 'completado')
    list_filter = ('completado', 'servicio__categoria')
    search_fields = ('cita__mascota__nombre', 'servicio__nombre')

@admin.register(FotosAntesDepues)
class FotosAntesDepuesAdmin(admin.ModelAdmin):
    list_display = ('cita', 'fecha_subida')
    list_filter = ('fecha_subida',)
    search_fields = ('cita__mascota__nombre',)
