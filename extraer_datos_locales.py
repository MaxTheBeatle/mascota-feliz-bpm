#!/usr/bin/env python
"""
Script para extraer todos los datos de la base de datos local
y generar el código para replicarlos exactamente
"""

import os
import sys
import django
from decimal import Decimal

def setup_django():
    """Configurar Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mascota_feliz.settings')
    django.setup()

def extraer_usuarios():
    """Extraer todos los usuarios con sus datos completos"""
    from veterinaria.models import User, Veterinario, Peluquero, Farmaceutico
    
    print("# ===== USUARIOS =====")
    usuarios = User.objects.all()
    
    for user in usuarios:
        print(f"\n# Usuario: {user.username}")
        print(f"if not User.objects.filter(username='{user.username}').exists():")
        
        # Determinar si es superuser
        if user.is_superuser:
            print(f"    user = User.objects.create_superuser(")
        else:
            print(f"    user = User.objects.create_user(")
        
        print(f"        username='{user.username}',")
        print(f"        email='{user.email}',")
        print(f"        password='admin123',")  # Contraseña por defecto
        print(f"        first_name='{user.first_name}',")
        print(f"        last_name='{user.last_name}',")
        print(f"        is_staff={user.is_staff},")
        print(f"        region='{user.region}',")
        print(f"        phone='{user.phone}'")
        print(f"    )")
        
        # Verificar si tiene perfil de veterinario
        try:
            vet = Veterinario.objects.get(user=user)
            print(f"    Veterinario.objects.create(")
            print(f"        user=user,")
            print(f"        especialidad='{vet.especialidad}',")
            print(f"        telefono='{vet.telefono}'")
            print(f"    )")
        except Veterinario.DoesNotExist:
            pass
        
        # Verificar si tiene perfil de peluquero
        try:
            pel = Peluquero.objects.get(user=user)
            print(f"    Peluquero.objects.create(")
            print(f"        user=user,")
            print(f"        telefono='{pel.telefono}',")
            print(f"        experiencia_años={pel.experiencia_años}")
            print(f"    )")
        except Peluquero.DoesNotExist:
            pass
        
        # Verificar si tiene perfil de farmacéutico
        try:
            farm = Farmaceutico.objects.get(user=user)
            print(f"    Farmaceutico.objects.create(")
            print(f"        user=user,")
            print(f"        telefono='{farm.telefono}',")
            print(f"        numero_registro='{farm.numero_registro}',")
            print(f"        especialidad='{farm.especialidad}',")
            print(f"        experiencia_años={farm.experiencia_años}")
            print(f"    )")
        except Farmaceutico.DoesNotExist:
            pass

def extraer_categorias():
    """Extraer categorías de productos"""
    from veterinaria.models import Categoria
    
    print("\n\n# ===== CATEGORÍAS =====")
    categorias = Categoria.objects.all()
    
    for cat in categorias:
        print(f"Categoria.objects.get_or_create(")
        print(f"    nombre='{cat.nombre}',")
        print(f"    defaults={{'descripcion': '{cat.descripcion}'}}")
        print(f")")

def extraer_productos():
    """Extraer todos los productos"""
    from veterinaria.models import Producto
    
    print("\n\n# ===== PRODUCTOS =====")
    productos = Producto.objects.all()
    
    for prod in productos:
        print(f"\nProducto.objects.get_or_create(")
        print(f"    nombre='{prod.nombre}',")
        print(f"    defaults={{")
        print(f"        'descripcion': '{prod.descripcion}',")
        print(f"        'precio': Decimal('{prod.precio}'),")
        print(f"        'categoria': Categoria.objects.get(nombre='{prod.categoria.nombre}'),")
        print(f"        'stock': {prod.stock},")
        print(f"        'es_destacado': {prod.es_destacado}")
        print(f"    }}")
        print(f")")

def extraer_servicios_peluqueria():
    """Extraer servicios de peluquería"""
    from veterinaria.models import ServicioPeluqueria, CategoriaServicioPeluqueria
    
    print("\n\n# ===== CATEGORÍAS SERVICIOS PELUQUERÍA =====")
    categorias = CategoriaServicioPeluqueria.objects.all()
    
    for cat in categorias:
        print(f"CategoriaServicioPeluqueria.objects.get_or_create(")
        print(f"    nombre='{cat.nombre}',")
        print(f"    defaults={{")
        print(f"        'descripcion': '{cat.descripcion}',")
        print(f"        'icono': '{cat.icono}',")
        print(f"        'activo': {cat.activo}")
        print(f"    }}")
        print(f")")
    
    print("\n\n# ===== SERVICIOS PELUQUERÍA =====")
    servicios = ServicioPeluqueria.objects.all()
    
    for serv in servicios:
        print(f"\nServicioPeluqueria.objects.get_or_create(")
        print(f"    nombre='{serv.nombre}',")
        print(f"    defaults={{")
        print(f"        'descripcion': '{serv.descripcion}',")
        print(f"        'precio_base': Decimal('{serv.precio_base}'),")
        print(f"        'duracion_estimada': {serv.duracion_estimada},")
        print(f"        'categoria': CategoriaServicioPeluqueria.objects.get(nombre='{serv.categoria.nombre}'),")
        print(f"        'tipo_mascota': '{serv.tipo_mascota}',")
        print(f"        'tamaño_mascota': '{serv.tamaño_mascota}',")
        print(f"        'incluye': '{serv.incluye}',")
        print(f"        'recomendaciones': '{serv.recomendaciones}',")
        print(f"        'activo': {serv.activo}")
        print(f"    }}")
        print(f")")

def extraer_medicamentos():
    """Extraer medicamentos"""
    from veterinaria.models import Medicamento, CategoriaFarmacia
    
    print("\n\n# ===== CATEGORÍAS FARMACIA =====")
    categorias = CategoriaFarmacia.objects.all()
    
    for cat in categorias:
        print(f"CategoriaFarmacia.objects.get_or_create(")
        print(f"    nombre='{cat.nombre}',")
        print(f"    defaults={{")
        print(f"        'descripcion': '{cat.descripcion}',")
        print(f"        'icono': '{cat.icono}'")
        print(f"    }}")
        print(f")")
    
    print("\n\n# ===== MEDICAMENTOS =====")
    medicamentos = Medicamento.objects.all()
    
    for med in medicamentos:
        print(f"\nMedicamento.objects.get_or_create(")
        print(f"    nombre='{med.nombre}',")
        print(f"    defaults={{")
        print(f"        'nombre_generico': '{med.nombre_generico}',")
        print(f"        'categoria': CategoriaFarmacia.objects.get(nombre='{med.categoria.nombre}'),")
        print(f"        'tipo': '{med.tipo}',")
        print(f"        'presentacion': '{med.presentacion}',")
        print(f"        'concentracion': '{med.concentracion}',")
        print(f"        'laboratorio': '{med.laboratorio}',")
        print(f"        'descripcion': '{med.descripcion}',")
        print(f"        'indicaciones': '{med.indicaciones}',")
        print(f"        'contraindicaciones': '{med.contraindicaciones}',")
        print(f"        'efectos_secundarios': '{med.efectos_secundarios}',")
        print(f"        'dosis_recomendada': '{med.dosis_recomendada}',")
        print(f"        'precio': Decimal('{med.precio}'),")
        print(f"        'stock': {med.stock},")
        print(f"        'stock_minimo': {med.stock_minimo},")
        print(f"        'requiere_receta': {med.requiere_receta},")
        print(f"        'activo': {med.activo}")
        print(f"    }}")
        print(f")")

def extraer_mascotas():
    """Extraer mascotas"""
    from veterinaria.models import Mascota
    
    print("\n\n# ===== MASCOTAS =====")
    mascotas = Mascota.objects.all()
    
    for mascota in mascotas:
        print(f"\nMascota.objects.get_or_create(")
        print(f"    id={mascota.id},")
        print(f"    defaults={{")
        print(f"        'nombre': '{mascota.nombre}',")
        print(f"        'especie': '{mascota.especie}',")
        print(f"        'raza': '{mascota.raza}',")
        print(f"        'color': '{mascota.color}',")
        print(f"        'condicion': '{mascota.condicion}',")
        print(f"        'edad': '{mascota.edad}',")
        print(f"        'sexo': '{mascota.sexo}',")
        if mascota.propietario:
            print(f"        'propietario': User.objects.get(username='{mascota.propietario.username}')")
        else:
            print(f"        'propietario': None")
        print(f"    }}")
        print(f")")

def main():
    """Función principal"""
    print("#!/usr/bin/env python")
    print('"""')
    print("Script con datos exactos de la base de datos local")
    print("Generado automáticamente desde extraer_datos_locales.py")
    print('"""')
    print()
    print("import os")
    print("import sys")
    print("import django")
    print("from decimal import Decimal")
    print()
    print("def setup_django():")
    print("    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mascota_feliz.settings')")
    print("    django.setup()")
    print()
    print("def crear_datos_exactos():")
    print("    from veterinaria.models import *")
    print("    from django.core.management import execute_from_command_line")
    print()
    print("    # Aplicar migraciones")
    print("    execute_from_command_line(['manage.py', 'migrate'])")
    print()
    
    # Configurar Django
    setup_django()
    
    # Extraer todos los datos
    extraer_usuarios()
    extraer_categorias()
    extraer_productos()
    extraer_servicios_peluqueria()
    extraer_medicamentos()
    extraer_mascotas()
    
    print("\n\nif __name__ == '__main__':")
    print("    setup_django()")
    print("    crear_datos_exactos()")
    print("    print('✅ Datos exactos creados correctamente')")

if __name__ == '__main__':
    main() 