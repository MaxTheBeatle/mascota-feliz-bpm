#!/usr/bin/env python
"""
Script para crear datos exactos de la base de datos local del Sistema Veterinario Mascota Feliz
Replica exactamente los usuarios, productos, servicios y datos que ya tienes
Incluye imágenes para productos y servicios, crea mascotas y citas para el home
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta, date
from django.core.files.base import ContentFile
from io import BytesIO
import urllib.request
from io import BytesIO

def setup_django():
    """Configurar Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mascota_feliz.settings')
    django.setup()

def crear_superuser():
    """Crear superuser para administración"""
    from veterinaria.models import User
    
    print("👑 Creando superuser...")
    
    # Superuser principal
    if not User.objects.filter(username='superadmin').exists():
        superuser = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@mascotafeliz.com',
            password='admin123',
            first_name='Super',
            last_name='Administrador',
            region='Región Metropolitana',
            phone='+56912345678'
        )
        print("✅ Superuser 'superadmin' creado (superadmin / admin123)")

def crear_usuarios_reales():
    """Crear usuarios exactos de la base de datos local"""
    from veterinaria.models import User, Veterinario, Peluquero, Farmaceutico
    
    print("👥 Creando usuarios reales...")
    
    # Usuario admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@mascotafeliz.com',
            password='admin123',
            first_name='',
            last_name='',
            region='Región Metropolitana',
            phone=''
        )
        print("✅ Admin creado")
    
    # Cliente de ejemplo
    if not User.objects.filter(username='cliente1').exists():
        User.objects.create_user(
            username='cliente1',
            email='cliente1@example.com',
            password='cliente123',
            first_name='Juan',
            last_name='Pérez',
            region='Región de Los Lagos',
            phone='+56912345678'
        )
        print("✅ Cliente1 creado")
    
    # Veterinarios
    veterinarios_data = [
        ('dr_martinez', 'carlos.martinez@mascotafeliz.cl', 'Carlos', 'Martínez', 'Medicina General', '+56 9 1234 5678'),
        ('dra_rodriguez', 'maria.rodriguez@mascotafeliz.cl', 'María', 'Rodríguez', 'Cirugía Veterinaria', '+56 9 7654 3210'),
        ('dr_gonzalez', 'pedro.gonzalez@mascotafeliz.cl', 'Pedro', 'González', 'Dermatología Veterinaria', '+56 9 6543 2109'),
        ('dra_lopez', 'ana.lopez@mascotafeliz.cl', 'Ana', 'López', 'Cardiología Veterinaria', '+56 9 5432 1098'),
        ('dr_silva', 'roberto.silva@mascotafeliz.cl', 'Roberto', 'Silva', 'Medicina Felina', '+56 9 4321 0987'),
        ('veterinario1', 'veterinario@mascotafeliz.com', 'Carlos', 'Mendoza', 'Medicina General', '+56912345678')
    ]
    
    for username, email, first_name, last_name, especialidad, telefono in veterinarios_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password='vet123',
                first_name=first_name,
                last_name=last_name,
                is_staff=True if username == 'veterinario1' else False,
                region='Santiago' if username == 'veterinario1' else '',
                phone='+56912345678' if username == 'veterinario1' else ''
            )
            
            Veterinario.objects.create(
                user=user,
                especialidad=especialidad,
                telefono=telefono
            )
            print(f"✅ Veterinario {username} creado")
    
    # Peluqueros
    peluqueros_data = [
        ('peluquero1', 'maria.gonzalez@mascotafeliz.com', 'María', 'González', '+56 9 8765 4321', 8),
        ('peluquero2', 'carlos.rodriguez@mascotafeliz.com', 'Carlos', 'Rodríguez', '+56 9 7654 3210', 5),
        ('peluquero3', 'ana.martinez@mascotafeliz.com', 'Ana', 'Martínez', '+56 9 6543 2109', 12)
    ]
    
    for username, email, first_name, last_name, telefono, experiencia in peluqueros_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password='peluquero123',
                first_name=first_name,
                last_name=last_name,
                region='',
                phone=''
            )
            
            Peluquero.objects.create(
                user=user,
                telefono=telefono,
                experiencia_años=experiencia
            )
            print(f"✅ Peluquero {username} creado")
    
    # Farmacéutico
    if not User.objects.filter(username='farmaceutico1').exists():
        farm_user = User.objects.create_user(
            username='farmaceutico1',
            email='farmaceutico@mascotafeliz.com',
            password='farm123',
            first_name='María',
            last_name='González',
            region='Santiago',
            phone='+56987654321'
        )
        
        Farmaceutico.objects.create(
            user=farm_user,
            telefono='+56987654321',
            numero_registro='FARM001',
            especialidad='Farmacia General',
            experiencia_años=5
        )
        print("✅ Farmacéutico creado")

