# 🐾 Mascota Feliz - Sistema Veterinario Integral

Sistema completo de gestión veterinaria desarrollado en Django que incluye clínica veterinaria, peluquería profesional, tienda de productos y farmacia.

## 🌟 Características Principales

### 🏥 Clínica Veterinaria
- **Gestión de mascotas** y propietarios
- **Sistema de citas médicas** con veterinarios
- **Fichas médicas** completas con historial
- **Panel de veterinario** con control total de citas
- **Gestión de recetas** médicas

### ✂️ Peluquería Profesional
- **Catálogo de servicios** de peluquería canina
- **Sistema de citas** especializadas
- **Panel de peluquero** con gestión completa
- **Control de estados** de citas (programada, confirmada, en proceso, completada)
- **Subida de fotos** antes/después del servicio

### 🛒 Tienda de Productos
- **Catálogo de productos** para mascotas
- **Sistema de carrito** de compras
- **Gestión de pedidos** y envíos
- **Categorización** de productos
- **Control de inventario**

### 💊 Farmacia Veterinaria
- **Catálogo de medicamentos** veterinarios
- **Sistema de recetas** médicas
- **Reserva de medicamentos** con y sin receta
- **Control de stock** y disponibilidad

## 🚀 Tecnologías Utilizadas

- **Backend:** Django 5.0.1
- **Frontend:** Bootstrap 5 + HTML/CSS/JavaScript
- **Base de Datos:** SQLite (desarrollo)
- **Autenticación:** Sistema Django integrado
- **Gestión de archivos:** Django File Storage

## 📋 Requisitos del Sistema

- Python 3.8+
- Django 5.0.1
- Pillow (para manejo de imágenes)
- django-crispy-forms
- crispy-bootstrap5

## ⚙️ Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/mascota-feliz.git
cd mascota-feliz
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor:**
```bash
python manage.py runserver
```

## 👥 Tipos de Usuario

### 🔑 Cliente
- Gestionar mascotas personales
- Agendar citas médicas y de peluquería
- Realizar compras en la tienda
- Ver historial médico de mascotas

### 👨‍⚕️ Veterinario
- Dashboard con estadísticas
- Gestión completa de citas médicas
- Crear y editar fichas médicas
- Prescribir medicamentos

### ✂️ Peluquero
- Dashboard especializado
- Control total de citas de peluquería
- Subida de fotos antes/después
- Gestión de estados de servicio

### 👨‍💼 Administrador
- Acceso completo al sistema
- Gestión de usuarios y personal
- Estadísticas generales
- Configuración del sistema

## 🗂️ Estructura del Proyecto

```
mascota_feliz/
├── mascota_feliz/          # Configuración principal
├── veterinaria/            # App principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Lógica de negocio
│   ├── forms.py           # Formularios
│   ├── urls.py            # URLs de la app
│   └── templates/         # Templates HTML
├── media/                 # Archivos subidos
├── static/               # Archivos estáticos
├── requirements.txt      # Dependencias
└── manage.py            # Comando Django
```

## 🎯 Funcionalidades Destacadas

### 📊 Dashboard Inteligente
- Estadísticas en tiempo real
- Citas del día y próximas
- Indicadores de rendimiento

### 🔄 Gestión de Estados
- Control completo del flujo de citas
- Estados: Programada → Confirmada → En Proceso → Completada
- Notificaciones automáticas

### 📱 Diseño Responsivo
- Interfaz moderna con Bootstrap 5
- Adaptable a dispositivos móviles
- UX optimizada para todos los roles

### 🔐 Seguridad
- Autenticación robusta
- Permisos por tipo de usuario
- Protección de datos sensibles

## 🌐 URLs Principales

- `/` - Página principal
- `/admin/` - Panel de administración Django
- `/peluqueria/` - Catálogo de peluquería
- `/tienda/` - Tienda de productos
- `/farmacia/` - Farmacia veterinaria
- `/veterinario/dashboard/` - Panel veterinario
- `/peluquero/dashboard/` - Panel peluquero

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

## 🙏 Agradecimientos

- Django Community por el excelente framework
- Bootstrap team por el sistema de diseño
- Todos los contribuidores del proyecto

---

⭐ **¡No olvides dar una estrella al proyecto si te fue útil!** ⭐ 