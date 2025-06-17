#!/usr/bin/env python
"""
Script para crear datos de ejemplo del Sistema Veterinario Mascota Feliz
Crea usuarios, mascotas, productos, servicios y otros datos necesarios
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

def setup_django():
    """Configurar Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mascota_feliz.settings')
    django.setup()

def crear_usuarios():
    """Crear usuarios de ejemplo"""
    from veterinaria.models import User, Veterinario, Peluquero
    
    print("👥 Creando usuarios...")
    
    # Crear administrador
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@mascotafeliz.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            region='Santiago',
            phone='+56912345678'
        )
        print("✅ Administrador creado: admin / admin123")
    
    # Crear veterinario
    if not User.objects.filter(username='veterinario1').exists():
        vet_user = User.objects.create_user(
            username='veterinario1',
            email='veterinario@mascotafeliz.com',
            password='vet123',
            first_name='Carlos',
            last_name='Mendoza',
            is_staff=True,
            region='Santiago',
            phone='+56912345678'
        )
        
        Veterinario.objects.create(
            user=vet_user,
            especialidad='Medicina General',
            telefono='+56912345678'
        )
        print("✅ Veterinario creado: veterinario1 / vet123")
    
    # Crear peluquero
    if not User.objects.filter(username='peluquero1').exists():
        pel_user = User.objects.create_user(
            username='peluquero1',
            email='peluquero@mascotafeliz.com',
            password='peluquero123',
            first_name='María',
            last_name='González',
            is_staff=True,
            region='Santiago',
            phone='+56987654321'
        )
        
        Peluquero.objects.create(
            user=pel_user,
            telefono='+56987654321',
            experiencia_años=8
        )
        print("✅ Peluquero creado: peluquero1 / peluquero123")
    
    # Crear cliente de ejemplo
    if not User.objects.filter(username='cliente1').exists():
        User.objects.create_user(
            username='cliente1',
            email='cliente@ejemplo.com',
            password='cliente123',
            first_name='Juan',
            last_name='Pérez',
            region='Santiago',
            phone='+56987654321'
        )
        print("✅ Cliente creado: cliente1 / cliente123")

def crear_productos():
    """Crear productos de ejemplo"""
    from veterinaria.models import Producto, Categoria
    
    print("🛒 Creando productos...")
    
    # Crear categorías primero
    categorias = [
        {'nombre': 'Alimentos', 'descripcion': 'Alimentos para mascotas'},
        {'nombre': 'Juguetes', 'descripcion': 'Juguetes y entretenimiento'},
        {'nombre': 'Salud', 'descripcion': 'Productos de salud'},
        {'nombre': 'Higiene', 'descripcion': 'Productos de higiene'},
    ]
    
    for cat_data in categorias:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults=cat_data
        )
        if created:
            print(f"  ✅ Categoría: {cat_data['nombre']}")
    
    # Crear productos
    productos = [
        {
            'nombre': 'Royal Canin Adult',
            'descripcion': 'Alimento premium para perros adultos',
            'precio': Decimal('25990'),
            'categoria': Categoria.objects.get(nombre='Alimentos'),
            'stock': 50
        },
        {
            'nombre': 'Whiskas Gatitos',
            'descripcion': 'Alimento húmedo para gatitos',
            'precio': Decimal('1890'),
            'categoria': Categoria.objects.get(nombre='Alimentos'),
            'stock': 100
        },
        {
            'nombre': 'Pelota Kong Classic',
            'descripcion': 'Juguete resistente para perros',
            'precio': Decimal('8990'),
            'categoria': Categoria.objects.get(nombre='Juguetes'),
            'stock': 30
        },
        {
            'nombre': 'Collar Antipulgas',
            'descripcion': 'Collar antipulgas de larga duración',
            'precio': Decimal('12990'),
            'categoria': Categoria.objects.get(nombre='Salud'),
            'stock': 25
        },
        {
            'nombre': 'Shampoo Canino',
            'descripcion': 'Shampoo especial para perros',
            'precio': Decimal('6990'),
            'categoria': Categoria.objects.get(nombre='Higiene'),
            'stock': 40
        }
    ]
    
    for prod_data in productos:
        if not Producto.objects.filter(nombre=prod_data['nombre']).exists():
            Producto.objects.create(**prod_data)
            print(f"  ✅ {prod_data['nombre']}")