def crear_categorias_reales():
    """Crear categorías exactas"""
    from veterinaria.models import Categoria, CategoriaServicioPeluqueria, CategoriaFarmacia
    
    print("📂 Creando categorías...")
    
    # Categorías de productos
    categorias_productos = [
        ('Comida para perros', 'Alimentos especializados para perros'),
        ('Juguetes', 'Juguetes y entretenimiento para mascotas'),
        ('Cuidado', 'Productos de cuidado e higiene'),
        ('Accesorios', 'Accesorios y complementos'),
        ('Alimentos', 'Alimentos para mascotas'),
        ('Salud', 'Productos de salud y medicina'),
        ('Higiene', 'Productos de higiene')
    ]
    
    for nombre, descripcion in categorias_productos:
        Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion}
        )
    
    # Categorías de servicios de peluquería
    categorias_peluqueria = [
        ('Baño y Secado', 'Servicios de baño y secado profesional'),
        ('Corte y Estilismo', 'Servicios de corte y estilismo'),
        ('Cuidado de Uñas', 'Corte y cuidado de uñas'),
        ('Limpieza', 'Servicios de limpieza especializada'),
        ('Paquetes', 'Paquetes completos de servicios')
    ]
    
    for nombre, descripcion in categorias_peluqueria:
        CategoriaServicioPeluqueria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion}
        )
    
    # Categorías de farmacia
    categorias_farmacia = [
        ('Antibióticos', 'Medicamentos antibióticos'),
        ('Suplementos', 'Vitaminas y suplementos'),
        ('Antiinflamatorios', 'Medicamentos antiinflamatorios'),
        ('Antiparasitarios', 'Medicamentos antiparasitarios'),
        ('Dermatológicos', 'Medicamentos para la piel')
    ]
    
    for nombre, descripcion in categorias_farmacia:
        CategoriaFarmacia.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion}
        )
    
    print("✅ Categorías creadas")

