from .models import Carrito, ItemCarrito

def carrito_context(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        items = ItemCarrito.objects.filter(carrito=carrito)

        total = sum(item.producto.precio * item.cantidad for item in items)

        return {
            'cart_items': items,
            'cart_total': total,
            'cart_count': items.count()
        }

    return {
        'cart_items': [],
        'cart_total': 0,
        'cart_count': 0
    }