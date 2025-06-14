from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from veterinaria.models import Mascota, Servicio
import os

class Command(BaseCommand):
    help = 'Importa datos desde el archivo HTML de la base de datos'

    def handle(self, *args, **options):
        # Leer el archivo HTML
        html_path = os.path.join('veterinaria', 'templates', 'veterinaria', 'Base de datos.html')
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')

        # Encontrar la tabla
        table = soup.find('table', class_='waffle')
        if not table:
            self.stdout.write(self.style.ERROR('No se encontró la tabla en el archivo HTML'))
            return

        # Obtener todas las filas excepto el encabezado
        rows = table.find_all('tr')[1:]  # Ignorar la primera fila (encabezados)
        
        mascotas_procesadas = set()
        mascota_id = 1  # Iniciar con ID 1
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 11:  # Verificar que la fila tenga todas las columnas necesarias
                continue

            # Si ya procesamos esta mascota, continuamos con la siguiente fila
            nombre_mascota = cells[1].text.strip()
            if nombre_mascota in mascotas_procesadas:
                # Solo crear el servicio para esta mascota
                mascota = Mascota.objects.get(nombre=nombre_mascota)
                servicio = Servicio(
                    mascota=mascota,
                    tipo_servicio=cells[8].text.strip(),
                    tipo_reserva=cells[9].text.strip(),
                    region=cells[10].text.strip()
                )
                servicio.save()
                continue
                
            # Si es una nueva mascota, la creamos
            mascota = Mascota(
                id=mascota_id,
                nombre=nombre_mascota,
                raza=cells[2].text.strip(),
                color=cells[3].text.strip(),
                especie=cells[4].text.strip(),
                condicion=cells[5].text.strip(),
                edad=cells[6].text.strip(),
                sexo=cells[7].text.strip()
            )
            mascota.save()
            mascotas_procesadas.add(nombre_mascota)
            
            # Crear el servicio asociado
            servicio = Servicio(
                mascota=mascota,
                tipo_servicio=cells[8].text.strip(),
                tipo_reserva=cells[9].text.strip(),
                region=cells[10].text.strip()
            )
            servicio.save()
            
            mascota_id += 1  # Incrementar el ID para la siguiente mascota

        self.stdout.write(
            self.style.SUCCESS(f'Se importaron exitosamente {len(mascotas_procesadas)} mascotas y sus servicios')
        ) 