def crear_imagen_placeholder(nombre_archivo):
    """Crear imagen placeholder simple"""
    try:
        # Crear una imagen simple de color sólido usando PIL si está disponible
        from PIL import Image, ImageDraw, ImageFont
        
        # Crear imagen de 300x300 con color de fondo
        img = Image.new('RGB', (300, 300), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Agregar texto simple
        try:
            # Usar fuente por defecto
            draw.text((150, 150), nombre_archivo[:20], fill='#666666', anchor='mm')
        except:
            pass
        
        # Guardar en memoria
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        return ContentFile(img_io.getvalue(), name=f'{nombre_archivo}.jpg')
    except ImportError:
        # Si PIL no está disponible, crear archivo vacío
        return ContentFile(b'placeholder', name=f'{nombre_archivo}.jpg')

def crear_productos_reales():
    """Crear productos exactos de la base de datos local con imágenes"""
    from veterinaria.models import Producto, Categoria
    
    print("🛒 Creando productos reales con imágenes...")
    
    # Productos reales de tu base de datos
    productos_data = [
        ('Nómade Adulto Razas Medianas y Grandes 20 kg', 'Alimento premium para perros adultos de razas medianas y grandes', '28990.00', 'Comida para perros', 50, 'nomade_adulto'),
        ('Pelota porfiada para gatos', 'Juguete interactivo para gatos', '2490.00', 'Juguetes', 15, 'pelota_gatos'),
        ('Shampoo Hipoalergénico Premium', 'Shampoo especial para pieles sensibles', '12500.00', 'Cuidado', 29, 'shampoo_premium'),
        ('Collar GPS Inteligente', 'Collar con GPS para seguimiento de mascotas', '89990.00', 'Accesorios', 8, 'collar_gps'),
        ('Cama Ortopédica para Perros', 'Cama ortopédica para el descanso de perros', '45990.00', 'Accesorios', 12, 'cama_ortopedica'),
        ('PURINA® DENTALIFE® snacks de salmón para gatos', 'Snacks dentales para gatos sabor salmón', '3990.00', 'Alimentos', 40, 'dentalife_salmon'),
        ('Royal Canin Adult', 'Alimento premium para perros adultos', '25990.00', 'Alimentos', 50, 'royal_canin'),
        ('Whiskas Gatitos', 'Alimento húmedo para gatitos', '1890.00', 'Alimentos', 100, 'whiskas_gatitos'),
        ('Pelota Kong Classic', 'Juguete resistente para perros', '8990.00', 'Juguetes', 30, 'kong_classic'),
        ('Collar Antipulgas', 'Collar antipulgas de larga duración', '12990.00', 'Salud', 25, 'collar_antipulgas'),
        ('Shampoo Canino', 'Shampoo especial para perros', '6990.00', 'Higiene', 40, 'shampoo_canino')
    ]
    
    for nombre, descripcion, precio, categoria_nombre, stock, imagen_nombre in productos_data:
        try:
            categoria = Categoria.objects.get(nombre=categoria_nombre)
            if not Producto.objects.filter(nombre=nombre).exists():
                producto = Producto.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=Decimal(precio),
                    categoria=categoria,
                    stock=stock,
                    es_destacado=False
                )
                
                # Agregar imagen placeholder
                try:
                    imagen = crear_imagen_placeholder(imagen_nombre)
                    producto.imagen.save(f'{imagen_nombre}.jpg', imagen, save=True)
                except Exception as e:
                    print(f"  ⚠️ No se pudo crear imagen para {nombre}: {e}")
                
                print(f"  ✅ {nombre}")
        except Categoria.DoesNotExist:
            print(f"  ⚠️ Categoría {categoria_nombre} no encontrada para {nombre}")

def crear_servicios_peluqueria_reales():
    """Crear servicios de peluquería exactos con imágenes"""
    from veterinaria.models import ServicioPeluqueria, CategoriaServicioPeluqueria
    
    print("✂️ Creando servicios de peluquería reales con imágenes...")
    
    # Servicios reales de tu base de datos
    servicios_data = [
        ('Baño Básico', 'Baño básico con shampoo estándar', '15000.00', 45, 'Baño y Secado', 'Baño con shampoo, secado básico', 'bano_basico'),
        ('Baño Completo', 'Baño completo con productos premium', '15000.00', 60, 'Baño y Secado', 'Baño completo, secado y cepillado', 'bano_completo'),
        ('Baño Medicado', 'Baño con shampoo medicado especial', '30000.00', 75, 'Baño y Secado', 'Baño medicado para pieles sensibles', 'bano_medicado'),
        ('Baño Premium', 'Baño premium con productos de lujo', '25000.00', 60, 'Baño y Secado', 'Baño premium con productos de alta gama', 'bano_premium'),
        ('Corte Creativo', 'Corte creativo y estilismo avanzado', '40000.00', 120, 'Corte y Estilismo', 'Corte creativo según preferencias', 'corte_creativo'),
        ('Hidratación Profunda', 'Tratamiento de hidratación profunda', '35000.00', 90, 'Cuidado de Uñas', 'Tratamiento hidratante intensivo', 'hidratacion'),
        ('Tratamiento Antipulgas', 'Tratamiento especializado antipulgas', '20000.00', 60, 'Limpieza', 'Tratamiento contra pulgas y parásitos', 'antipulgas'),
        ('Paquete Básico', 'Paquete básico de servicios', '35000.00', 90, 'Paquetes', 'Baño + corte básico', 'paquete_basico'),
        ('Paquete Premium', 'Paquete premium completo', '60000.00', 150, 'Paquetes', 'Servicios premium completos', 'paquete_premium'),
        ('Paquete VIP', 'Paquete VIP con todos los servicios', '80000.00', 180, 'Paquetes', 'Todos los servicios incluidos', 'paquete_vip'),
        ('Limpieza de Oídos', 'Limpieza profunda de oídos', '10000.00', 30, 'Limpieza', 'Limpieza especializada de oídos', 'limpieza_oidos'),
        ('Paquete Completo', 'Paquete completo de servicios', '45000.00', 180, 'Paquetes', 'Baño, corte, uñas y limpieza completa', 'paquete_completo')
    ]
    
    for nombre, descripcion, precio, duracion, categoria_nombre, incluye, imagen_nombre in servicios_data:
        try:
            categoria = CategoriaServicioPeluqueria.objects.get(nombre=categoria_nombre)
            if not ServicioPeluqueria.objects.filter(nombre=nombre).exists():
                servicio = ServicioPeluqueria.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio_base=Decimal(precio),
                    duracion_estimada=duracion,
                    categoria=categoria,
                    tipo_mascota='ambos',
                    tamaño_mascota='todos',
                    incluye=incluye,
                    recomendaciones='',
                    activo=True
                )
                
                # Agregar imagen placeholder
                try:
                    imagen = crear_imagen_placeholder(imagen_nombre)
                    servicio.imagen.save(f'{imagen_nombre}.jpg', imagen, save=True)
                except Exception as e:
                    print(f"  ⚠️ No se pudo crear imagen para {nombre}: {e}")
                
                print(f"  ✅ {nombre}")
        except CategoriaServicioPeluqueria.DoesNotExist:
            print(f"  ⚠️ Categoría {categoria_nombre} no encontrada para {nombre}")

