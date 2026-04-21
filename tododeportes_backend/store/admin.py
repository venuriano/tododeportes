from django.contrib import admin
from .models import Categoria, Producto, Carrito, ItemCarrito

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)