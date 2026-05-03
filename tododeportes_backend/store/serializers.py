from rest_framework import serializers
from .models import Producto, Categoria, Orden, ItemOrden


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria']


class ItemOrdenSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = ItemOrden
        fields = ['id', 'producto', 'cantidad', 'precio']


class OrdenSerializer(serializers.ModelSerializer):
    items = ItemOrdenSerializer(source='itemorden_set', many=True, read_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'total', 'items']