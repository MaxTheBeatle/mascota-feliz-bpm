from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Pet, Service, Veterinario, Mascota, Cita, Producto, Categoria, CarritoItem, Pedido, PedidoItem

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
admin.site.register(Mascota)
admin.site.register(Cita)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(CarritoItem)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
