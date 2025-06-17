from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db import models
from .forms import UserRegistrationForm, MascotaForm, CitaForm, CarritoItemForm, PedidoForm, VeterinarioRegistrationForm, VeterinarioProfileForm, RecetaMedicaForm, ItemRecetaForm, ReservaMedicamentoForm, ItemReservaForm, BuscarMedicamentoForm
from .models import Mascota, Cita, Producto, Categoria, CarritoItem, Pedido, PedidoItem, Pet, Service, User, Veterinario, Medicamento, RecetaMedica, ItemReceta, ReservaMedicamento, ItemReserva, CategoriaFarmacia, Farmaceutico, Peluquero
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.db.models import Sum, F, Q
from decimal import Decimal
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a Mascota Feliz.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'veterinaria/register.html', {'form': form})

def home(request):
    context = {
        'title': 'Bienvenido a Mascota Feliz',
        'description': 'Tu clínica veterinaria de confianza'
    }
    
    # Obtener productos destacados para mostrar en el home
    productos_destacados = Producto.objects.filter(es_destacado=True)[:4]
    if not productos_destacados.exists():
        # Si no hay productos destacados, tomar los primeros 4 productos
        productos_destacados = Producto.objects.all()[:4]
    context['productos_destacados'] = productos_destacados
    
    # Si el usuario está autenticado, obtener sus próximas citas y mascotas
    if request.user.is_authenticated:
        from datetime import date
        
        # Obtener mascotas del usuario directamente
        user_mascotas = Mascota.objects.filter(propietario=request.user)
        
        # Obtener próximas citas usando mascota__propietario
        proximas_citas = Cita.objects.filter(
            mascota__propietario=request.user,
            fecha__gte=date.today(),
            estado__in=['programada', 'confirmada']
        ).order_by('fecha', 'hora')[:3]  # Solo las próximas 3 citas
        
        context['proximas_citas'] = proximas_citas
        context['user_mascotas'] = user_mascotas[:4]  # Solo las primeras 4 mascotas
    
    return render(request, 'veterinaria/home.html', context)

@login_required
def mascota_list(request):
    mascotas = Mascota.objects.filter(propietario=request.user)
    return render(request, 'veterinaria/mascota_list.html', {'mascotas': mascotas})

@login_required
def mascota_create(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.propietario = request.user
            mascota.save()
            messages.success(request, 'Mascota registrada exitosamente.')
            return redirect('mascota_list')
    else:
        form = MascotaForm()
    return render(request, 'veterinaria/mascota_form.html', {'form': form, 'action': 'Crear'})

@login_required
def mascota_update(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk, propietario=request.user)
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota actualizada exitosamente.')
            return redirect('mascota_list')
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'veterinaria/mascota_form.html', {'form': form, 'action': 'Actualizar'})

@login_required
def mascota_delete(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk, propietario=request.user)
    if request.method == 'POST':
        # También eliminar el objeto Pet correspondiente si existe
        try:
            pet = Pet.objects.get(id=str(pk))
            pet.delete()
        except Pet.DoesNotExist:
            pass
        
        mascota_nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f'Mascota {mascota_nombre} eliminada exitosamente.')
        return redirect('mascota_list')
    return render(request, 'veterinaria/mascota_confirm_delete.html', {'mascota': mascota})

@login_required
def cita_list(request):
    # Obtener las mascotas del usuario actual directamente
    user_mascotas = Mascota.objects.filter(propietario=request.user)
    
    # Obtener citas activas (excluyendo canceladas)
    citas_activas = Cita.objects.filter(
        mascota__in=user_mascotas,
        estado__in=['programada', 'confirmada', 'en_curso']
    ).order_by('fecha', 'hora')
    
    # Obtener citas completadas
    citas_completadas = Cita.objects.filter(
        mascota__in=user_mascotas,
        estado='completada'
    ).order_by('-fecha', '-hora')
    
    return render(request, 'veterinaria/cita_list.html', {
        'citas_activas': citas_activas,
        'citas_completadas': citas_completadas
    })

