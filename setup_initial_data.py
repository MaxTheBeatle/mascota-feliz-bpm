#!/usr/bin/env python
"""
Script para configurar datos iniciales del Sistema Veterinario Mascota Feliz
Ejecutar después de hacer las migraciones para cargar todos los datos de ejemplo
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_initial_data():
    """Configura la base de datos con datos iniciales"""
    
    print("🐾 Configurando Sistema Veterinario Mascota Feliz...")
    print("=" * 60)
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mascota_feliz.settings')
    django.setup()
    
    try:
        # 1. Hacer migraciones
        print("📋 1. Aplicando migraciones de base de datos...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migraciones aplicadas correctamente\n")
        
        # 2. Cargar datos iniciales
        print("📦 2. Cargando datos iniciales...")
        if os.path.exists('initial_data.json'):
            execute_from_command_line(['manage.py', 'loaddata', 'initial_data.json'])
            print("✅ Datos iniciales cargados correctamente\n")
        else:
            print("⚠️  Archivo initial_data.json no encontrado")
            print("   Creando superusuario manualmente...\n")
            create_superuser()
        
        # 3. Mostrar información de usuarios
        print("👥 3. Usuarios disponibles en el sistema:")
        print("-" * 40)
        show_users_info()
        
        print("\n🎉 ¡Configuración completada!")
        print("=" * 60)
        print("🚀 Para iniciar el servidor ejecuta: python manage.py runserver")
        print("🌐 Luego visita: http://127.0.0.1:8000/")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        return False
    
    return True

def create_superuser():
    """Crea un superusuario básico si no hay datos iniciales"""
    from django.contrib.auth.models import User
    
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@mascotafeliz.com',
            password='admin123'
        )
        print("✅ Superusuario creado: admin / admin123")

def show_users_info():
    """Muestra información de los usuarios disponibles"""
    from django.contrib.auth.models import User
    from veterinaria.models import Veterinario, Peluquero
    
    print("🔐 ADMINISTRADORES:")
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        print(f"   • {admin.username} - {admin.email}")
    
    print("\n🩺 VETERINARIOS:")
    veterinarios = Veterinario.objects.all()
    for vet in veterinarios:
        print(f"   • {vet.user.username} - {vet.nombre} ({vet.especialidad})")
        print(f"     Email: {vet.user.email}")
    
    print("\n✂️  PELUQUEROS:")
    peluqueros = Peluquero.objects.all()
    for pel in peluqueros:
        print(f"   • {pel.user.username} - {pel.nombre}")
        print(f"     Email: {pel.user.email} - Experiencia: {pel.anos_experiencia} años")
    
    print("\n👤 CLIENTES:")
    clientes = User.objects.filter(is_staff=False, is_superuser=False)
    for cliente in clientes[:5]:  # Mostrar solo los primeros 5
        print(f"   • {cliente.username} - {cliente.email}")
    
    if clientes.count() > 5:
        print(f"   ... y {clientes.count() - 5} clientes más")

if __name__ == '__main__':
    setup_initial_data() 