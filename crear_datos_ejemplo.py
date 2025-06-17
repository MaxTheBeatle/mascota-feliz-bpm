#!/usr/bin/env python
"""
Script para crear datos de ejemplo del sistema Mascota Feliz
Incluye Max Guzman con sus mascotas específicas: Nacho (gato) y Polo (perro)
"""

import os
import sys
import django
from datetime import date, timedelta, datetime
from decimal import Decimal
from io import BytesIO
from django.core.files.base import ContentFile

def setup_django():
    """Configurar Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mascota_feliz.settings')
    django.setup()

def crear_superuser():
    """Crear superusuario si no existe"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@mascotafeliz.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            region='Región Metropolitana',
            phone='+56912345678'
        )
        print("✅ Superusuario 'admin' creado")
    else:
        print("ℹ️ Superusuario 'admin' ya existe")

def crear_usuarios_completos():
    """Crear todos los usuarios del sistema incluyendo Max Guzman"""
    from veterinaria.models import User, Veterinario, Peluquero, Farmaceutico
    
    print("👥 Creando usuarios del sistema...")
    
    # Max Guzman - Cliente principal
    if not User.objects.filter(username='cliente1').exists():
        User.objects.create_user(
            username='cliente1',
            email='max.guzman@example.com',
            password='cliente123',
            first_name='Max',
            last_name='Guzman',
            region='Región Metropolitana',
            phone='+56912345678'
        )
        print("✅ Max Guzman (cliente1) creado")
    else:
        # Actualizar datos existentes
        cliente1 = User.objects.get(username='cliente1')
        cliente1.first_name = 'Max'
        cliente1.last_name = 'Guzman'
        cliente1.email = 'max.guzman@example.com'
        cliente1.region = 'Región Metropolitana'
        cliente1.save()
        print("✅ Max Guzman (cliente1) actualizado")

    # Clientes adicionales
    clientes_data = [
        ('cliente2', 'ana.martinez@example.com', 'Ana', 'Martínez', 'Región de Valparaíso'),
        ('cliente3', 'carlos.lopez@example.com', 'Carlos', 'López', 'Región del Biobío'),
        ('cliente4', 'maria.gonzalez@example.com', 'María', 'González', 'Región de Los Lagos'),
        ('cliente5', 'pedro.rodriguez@example.com', 'Pedro', 'Rodríguez', 'Región de Coquimbo'),
        ('cliente6', 'laura.fernandez@example.com', 'Laura', 'Fernández', 'Región de La Araucanía'),
        ('cliente7', 'jose.silva@example.com', 'José', 'Silva', 'Región de Antofagasta'),
        ('cliente8', 'sofia.torres@example.com', 'Sofía', 'Torres', 'Región de Atacama'),
        ('cliente9', 'diego.morales@example.com', 'Diego', 'Morales', 'Región de Tarapacá'),
    ]
    
    for username, email, first_name, last_name, region in clientes_data:
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                password='cliente123',
                first_name=first_name,
                last_name=last_name,
                region=region,
                phone='+56987654321'
            )
            print(f"✅ Cliente {username} ({first_name} {last_name}) creado")

    # Veterinarios
    veterinarios_data = [
        ('veterinario1', 'carlos.mendoza@mascotafeliz.cl', 'Carlos', 'Mendoza', 'Medicina General', '+56912345678'),
        ('veterinario2', 'maria.rodriguez@mascotafeliz.cl', 'María', 'Rodríguez', 'Cirugía Veterinaria', '+56987654321'),
        ('veterinario3', 'pedro.gonzalez@mascotafeliz.cl', 'Pedro', 'González', 'Dermatología Veterinaria', '+56976543210'),
    ]
    
    for username, email, first_name, last_name, especialidad, telefono in veterinarios_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password='vet123',
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                region='Región Metropolitana',
                phone=telefono
            )
            
            Veterinario.objects.create(
                user=user,
                especialidad=especialidad,
                telefono=telefono
            )
            print(f"✅ Veterinario {username} ({first_name} {last_name}) creado")

    # Peluqueros
    peluqueros_data = [
        ('peluquero1', 'maria.peluquera@mascotafeliz.cl', 'María', 'Estilista', '+56965432109', 8),
        ('peluquero2', 'carlos.peluquero@mascotafeliz.cl', 'Carlos', 'Cortés', '+56954321098', 5),
        ('peluquero3', 'ana.groomer@mascotafeliz.cl', 'Ana', 'Belleza', '+56943210987', 12)
    ]
    
    for username, email, first_name, last_name, telefono, experiencia in peluqueros_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password='peluquero123',
                first_name=first_name,
                last_name=last_name,
                region='Región Metropolitana',
                phone=telefono
            )
            
            Peluquero.objects.create(
                user=user,
                telefono=telefono,
                experiencia_años=experiencia
            )
            print(f"✅ Peluquero {username} ({first_name} {last_name}) creado")

    # Farmacéuticos
    farmaceuticos_data = [
        ('farmaceutico1', 'lucia.farmacia@mascotafeliz.cl', 'Lucía', 'Medicamentos', '+56932109876', 'FARM001'),
        ('farmaceutico2', 'roberto.farmacia@mascotafeliz.cl', 'Roberto', 'Recetas', '+56921098765', 'FARM002'),
    ]
    
    for username, email, first_name, last_name, telefono, registro in farmaceuticos_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password='farm123',
                first_name=first_name,
                last_name=last_name,
                region='Región Metropolitana',
                phone=telefono
            )
            
            Farmaceutico.objects.create(
                user=user,
                telefono=telefono,
                numero_registro=registro,
                especialidad='Farmacia Veterinaria',
                experiencia_años=6
            )
            print(f"✅ Farmacéutico {username} ({first_name} {last_name}) creado")

