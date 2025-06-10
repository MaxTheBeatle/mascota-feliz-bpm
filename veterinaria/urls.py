from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='veterinaria/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
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
] 