def crear_servicios_peluqueria():
    """Crear servicios de peluquería"""
    from veterinaria.models import ServicioPeluqueria, CategoriaServicioPeluqueria
    
    print("✂️ Creando servicios de peluquería...")
    
    # Crear categorías de servicios
    categorias = [
        {'nombre': 'Baño y Secado', 'descripcion': 'Servicios de baño y secado'},
        {'nombre': 'Corte y Estilismo', 'descripcion': 'Servicios de corte de pelo'},
        {'nombre': 'Cuidado de Uñas', 'descripcion': 'Corte y cuidado de uñas'},
        {'nombre': 'Limpieza', 'descripcion': 'Servicios de limpieza'},
        {'nombre': 'Paquetes', 'descripcion': 'Paquetes completos de servicios'},
    ]
    
    for cat_data in categorias:
        categoria, created = CategoriaServicioPeluqueria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults=cat_data
        )
        if created:
            print(f"  ✅ Categoría: {cat_data['nombre']}")
    
    # Crear servicios
    servicios = [
        {
            'nombre': 'Baño Completo',
            'descripcion': 'Baño con shampoo especializado, secado y cepillado',
            'precio_base': Decimal('15000'),
            'duracion_estimada': 60,
            'categoria': CategoriaServicioPeluqueria.objects.get(nombre='Baño y Secado'),
            'incluye': 'Baño con shampoo, secado, cepillado básico'
        },
        {
            'nombre': 'Corte de Pelo',
            'descripcion': 'Corte profesional según raza y preferencias',
            'precio_base': Decimal('20000'),
            'duracion_estimada': 90,
            'categoria': CategoriaServicioPeluqueria.objects.get(nombre='Corte y Estilismo'),
            'incluye': 'Corte profesional, estilizado según raza'
        },
        {
            'nombre': 'Corte de Uñas',
            'descripcion': 'Corte seguro de uñas con herramientas profesionales',
            'precio_base': Decimal('8000'),
            'duracion_estimada': 30,
            'categoria': CategoriaServicioPeluqueria.objects.get(nombre='Cuidado de Uñas'),
            'incluye': 'Corte de uñas, limado, revisión de almohadillas'
        },
        {
            'nombre': 'Limpieza de Oídos',
            'descripcion': 'Limpieza profunda de oídos con productos especializados',
            'precio_base': Decimal('10000'),
            'duracion_estimada': 30,
            'categoria': CategoriaServicioPeluqueria.objects.get(nombre='Limpieza'),
            'incluye': 'Limpieza de oídos, aplicación de productos especiales'
        },
        {
            'nombre': 'Paquete Completo',
            'descripcion': 'Baño, corte, uñas y limpieza de oídos',
            'precio_base': Decimal('45000'),
            'duracion_estimada': 180,
            'categoria': CategoriaServicioPeluqueria.objects.get(nombre='Paquetes'),
            'incluye': 'Baño completo, corte de pelo, corte de uñas, limpieza de oídos'
        }
    ]
    
    for serv_data in servicios:
        if not ServicioPeluqueria.objects.filter(nombre=serv_data['nombre']).exists():
            ServicioPeluqueria.objects.create(**serv_data)
            print(f"  ✅ {serv_data['nombre']}")