def crear_categorias():
    """Crear todas las categorías del sistema"""
    from veterinaria.models import Categoria, CategoriaServicioPeluqueria, CategoriaFarmacia
    
    print("📂 Creando categorías...")
    
    # Categorías de productos
    categorias_productos = [
        ('Alimentos', 'Alimentos para mascotas'),
        ('Juguetes', 'Juguetes y entretenimiento'),
        ('Cuidado', 'Productos de cuidado e higiene'),
        ('Accesorios', 'Accesorios y complementos'),
        ('Salud', 'Productos de salud y medicina'),
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
            defaults={'descripcion': descripcion, 'activo': True}
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

def crear_productos():
    """Crear productos de la tienda"""
    from veterinaria.models import Producto, Categoria
    
    print("🛒 Creando productos...")
    
    productos_data = [
        ('Royal Canin Adult', 'Alimento premium para perros adultos', '25990', 'Alimentos', True),
        ('Whiskas Gatitos', 'Alimento húmedo para gatitos', '1890', 'Alimentos', False),
        ('Pelota Kong Classic', 'Juguete resistente para perros', '8990', 'Juguetes', True),
        ('Rascador para Gatos', 'Torre rascadora con juguetes', '15990', 'Juguetes', False),
        ('Shampoo Hipoalergénico', 'Shampoo especial para pieles sensibles', '12500', 'Cuidado', True),
        ('Collar GPS Inteligente', 'Collar con GPS para seguimiento', '89990', 'Accesorios', True),
        ('Cama Ortopédica', 'Cama ortopédica para perros grandes', '45990', 'Accesorios', False),
        ('Snacks Dentales', 'Snacks para limpieza dental', '3990', 'Salud', False),
        ('Vitaminas para Cachorros', 'Suplemento vitamínico completo', '18990', 'Salud', False),
        ('Transportadora Premium', 'Transportadora para viajes seguros', '35990', 'Accesorios', False),
        ('Alimento Gatos Senior', 'Alimento especializado para gatos mayores', '22990', 'Alimentos', False),
    ]
    
    for nombre, descripcion, precio, categoria_nombre, destacado in productos_data:
        try:
            categoria = Categoria.objects.get(nombre=categoria_nombre)
            producto, created = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'categoria': categoria,
                    'descripcion': descripcion,
                    'precio': Decimal(precio),
                    'stock': 50,
                    'es_destacado': destacado
                }
            )
            if created:
                print(f"  ✅ {nombre}")
        except Categoria.DoesNotExist:
            print(f"  ⚠️ Categoría {categoria_nombre} no encontrada para {nombre}")

