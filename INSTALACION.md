# 🚀 Guía de Instalación - Mascota Feliz

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:
- **Python 3.8 o superior** ([Descargar aquí](https://www.python.org/downloads/))
- **Git** ([Descargar aquí](https://git-scm.com/downloads))

## 🔧 Instalación Paso a Paso

### 1. 📥 Descargar el Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/MaxTheBeatle/mascota-feliz-bpm.git

# Entrar al directorio
cd mascota-feliz-bpm
```

### 2. 🐍 Crear Entorno Virtual

**En Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 📦 Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. 🗄️ Configurar Base de Datos

**Opción A: Configuración Automática (Recomendada)**
```bash
python crear_datos_ejemplo.py
```

**Opción B: Configuración Manual**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data.json
```

### 5. 🚀 Iniciar el Servidor

```bash
python manage.py runserver
```

### 6. 🌐 Acceder al Sistema

Abre tu navegador y ve a: **http://127.0.0.1:8000/**

## 👥 Usuarios de Prueba

Una vez configurado, puedes usar estos usuarios de ejemplo:

### 🔑 Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Acceso:** Panel de administración completo

### 👨‍⚕️ Veterinario
- **Usuario:** `veterinario1`
- **Contraseña:** `vet123`
- **Nombre:** Dr. Carlos Mendoza
- **Especialidad:** Medicina General

### ✂️ Peluquero
- **Usuario:** `peluquero1`
- **Contraseña:** `peluquero123`
- **Nombre:** María González
- **Experiencia:** 8 años

### 👤 Cliente
- **Usuario:** `cliente1`
- **Contraseña:** `cliente123`
- **Funciones:** Gestionar mascotas, agendar citas, comprar productos

## 🏠 Navegación del Sistema

Una vez que inicies sesión, puedes acceder a:

- **🏠 Inicio:** Página principal con información general
- **🏥 Citas Médicas:** Sistema de citas veterinarias
- **✂️ Peluquería:** Catálogo y citas de peluquería
- **🛒 Tienda:** Productos para mascotas
- **💊 Farmacia:** Medicamentos veterinarios
- **👤 Mi Perfil:** Gestión de datos personales

## 🔧 Solución de Problemas

### ❌ Error: "No module named 'django'"
```bash
# Asegúrate de que el entorno virtual esté activado
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### ❌ Error de Base de Datos
```bash
# Eliminar base de datos actual y recrear
rm db.sqlite3
python crear_datos_ejemplo.py
```

### ❌ Error de Puerto en Uso
```bash
# Usar un puerto diferente
python manage.py runserver 8080
# Luego accede a: http://127.0.0.1:8080/
```

## 📁 Datos Incluidos

El sistema viene preconfigurado con:

### 🐕 Mascotas de Ejemplo
- Max (Golden Retriever, 3 años)
- Luna (Persa, 2 años)
- Propietarios asignados

### 🛒 Productos de Tienda
- Alimentos para perros y gatos
- Juguetes y accesorios
- Productos de higiene y salud
- Precios en pesos chilenos (CLP)

### 💊 Medicamentos
- Antibióticos (Amoxicilina)
- Suplementos vitamínicos
- Antiinflamatorios
- Control de recetas médicas

### ✂️ Servicios de Peluquería
- Baño completo ($15.000)
- Corte de pelo ($20.000)
- Corte de uñas ($8.000)
- Limpieza de oídos ($10.000)
- Paquete completo ($45.000)

## 🆘 Soporte

Si tienes problemas con la instalación:

1. **Verifica los requisitos:** Python 3.8+ y Git instalados
2. **Revisa el entorno virtual:** Debe estar activado
3. **Consulta los logs:** Revisa los mensajes de error en la consola
4. **Reinstala:** Elimina el directorio y clona nuevamente

## 📧 Contacto

Para soporte técnico o consultas:
- **GitHub Issues:** [Crear issue](https://github.com/MaxTheBeatle/mascota-feliz-bpm/issues)
- **Email:** Contacta al desarrollador

---

🎉 **¡Disfruta usando el Sistema Veterinario Mascota Feliz!** 🐾 