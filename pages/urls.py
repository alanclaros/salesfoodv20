from django.urls import path
from pages.views import index, notificaciones_pagina, productos_inicio, sucursales_empresa, acerca_de, contactenos
from pages.views import carrito, without_permission, internal_error

urlpatterns = [
    path('', index, name='index'),

    path('productosinicio/', productos_inicio, name='productos_inicio'),
    path('sucursalesempresa/', sucursales_empresa, name='sucursales_empresa'),
    path('acercade/', acerca_de, name='acerca_de'),
    path('contactenos/', contactenos, name='contactenos'),
    # path('cambiarpassword/', views.cambiar_password, name='cambiar_password'),
    path('carrito/', carrito, name='carrito'),
    path('notificacionespagina/', notificaciones_pagina, name='notificaciones_pagina'),

    path('without_permission', without_permission, name='without_permission'),
    path('internal_error', internal_error, name='internal_error'),
]
