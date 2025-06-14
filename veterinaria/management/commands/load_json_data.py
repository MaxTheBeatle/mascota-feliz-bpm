from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from veterinaria.models import Pet, Service
import json
from datetime import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Load data from JSON file and create sample users'

    def handle(self, *args, **kwargs):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@mascotafeliz.com',
                'is_staff': True,
                'is_superuser': True,
                'is_admin': True,
                'region': 'Región Metropolitana'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Create client user
        client_user, created = User.objects.get_or_create(
            username='cliente1',
            defaults={
                'email': 'cliente1@example.com',
                'is_admin': False,
                'region': 'Región de Los Lagos',
                'phone': '+56912345678'
            }
        )
        if created:
            client_user.set_password('cliente123')
            client_user.save()
            self.stdout.write(self.style.SUCCESS('Client user created'))

        # Load JSON data
        with open('tableConvert.com_kdpml7.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Get two random pets for the client
        sample_pets = data[:2]  # Get first two pets for simplicity
        
        for pet_data in sample_pets:
            # Parse age
            age_str = pet_data['Edad del animal']
            age_parts = age_str.split()
            years = int(age_parts[0])
            months = int(age_parts[3]) if len(age_parts) > 4 else 0

            # Create pet
            pet = Pet.objects.create(
                id=pet_data['id'],
                owner=client_user,
                name=pet_data['Nombre Animal'],
                species=pet_data['Especie'],
                breed=pet_data['Raza'],
                base_color=pet_data['Color Base'],
                condition=pet_data['Condicion'],
                age_years=years,
                age_months=months,
                sex=pet_data['Sexo']
            )

            # Create service
            Service.objects.create(
                pet=pet,
                service_type=pet_data['Tipo de Servicio'],
                reservation_type=pet_data['Tipo de Reserva'],
                date=datetime.now().date()
            )

            self.stdout.write(self.style.SUCCESS(f'Created pet: {pet.name}')) 