from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, MascotaForm, CitaForm, CarritoItemForm, PedidoForm
from .models import Mascota, Cita, Producto, Categoria, CarritoItem, Pedido, PedidoItem
from django.contrib.auth import login
from django.urls import reverse
from django.db.models import Sum, F
from decimal import Decimal

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

@login_required
def home(request):
    productos_destacados = Producto.objects.filter(es_destacado=True)[:4]
    context = {
        'productos_destacados': productos_destacados
    }
    
    if request.user.is_authenticated:
        context.update({
            'mascotas': Mascota.objects.filter(propietario=request.user),
            'citas_pendientes': Cita.objects.filter(
                mascota__propietario=request.user,
                estado__in=['pendiente', 'confirmada']
            ).order_by('fecha')
        })
    
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
        mascota.delete()
        messages.success(request, 'Mascota eliminada exitosamente.')
        return redirect('mascota_list')
    return render(request, 'veterinaria/mascota_confirm_delete.html', {'mascota': mascota})

@login_required
def cita_list(request):
    citas = Cita.objects.filter(mascota__propietario=request.user).order_by('-fecha')
    return render(request, 'veterinaria/cita_list.html', {'citas': citas})

@login_required
def cita_create(request):
    if request.method == 'POST':
        form = CitaForm(request.user, request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.estado = 'pendiente'
            cita.save()
            messages.success(request, 'Cita agendada exitosamente.')
            return redirect('cita_list')
    else:
        form = CitaForm(request.user)
    return render(request, 'veterinaria/cita_form.html', {'form': form, 'action': 'Agendar'})

@login_required
def cita_update(request, pk):
    cita = get_object_or_404(Cita, pk=pk, mascota__propietario=request.user)
    if request.method == 'POST':
        form = CitaForm(request.user, request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('cita_list')
    else:
        form = CitaForm(request.user, instance=cita)
    return render(request, 'veterinaria/cita_form.html', {'form': form, 'action': 'Actualizar'})

@login_required
def cita_cancel(request, pk):
    cita = get_object_or_404(Cita, pk=pk, mascota__propietario=request.user)
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
