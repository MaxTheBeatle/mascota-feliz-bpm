# Mascota Feliz - Sistema de Gestión Veterinaria

Sistema web para la gestión de una clínica veterinaria, desarrollado con Django.

## Características

- Gestión de mascotas y sus propietarios
- Sistema de citas médicas
- Tienda en línea de productos veterinarios
- Carrito de compras
- Sistema de pedidos
- Diseño responsive con Bootstrap 5

## Tecnologías Utilizadas

- Python 3.x
- Django 5.0
- Bootstrap 5
- SQLite
- Font Awesome 6

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/MaxTheBeatle/mascota-feliz.git
cd mascota-feliz
```

2. Crear un entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Realizar las migraciones:
```bash
python manage.py migrate
```

4. Crear un superusuario:
```bash
python manage.py createsuperuser
```

5. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

- `veterinaria/`: Aplicación principal
  - `models.py`: Modelos de datos (Mascota, Cita, Producto, etc.)
  - `views.py`: Vistas y lógica de negocio
  - `templates/`: Plantillas HTML
  - `static/`: Archivos estáticos (CSS, JS, imágenes)

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

## Contacto

MaxTheBeatle - [GitHub Profile](https://github.com/MaxTheBeatle)

Link del proyecto: [https://github.com/MaxTheBeatle/mascota-feliz](https://github.com/MaxTheBeatle/mascota-feliz) 