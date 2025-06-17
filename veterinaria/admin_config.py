"""
Configuraciones adicionales para el panel de administración de Django
"""

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html

class MascotaFelizAdminSite(AdminSite):
    """Panel de administración personalizado para Mascota Feliz."""
    
    site_header = "🐾 Mascota Feliz - Panel de Administración"
    site_title = "Mascota Feliz Admin"
    index_title = "Sistema de Gestión Veterinaria"
    
    def index(self, request, extra_context=None):
        """Personaliza la página de inicio del admin."""
        extra_context = extra_context or {}
        
        # Importar aquí para evitar problemas de importación circular
        from .models import (
            User, Mascota, Pet, Veterinario, Farmaceutico, Peluquero,
            Producto, Medicamento, ServicioPeluqueria, Cita, CitaPeluqueria
        )
        
        # Estadísticas rápidas
        estadisticas = {
            'total_usuarios': User.objects.count(),
            'total_mascotas': Mascota.objects.count(),
            'total_pets': Pet.objects.count(),
            'total_veterinarios': Veterinario.objects.count(),
            'total_farmaceuticos': Farmaceutico.objects.count(),
            'total_peluqueros': Peluquero.objects.count(),
            'total_productos': Producto.objects.count(),
            'total_medicamentos': Medicamento.objects.count(),
            'total_servicios_peluqueria': ServicioPeluqueria.objects.count(),
            'citas_veterinaria_pendientes': Cita.objects.filter(estado='programada').count(),
            'citas_peluqueria_pendientes': CitaPeluqueria.objects.filter(estado='programada').count(),
        }
        
        extra_context['estadisticas'] = estadisticas
        
        return super().index(request, extra_context)

# Crear instancia personalizada del admin
admin_site = MascotaFelizAdminSite(name='mascota_feliz_admin')

def get_admin_stats():
    """Función para obtener estadísticas del sistema."""
    from .models import (
        User, Mascota, Pet, Veterinario, Farmaceutico, Peluquero,
        Producto, Medicamento, ServicioPeluqueria, Cita, CitaPeluqueria,
        Pedido, RecetaMedica, ReservaMedicamento
    )
    
    return {
        'usuarios': {
            'total': User.objects.count(),
            'admins': User.objects.filter(is_admin=True).count(),
            'activos': User.objects.filter(is_active=True).count(),
        },
        'mascotas': {
            'total_mascotas': Mascota.objects.count(),
            'total_pets': Pet.objects.count(),
            'perros': Mascota.objects.filter(especie='Perro').count(),
            'gatos': Mascota.objects.filter(especie='Gato').count(),
        },
        'personal': {
            'veterinarios': Veterinario.objects.count(),
            'farmaceuticos': Farmaceutico.objects.count(),
            'peluqueros': Peluquero.objects.count(),
        },
        'productos': {
            'tienda': Producto.objects.count(),
            'medicamentos': Medicamento.objects.count(),
            'servicios_peluqueria': ServicioPeluqueria.objects.count(),
        },
        'actividad': {
            'citas_veterinaria': Cita.objects.count(),
            'citas_peluqueria': CitaPeluqueria.objects.count(),
            'pedidos': Pedido.objects.count(),
            'recetas': RecetaMedica.objects.count(),
            'reservas': ReservaMedicamento.objects.count(),
        }
    }

def format_currency(amount):
    """Formatea un monto como moneda chilena."""
    return f"${amount:,.0f} CLP"

def format_boolean_icon(value):
    """Convierte un booleano en un ícono."""
    if value:
        return format_html('<span style="color: green;">✅</span>')
    else:
        return format_html('<span style="color: red;">❌</span>')

def format_status_badge(status):
    """Formatea el estado como una etiqueta colorida."""
    colors = {
        'programada': 'primary',
        'confirmada': 'success',
        'completada': 'success',
        'cancelada': 'danger',
        'pendiente': 'warning',
        'en_proceso': 'info',
        'finalizada': 'success',
    }
    
    color = colors.get(status.lower(), 'secondary')
    return format_html(
        '<span class="badge badge-{}">{}</span>',
        color, status.title()
    )

# Configuraciones adicionales para mejorar la experiencia del admin
ADMIN_REORDER = [
    # Usuarios y autenticación
    {
        'label': '👥 Usuarios y Autenticación',
        'models': [
            'veterinaria.User',
        ]
    },
    # Mascotas
    {
        'label': '🐕 Mascotas',
        'models': [
            'veterinaria.Mascota',
            'veterinaria.Pet',
        ]
    },
    # Personal
    {
        'label': '👨‍⚕️ Personal',
        'models': [
            'veterinaria.Veterinario',
            'veterinaria.Farmaceutico',
            'veterinaria.Peluquero',
        ]
    },
    # Servicios veterinarios
    {
        'label': '🏥 Servicios Veterinarios',
        'models': [
            'veterinaria.Cita',
            'veterinaria.Service',
            'veterinaria.RecetaMedica',
            'veterinaria.ItemReceta',
        ]
    },
    # Tienda
    {
        'label': '🛒 Tienda',
        'models': [
            'veterinaria.Categoria',
            'veterinaria.Producto',
            'veterinaria.Pedido',
            'veterinaria.PedidoItem',
            'veterinaria.CarritoItem',
        ]
    },
    # Farmacia
    {
        'label': '💊 Farmacia',
        'models': [
            'veterinaria.CategoriaFarmacia',
            'veterinaria.Medicamento',
            'veterinaria.ReservaMedicamento',
            'veterinaria.ItemReserva',
        ]
    },
    # Peluquería
    {
        'label': '✂️ Peluquería',
        'models': [
            'veterinaria.CategoriaServicioPeluqueria',
            'veterinaria.ServicioPeluqueria',
            'veterinaria.CitaPeluqueria',
            'veterinaria.ServicioCitaPeluqueria',
            'veterinaria.FotosAntesDepues',
        ]
    },
] 