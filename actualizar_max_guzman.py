#!/usr/bin/env python
"""
Script para actualizar cliente1 a Max Guzman con sus mascotas específicas
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mascota_feliz.settings')
django.setup()

from django.contrib.auth import get_user_model
from veterinaria.models import Mascota, Pet

User = get_user_model()

def actualizar_max_guzman():
    """Actualizar cliente1 a Max Guzman"""
    print("👤 Actualizando cliente1 a Max Guzman...")
    
    try:
        cliente1 = User.objects.get(username='cliente1')
        cliente1.first_name = 'Max'
        cliente1.last_name = 'Guzman'
        cliente1.email = 'max.guzman@example.com'
        cliente1.region = 'Región Metropolitana'
        cliente1.save()
        print("✅ Cliente1 actualizado a Max Guzman")
        return cliente1
    except User.DoesNotExist:
        print("❌ Cliente1 no encontrado")
        return None

def crear_mascotas_max():
    """Crear mascotas específicas para Max Guzman"""
    print("🐕 Creando mascotas para Max Guzman...")
    
    cliente = User.objects.get(username='cliente1')
    
    # Eliminar mascotas existentes del cliente1
    mascotas_existentes = Mascota.objects.filter(propietario=cliente)
    pets_existentes = Pet.objects.filter(owner=cliente)
    
    print(f"  🗑️ Eliminando {mascotas_existentes.count()} mascotas existentes...")
    mascotas_existentes.delete()
    pets_existentes.delete()
    
    # Crear solo las dos mascotas específicas
    mascotas_data = [
        (1, 'Nacho', 'Gato', 'Mestizo', 'Naranja', 'Normal', '2 años', 'Macho'),
        (2, 'Polo', 'Perro', 'Labrador', 'Negro', 'Normal', '3 años', 'Macho')
    ]
    
    mascotas_creadas = []
    
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
            propietario=cliente
        )
        
        # Crear Pet correspondiente
        Pet.objects.create(
            id=str(id_mascota),
            owner=cliente,
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
        
        mascotas_creadas.append(mascota)
        print(f"  ✅ {nombre} ({especie}) creado")
    
    return mascotas_creadas

def crear_citas_ejemplo():
    """Crear citas de ejemplo para las mascotas de Max"""
    from veterinaria.models import Cita, Veterinario
    from datetime import date, timedelta
    
    print("📅 Creando citas de ejemplo...")
    
    try:
        cliente = User.objects.get(username='cliente1')
        veterinario = Veterinario.objects.first()
        mascotas = Mascota.objects.filter(propietario=cliente)
        
        if veterinario and mascotas.exists():
            # Eliminar citas existentes
            Cita.objects.filter(mascota__propietario=cliente).delete()
            
            # Crear nuevas citas
            citas_data = [
                {
                    'fecha': date.today() + timedelta(days=5),
                    'hora': '10:00',
                    'motivo': 'Control de rutina y vacunación',
                    'mascota': mascotas.get(nombre='Nacho'),
                },
                {
                    'fecha': date.today() + timedelta(days=12),
                    'hora': '15:30',
                    'motivo': 'Revisión general y desparasitación',
                    'mascota': mascotas.get(nombre='Polo'),
                }
            ]
            
            for cita_data in citas_data:
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
            print("  ⚠️ No se encontró veterinario para crear citas")
            
    except Exception as e:
        print(f"  ❌ Error creando citas: {e}")

def main():
    """Función principal"""
    print("🔄 Actualizando datos de Max Guzman...")
    print("=" * 50)
    
    try:
        # Actualizar usuario
        cliente = actualizar_max_guzman()
        if not cliente:
            return
        
        # Crear mascotas específicas
        mascotas = crear_mascotas_max()
        
        # Crear citas de ejemplo
        crear_citas_ejemplo()
        
        print("\n✅ Actualización completada!")
        print("=" * 50)
        print(f"👤 Usuario: {cliente.first_name} {cliente.last_name}")
        print(f"📧 Email: {cliente.email}")
        print("🐕 Mascotas:")
        
        for mascota in Mascota.objects.filter(propietario=cliente):
            print(f"   • {mascota.nombre} ({mascota.especie}) - {mascota.raza}")
        
        print(f"\n📅 Citas programadas: {Cita.objects.filter(mascota__propietario=cliente).count()}")
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 