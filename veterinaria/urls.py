from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='veterinaria/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='veterinaria/logout.html', next_page='home'), name='logout'),
    
    # Mascotas URLs
    path('mascotas/', views.mascota_list, name='mascota_list'),
    path('mascotas/crear/', views.mascota_create, name='mascota_create'),
    path('mascotas/<int:pk>/editar/', views.mascota_update, name='mascota_update'),
    path('mascotas/<int:pk>/eliminar/', views.mascota_delete, name='mascota_delete'),
    
    # Citas URLs
    path('citas/', views.cita_list, name='cita_list'),
    path('citas/agendar/', views.cita_create, name='cita_create'),
    path('citas/<int:pk>/editar/', views.cita_update, name='cita_update'),
    path('citas/<int:pk>/cancelar/', views.cita_cancel, name='cita_cancel'),

    # Tienda URLs
    path('tienda/', views.tienda, name='tienda'),
    path('tienda/producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('tienda/carrito/', views.carrito, name='carrito'),
    path('tienda/carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('tienda/carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('tienda/carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('tienda/checkout/', views.checkout, name='checkout'),
    path('tienda/mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('tienda/pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('profile/', views.profile, name='profile'),
    path('pet/<str:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pet/<str:pet_id>/edit/', views.pet_edit, name='pet_edit'),
    path('pet/<str:pet_id>/agendar-cita/', views.pet_agendar_cita, name='pet_agendar_cita'),
    path('pet/<str:pet_id>/nuevo-servicio/', views.pet_nuevo_servicio, name='pet_nuevo_servicio'),
    path('pet/<str:pet_id>/ficha-medica/', views.descargar_ficha_medica, name='descargar_ficha_medica'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # URLs para veterinarios
    path('veterinario/registro/', views.veterinario_register, name='veterinario_register'),
    path('veterinario/dashboard/', views.veterinario_dashboard, name='veterinario_dashboard'),
    path('veterinario/citas/', views.veterinario_citas, name='veterinario_citas'),
    path('veterinario/cita/<int:cita_id>/', views.veterinario_cita_detalle, name='veterinario_cita_detalle'),
    path('veterinario/tomar-cita/<int:cita_id>/', views.veterinario_tomar_cita, name='veterinario_tomar_cita'),
    path('veterinario/perfil/', views.veterinario_profile, name='veterinario_profile'),
    
    # URLs de farmacia
    path('farmacia/', views.farmacia_catalogo, name='farmacia_catalogo'),
    path('farmacia/medicamento/<int:medicamento_id>/', views.medicamento_detalle, name='medicamento_detalle'),
    path('farmacia/recetas/', views.mis_recetas, name='mis_recetas'),
    path('farmacia/receta/<int:receta_id>/', views.detalle_receta, name='detalle_receta'),
    path('farmacia/reservas/', views.mis_reservas, name='mis_reservas'),
    path('farmacia/reserva/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('farmacia/reservar-receta/<int:receta_id>/', views.reservar_medicamentos_receta, name='reservar_medicamentos_receta'),
    path('farmacia/reservar-libre/<int:medicamento_id>/', views.reservar_medicamento_libre, name='reservar_medicamento_libre'),
    
    # URLs para veterinarios - recetas
    path('veterinario/crear-receta/<int:cita_id>/', views.crear_receta, name='crear_receta'),
    path('veterinario/editar-receta/<int:receta_id>/', views.editar_receta, name='editar_receta'),
    path('veterinario/eliminar-item-receta/<int:item_id>/', views.eliminar_item_receta, name='eliminar_item_receta'),
    
    # ==================== URLs DE PELUQUERÍA ====================
    path('peluqueria/', views.peluqueria_catalogo, name='peluqueria_catalogo'),
    path('peluqueria/servicio/<int:servicio_id>/', views.servicio_peluqueria_detalle, name='servicio_peluqueria_detalle'),
    path('peluqueria/agendar/', views.agendar_cita_peluqueria, name='agendar_cita_peluqueria'),
    path('peluqueria/agendar/<int:servicio_id>/', views.agendar_cita_peluqueria, name='agendar_cita_peluqueria_servicio'),
    path('peluqueria/mis-citas/', views.mis_citas_peluqueria, name='mis_citas_peluqueria'),
    path('peluqueria/cita/<int:cita_id>/', views.detalle_cita_peluqueria, name='detalle_cita_peluqueria'),
    path('peluqueria/cita/<int:cita_id>/cancelar/', views.cancelar_cita_peluqueria, name='cancelar_cita_peluqueria'),
    path('peluqueria/galeria/', views.galeria_peluqueria, name='galeria_peluqueria'),
    
    # URLs para peluqueros
    path('peluquero/registro/', views.peluquero_register, name='peluquero_register'),
    path('peluquero/dashboard/', views.peluquero_dashboard, name='peluquero_dashboard'),
    path('peluquero/citas/', views.peluquero_citas, name='peluquero_citas'),
    path('peluquero/cita/<int:cita_id>/', views.peluquero_cita_detalle, name='peluquero_cita_detalle'),
    path('peluquero/cita/<int:cita_id>/completar/', views.peluquero_completar_cita, name='peluquero_completar_cita'),
    path('peluquero/perfil/', views.peluquero_profile, name='peluquero_profile'),
] 