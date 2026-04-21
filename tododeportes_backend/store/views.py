from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, update_session_auth_hash

from .models import Producto, Carrito, ItemCarrito, Orden, ItemOrden, Categoria


def es_admin(user):
    return user.is_staff


def home(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})



@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)

    total = 0
    for item in items:
        item.total = item.producto.precio * item.cantidad
        total += item.total

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )

    if not created:
        item.cantidad += 1
        item.save()

    return redirect('cart')



@login_required
def checkout(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
    except Carrito.DoesNotExist:
        return redirect('cart')

    items = ItemCarrito.objects.filter(carrito=carrito)

    if not items.exists():
        return redirect('cart')

    total = 0

    orden = Orden.objects.create(usuario=request.user, total=0)

    for item in items:
        subtotal = item.producto.precio * item.cantidad
        total += subtotal

        ItemOrden.objects.create(
            orden=orden,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )

    orden.total = total
    orden.save()

    items.delete()

    return render(request, 'checkout_success.html', {'orden': orden})


import re
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        errors = {}

        if not email:
            errors['email'] = "El email es obligatorio"

        elif User.objects.filter(username=email).exists():
            errors['email'] = "Este email ya está registrado"

        if not password:
            errors['password'] = "La contraseña es obligatoria"

        elif password != confirm:
            errors['confirm'] = "Las contraseñas no coinciden"


        if password:
            if len(password) < 8:
                errors['password'] = "Debe tener mínimo 8 caracteres"

            elif len(password) > 20:
                errors['password'] = "Debe tener máximo 20 caracteres"

            elif not re.search(r'[A-Za-z]', password):
                errors['password'] = "Debe contener letras"

            elif not re.search(r'[0-9]', password):
                errors['password'] = "Debe contener números"

            elif not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
                errors['password'] = "Debe contener un carácter especial"

        if errors:
            return render(request, 'register.html', {
                'errors': errors,
                'email': email
            })

        User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def profile(request):
    context = {}

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        error = False

        if not nombre:
            context['error_nombre'] = "El nombre no puede estar vacío"
            error = True

        if password:
            if len(password) < 8:
                context['error_password'] = "Debe tener al menos 8 caracteres"
                error = True
            elif password != confirm:
                context['error_confirm'] = "Las contraseñas no coinciden"
                error = True

        if not error:
            user = request.user
            user.first_name = nombre

            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)

            user.save()
            context['success'] = True

    return render(request, 'profile.html', context)


@login_required
def admin_productos(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']
        categoria_id = request.POST['categoria']

        categoria = Categoria.objects.get(id=categoria_id)

        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria
        )

        return redirect('admin_productos')

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'admin_productos.html', {
        'productos': productos,
        'categorias': categorias
    })

@login_required
@user_passes_test(es_admin)
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')

        categoria_id = request.POST.get('categoria')
        producto.categoria = get_object_or_404(Categoria, id=categoria_id)

        producto.save()
        return redirect('admin_productos')

    categorias = Categoria.objects.all()

    return render(request, 'editar_producto.html', {
        'producto': producto,
        'categorias': categorias
    })

@login_required
@user_passes_test(es_admin)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        return redirect('admin_productos')

    return redirect('admin_productos')