def crear_medicamentos():
    """Crear medicamentos de farmacia"""
    from veterinaria.models import Medicamento, CategoriaFarmacia
    
    print("💊 Creando medicamentos...")
    
    medicamentos_data = [
        ('Amoxicilina 250mg', 'Antibióticos', 'antibiotico', 'tableta', '250mg', 'LabVet', 'Antibiótico de amplio espectro', '8990', True),
        ('Meloxicam 5mg', 'Antiinflamatorios', 'antiinflamatorio', 'tableta', '5mg', 'PetPharma', 'Antiinflamatorio no esteroidal', '12500', True),
        ('Ivermectina 1%', 'Antiparasitarios', 'antiparasitario', 'inyectable', '1%', 'AnimalHealth', 'Antiparasitario interno y externo', '15990', True),
        ('Vitamina B Complex', 'Suplementos', 'vitamina', 'jarabe', '100ml', 'VitaPet', 'Complejo vitamínico B', '9990', False),
        ('Shampoo Medicado', 'Dermatológicos', 'dermatologico', 'suspension', '250ml', 'DermaPet', 'Shampoo para dermatitis', '18990', False),
        ('Dipirona 500mg', 'Antiinflamatorios', 'analgesico', 'tableta', '500mg', 'PainFree', 'Analgésico y antipirético', '6990', False),
        ('Drontal Plus', 'Antiparasitarios', 'desparasitante', 'tableta', '1 tab', 'Bayer', 'Desparasitante interno', '4990', False),
        ('Suero Fisiológico', 'Suplementos', 'otro', 'inyectable', '500ml', 'MedVet', 'Solución salina estéril', '3990', False),
        ('Gentamicina Gotas', 'Antibióticos', 'oftalmico', 'gotas', '10ml', 'EyeCare', 'Antibiótico oftálmico', '11990', True),
        ('Cortisona Crema', 'Dermatológicos', 'dermatologico', 'crema', '30g', 'SkinVet', 'Antiinflamatorio tópico', '14990', False),
        ('Vacuna Antirrábica', 'Suplementos', 'vacuna', 'inyectable', '1 dosis', 'VaccPet', 'Vacuna contra la rabia', '25990', True),
        ('Omeprazol 20mg', 'Suplementos', 'digestivo', 'capsula', '20mg', 'GastroPet', 'Protector gástrico', '16990', False),
        ('Furosemida 40mg', 'Suplementos', 'cardiaco', 'tableta', '40mg', 'CardioVet', 'Diurético para problemas cardíacos', '13990', True),
        ('Colirio Lubricante', 'Suplementos', 'oftalmico', 'gotas', '15ml', 'EyeComfort', 'Lubricante ocular', '8990', False),
    ]
    
    for nombre, categoria_nombre, tipo, presentacion, concentracion, laboratorio, descripcion, precio, requiere_receta in medicamentos_data:
        try:
            categoria = CategoriaFarmacia.objects.get(nombre=categoria_nombre)
            medicamento, created = Medicamento.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'categoria': categoria,
                    'tipo': tipo,
                    'presentacion': presentacion,
                    'concentracion': concentracion,
                    'laboratorio': laboratorio,
                    'descripcion': descripcion,
                    'indicaciones': f'Indicaciones para {nombre}',
                    'dosis_recomendada': 'Según prescripción veterinaria',
                    'precio': Decimal(precio),
                    'stock': 25,
                    'requiere_receta': requiere_receta,
                    'activo': True
                }
            )
            if created:
                print(f"  ✅ {nombre}")
        except CategoriaFarmacia.DoesNotExist:
            print(f"  ⚠️ Categoría {categoria_nombre} no encontrada para {nombre}")

