#!/usr/bin/env python
"""
Script de gestión de datos para el administrador del sistema Mascota Feliz
Permite al usuario admin controlar y gestionar todos los datos creados por crear_datos_ejemplo.py
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mascota_feliz.settings')
django.setup()

from django.contrib.auth import get_user_model
from veterinaria.models import *

User = get_user_model()

def mostrar_estadisticas():
    """Muestra estadísticas completas del sistema."""
    print("\n" + "="*60)
    print("🐾 ESTADÍSTICAS DEL SISTEMA MASCOTA FELIZ")
    print("="*60)
    
    # Usuarios
    total_usuarios = User.objects.count()
    admins = User.objects.filter(is_admin=True).count()
    clientes = total_usuarios - admins
    print(f"👥 USUARIOS:")
    print(f"   • Total: {total_usuarios}")
    print(f"   • Administradores: {admins}")
    print(f"   • Clientes: {clientes}")
    
    # Mascotas
    mascotas = Mascota.objects.count()
    pets = Pet.objects.count()
    print(f"\n🐕 MASCOTAS:")
    print(f"   • Mascotas (modelo principal): {mascotas}")
    print(f"   • Pets (modelo secundario): {pets}")
    
    # Personal
    veterinarios = Veterinario.objects.count()
    farmaceuticos = Farmaceutico.objects.count()
    peluqueros = Peluquero.objects.count()
    print(f"\n👨‍⚕️ PERSONAL:")
    print(f"   • Veterinarios: {veterinarios}")
    print(f"   • Farmacéuticos: {farmaceuticos}")
    print(f"   • Peluqueros: {peluqueros}")
    
    # Productos y servicios
    productos = Producto.objects.count()
    categorias = Categoria.objects.count()
    medicamentos = Medicamento.objects.count()
    servicios_peluqueria = ServicioPeluqueria.objects.count()
    print(f"\n🛒 PRODUCTOS Y SERVICIOS:")
    print(f"   • Productos tienda: {productos}")
    print(f"   • Categorías tienda: {categorias}")
    print(f"   • Medicamentos farmacia: {medicamentos}")
    print(f"   • Servicios peluquería: {servicios_peluqueria}")
    
    # Citas y reservas
    citas_veterinaria = Cita.objects.count()
    citas_peluqueria = CitaPeluqueria.objects.count()
    recetas = RecetaMedica.objects.count()
    reservas = ReservaMedicamento.objects.count()
    print(f"\n📅 CITAS Y RESERVAS:")
    print(f"   • Citas veterinaria: {citas_veterinaria}")
    print(f"   • Citas peluquería: {citas_peluqueria}")
    print(f"   • Recetas médicas: {recetas}")
    print(f"   • Reservas medicamentos: {reservas}")
    
    # Pedidos
    pedidos = Pedido.objects.count()
    items_carrito = CarritoItem.objects.count()
    print(f"\n🛍️ COMERCIO:")
    print(f"   • Pedidos: {pedidos}")
    print(f"   • Items en carritos: {items_carrito}")
    
    print("="*60)

def listar_usuarios():
    """Lista todos los usuarios del sistema."""
    print("\n" + "="*60)
    print("👥 LISTA DE USUARIOS")
    print("="*60)
    
    usuarios = User.objects.all().order_by('username')
    for usuario in usuarios:
        tipo = "ADMIN" if usuario.is_admin else "CLIENTE"
        estado = "ACTIVO" if usuario.is_active else "INACTIVO"
        print(f"• {usuario.username} ({tipo}) - {usuario.email} - {estado}")
        if usuario.first_name or usuario.last_name:
            print(f"  Nombre: {usuario.first_name} {usuario.last_name}")
        if usuario.region:
            print(f"  Región: {usuario.region}")
        if usuario.phone:
            print(f"  Teléfono: {usuario.phone}")
        print()

def listar_mascotas():
    """Lista todas las mascotas del sistema."""
    print("\n" + "="*60)
    print("🐕 LISTA DE MASCOTAS")
    print("="*60)
    
    mascotas = Mascota.objects.all().order_by('id')
    for mascota in mascotas:
        print(f"• ID: {mascota.id} - {mascota.nombre} ({mascota.especie})")
        print(f"  Propietario: {mascota.propietario.username}")
        print(f"  Raza: {mascota.raza}")
        print(f"  Edad: {mascota.edad} años")
        print(f"  Condición: {mascota.condicion}")
        print()

def listar_productos():
    """Lista todos los productos del sistema."""
    print("\n" + "="*60)
    print("🛒 LISTA DE PRODUCTOS")
    print("="*60)
    
    productos = Producto.objects.all().order_by('categoria', 'nombre')
    for producto in productos:
        destacado = "⭐ DESTACADO" if producto.es_destacado else ""
        print(f"• {producto.nombre} - ${producto.precio:,.0f} {destacado}")
        print(f"  Categoría: {producto.categoria.nombre}")
        print(f"  Stock: {producto.stock}")
        if producto.descripcion:
            print(f"  Descripción: {producto.descripcion[:100]}...")
        print()

def listar_citas_proximas():
    """Lista las citas próximas del sistema."""
    print("\n" + "="*60)
    print("📅 CITAS PRÓXIMAS")
    print("="*60)
    
    # Citas veterinaria
    citas_vet = Cita.objects.filter(
        fecha__gte=datetime.now().date()
    ).order_by('fecha', 'hora')[:10]
    
    if citas_vet:
        print("🏥 VETERINARIA:")
        for cita in citas_vet:
            print(f"• {cita.fecha} {cita.hora} - {cita.mascota.nombre}")
            print(f"  Propietario: {cita.mascota.propietario.username}")
            print(f"  Veterinario: {cita.veterinario.user.get_full_name()}")
            print(f"  Estado: {cita.estado}")
            print()
    
    # Citas peluquería
    citas_pel = CitaPeluqueria.objects.filter(
        fecha__gte=datetime.now().date()
    ).order_by('fecha', 'hora')[:10]
    
    if citas_pel:
        print("✂️ PELUQUERÍA:")
        for cita in citas_pel:
            print(f"• {cita.fecha} {cita.hora} - {cita.mascota.nombre}")
            print(f"  Cliente: {cita.cliente.get_full_name()}")
            print(f"  Peluquero: {cita.peluquero.user.get_full_name()}")
            print(f"  Estado: {cita.estado}")
            print(f"  Total: ${cita.total:,.0f}")
            print()

def crear_usuario_admin():
    """Crea un nuevo usuario administrador."""
    print("\n" + "="*60)
    print("➕ CREAR NUEVO ADMINISTRADOR")
    print("="*60)
    
    username = input("Nombre de usuario: ")
    if User.objects.filter(username=username).exists():
        print("❌ Error: El usuario ya existe")
        return
    
    email = input("Email: ")
    password = input("Contraseña: ")
    first_name = input("Nombre (opcional): ")
    last_name = input("Apellido (opcional): ")
    
    usuario = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_admin=True,
        is_staff=True,
        is_superuser=True
    )
    
    print(f"✅ Usuario administrador '{username}' creado exitosamente")

def resetear_datos():
    """Resetea todos los datos del sistema (PELIGROSO)."""
    print("\n" + "="*60)
    print("⚠️  RESETEAR TODOS LOS DATOS")
    print("="*60)
    print("ADVERTENCIA: Esta acción eliminará TODOS los datos del sistema")
    print("excepto los usuarios administradores.")
    
    confirmacion = input("Escriba 'CONFIRMAR' para continuar: ")
    if confirmacion != 'CONFIRMAR':
        print("❌ Operación cancelada")
        return
    
    # Eliminar datos pero mantener admins
    print("🗑️  Eliminando datos...")
    
    # Eliminar en orden para evitar problemas de FK
    FotosAntesDepues.objects.all().delete()
    ServicioCitaPeluqueria.objects.all().delete()
    CitaPeluqueria.objects.all().delete()
    
    ItemReserva.objects.all().delete()
    ReservaMedicamento.objects.all().delete()
    ItemReceta.objects.all().delete()
    RecetaMedica.objects.all().delete()
    
    PedidoItem.objects.all().delete()
    Pedido.objects.all().delete()
    CarritoItem.objects.all().delete()
    
    Service.objects.all().delete()
    Pet.objects.all().delete()
    
    Cita.objects.all().delete()
    Mascota.objects.all().delete()
    
    Medicamento.objects.all().delete()
    CategoriaFarmacia.objects.all().delete()
    
    ServicioPeluqueria.objects.all().delete()
    CategoriaServicioPeluqueria.objects.all().delete()
    
    Producto.objects.all().delete()
    Categoria.objects.all().delete()
    
    Peluquero.objects.all().delete()
    Farmaceutico.objects.all().delete()
    Veterinario.objects.all().delete()
    
    # Eliminar usuarios no admin
    User.objects.filter(is_admin=False).delete()
    
    print("✅ Todos los datos han sido eliminados")
    print("ℹ️  Puede ejecutar 'python crear_datos_ejemplo.py' para recrear datos de ejemplo")

def menu_principal():
    """Menú principal del sistema de gestión."""
    while True:
        print("\n" + "="*60)
        print("🐾 SISTEMA DE GESTIÓN MASCOTA FELIZ")
        print("="*60)
        print("1. 📊 Ver estadísticas del sistema")
        print("2. 👥 Listar usuarios")
        print("3. 🐕 Listar mascotas")
        print("4. 🛒 Listar productos")
        print("5. 📅 Ver citas próximas")
        print("6. ➕ Crear nuevo administrador")
        print("7. ⚠️  Resetear todos los datos")
        print("8. 🌐 Abrir panel de administración Django")
        print("0. 🚪 Salir")
        print("="*60)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            mostrar_estadisticas()
        elif opcion == '2':
            listar_usuarios()
        elif opcion == '3':
            listar_mascotas()
        elif opcion == '4':
            listar_productos()
        elif opcion == '5':
            listar_citas_proximas()
        elif opcion == '6':
            crear_usuario_admin()
        elif opcion == '7':
            resetear_datos()
        elif opcion == '8':
            print("\n🌐 Para acceder al panel de administración Django:")
            print("1. Ejecute: python manage.py runserver")
            print("2. Vaya a: http://127.0.0.1:8000/admin/")
            print("3. Use sus credenciales de administrador")
        elif opcion == '0':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    print("🐾 Iniciando sistema de gestión Mascota Feliz...")
    menu_principal() 