@login_required
def cita_create(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            messages.success(request, 'Cita agendada exitosamente.')
            return redirect('cita_list')
    else:
        form = CitaForm()
        # Filtrar mascotas para mostrar solo las del usuario actual
        user_mascotas = Mascota.objects.filter(propietario=request.user)
        form.fields['mascota'].queryset = user_mascotas
    return render(request, 'veterinaria/cita_form.html', {'form': form, 'action': 'Agendar'})

@login_required
def cita_update(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    # Verificar que la mascota pertenezca al usuario
    user_mascotas = Mascota.objects.filter(propietario=request.user)
    if cita.mascota not in user_mascotas:
        messages.error(request, 'No tienes permiso para editar esta cita.')
        return redirect('cita_list')
    
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('cita_list')
    else:
        form = CitaForm(instance=cita)
        form.fields['mascota'].queryset = user_mascotas
    return render(request, 'veterinaria/cita_form.html', {'form': form, 'action': 'Actualizar'})

@login_required
def cita_cancel(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada exitosamente.')
        return redirect('cita_list')
    return render(request, 'veterinaria/cita_confirm_cancel.html', {'cita': cita})

def tienda(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    destacados = Producto.objects.filter(es_destacado=True)[:4]
    
    return render(request, 'veterinaria/tienda/tienda.html', {
        'categorias': categorias,
        'productos': productos,
        'destacados': destacados,
        'categoria_actual': categoria_id
    })

def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = CarritoItemForm()
    return render(request, 'veterinaria/tienda/producto_detalle.html', {
        'producto': producto,
        'form': form
    })

@login_required
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        form = CarritoItemForm(request.POST)
        
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            if cantidad > producto.stock:
                messages.error(request, 'No hay suficiente stock disponible.')
                return redirect('producto_detalle', pk=producto_id)
            
            carrito_item, created = CarritoItem.objects.get_or_create(
                usuario=request.user,
                producto=producto,
                defaults={'cantidad': cantidad}
            )
            
            if not created:
                carrito_item.cantidad += cantidad
                carrito_item.save()
            
            messages.success(request, f'{producto.nombre} agregado al carrito.')
            return redirect('carrito')
    
    return redirect('producto_detalle', pk=producto_id)

@login_required
def carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, 'veterinaria/tienda/carrito.html', {
        'items': items,
        'total': total
    })

@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        if cantidad > 0 and cantidad <= item.producto.stock:
            item.cantidad = cantidad
            item.save()
        elif cantidad == 0:
            item.delete()
    return redirect('carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')

@login_required
def checkout(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    if not items.exists():
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('carrito')
    
    total = sum(item.subtotal() for item in items)
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.total = total
            pedido.save()
            
            # Crear items del pedido y actualizar stock
            for item in items:
                PedidoItem.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio,
                    subtotal=item.subtotal()
                )
                # Actualizar stock
                item.producto.stock -= item.cantidad
                item.producto.save()
            
            # Limpiar carrito
            items.delete()
            
            messages.success(request, 'Pedido realizado con éxito.')
            return redirect('mis_pedidos')
    else:
        form = PedidoForm()
    
    return render(request, 'veterinaria/tienda/checkout.html', {
        'form': form,
        'items': items,
        'total': total
    })

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    return render(request, 'veterinaria/tienda/mis_pedidos.html', {
        'pedidos': pedidos
    })

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'veterinaria/tienda/detalle_pedido.html', {
        'pedido': pedido
    })

@login_required
def profile(request):
    """Vista mejorada del perfil de usuario con mascotas y opciones de descarga"""
    user_mascotas = Mascota.objects.filter(propietario=request.user)
    
    # Obtener próximas citas del usuario
    from datetime import date
    proximas_citas = Cita.objects.filter(
        mascota__propietario=request.user,
        fecha__gte=date.today(),
        estado__in=['programada', 'confirmada']
    ).order_by('fecha', 'hora')[:5]
    
    # Obtener historial de citas recientes
    historial_citas = Cita.objects.filter(
        mascota__propietario=request.user,
        estado='completada'
    ).order_by('-fecha', '-hora')[:5]
    
    context = {
        'user_mascotas': user_mascotas,
        'proximas_citas': proximas_citas,
        'historial_citas': historial_citas,
        'total_mascotas': user_mascotas.count(),
        'total_citas': Cita.objects.filter(mascota__propietario=request.user).count(),
    }
    
    return render(request, 'veterinaria/profile.html', context)

@login_required
def edit_profile(request):
    """Vista para editar el perfil del usuario"""
    if request.method == 'POST':
        # Actualizar datos del usuario
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.region = request.POST.get('region', '')
        
        try:
            user.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Error al actualizar el perfil: {e}')
    
    return render(request, 'veterinaria/edit_profile.html', {'user': request.user})

@login_required
def descargar_ficha_mascota(request, mascota_id):
    """Descargar ficha médica de una mascota específica"""
    mascota = get_object_or_404(Mascota, id=mascota_id, propietario=request.user)
    
    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ficha_medica_{mascota.nombre}.pdf"'
    
    # Crear documento PDF
    doc = SimpleDocTemplate(response, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50'),
        alignment=1  # Centrado
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#34495e'),
    )
    
    # Título principal
    story.append(Paragraph("🐾 FICHA MÉDICA VETERINARIA", title_style))
    story.append(Spacer(1, 20))
    
    # Información de la clínica
    clinic_info = [
        ["CLÍNICA VETERINARIA MASCOTA FELIZ", ""],
        ["Dirección: Av. Principal 123, Santiago", ""],
        ["Teléfono: +56 2 2345 6789", ""],
        ["Email: info@mascotafeliz.cl", ""],
    ]
    
    clinic_table = Table(clinic_info, colWidths=[4*inch, 2*inch])
    clinic_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#7f8c8d')),
    ]))
    story.append(clinic_table)
    story.append(Spacer(1, 30))
    
    # Información del propietario
    story.append(Paragraph("INFORMACIÓN DEL PROPIETARIO", subtitle_style))
    
    owner_data = [
        ["Nombre:", f"{mascota.propietario.first_name} {mascota.propietario.last_name}"],
        ["Email:", mascota.propietario.email],
        ["Teléfono:", mascota.propietario.phone or "No especificado"],
        ["Región:", mascota.propietario.region or "No especificada"],
    ]
    
    owner_table = Table(owner_data, colWidths=[2*inch, 4*inch])
    owner_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
    ]))
    story.append(owner_table)
    story.append(Spacer(1, 20))
    
    # Información de la mascota
    story.append(Paragraph("INFORMACIÓN DE LA MASCOTA", subtitle_style))
    
    pet_data = [
        ["Nombre:", mascota.nombre],
        ["Especie:", mascota.especie],
        ["Raza:", mascota.raza],
        ["Color:", mascota.color],
        ["Sexo:", mascota.sexo],
        ["Edad:", mascota.edad],
        ["Condición:", mascota.condicion],
        ["ID Mascota:", str(mascota.id)],
    ]
    
    pet_table = Table(pet_data, colWidths=[2*inch, 4*inch])
    pet_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e8')),
    ]))
    story.append(pet_table)
    story.append(Spacer(1, 20))
    
    # Historial de citas
    story.append(Paragraph("HISTORIAL MÉDICO", subtitle_style))
    
    citas = Cita.objects.filter(mascota=mascota).order_by('-fecha', '-hora')
    
    if citas.exists():
        citas_data = [["Fecha", "Hora", "Veterinario", "Motivo", "Estado"]]
        
        for cita in citas[:10]:  # Últimas 10 citas
            veterinario_nombre = cita.veterinario.user.get_full_name() if cita.veterinario else "No asignado"
            citas_data.append([
                cita.fecha.strftime("%d/%m/%Y"),
                cita.hora.strftime("%H:%M"),
                veterinario_nombre,
                cita.motivo[:30] + "..." if len(cita.motivo) > 30 else cita.motivo,
                cita.get_estado_display()
            ])
        
        citas_table = Table(citas_data, colWidths=[1.2*inch, 0.8*inch, 1.5*inch, 2*inch, 1*inch])
        citas_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ]))
        story.append(citas_table)
    else:
        story.append(Paragraph("No hay historial médico registrado.", styles['Normal']))
    
    story.append(Spacer(1, 30))
    
    # Pie de página
    footer_text = f"Documento generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}"
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    
    return response

@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if not request.user.is_admin and pet.owner != request.user:
        messages.error(request, "No tienes permiso para ver esta mascota")
        return redirect('profile')
    
    services = Service.objects.filter(pet=pet)
    online_services_count = services.filter(reservation_type='Online').count()
    presencial_services_count = services.filter(reservation_type='Presencial').count()
    
    # Obtener recetas y reservas si existe la mascota en el sistema de citas
    recetas = []
    reservas = []
    citas = []
    
    try:
        mascota = Mascota.objects.get(id=int(pet.id))
        recetas = RecetaMedica.objects.filter(mascota=mascota).order_by('-fecha_emision')
        reservas = ReservaMedicamento.objects.filter(cliente=request.user).order_by('-fecha_reserva')
        citas = Cita.objects.filter(mascota=mascota).order_by('-fecha', '-hora')
    except (Mascota.DoesNotExist, ValueError):
        pass
    
    context = {
        'pet': pet,
        'services': services,
        'online_services_count': online_services_count,
        'presencial_services_count': presencial_services_count,
        'recetas': recetas,
        'reservas': reservas,
        'citas': citas,
    }
    return render(request, 'veterinaria/pet_detail.html', context)