def crear_servicios_peluqueria():
    """Crear servicios de peluquería"""
    from veterinaria.models import ServicioPeluqueria, CategoriaServicioPeluqueria
    
    print("✂️ Creando servicios de peluquería...")
    
    servicios_data = [
        ('Baño Completo', 'Baño y Secado', 'Baño con shampoo especializado y secado', '15000', 60, 'ambos'),
        ('Corte de Pelo Básico', 'Corte y Estilismo', 'Corte básico de mantenimiento', '20000', 45, 'ambos'),
        ('Corte de Uñas', 'Cuidado de Uñas', 'Corte profesional de uñas', '8000', 20, 'ambos'),
        ('Limpieza de Oídos', 'Limpieza', 'Limpieza profunda de oídos', '10000', 25, 'ambos'),
        ('Paquete Completo', 'Paquetes', 'Baño, corte, uñas y limpieza de oídos', '45000', 120, 'ambos'),
        ('Corte Estilo Poodle', 'Corte y Estilismo', 'Corte estilo poodle profesional', '35000', 90, 'perro'),
        ('Baño Medicado', 'Baño y Secado', 'Baño con shampoo medicado especial', '25000', 75, 'ambos'),
        ('Desenredado Profundo', 'Cuidado', 'Desenredado para pelo largo y enredado', '30000', 60, 'ambos'),
        ('Corte Higiénico', 'Corte y Estilismo', 'Corte en zonas íntimas e higiénicas', '12000', 30, 'ambos'),
        ('Limpieza Dental', 'Limpieza', 'Limpieza básica de dientes', '15000', 35, 'ambos'),
        ('Pedicure Completo', 'Cuidado de Uñas', 'Corte de uñas y limado', '12000', 30, 'ambos'),
        ('Baño Anti-Pulgas', 'Baño y Secado', 'Baño especializado anti-pulgas', '20000', 70, 'ambos'),
        ('Corte de Verano', 'Corte y Estilismo', 'Corte corto para época de calor', '18000', 50, 'perro'),
        ('Spa Relajante', 'Paquetes', 'Tratamiento spa completo', '60000', 150, 'ambos'),
        ('Limpieza de Glándulas', 'Limpieza', 'Limpieza de glándulas anales', '18000', 25, 'perro'),
        ('Corte Felino Especial', 'Corte y Estilismo', 'Corte especializado para gatos', '25000', 60, 'gato'),
        ('Tratamiento Antipulgas', 'Limpieza', 'Aplicación de tratamiento antipulgas', '22000', 40, 'ambos'),
        ('Paquete Premium', 'Paquetes', 'Servicio premium con todos los tratamientos', '80000', 180, 'ambos'),
    ]
    
    for nombre, categoria_nombre, descripcion, precio, duracion, tipo_mascota in servicios_data:
        try:
            categoria = CategoriaServicioPeluqueria.objects.get(nombre=categoria_nombre)
            servicio, created = ServicioPeluqueria.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'categoria': categoria,
                    'descripcion': descripcion,
                    'precio_base': Decimal(precio),
                    'duracion_estimada': duracion,
                    'tipo_mascota': tipo_mascota,
                    'tamaño_mascota': 'todos',
                    'incluye': f'Incluye {nombre.lower()}',
                    'activo': True
                }
            )
            if created:
                print(f"  ✅ {nombre}")
        except CategoriaServicioPeluqueria.DoesNotExist:
            print(f"  ⚠️ Categoría {categoria_nombre} no encontrada para {nombre}")

def crear_mascotas_max_guzman():
    """Crear las mascotas específicas de Max Guzman"""
    from veterinaria.models import Mascota, Pet, User
    
    print("🐕 Creando mascotas de Max Guzman...")
    
    try:
        max_guzman = User.objects.get(username='cliente1')
        
        # Eliminar mascotas existentes del cliente1
        Mascota.objects.filter(propietario=max_guzman).delete()
        Pet.objects.filter(owner=max_guzman).delete()
        
        # Crear las dos mascotas específicas
        mascotas_data = [
            (1, 'Nacho', 'Gato', 'Mestizo', 'Naranja', 'Normal', '2 años', 'Macho'),
            (2, 'Polo', 'Perro', 'Labrador', 'Negro', 'Normal', '3 años', 'Macho')
        ]
        
        for id_mascota, nombre, especie, raza, color, condicion, edad, sexo in mascotas_data:
            # Crear Mascota
            mascota = Mascota.objects.create(
                id=id_mascota,
                nombre=nombre,
                especie=especie,
                raza=raza,
                color=color,
                condicion=condicion,
                edad=edad,
                sexo=sexo,
                propietario=max_guzman
            )
            
            # Crear Pet correspondiente
            Pet.objects.create(
                id=str(id_mascota),
                owner=max_guzman,
                name=nombre,
                species=especie,
                breed=raza,
                base_color=color,
                condition=condicion,
                age_years=int(edad.split()[0]) if edad.split()[0].isdigit() else 2,
                age_months=0,
                sex=sexo,
                service_history=[]
            )
            
            print(f"  ✅ {nombre} ({especie}) creado")
            
    except User.DoesNotExist:
        print("  ⚠️ Max Guzman no encontrado")

