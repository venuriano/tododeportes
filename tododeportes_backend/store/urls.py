from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('carrito/', views.ver_carrito, name='cart'),
    path('perfil/', views.profile, name='profile'),
    path('register/', views.register, name='register'),

    path('checkout/', views.checkout, name='checkout'),

    path('logout/', views.logout_view, name='logout'),  
     path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
     path('admin-productos/', views.admin_productos, name='admin_productos'),
    path('admin-productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('admin-productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
]