def crear_mascotas_reales():
    """Crear mascotas de ejemplo para mostrar en el home"""
    from veterinaria.models import Mascota, User
    
    print("🐕 Creando mascotas de ejemplo...")
    
    try:
        cliente = User.objects.get(username='cliente1')
        
        mascotas_data = [
            (1, 'Max', 'Perro', 'Golden Retriever', 'Dorado', 'Normal', '3 años', 'Macho'),
            (2, 'Luna', 'Gato', 'Persa', 'Blanco', 'Normal', '2 años', 'Hembra'),
            (3, 'Rocky', 'Perro', 'Bulldog', 'Marrón', 'Normal', '4 años', 'Macho'),
            (4, 'Mia', 'Gato', 'Siamés', 'Crema', 'Normal', '1 año', 'Hembra')
        ]
        
        for id_mascota, nombre, especie, raza, color, condicion, edad, sexo in mascotas_data:
            if not Mascota.objects.filter(id=id_mascota).exists():
                Mascota.objects.create(
                    id=id_mascota,
                    nombre=nombre,
                    especie=especie,
                    raza=raza,
                    color=color,
                    condicion=condicion,
                    edad=edad,
                    sexo=sexo,
                    propietario=cliente
                )
                print(f"  ✅ {nombre} ({especie})")
                
    except User.DoesNotExist:
        print("  ⚠️ Cliente no encontrado, saltando creación de mascotas")

def crear_citas_ejemplo():
    """Crear citas de ejemplo para mostrar en el home"""
    from veterinaria.models import Cita, Mascota, Veterinario, User
    
    print("📅 Creando citas de ejemplo...")
    
    try:
        cliente = User.objects.get(username='cliente1')
        veterinario = Veterinario.objects.first()
        mascotas = Mascota.objects.filter(propietario=cliente)
        
        if veterinario and mascotas.exists():
            # Citas futuras para mostrar en "Próximas citas"
            citas_data = [
                {
                    'fecha': date.today() + timedelta(days=3),
                    'hora': '10:00',
                    'motivo': 'Control de rutina',
                    'mascota': mascotas[0],  # Max
                },
                {
                    'fecha': date.today() + timedelta(days=7),
                    'hora': '15:30',
                    'motivo': 'Vacunación anual',
                    'mascota': mascotas[1],  # Luna
                },
                {
                    'fecha': date.today() + timedelta(days=10),
                    'hora': '09:15',
                    'motivo': 'Revisión dental',
                    'mascota': mascotas[2] if len(mascotas) > 2 else mascotas[0],  # Rocky o Max
                }
            ]
            
            for cita_data in citas_data:
                # Verificar si ya existe una cita similar
                existing_cita = Cita.objects.filter(
                    mascota=cita_data['mascota'],
                    fecha=cita_data['fecha'],
                    hora=cita_data['hora']
                ).first()
                
                if not existing_cita:
                    Cita.objects.create(
                        mascota=cita_data['mascota'],
                        veterinario=veterinario,
                        fecha=cita_data['fecha'],
                        hora=cita_data['hora'],
                        motivo=cita_data['motivo'],
                        estado='programada'
                    )
                    print(f"  ✅ Cita para {cita_data['mascota'].nombre} - {cita_data['fecha']}")
        else:
            print("  ⚠️ No se encontró veterinario o mascotas para crear citas")
            
    except User.DoesNotExist:
        print("  ⚠️ Cliente no encontrado, saltando creación de citas")