@login_required
def pet_edit(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if not request.user.is_admin and pet.owner != request.user:
        messages.error(request, "No tienes permiso para editar esta mascota")
        return redirect('pet_detail', pet_id=pet_id)
    
    if request.method == 'POST':
        # Actualizar datos básicos de la mascota
        pet.name = request.POST.get('name', pet.name)
        pet.breed = request.POST.get('breed', pet.breed)
        pet.base_color = request.POST.get('base_color', pet.base_color)
        pet.condition = request.POST.get('condition', pet.condition)
        pet.age_years = int(request.POST.get('age_years', pet.age_years))
        pet.age_months = int(request.POST.get('age_months', pet.age_months))
        pet.sex = request.POST.get('sex', pet.sex)
        pet.save()
        
        # Sincronizar con tabla Mascota si existe
        try:
            mascota = Mascota.objects.get(id=int(pet.id))
            mascota.nombre = pet.name
            mascota.raza = pet.breed
            mascota.color = pet.base_color
            mascota.especie = 'Gato' if pet.species.lower() in ['cat', 'gato'] else 'Perro'
            mascota.condicion = pet.condition if pet.condition in ['Normal', 'Herido', 'Vejez'] else 'Normal'
            mascota.edad = f"{pet.age_years} años" + (f" {pet.age_months} meses" if pet.age_months > 0 else "")
            mascota.sexo = pet.sex if pet.sex in ['Macho', 'Hembra'] else 'Macho'
            mascota.save()
        except (Mascota.DoesNotExist, ValueError):
            pass
        
        messages.success(request, f'Información de {pet.name} actualizada exitosamente.')
        return redirect('pet_detail', pet_id=pet_id)
    
    context = {
        'pet': pet,
        'condition_choices': ['Normal', 'Herido', 'Vejez'],
        'sex_choices': ['Macho', 'Hembra']
    }
    return render(request, 'veterinaria/pet_edit.html', context)

@login_required
def pet_agendar_cita(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if not request.user.is_admin and pet.owner != request.user:
        messages.error(request, "No tienes permiso para agendar citas para esta mascota")
        return redirect('pet_detail', pet_id=pet_id)
    
    # Verificar si existe la mascota en tabla Mascota
    try:
        mascota = Mascota.objects.get(id=int(pet.id))
    except (Mascota.DoesNotExist, ValueError):
        messages.error(request, "Esta mascota no está sincronizada en el sistema de citas.")
        return redirect('pet_detail', pet_id=pet_id)
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.mascota = mascota
            cita.save()
            messages.success(request, f'Cita agendada exitosamente para {pet.name}.')
            return redirect('pet_detail', pet_id=pet_id)
    else:
        form = CitaForm()
        # Pre-seleccionar la mascota
        form.fields['mascota'].queryset = Mascota.objects.filter(id=mascota.id)
        form.fields['mascota'].initial = mascota
    
    context = {
        'pet': pet,
        'form': form,
        'action': 'Agendar Cita'
    }
    return render(request, 'veterinaria/pet_agendar_cita.html', context)

@login_required
def pet_nuevo_servicio(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if not request.user.is_admin and pet.owner != request.user:
        messages.error(request, "No tienes permiso para agregar servicios a esta mascota")
        return redirect('pet_detail', pet_id=pet_id)
    
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        reservation_type = request.POST.get('reservation_type')
        date = request.POST.get('date')
        
        if service_type and reservation_type and date:
            Service.objects.create(
                pet=pet,
                service_type=service_type,
                reservation_type=reservation_type,
                date=date
            )
            messages.success(request, f'Servicio agregado exitosamente para {pet.name}.')
            return redirect('pet_detail', pet_id=pet_id)
        else:
            messages.error(request, 'Por favor completa todos los campos.')
    
    context = {
        'pet': pet,
        'service_types': ['Veterinario', 'Peluquería', 'Consulta General', 'Vacunación', 'Desparasitación'],
        'reservation_types': ['Online', 'Presencial']
    }
    return render(request, 'veterinaria/pet_nuevo_servicio.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, "No tienes permiso para acceder al panel de administración")
        return redirect('profile')
    
    # Obtener todas las mascotas del sistema
    all_mascotas = Mascota.objects.all().select_related('propietario')
    all_pets = Pet.objects.all().select_related('owner')
    all_services = Service.objects.all().select_related('pet')
    
    # Estadísticas generales
    total_usuarios = User.objects.count()
    total_veterinarios = Veterinario.objects.count()
    total_farmaceuticos = Farmaceutico.objects.count()
    total_peluqueros = Peluquero.objects.count()
    total_citas = Cita.objects.count()
    total_recetas = RecetaMedica.objects.count()
    total_reservas = ReservaMedicamento.objects.count()
    
    # Citas por estado
    citas_programadas = Cita.objects.filter(estado='programada').count()
    citas_completadas = Cita.objects.filter(estado='completada').count()
    citas_canceladas = Cita.objects.filter(estado='cancelada').count()
    
    context = {
        'mascotas': all_mascotas,
        'pets': all_pets,
        'services': all_services,
        'total_mascotas': all_mascotas.count(),
        'total_pets': all_pets.count(),
        'total_services': all_services.count(),
        'total_usuarios': total_usuarios,
        'total_veterinarios': total_veterinarios,
        'total_farmaceuticos': total_farmaceuticos,
        'total_peluqueros': total_peluqueros,
        'total_citas': total_citas,
        'total_recetas': total_recetas,
        'total_reservas': total_reservas,
        'citas_programadas': citas_programadas,
        'citas_completadas': citas_completadas,
        'citas_canceladas': citas_canceladas,
    }
    return render(request, 'veterinaria/admin_dashboard.html', context)

@login_required
def descargar_ficha_medica(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if not request.user.is_admin and pet.owner != request.user:
        messages.error(request, "No tienes permiso para descargar la ficha médica de esta mascota")
        return redirect('pet_detail', pet_id=pet_id)
    
    # Crear el PDF en memoria
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50'),
        alignment=1  # Centrado
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#34495e'),
        leftIndent=0
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leftIndent=20
    )
    
    # Título principal
    story.append(Paragraph("FICHA MÉDICA VETERINARIA", title_style))
    story.append(Paragraph("Clínica Veterinaria Mascota Feliz", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Información básica de la mascota
    story.append(Paragraph("INFORMACIÓN BÁSICA", heading_style))
    
    # Crear tabla con información básica
    basic_data = [
        ['Nombre:', pet.name],
        ['Especie:', pet.species],
        ['Raza:', pet.breed],
        ['Color:', pet.base_color],
        ['Sexo:', pet.sex],
        ['Edad:', f"{pet.age_years} años, {pet.age_months} meses"],
        ['Condición:', pet.condition],
        ['Propietario:', f"{pet.owner.first_name} {pet.owner.last_name}"],
        ['Email del propietario:', pet.owner.email],
    ]
    
    basic_table = Table(basic_data, colWidths=[2*inch, 4*inch])
    basic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(basic_table)
    story.append(Spacer(1, 20))
    
    # Historial de servicios
    services = Service.objects.filter(pet=pet).order_by('-date')
    story.append(Paragraph("HISTORIAL DE SERVICIOS", heading_style))
    
    if services.exists():
        service_data = [['Fecha', 'Tipo de Servicio', 'Modalidad']]
        for service in services:
            service_data.append([
                service.date.strftime('%d/%m/%Y'),
                service.service_type,
                service.reservation_type
            ])
        
        service_table = Table(service_data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
        service_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        story.append(service_table)
    else:
        story.append(Paragraph("No hay servicios registrados para esta mascota.", normal_style))
    
    story.append(Spacer(1, 20))
    
    # Historial de citas
    try:
        mascota = Mascota.objects.get(id=int(pet.id))
        citas = Cita.objects.filter(mascota=mascota).order_by('-fecha', '-hora')
        
        story.append(Paragraph("HISTORIAL DE CITAS MÉDICAS", heading_style))
        
        if citas.exists():
            cita_data = [['Fecha', 'Hora', 'Estado', 'Motivo']]
            for cita in citas[:10]:  # Últimas 10 citas
                motivo = cita.motivo[:30] + '...' if len(cita.motivo) > 30 else cita.motivo
                cita_data.append([
                    cita.fecha.strftime('%d/%m/%Y'),
                    cita.hora.strftime('%H:%M'),
                    cita.get_estado_display(),
                    motivo or 'Sin especificar'
                ])
            
            cita_table = Table(cita_data, colWidths=[1.2*inch, 1*inch, 1.3*inch, 2.5*inch])
            cita_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            story.append(cita_table)
        else:
            story.append(Paragraph("No hay citas médicas registradas para esta mascota.", normal_style))
    except (Mascota.DoesNotExist, ValueError):
        story.append(Paragraph("HISTORIAL DE CITAS MÉDICAS", heading_style))
        story.append(Paragraph("Esta mascota no está sincronizada en el sistema de citas médicas.", normal_style))
    
    # Historial de recetas médicas
    try:
        mascota = Mascota.objects.get(id=int(pet.id))
        recetas = RecetaMedica.objects.filter(mascota=mascota).order_by('-fecha_emision')
        
        story.append(Paragraph("HISTORIAL DE RECETAS MÉDICAS", heading_style))
        
        if recetas.exists():
            for receta in recetas[:5]:  # Últimas 5 recetas
                story.append(Paragraph(f"Receta #{receta.id} - {receta.fecha_emision.strftime('%d/%m/%Y')}", normal_style))
                story.append(Paragraph(f"Veterinario: {receta.veterinario.user.get_full_name()}", normal_style))
                story.append(Paragraph(f"Diagnóstico: {receta.diagnostico}", normal_style))
                
                # Medicamentos de la receta
                if receta.items.exists():
                    story.append(Paragraph("Medicamentos prescritos:", normal_style))
                    for item in receta.items.all():
                        story.append(Paragraph(f"• {item.medicamento.nombre} - {item.dosis} - {item.duracion}", normal_style))
                
                story.append(Spacer(1, 10))
        else:
            story.append(Paragraph("No hay recetas médicas registradas para esta mascota.", normal_style))
    except (Mascota.DoesNotExist, ValueError):
        story.append(Paragraph("HISTORIAL DE RECETAS MÉDICAS", heading_style))
        story.append(Paragraph("Esta mascota no está sincronizada en el sistema de recetas médicas.", normal_style))
    
    story.append(Spacer(1, 20))
    
    # Historial de reservas de medicamentos
    reservas = ReservaMedicamento.objects.filter(cliente=pet.owner).order_by('-fecha_reserva')
    
    story.append(Paragraph("HISTORIAL DE RESERVAS DE MEDICAMENTOS", heading_style))
    
    if reservas.exists():
        reserva_data = [['Número', 'Fecha', 'Tipo', 'Estado', 'Total']]
        for reserva in reservas[:10]:  # Últimas 10 reservas
            reserva_data.append([
                reserva.numero_reserva,
                reserva.fecha_reserva.strftime('%d/%m/%Y'),
                reserva.get_tipo_display(),
                reserva.get_estado_display(),
                f"${reserva.total:,.0f}"
            ])
        
        reserva_table = Table(reserva_data, colWidths=[1.2*inch, 1.2*inch, 1.5*inch, 1.5*inch, 1*inch])
        reserva_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        story.append(reserva_table)
    else:
        story.append(Paragraph("No hay reservas de medicamentos registradas.", normal_style))
    
    story.append(Spacer(1, 30))
    
    # Pie de página
    story.append(Paragraph("_" * 80, styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"Documento generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", styles['Normal']))
    story.append(Paragraph("Clínica Veterinaria Mascota Feliz - Tu mascota, nuestra prioridad", styles['Normal']))
    
    # Construir el PDF
    doc.build(story)
    
    # Preparar la respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ficha_medica_{pet.name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response

# ==================== VISTAS PARA VETERINARIOS ====================

def veterinario_register(request):
    """Registro de nuevos veterinarios"""
    if request.method == 'POST':
        form = VeterinarioRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido al equipo de Mascota Feliz.')
            return redirect('veterinario_dashboard')
    else:
        form = VeterinarioRegistrationForm()
    return render(request, 'veterinaria/veterinario/register.html', {'form': form})

@login_required
def veterinario_dashboard(request):
    """Panel principal para veterinarios"""
    try:
        veterinario = Veterinario.objects.get(user=request.user)
    except Veterinario.DoesNotExist:
        messages.error(request, "No tienes permisos de veterinario.")
        return redirect('home')
    
    # Obtener citas del veterinario
    from datetime import date, timedelta
    hoy = date.today()
    
    # Citas de hoy
    citas_hoy = Cita.objects.filter(
        veterinario=veterinario,
        fecha=hoy,
        estado__in=['programada', 'confirmada', 'en_curso']
    ).order_by('hora')
    
    # Próximas citas (próximos 7 días)
    proximas_citas = Cita.objects.filter(
        veterinario=veterinario,
        fecha__range=[hoy + timedelta(days=1), hoy + timedelta(days=7)],
        estado__in=['programada', 'confirmada']
    ).order_by('fecha', 'hora')[:5]
    
    # Citas sin asignar (para que el veterinario pueda tomarlas)
    citas_sin_asignar = Cita.objects.filter(
        veterinario__isnull=True,
        fecha__gte=hoy,
        estado='programada'
    ).order_by('fecha', 'hora')[:10]
    
    # Estadísticas
    total_citas_mes = Cita.objects.filter(
        veterinario=veterinario,
        fecha__month=hoy.month,
        fecha__year=hoy.year
    ).count()
    
    citas_completadas_mes = Cita.objects.filter(
        veterinario=veterinario,
        fecha__month=hoy.month,
        fecha__year=hoy.year,
        estado='completada'
    ).count()
    
    context = {
        'veterinario': veterinario,
        'citas_hoy': citas_hoy,
        'proximas_citas': proximas_citas,
        'citas_sin_asignar': citas_sin_asignar,
        'total_citas_mes': total_citas_mes,
        'citas_completadas_mes': citas_completadas_mes,
    }
    
    return render(request, 'veterinaria/veterinario/dashboard.html', context)

@login_required
def veterinario_citas(request):
    """Lista de todas las citas del veterinario"""
    try:
        veterinario = Veterinario.objects.get(user=request.user)
    except Veterinario.DoesNotExist:
        messages.error(request, "No tienes permisos de veterinario.")
        return redirect('home')
    
    # Filtros
    estado = request.GET.get('estado', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    
    citas = Cita.objects.filter(veterinario=veterinario)
    
    if estado:
        citas = citas.filter(estado=estado)
    
    if fecha_desde:
        citas = citas.filter(fecha__gte=fecha_desde)
    
    if fecha_hasta:
        citas = citas.filter(fecha__lte=fecha_hasta)
    
    citas = citas.order_by('-fecha', '-hora')
    
    context = {
        'veterinario': veterinario,
        'citas': citas,
        'estado_actual': estado,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estados_choices': Cita.ESTADO_CHOICES,
    }
    
    return render(request, 'veterinaria/veterinario/citas.html', context)

@login_required
def veterinario_cita_detalle(request, cita_id):
    """Detalle de una cita específica"""
    try:
        veterinario = Veterinario.objects.get(user=request.user)
    except Veterinario.DoesNotExist:
        messages.error(request, "No tienes permisos de veterinario.")
        return redirect('home')
    
    cita = get_object_or_404(Cita, id=cita_id, veterinario=veterinario)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'confirmar':
            cita.estado = 'confirmada'
            cita.save()
            messages.success(request, 'Cita confirmada exitosamente.')
        
        elif accion == 'iniciar':
            cita.estado = 'en_curso'
            cita.save()
            messages.success(request, 'Cita iniciada.')
        
        elif accion == 'completar':
            notas = request.POST.get('notas_veterinario', '')
            cita.estado = 'completada'
            cita.notas_veterinario = notas
            cita.save()
            messages.success(request, 'Cita completada exitosamente.')
        
        elif accion == 'cancelar':
            cita.estado = 'cancelada'
            cita.save()
            messages.success(request, 'Cita cancelada.')
        
        return redirect('veterinario_cita_detalle', cita_id=cita.id)
    
    context = {
        'veterinario': veterinario,
        'cita': cita,
    }
    
    return render(request, 'veterinaria/veterinario/cita_detalle.html', context)

@login_required
def veterinario_tomar_cita(request, cita_id):
    """Permite al veterinario tomar una cita sin asignar"""
    try:
        veterinario = Veterinario.objects.get(user=request.user)
    except Veterinario.DoesNotExist:
        messages.error(request, "No tienes permisos de veterinario.")
        return redirect('home')
    
    cita = get_object_or_404(Cita, id=cita_id, veterinario__isnull=True, estado='programada')
    
    # Verificar que el veterinario no tenga conflictos de horario
    conflictos = Cita.objects.filter(
        veterinario=veterinario,
        fecha=cita.fecha,
        estado__in=['programada', 'confirmada', 'en_curso']
    )
    
    for conflicto in conflictos:
        if (cita.hora < conflicto.hora_fin and cita.hora_fin > conflicto.hora):
            messages.error(request, f'Tienes un conflicto de horario con otra cita a las {conflicto.hora}.')
            return redirect('veterinario_dashboard')
    
    # Asignar la cita al veterinario
    cita.veterinario = veterinario
    cita.save()
    
    messages.success(request, f'Has tomado la cita para {cita.mascota.nombre} el {cita.fecha} a las {cita.hora}.')
    return redirect('veterinario_dashboard')

@login_required
def veterinario_profile(request):
    """Perfil del veterinario"""
    try:
        veterinario = Veterinario.objects.get(user=request.user)
    except Veterinario.DoesNotExist:
        messages.error(request, "No tienes permisos de veterinario.")
        return redirect('home')
    
    if request.method == 'POST':
        form = VeterinarioProfileForm(request.POST, instance=veterinario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('veterinario_profile')
    else:
        form = VeterinarioProfileForm(instance=veterinario)
    
    context = {
        'veterinario': veterinario,
        'form': form,
    }
    
    return render(request, 'veterinaria/veterinario/profile.html', context)

# ==================== VISTAS DE FARMACIA ====================

def farmacia_catalogo(request):
    """Catálogo público de medicamentos"""
    form = BuscarMedicamentoForm(request.GET or None)
    medicamentos = Medicamento.objects.filter(activo=True)
    
    # Aplicar filtros
    if form.is_valid():
        busqueda = form.cleaned_data.get('busqueda')
        categoria = form.cleaned_data.get('categoria')
        tipo = form.cleaned_data.get('tipo')
        requiere_receta = form.cleaned_data.get('requiere_receta')
        disponible = form.cleaned_data.get('disponible')
        
        if busqueda:
            medicamentos = medicamentos.filter(
                models.Q(nombre__icontains=busqueda) |
                models.Q(nombre_generico__icontains=busqueda) |
                models.Q(laboratorio__icontains=busqueda)
            )
        
        if categoria:
            medicamentos = medicamentos.filter(categoria=categoria)
        
        if tipo:
            medicamentos = medicamentos.filter(tipo=tipo)
        
        if requiere_receta:
            medicamentos = medicamentos.filter(requiere_receta=requiere_receta == 'True')
        
        if disponible:
            medicamentos = medicamentos.filter(stock__gt=0)
    
    # Obtener categorías para mostrar
    categorias = CategoriaFarmacia.objects.all()
    
    context = {
        'medicamentos': medicamentos,
        'categorias': categorias,
        'form': form,
    }
    
    return render(request, 'veterinaria/farmacia/catalogo.html', context)

def medicamento_detalle(request, medicamento_id):
    """Detalle de un medicamento específico"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id, activo=True)
    
    # Medicamentos relacionados (misma categoría)
    relacionados = Medicamento.objects.filter(
        categoria=medicamento.categoria,
        activo=True
    ).exclude(id=medicamento.id)[:4]
    
    context = {
        'medicamento': medicamento,
        'relacionados': relacionados,
    }
    
    return render(request, 'veterinaria/farmacia/medicamento_detalle.html', context)

@login_required
def crear_receta(request, cita_id):
    """Crear receta médica para una cita (solo veterinarios)"""
    try:
        veterinario = Veterinario.objects.get(user=request.user)
    except Veterinario.DoesNotExist:
        messages.error(request, "No tienes permisos para crear recetas.")
        return redirect('home')
    
    cita = get_object_or_404(Cita, id=cita_id, veterinario=veterinario)
    
    if request.method == 'POST':
        form = RecetaMedicaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.cita = cita
            receta.veterinario = veterinario
            receta.mascota = cita.mascota
            receta.save()
            
            messages.success(request, f'Receta médica creada exitosamente y guardada en el perfil de {cita.mascota.propietario.get_full_name()}.')
            return redirect('editar_receta', receta_id=receta.id)
    else:
        form = RecetaMedicaForm()
    
    context = {
        'form': form,
        'cita': cita,
        'veterinario': veterinario,
    }
    
    return render(request, 'veterinaria/farmacia/crear_receta.html', context)

@login_required
def editar_receta(request, receta_id):
    """Editar receta médica y agregar medicamentos"""
    try:
        veterinario = Veterinario.objects.get(user=request.user)
    except Veterinario.DoesNotExist:
        messages.error(request, "No tienes permisos para editar recetas.")
        return redirect('home')
    
    receta = get_object_or_404(RecetaMedica, id=receta_id, veterinario=veterinario)
    
    if request.method == 'POST':
        if 'agregar_medicamento' in request.POST:
            item_form = ItemRecetaForm(request.POST)
            if item_form.is_valid():
                item = item_form.save(commit=False)
                item.receta = receta
                item.save()
                messages.success(request, f'Medicamento {item.medicamento.nombre} agregado a la receta.')
                return redirect('editar_receta', receta_id=receta.id)
        
        elif 'finalizar_receta' in request.POST:
            if receta.items.exists():
                messages.success(request, f'Receta finalizada exitosamente. {receta.mascota.propietario.get_full_name()} puede ver y reservar los medicamentos desde su perfil.')
                return redirect('veterinario_cita_detalle', cita_id=receta.cita.id)
            else:
                messages.error(request, 'Debe agregar al menos un medicamento a la receta.')
    
    item_form = ItemRecetaForm()
    
    context = {
        'receta': receta,
        'item_form': item_form,
        'veterinario': veterinario,
    }
    
    return render(request, 'veterinaria/farmacia/editar_receta.html', context)

@login_required
def eliminar_item_receta(request, item_id):
    """Eliminar medicamento de una receta"""
    try:
        veterinario = Veterinario.objects.get(user=request.user)
    except Veterinario.DoesNotExist:
        messages.error(request, "No tienes permisos.")
        return redirect('home')
    
    item = get_object_or_404(ItemReceta, id=item_id, receta__veterinario=veterinario)
    receta_id = item.receta.id
    
    item.delete()
    messages.success(request, 'Medicamento eliminado de la receta.')
    
    return redirect('editar_receta', receta_id=receta_id)

@login_required
def mis_recetas(request):
    """Lista de recetas del cliente"""
    recetas = RecetaMedica.objects.filter(mascota__propietario=request.user).order_by('-fecha_emision')
    
    context = {
        'recetas': recetas,
    }
    
    return render(request, 'veterinaria/farmacia/mis_recetas.html', context)

@login_required
def detalle_receta(request, receta_id):
    """Detalle de una receta específica"""
    receta = get_object_or_404(RecetaMedica, id=receta_id, mascota__propietario=request.user)
    
    context = {
        'receta': receta,
    }
    
    return render(request, 'veterinaria/farmacia/detalle_receta.html', context)

@login_required
def reservar_medicamentos_receta(request, receta_id):
    """Reservar medicamentos de una receta"""
    receta = get_object_or_404(RecetaMedica, id=receta_id, mascota__propietario=request.user)
    
    if receta.esta_vencida:
        messages.error(request, 'Esta receta ha vencido y no se puede usar.')
        return redirect('detalle_receta', receta_id=receta.id)
    
    if request.method == 'POST':
        form = ReservaMedicamentoForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user
            reserva.receta = receta
            reserva.tipo = 'receta'
            reserva.save()
            
            # Agregar todos los medicamentos de la receta a la reserva
            for item_receta in receta.items.all():
                if item_receta.medicamento.stock >= item_receta.cantidad:
                    ItemReserva.objects.create(
                        reserva=reserva,
                        medicamento=item_receta.medicamento,
                        cantidad=item_receta.cantidad
                    )
                else:
                    messages.warning(request, f'Stock insuficiente para {item_receta.medicamento.nombre}')
            
            messages.success(request, f'Reserva {reserva.numero_reserva} creada exitosamente.')
            return redirect('mis_reservas')
    else:
        form = ReservaMedicamentoForm()
    
    context = {
        'form': form,
        'receta': receta,
    }
    
    return render(request, 'veterinaria/farmacia/reservar_receta.html', context)

@login_required
def reservar_medicamento_libre(request, medicamento_id):
    """Reservar medicamento de venta libre"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id, activo=True, requiere_receta=False)
    
    if request.method == 'POST':
        reserva_form = ReservaMedicamentoForm(request.POST)
        item_form = ItemReservaForm(request.POST)
        
        if reserva_form.is_valid() and item_form.is_valid():
            # Crear reserva
            reserva = reserva_form.save(commit=False)
            reserva.cliente = request.user
            reserva.tipo = 'libre'
            reserva.save()
            
            # Agregar medicamento a la reserva
            item = item_form.save(commit=False)
            item.reserva = reserva
            item.medicamento = medicamento
            item.save()
            
            messages.success(request, f'Reserva {reserva.numero_reserva} creada exitosamente.')
            return redirect('mis_reservas')
    else:
        reserva_form = ReservaMedicamentoForm()
        item_form = ItemReservaForm()
        item_form.fields['medicamento'].initial = medicamento
        item_form.fields['medicamento'].widget.attrs['readonly'] = True
    
    context = {
        'reserva_form': reserva_form,
        'item_form': item_form,
        'medicamento': medicamento,
    }
    
    return render(request, 'veterinaria/farmacia/reservar_libre.html', context)

@login_required
def mis_reservas(request):
    """Lista de reservas del cliente"""
    reservas = ReservaMedicamento.objects.filter(cliente=request.user).order_by('-fecha_reserva')
    
    context = {
        'reservas': reservas,
    }
    
    return render(request, 'veterinaria/farmacia/mis_reservas.html', context)

@login_required
def detalle_reserva(request, reserva_id):
    """Detalle de una reserva específica"""
    reserva = get_object_or_404(ReservaMedicamento, id=reserva_id, cliente=request.user)
    
    context = {
        'reserva': reserva,
    }
    
    return render(request, 'veterinaria/farmacia/detalle_reserva.html', context)

# ==================== VISTAS DE PELUQUERÍA ====================

def peluqueria_catalogo(request):
    """Catálogo de servicios de peluquería - Página principal"""
    from .models import CategoriaServicioPeluqueria, ServicioPeluqueria
    
    categorias = CategoriaServicioPeluqueria.objects.filter(activo=True)
    servicios = ServicioPeluqueria.objects.filter(activo=True)
    
    # Servicios destacados (los 4 más caros o los primeros)
    servicios_destacados = servicios.order_by('-precio_base')[:4]
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    tipo_mascota = request.GET.get('tipo_mascota')
    tamaño = request.GET.get('tamaño')
    
    if categoria_id:
        servicios = servicios.filter(categoria_id=categoria_id)
    if tipo_mascota:
        servicios = servicios.filter(tipo_mascota__in=[tipo_mascota, 'ambos'])
    if tamaño:
        servicios = servicios.filter(tamaño_mascota__in=[tamaño, 'todos'])
    
    context = {
        'categorias': categorias,
        'servicios': servicios,
        'servicios_destacados': servicios_destacados,
        'categoria_actual': categoria_id,
        'tipo_mascota_actual': tipo_mascota,
        'tamaño_actual': tamaño,
    }
    
    return render(request, 'veterinaria/peluqueria/home.html', context)

def servicio_peluqueria_detalle(request, servicio_id):
    """Detalle de un servicio de peluquería"""
    from .models import ServicioPeluqueria
    
    servicio = get_object_or_404(ServicioPeluqueria, id=servicio_id, activo=True)
    
    context = {
        'servicio': servicio,
    }
    
    return render(request, 'veterinaria/peluqueria/servicio_detalle.html', context)

@login_required
def agendar_cita_peluqueria(request, servicio_id=None):
    """Agendar cita de peluquería"""
    from .models import ServicioPeluqueria, CitaPeluqueria, ServicioCitaPeluqueria, Peluquero
    from .forms import CitaPeluqueriaForm
    
    servicio_seleccionado = None
    if servicio_id:
        servicio_seleccionado = get_object_or_404(ServicioPeluqueria, id=servicio_id, activo=True)
    
    # Obtener mascotas del usuario
    user_mascotas = Mascota.objects.filter(propietario=request.user)
    
    if not user_mascotas.exists():
        messages.error(request, 'Debes tener al menos una mascota registrada para agendar una cita de peluquería.')
        return redirect('mascota_create')
    
    if request.method == 'POST':
        form = CitaPeluqueriaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente = request.user
            cita.save()
            
            # Si hay un servicio preseleccionado, agregarlo automáticamente
            if servicio_seleccionado:
                ServicioCitaPeluqueria.objects.create(
                    cita=cita,
                    servicio=servicio_seleccionado,
                    precio=servicio_seleccionado.precio_base
                )
            
            messages.success(request, f'Cita de peluquería {cita.numero_cita} agendada exitosamente.')
            return redirect('mis_citas_peluqueria')
    else:
        form = CitaPeluqueriaForm()
        form.fields['mascota'].queryset = user_mascotas
    
    context = {
        'form': form,
        'servicio_seleccionado': servicio_seleccionado,
        'user_mascotas': user_mascotas,
    }
    
    return render(request, 'veterinaria/peluqueria/agendar_cita.html', context)

@login_required
def mis_citas_peluqueria(request):
    """Lista de citas de peluquería del cliente"""
    from .models import CitaPeluqueria
    
    # Obtener mascotas del usuario
    user_mascotas = Mascota.objects.filter(propietario=request.user)
    
    citas = CitaPeluqueria.objects.filter(mascota__in=user_mascotas).order_by('-fecha', '-hora')
    
    # Calcular estadísticas
    proximas_citas = citas.filter(estado__in=['programada', 'confirmada']).count()
    completadas = citas.filter(estado='completada').count()
    total_invertido = sum(cita.total for cita in citas.filter(estado='completada'))
    
    stats = {
        'proximas_citas': proximas_citas,
        'completadas': completadas,
        'total_invertido': total_invertido,
    }
    
    context = {
        'citas': citas,
        'stats': stats,
    }
    
    return render(request, 'veterinaria/peluqueria/mis_citas.html', context)

@login_required
def detalle_cita_peluqueria(request, cita_id):
    """Detalle de una cita de peluquería"""
    from .models import CitaPeluqueria
    
    # Obtener mascotas del usuario
    user_mascotas = Mascota.objects.filter(propietario=request.user)
    
    cita = get_object_or_404(CitaPeluqueria, id=cita_id, mascota__in=user_mascotas)
    
    context = {
        'cita': cita,
    }
    
    return render(request, 'veterinaria/peluqueria/detalle_cita.html', context)

@login_required
def cancelar_cita_peluqueria(request, cita_id):
    """Cancelar cita de peluquería"""
    from .models import CitaPeluqueria
    
    # Obtener mascotas del usuario
    user_mascotas = Mascota.objects.filter(propietario=request.user)
    
    cita = get_object_or_404(CitaPeluqueria, id=cita_id, mascota__in=user_mascotas)
    
    if cita.estado in ['completada', 'cancelada']:
        messages.error(request, 'No se puede cancelar esta cita.')
        return redirect('detalle_cita_peluqueria', cita_id=cita.id)
    
    if request.method == 'POST':
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, f'Cita {cita.numero_cita} cancelada exitosamente.')
        return redirect('mis_citas_peluqueria')
    
    context = {
        'cita': cita,
    }
    
    return render(request, 'veterinaria/peluqueria/cancelar_cita.html', context)

# ==================== VISTAS PARA PELUQUEROS ====================

def peluquero_register(request):
    """Registro de peluqueros"""
    from .forms import PeluqueroRegistrationForm
    
    if request.method == 'POST':
        form = PeluqueroRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro como peluquero exitoso! Bienvenido al equipo de Mascota Feliz.')
            return redirect('peluquero_dashboard')
    else:
        form = PeluqueroRegistrationForm()
    
    return render(request, 'veterinaria/peluqueria/peluquero_register.html', {'form': form})

@login_required
def peluquero_dashboard(request):
    """Dashboard del peluquero"""
    from .models import Peluquero, CitaPeluqueria
    from datetime import date, timedelta
    
    try:
        peluquero = Peluquero.objects.get(user=request.user)
    except Peluquero.DoesNotExist:
        messages.error(request, "No tienes permisos de peluquero.")
        return redirect('home')
    
    # Estadísticas
    hoy = date.today()
    citas_hoy = CitaPeluqueria.objects.filter(peluquero=peluquero, fecha=hoy)
    citas_semana = CitaPeluqueria.objects.filter(
        peluquero=peluquero,
        fecha__range=[hoy, hoy + timedelta(days=7)]
    )
    citas_pendientes = CitaPeluqueria.objects.filter(
        peluquero=peluquero,
        estado__in=['programada', 'confirmada']
    )
    
    context = {
        'peluquero': peluquero,
        'citas_hoy': citas_hoy,
        'citas_semana': citas_semana,
        'citas_pendientes': citas_pendientes,
        'total_citas_hoy': citas_hoy.count(),
        'total_citas_semana': citas_semana.count(),
        'total_pendientes': citas_pendientes.count(),
    }
    
    return render(request, 'veterinaria/peluqueria/peluquero_dashboard.html', context)

@login_required
def peluquero_citas(request):
    """Lista de citas del peluquero con filtros avanzados"""
    from .models import Peluquero, CitaPeluqueria
    
    try:
        peluquero = Peluquero.objects.get(user=request.user)
    except Peluquero.DoesNotExist:
        messages.error(request, "No tienes permisos de peluquero.")
        return redirect('home')
    
    # Filtros
    estado = request.GET.get('estado', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    
    citas = CitaPeluqueria.objects.filter(peluquero=peluquero)
    
    if estado:
        citas = citas.filter(estado=estado)
    
    if fecha_desde:
        citas = citas.filter(fecha__gte=fecha_desde)
    
    if fecha_hasta:
        citas = citas.filter(fecha__lte=fecha_hasta)
    
    citas = citas.order_by('-fecha', '-hora')
    
    context = {
        'peluquero': peluquero,
        'citas': citas,
        'estado_actual': estado,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estados_choices': CitaPeluqueria.ESTADO_CHOICES,
    }
    
    return render(request, 'veterinaria/peluqueria/peluquero_citas.html', context)

@login_required
def peluquero_cita_detalle(request, cita_id):
    """Detalle de cita para el peluquero con control completo"""
    from .models import Peluquero, CitaPeluqueria
    
    try:
        peluquero = Peluquero.objects.get(user=request.user)
    except Peluquero.DoesNotExist:
        messages.error(request, "No tienes permisos de peluquero.")
        return redirect('home')
    
    cita = get_object_or_404(CitaPeluqueria, id=cita_id, peluquero=peluquero)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'confirmar':
            cita.estado = 'confirmada'
            cita.save()
            messages.success(request, 'Cita confirmada exitosamente.')
        
        elif accion == 'iniciar':
            cita.estado = 'en_proceso'
            cita.save()
            messages.success(request, 'Cita iniciada.')
        
        elif accion == 'completar':
            observaciones = request.POST.get('observaciones_peluquero', '')
            cita.estado = 'completada'
            cita.observaciones_peluquero = observaciones
            cita.save()
            messages.success(request, 'Cita completada exitosamente.')
        
        elif accion == 'cancelar':
            cita.estado = 'cancelada'
            cita.save()
            messages.success(request, 'Cita cancelada.')
        
        return redirect('peluquero_cita_detalle', cita_id=cita.id)
    
    context = {
        'peluquero': peluquero,
        'cita': cita,
    }
    
    return render(request, 'veterinaria/peluqueria/peluquero_cita_detalle.html', context)

@login_required
def peluquero_completar_cita(request, cita_id):
    """Completar cita y subir fotos antes/después"""
    from .models import Peluquero, CitaPeluqueria, FotosAntesDepues
    from .forms import FotosAntesDepuesForm
    
    try:
        peluquero = Peluquero.objects.get(user=request.user)
    except Peluquero.DoesNotExist:
        messages.error(request, "No tienes permisos de peluquero.")
        return redirect('home')
    
    cita = get_object_or_404(CitaPeluqueria, id=cita_id, peluquero=peluquero)
    
    if request.method == 'POST':
        form = FotosAntesDepuesForm(request.POST, request.FILES)
        if form.is_valid():
            fotos = form.save(commit=False)
            fotos.cita = cita
            fotos.save()
            
            cita.estado = 'completada'
            cita.observaciones_peluquero = request.POST.get('observaciones_peluquero', '')
            cita.save()
            
            messages.success(request, 'Cita completada y fotos guardadas exitosamente.')
            return redirect('peluquero_dashboard')
    else:
        form = FotosAntesDepuesForm()
    
    context = {
        'peluquero': peluquero,
        'cita': cita,
        'form': form,
    }
    
    return render(request, 'veterinaria/peluqueria/peluquero_completar_cita.html', context)

@login_required
def peluquero_profile(request):
    """Perfil del peluquero con estadísticas completas"""
    from .models import Peluquero, CitaPeluqueria
    from .forms import PeluqueroProfileForm
    
    try:
        peluquero = Peluquero.objects.get(user=request.user)
    except Peluquero.DoesNotExist:
        messages.error(request, "No tienes permisos de peluquero.")
        return redirect('home')
    
    if request.method == 'POST':
        form = PeluqueroProfileForm(request.POST, instance=peluquero)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('peluquero_profile')
    else:
        form = PeluqueroProfileForm(instance=peluquero)
    
    # Calcular estadísticas
    total_citas = CitaPeluqueria.objects.filter(peluquero=peluquero).count()
    citas_completadas = CitaPeluqueria.objects.filter(
        peluquero=peluquero, 
        estado='completada'
    ).count()
    citas_pendientes = CitaPeluqueria.objects.filter(
        peluquero=peluquero,
        estado__in=['programada', 'confirmada']
    ).count()
    especialidades_count = peluquero.especialidades.count()
    
    context = {
        'peluquero': peluquero,
        'form': form,
        'total_citas': total_citas,
        'citas_completadas': citas_completadas,
        'citas_pendientes': citas_pendientes,
        'especialidades_count': especialidades_count,
    }
    
    return render(request, 'veterinaria/peluqueria/peluquero_profile.html', context)

@login_required
def galeria_peluqueria(request):
    """Galería de trabajos de peluquería - fotos antes/después"""
    from .models import FotosAntesDepues, CitaPeluqueria
    
    # Obtener fotos de trabajos completados
    fotos = FotosAntesDepues.objects.filter(
        cita__estado='completada'
    ).order_by('-fecha_subida')[:20]  # Últimas 20 fotos
    
    # Estadísticas para mostrar
    total_trabajos = CitaPeluqueria.objects.filter(estado='completada').count()
    total_fotos = FotosAntesDepues.objects.count()
    
    context = {
        'fotos': fotos,
        'total_trabajos': total_trabajos,
        'total_fotos': total_fotos,
    }
    
    return render(request, 'veterinaria/peluqueria/galeria.html', context)