def crear_mascotas_otros_clientes():
    """Crear mascotas para otros clientes"""
    from veterinaria.models import Mascota, Pet, User
    
    print("🐕 Creando mascotas para otros clientes...")
    
    # Datos de mascotas para otros clientes
    mascotas_otros = [
        # Cliente2 - Ana Martínez
        (3, 'cliente2', 'Luna', 'Perro', 'Golden Retriever', 'Dorado', 'Normal', '4 años', 'Hembra'),
        (4, 'cliente2', 'Simba', 'Gato', 'Persa', 'Blanco', 'Normal', '3 años', 'Macho'),
        
        # Cliente3 - Carlos López
        (5, 'cliente3', 'Rocky', 'Perro', 'Bulldog', 'Marrón', 'Normal', '5 años', 'Macho'),
        (6, 'cliente3', 'Mia', 'Gato', 'Siamés', 'Crema', 'Normal', '2 años', 'Hembra'),
        
        # Cliente4 - María González
        (7, 'cliente4', 'Max', 'Perro', 'Pastor Alemán', 'Negro y café', 'Normal', '6 años', 'Macho'),
        
        # Cliente5 - Pedro Rodríguez
        (8, 'cliente5', 'Bella', 'Perro', 'Cocker Spaniel', 'Café', 'Normal', '3 años', 'Hembra'),
        (9, 'cliente5', 'Whiskers', 'Gato', 'Angora', 'Gris', 'Normal', '4 años', 'Macho'),
        
        # Cliente6 - Laura Fernández
        (10, 'cliente6', 'Charlie', 'Perro', 'Beagle', 'Tricolor', 'Normal', '2 años', 'Macho'),
        
        # Cliente7 - José Silva
        (11, 'cliente7', 'Daisy', 'Perro', 'Chihuahua', 'Blanco', 'Normal', '1 año', 'Hembra'),
        (12, 'cliente7', 'Shadow', 'Gato', 'Negro Común', 'Negro', 'Normal', '5 años', 'Macho'),
        
        # Cliente8 - Sofía Torres
        (13, 'cliente8', 'Lola', 'Perro', 'Pug', 'Beige', 'Normal', '3 años', 'Hembra'),
    ]
    
    for id_mascota, username, nombre, especie, raza, color, condicion, edad, sexo in mascotas_otros:
        try:
            propietario = User.objects.get(username=username)
            
            # Crear Mascota solo si no existe
            if not Mascota.objects.filter(id=id_mascota).exists():
                mascota = Mascota.objects.create(
                    id=id_mascota,
                    nombre=nombre,
                    especie=especie,
                    raza=raza,
                    color=color,
                    condicion=condicion,
                    edad=edad,
                    sexo=sexo,
                    propietario=propietario
                )
                
                # Crear Pet correspondiente
                Pet.objects.create(
                    id=str(id_mascota),
                    owner=propietario,
                    name=nombre,
                    species=especie,
                    breed=raza,
                    base_color=color,
                    condition=condicion,
                    age_years=int(edad.split()[0]) if edad.split()[0].isdigit() else 2,
                    age_months=0,
                    sex=sexo,
                    service_history=[]
                )
                
                print(f"  ✅ {nombre} ({especie}) para {propietario.first_name}")
            
        except User.DoesNotExist:
            print(f"  ⚠️ Usuario {username} no encontrado")