def sincronizar_mascotas_con_pet():
    """Sincronizar mascotas del modelo Mascota con el modelo Pet"""
    from veterinaria.models import Mascota, Pet
    
    print("🔄 Sincronizando mascotas con modelo Pet...")
    
    mascotas = Mascota.objects.all()
    
    for mascota in mascotas:
        # Verificar si ya existe un Pet con este ID
        if not Pet.objects.filter(id=str(mascota.id)).exists():
            # Crear objeto Pet correspondiente
            Pet.objects.create(
                id=str(mascota.id),
                owner=mascota.propietario,
                name=mascota.nombre,
                species=mascota.especie,
                breed=mascota.raza,
                base_color=mascota.color,
                condition=mascota.condicion,
                age_years=int(mascota.edad.split()[0]) if mascota.edad.split()[0].isdigit() else 1,
                age_months=0,  # Por defecto 0 meses
                sex=mascota.sexo,
                service_history=[]
            )
            print(f"  ✅ Pet creado para {mascota.nombre} (ID: {mascota.id})")
        else:
            print(f"  ⚠️ Pet ya existe para {mascota.nombre} (ID: {mascota.id})")

def main():
    """Función principal"""
    print("🐾 Configurando Sistema Veterinario Mascota Feliz con DATOS REALES...")
    print("=" * 70)
    
    # Configurar Django
    setup_django()
    
    try:
        # Aplicar migraciones
        print("📋 1. Aplicando migraciones...")
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migraciones aplicadas\n")
        
        # Crear datos reales
        crear_superuser()
        crear_categorias_reales()
        crear_usuarios_reales()
        crear_productos_reales()
        crear_servicios_peluqueria_reales()
        crear_mascotas_reales()
        crear_citas_ejemplo()
        sincronizar_mascotas_con_pet()
        
        print("\n🎉 ¡Configuración completada con DATOS REALES!")
        print("=" * 70)
        print("🚀 Para iniciar el servidor ejecuta: python manage.py runserver")
        print("🌐 Luego visita: http://127.0.0.1:8000/")
        print("\n👥 Usuarios disponibles:")
        print("   👑 superadmin / admin123 (Super Administrador)")
        print("   🔑 admin / admin123 (Administrador)")
        print("   👨‍⚕️ dr_martinez / vet123 (Dr. Carlos Martínez)")
        print("   👨‍⚕️ dra_rodriguez / vet123 (Dra. María Rodríguez)")
        print("   👨‍⚕️ dr_gonzalez / vet123 (Dr. Pedro González)")
        print("   👨‍⚕️ dra_lopez / vet123 (Dra. Ana López)")
        print("   👨‍⚕️ dr_silva / vet123 (Dr. Roberto Silva)")
        print("   👨‍⚕️ veterinario1 / vet123 (Dr. Carlos Mendoza)")
        print("   ✂️ peluquero1 / peluquero123 (María González)")
        print("   ✂️ peluquero2 / peluquero123 (Carlos Rodríguez)")
        print("   ✂️ peluquero3 / peluquero123 (Ana Martínez)")
        print("   💊 farmaceutico1 / farm123 (María González)")
        print("   👤 cliente1 / cliente123 (Juan Pérez - con mascotas y citas)")
        
        print("\n🏠 El home ahora muestra:")
        print("   🐕 Mascotas reales del cliente1")
        print("   📅 Próximas citas programadas")
        print("   🖼️ Productos y servicios con imágenes")
        print("   📄 Fichas médicas descargables")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    main() 