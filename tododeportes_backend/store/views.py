from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, update_session_auth_hash
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .serializers import ProductoSerializer, OrdenSerializer
from .models import Producto, Carrito, ItemCarrito, Orden, ItemOrden, Categoria
import re
import requests


def es_admin(user):
    return user.is_staff


def obtener_clima():
    cache_key = "clima_santiago"

    data = cache.get(cache_key)
    if data:
        return data

    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=-33.45&longitude=-70.66&current_weather=true"
        response = requests.get(url, timeout=3)
        response.raise_for_status()

        json_data = response.json()
        clima = json_data.get('current_weather', {})

        cache.set(cache_key, clima, timeout=300)  # 5 minutos
        return clima

    except Exception:
        return None


def obtener_monedas():
    cache_key = "monedas_usd"

    data = cache.get(cache_key)
    if data:
        return data

    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=3)
        response.raise_for_status()

        json_data = response.json()
        tasas = json_data.get('rates', {})

        resultado = {
            'usd_clp': tasas.get('CLP'),
            'usd_eur': tasas.get('EUR')
        }

        cache.set(cache_key, resultado, timeout=600)  # 10 minutos
        return resultado

    except Exception:
        return None


def home(request):
    productos = Producto.objects.all()

    clima = obtener_clima()
    monedas = obtener_monedas()

    return render(request, 'index.html', {
        'productos': productos,
        'clima': clima,
        'monedas': monedas
    })


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

    cantidad = int(request.POST.get('cantidad', 1))

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )

    if not created:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad

    item.save()

    return redirect('home')

@login_required
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)

    if item.carrito.usuario == request.user:
        item.delete()

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
        tipo = request.POST.get('tipo')

        user = request.user

        # ACTUALIZAR NOMBRE
        if tipo == 'datos':
            nombre = request.POST.get('nombre')

            if not nombre:
                context['error_nombre'] = "El nombre no puede estar vacío"
            else:
                user.first_name = nombre
                user.save()
                context['success_datos'] = True

        # CAMBIAR PASSWORD
        elif tipo == 'password':
            password = request.POST.get('password')
            confirm = request.POST.get('confirm_password')

            if len(password) < 8:
                context['error_password'] = "Debe tener al menos 8 caracteres"
            elif password != confirm:
                context['error_confirm'] = "No coinciden"
            else:
                user.set_password(password)
                update_session_auth_hash(request, user)
                context['success_password'] = True

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


# API REST

class ProductoListAPIView(generics.ListAPIView):
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductoSerializer


class ProductoDetailAPIView(generics.RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class MisOrdenesAPIView(generics.ListAPIView):
    serializer_class = OrdenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orden.objects.filter(
            usuario=self.request.user
        ).order_by('-id')

def clima_view(request):
    clima = obtener_clima()

    return render(request, 'clima.html', {
        'clima': clima
    })


def moneda_view(request):
    monedas = obtener_monedas()

    return render(request, 'moneda.html', {
        'usd_clp': monedas.get('usd_clp') if monedas else None,
        'usd_eur': monedas.get('usd_eur') if monedas else None,
    })