def crear_medicamentos():
    """Crear medicamentos de ejemplo"""
    from veterinaria.models import Medicamento, CategoriaFarmacia
    
    print("💊 Creando medicamentos...")
    
    # Crear categorías de farmacia
    categorias = [
        {'nombre': 'Antibióticos', 'descripcion': 'Medicamentos antibióticos'},
        {'nombre': 'Suplementos', 'descripcion': 'Vitaminas y suplementos'},
        {'nombre': 'Antiinflamatorios', 'descripcion': 'Medicamentos antiinflamatorios'},
    ]
    
    for cat_data in categorias:
        categoria, created = CategoriaFarmacia.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults=cat_data
        )
        if created:
            print(f"  ✅ Categoría: {cat_data['nombre']}")
    
    # Crear medicamentos
    medicamentos = [
        {
            'nombre': 'Amoxicilina 250mg',
            'descripcion': 'Antibiótico de amplio espectro',
            'precio': Decimal('8500'),
            'requiere_receta': True,
            'stock': 20,
            'tipo': 'antibiotico',
            'categoria': CategoriaFarmacia.objects.get(nombre='Antibióticos'),
            'presentacion': 'tableta',
            'concentracion': '250mg',
            'laboratorio': 'Laboratorio Veterinario',
            'indicaciones': 'Infecciones bacterianas',
            'dosis_recomendada': 'Según prescripción veterinaria'
        },
        {
            'nombre': 'Vitaminas Multiples',
            'descripcion': 'Suplemento vitamínico para mascotas',
            'precio': Decimal('12000'),
            'requiere_receta': False,
            'stock': 35,
            'tipo': 'vitamina',
            'categoria': CategoriaFarmacia.objects.get(nombre='Suplementos'),
            'presentacion': 'tableta',
            'concentracion': 'Multivitamínico',
            'laboratorio': 'Nutri Pet',
            'indicaciones': 'Suplemento nutricional',
            'dosis_recomendada': '1 tableta diaria'
        },
        {
            'nombre': 'Antiinflamatorio',
            'descripcion': 'Para dolor e inflamación',
            'precio': Decimal('15000'),
            'requiere_receta': True,
            'stock': 15,
            'tipo': 'antiinflamatorio',
            'categoria': CategoriaFarmacia.objects.get(nombre='Antiinflamatorios'),
            'presentacion': 'tableta',
            'concentracion': '50mg',
            'laboratorio': 'Pharma Vet',
            'indicaciones': 'Dolor e inflamación',
            'dosis_recomendada': 'Según prescripción veterinaria'
        }
    ]
    
    for med_data in medicamentos:
        if not Medicamento.objects.filter(nombre=med_data['nombre']).exists():
            Medicamento.objects.create(**med_data)
            print(f"  ✅ {med_data['nombre']}")

def crear_mascotas():
    """Crear mascotas de ejemplo"""
    from veterinaria.models import Mascota, User
    
    print("🐕 Creando mascotas de ejemplo...")
    
    try:
        cliente = User.objects.get(username='cliente1')
        
        mascotas = [
            {
                'id': 1,
                'nombre': 'Max',
                'especie': 'Perro',
                'raza': 'Golden Retriever',
                'edad': '3 años',
                'sexo': 'Macho',
                'propietario': cliente,
                'color': 'Dorado',
                'condicion': 'Normal'
            },
            {
                'id': 2,
                'nombre': 'Luna',
                'especie': 'Gato',
                'raza': 'Persa',
                'edad': '2 años',
                'sexo': 'Hembra',
                'propietario': cliente,
                'color': 'Blanco',
                'condicion': 'Normal'
            }
        ]
        
        for masc_data in mascotas:
            if not Mascota.objects.filter(id=masc_data['id']).exists():
                Mascota.objects.create(**masc_data)
                print(f"  ✅ {masc_data['nombre']} ({masc_data['especie']})")
                
    except User.DoesNotExist:
        print("  ⚠️ Cliente no encontrado, saltando creación de mascotas")

def main():
    """Función principal"""
    print("🐾 Configurando Sistema Veterinario Mascota Feliz...")
    print("=" * 60)
    
    # Configurar Django
    setup_django()
    
    try:
        # Aplicar migraciones
        print("📋 1. Aplicando migraciones...")
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migraciones aplicadas\n")
        
        # Crear datos
        crear_usuarios()
        crear_productos()
        crear_servicios_peluqueria()
        crear_medicamentos()
        crear_mascotas()
        
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("=" * 60)
        print("🚀 Para iniciar el servidor ejecuta: python manage.py runserver")
        print("🌐 Luego visita: http://127.0.0.1:8000/")
        print("\n👥 Usuarios creados:")
        print("   • admin / admin123 (Administrador)")
        print("   • veterinario1 / vet123 (Veterinario)")
        print("   • peluquero1 / peluquero123 (Peluquero)")
        print("   • cliente1 / cliente123 (Cliente)")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    main() 