def crear_citas_ejemplo():
    """Crear citas de ejemplo"""
    from veterinaria.models import Cita, Mascota, Veterinario, CitaPeluqueria, Peluquero
    
    print("📅 Creando citas de ejemplo...")
    
    # Citas veterinarias
    try:
        veterinario = Veterinario.objects.first()
        mascotas = Mascota.objects.all()[:8]  # Primeras 8 mascotas
        
        if veterinario and mascotas:
            citas_data = [
                (mascotas[0], date.today() + timedelta(days=3), '10:00', 'Control de rutina para Nacho'),
                (mascotas[1], date.today() + timedelta(days=5), '14:30', 'Vacunación anual para Polo'),
                (mascotas[2], date.today() + timedelta(days=7), '09:15', 'Revisión general para Luna'),
                (mascotas[3], date.today() + timedelta(days=10), '16:00', 'Control dental para Simba'),
                (mascotas[4], date.today() + timedelta(days=12), '11:30', 'Chequeo de rutina para Rocky'),
                (mascotas[5], date.today() + timedelta(days=15), '15:45', 'Consulta por alergias para Mia'),
            ]
            
            for mascota, fecha, hora, motivo in citas_data:
                if not Cita.objects.filter(mascota=mascota, fecha=fecha, hora=hora).exists():
                    Cita.objects.create(
                        mascota=mascota,
                        veterinario=veterinario,
                        fecha=fecha,
                        hora=hora,
                        motivo=motivo,
                        estado='programada'
                    )
                    print(f"  ✅ Cita para {mascota.nombre} - {fecha}")
    
    except Exception as e:
        print(f"  ⚠️ Error creando citas veterinarias: {e}")
    
    # Citas de peluquería
    try:
        peluquero = Peluquero.objects.first()
        if peluquero and mascotas:
            citas_peluqueria = [
                (mascotas[0], date.today() + timedelta(days=8), '10:00', '25000'),  # Nacho
                (mascotas[1], date.today() + timedelta(days=14), '14:00', '35000'), # Polo
                (mascotas[2], date.today() + timedelta(days=20), '11:30', '30000'), # Luna
            ]
            
            for mascota, fecha, hora, total in citas_peluqueria:
                if not CitaPeluqueria.objects.filter(mascota=mascota, fecha=fecha, hora=hora).exists():
                    CitaPeluqueria.objects.create(
                        cliente=mascota.propietario,
                        mascota=mascota,
                        peluquero=peluquero,
                        fecha=fecha,
                        hora=hora,
                        estado='programada',
                        total=Decimal(total),
                        telefono_contacto=mascota.propietario.phone or '+56912345678'
                    )
                    print(f"  ✅ Cita peluquería para {mascota.nombre} - {fecha}")
    
    except Exception as e:
        print(f"  ⚠️ Error creando citas de peluquería: {e}")

def main():
    """Función principal"""
    print("🐾 CONFIGURANDO SISTEMA MASCOTA FELIZ")
    print("=" * 60)
    print("👤 Incluye: Max Guzman con Nacho (gato) y Polo (perro)")
    print("=" * 60)
    
    # Configurar Django
    setup_django()
    
    try:
        # Aplicar migraciones
        print("\n📋 1. Aplicando migraciones...")
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migraciones aplicadas")
        
        # Crear datos
        print("\n👥 2. Creando usuarios...")
        crear_superuser()
        crear_usuarios_completos()
        
        print("\n📂 3. Creando categorías...")
        crear_categorias()
        
        print("\n🛒 4. Creando productos...")
        crear_productos()
        
        print("\n💊 5. Creando medicamentos...")
        crear_medicamentos()
        
        print("\n✂️ 6. Creando servicios de peluquería...")
        crear_servicios_peluqueria()
        
        print("\n🐕 7. Creando mascotas...")
        crear_mascotas_max_guzman()
        crear_mascotas_otros_clientes()
        
        print("\n📅 8. Creando citas...")
        crear_citas_ejemplo()
        
        print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
        print("=" * 60)
        print("🚀 Para iniciar: python manage.py runserver")
        print("🌐 Visita: http://127.0.0.1:8000/")
        print("\n👥 USUARIOS PRINCIPALES:")
        print("   🔑 admin / admin123 (Administrador)")
        print("   👤 cliente1 / cliente123 (Max Guzman)")
        print("   👨‍⚕️ veterinario1 / vet123 (Carlos Mendoza)")
        print("   ✂️ peluquero1 / peluquero123 (María Estilista)")
        print("   💊 farmaceutico1 / farm123 (Lucía Medicamentos)")
        
        print("\n🐾 MASCOTAS DE MAX GUZMAN:")
        print("   🐱 Nacho (Gato Mestizo Naranja)")
        print("   🐕 Polo (Perro Labrador Negro)")
        
        print("\n📊 RESUMEN DE DATOS:")
        from veterinaria.models import User, Mascota, Producto, Medicamento, ServicioPeluqueria, Cita
        print(f"   👥 Usuarios: {User.objects.count()}")
        print(f"   🐕 Mascotas: {Mascota.objects.count()}")
        print(f"   🛒 Productos: {Producto.objects.count()}")
        print(f"   💊 Medicamentos: {Medicamento.objects.count()}")
        print(f"   ✂️ Servicios: {ServicioPeluqueria.objects.count()}")
        print(f"   📅 Citas: {Cita.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    main() 