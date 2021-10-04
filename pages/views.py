from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.apps import apps
from django.urls import reverse
# cursor
from django.db import connection

# password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# configuraciones
from src.configuraciones.configuraciones import configuraciones_index
from src.configuraciones.proveedores import proveedores_index
from src.configuraciones.zonas import zonas_index
from src.configuraciones.sucursales import sucursales_index
from src.configuraciones.puntos import puntos_index
from src.configuraciones.lineas import lineas_index
from src.configuraciones.usuarios import usuarios_index

# cajas
from src.cajas.cajas_iniciar import cajas_iniciar_index
from src.cajas.cajas_iniciar_recibir import cajas_iniciar_recibir_index
from src.cajas.cajas_entregar import cajas_entregar_index
from src.cajas.cajas_entregar_recibir import cajas_entregar_recibir_index
from src.cajas.cajas_movimientos import cajas_movimientos_index
from src.cajas.cajas_ingresos import cajas_ingresos_index
from src.cajas.cajas_egresos import cajas_egresos_index

# productos
from src.productos.insumos import insumos_index
from src.productos.componentes import componentes_index
from src.productos.productos import productos_index

# inventarios
from src.inventarios.ingresos_almacen import ingresos_almacen_index
from src.inventarios.salidas_almacen import salidas_almacen_index
from src.inventarios.movimientos_almacen import movimientos_almacen_index

# reportes
from src.reportes.reportes import reportes_index

# clientes
from src.clientes.clientes import clientes_index

# ventas
from src.ventas.ventas import ventas_index
from src.planpagos.planpagos import plan_pagos_index

from decimal import Decimal

# utils
from utils.permissions import get_system_settings
# fechas
from utils.dates_functions import get_date_to_db, get_date_show, get_date_system

from controllers.SystemController import SystemController
from controllers.clientes.ClientesController import ClientesController
from controllers.ventas.VentasController import VentasController
from controllers.productos.ProductosController import ProductosController


def index(request):
    """pagina index"""

    if 'module_x' in request.POST.keys():
        module_id = int(request.POST['module_x'])

        # cambiar password
        if module_id == 1000:
            return cambiar_password(request)

        if module_id == settings.MOD_CONFIGURACIONES_SISTEMA:
            return configuraciones_index(request)

        if module_id == settings.MOD_PROVEEDORES:
            return proveedores_index(request)

        if module_id == settings.MOD_ZONAS:
            return zonas_index(request)

        if module_id == settings.MOD_SUCURSALES:
            return sucursales_index(request)

        if module_id == settings.MOD_PUNTOS:
            return puntos_index(request)

        if module_id == settings.MOD_LINEAS:
            return lineas_index(request)

        if module_id == settings.MOD_USUARIOS:
            return usuarios_index(request)

        # cajas
        # cajas
        if module_id == settings.MOD_INICIAR_CAJA:
            return cajas_iniciar_index(request)

        if module_id == settings.MOD_INICIAR_CAJA_RECIBIR:
            return cajas_iniciar_recibir_index(request)

        if module_id == settings.MOD_ENTREGAR_CAJA:
            return cajas_entregar_index(request)

        if module_id == settings.MOD_ENTREGAR_CAJA_RECIBIR:
            return cajas_entregar_recibir_index(request)

        if module_id == settings.MOD_CAJAS_INGRESOS:
            return cajas_ingresos_index(request)

        if module_id == settings.MOD_CAJAS_EGRESOS:
            return cajas_egresos_index(request)

        if module_id == settings.MOD_CAJAS_MOVIMIENTOS:
            return cajas_movimientos_index(request)

        # productos
        if module_id == settings.MOD_INSUMOS:
            return insumos_index(request)

        if module_id == settings.MOD_COMPONENTES:
            return componentes_index(request)

        if module_id == settings.MOD_PRODUCTOS:
            return productos_index(request)

        # inventarios
        if module_id == settings.MOD_INGRESOS_ALMACEN:
            return ingresos_almacen_index(request)

        if module_id == settings.MOD_SALIDAS_ALMACEN:
            return salidas_almacen_index(request)

        if module_id == settings.MOD_MOVIMIENTOS_ALMACEN:
            return movimientos_almacen_index(request)

        # clientes
        if module_id == settings.MOD_CLIENTES:
            return clientes_index(request)

        # ventas
        if module_id == settings.MOD_VENTAS:
            return ventas_index(request)

        # plan_pagos
        if module_id == settings.MOD_PLAN_PAGOS:
            return plan_pagos_index(request)

        # reportes
        if module_id == settings.MOD_REPORTES:
            return reportes_index(request)

        context = {
            'module_id': module_id,
        }

        return render(request, 'pages/nada.html', context)

    usuario = request.user
    #print('usuario: ', usuario)
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'
        usuario = {}

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    # webpush
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

    if settings.CURRENT_HOST == '127.0.0.1':
        url_productos = '/productosinicio/'
    else:
        url_productos = '/' + settings.SUB_URL_EMPRESA + '/productosinicio/'

    # lista de lineas
    system_controller = SystemController()
    listado_lineas = []

    if system_controller.model_exits('Lineas'):
        status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
        lista_lineas = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_principal=1).order_by('linea')

        for linea in lista_lineas:
            listado_lineas.append(linea)
            # verficamos sus sublineas
            listado2 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea.linea_id).order_by('linea')
            for linea2 in listado2:
                listado_lineas.append(linea2)
                # tercer nivel
                listado3 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea2.linea_id).order_by('linea')
                for linea3 in listado3:
                    listado_lineas.append(linea3)

    listado = []
    cant_fila = 3
    cant_actual = 0
    lista_fila = []
    contador = 0

    for linea_mostrar in listado_lineas:

        if cant_actual < cant_fila:
            dato_linea = {}
            dato_linea['linea'] = reemplazar_codigo_html(linea_mostrar.linea)
            dato_linea['linea_id'] = linea_mostrar.linea_id
            dato_linea['descripcion'] = reemplazar_codigo_html(linea_mostrar.descripcion)
            dato_linea['imagen'] = linea_mostrar.imagen
            dato_linea['imagen_thumb'] = linea_mostrar.imagen_thumb
            lista_fila.append(dato_linea)

        # aumentamos la columna
        cant_actual += 1

        if cant_actual == cant_fila:
            listado.append(lista_fila)
            cant_actual = 0
            lista_fila = []

        contador += 1

    # termina los productos
    if cant_actual > 0:
        # no termino de llenarse los datos de la fila
        for i in range(cant_actual, cant_fila):
            dato_linea = {}
            dato_linea['linea'] = ''
            dato_linea['linea_id'] = ''
            dato_linea['descripcion'] = ''
            dato_linea['imagen'] = ''
            dato_linea['imagen_thumb'] = ''
            lista_fila.append(dato_linea)

        # aniadimos a la lista principal
        listado.append(lista_fila)

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
        'pagina_inicio': 'si',
        'user': usuario,
        'vapid_key': vapid_key,
        'url_productos': url_productos,
        'lista_lineas': listado,
    }

    return render(request, 'pages/index.html', context)


def reemplazar_codigo_html(cadena):
    retorno = cadena
    retorno = retorno.replace('&', "&#38;")
    retorno = retorno.replace('#', "&#35;")

    retorno = retorno.replace("'", "&#39;")
    retorno = retorno.replace('"', "&#34;")
    retorno = retorno.replace('á', "&#225;")
    retorno = retorno.replace('é', "&#233;")
    retorno = retorno.replace('í', "&#237;")
    retorno = retorno.replace('ó', "&#243;")
    retorno = retorno.replace('ú', "&#250;")
    retorno = retorno.replace('Á', "&#193;")
    retorno = retorno.replace('É', "&#201;")
    retorno = retorno.replace('Í', "&#205;")
    retorno = retorno.replace('Ó', "&#211;")
    retorno = retorno.replace('Ú', "&#218;")
    retorno = retorno.replace('!', "&#33;")

    retorno = retorno.replace('$', "&#36;")
    retorno = retorno.replace('%', "&#37;")
    retorno = retorno.replace('*', "&#42;")
    retorno = retorno.replace('+', "&#43;")
    retorno = retorno.replace('-', "&#45;")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")

    return retorno


def cambiar_password(request):
    """cambio de password de los usuarios"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'
        return render(request, 'pages/without_permission.html')

    # por defecto
    usuario_actual = apps.get_model('auth', 'User').objects.get(pk=request.user.id)

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if operation == 'add':
            # verificamos
            error = 0
            password = request.POST['actual'].strip()
            nuevo = request.POST['nuevo'].strip()
            nuevo2 = request.POST['nuevo2'].strip()

            if error == 0 and nuevo == '' and nuevo2 == '':
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Debe llenar su nuevo password y su repeticion'})

            elif error == 0 and not check_password(password, usuario_actual.password):
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Error en su password'})

            elif error == 0 and nuevo != nuevo2:
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'La repeticion de su password no coincide'})

            elif error == 0 and len(nuevo) < 6:
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Su nuevo password debe tener al menos 6 letras'})

            if error == 0:
                # actualizamos
                usuario_actual.password = make_password(nuevo)
                usuario_actual.save()
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Usuario!', 'description': 'Su nuevo password se cambio correctamente'})

    context = {
        'autenticado': autenticado,
        'usuario_actual': usuario_actual,

        'module_x': 1000,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'pages/cambiar_password.html', context)


# carrito de compras
def carrito(request):
    """carrito de compras"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    system_settings = get_system_settings()
    vender_fracciones = system_settings['vender_fracciones']

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']

        # buscar CI cliente
        if operation == 'buscar_ci':
            ci_cliente = request.POST['ci'].strip()
            apellidos = ''
            nombres = ''
            telefonos = ''
            direccion = ''
            email = ''

            try:
                busqueda_cliente = apps.get_model('clientes', 'Clientes').objects.filter(ci_nit=ci_cliente)

                if busqueda_cliente:
                    cliente = busqueda_cliente.first()
                    apellidos = cliente.apellidos
                    nombres = cliente.nombres
                    telefonos = cliente.telefonos
                    direccion = cliente.direccion
                    email = cliente.email

            except Exception as ex:
                print('error al buscar CI')

            context = {
                'autenticado': autenticado,
                'apellidos': apellidos,
                'nombres': nombres,
                'telefonos': telefonos,
                'direccion': direccion,
                'email': email,
            }

            return render(request, 'pages/busqueda_ci_cliente.html', context)

        # eliminacion de un producto
        if operation == 'delete':
            posicion = request.POST['producto']
            lista = request.session['productos_cart']
            nueva_lista = []
            nueva_pos = 1
            for articulo in lista:
                if int(posicion) != articulo['posicion']:
                    articulo['posicion'] = nueva_pos
                    nueva_pos += 1
                    nueva_lista.append(articulo)

            request.session['productos_cart'] = nueva_lista
            request.session.modified = True

        # realizar pedido
        if operation == 'realizar_pedido':
            try:
                venta_controller = VentasController()
                cliente_controller = ClientesController()

                ci = request.POST['ci'].strip()
                nombres = request.POST['nombres'].strip()
                apellidos = request.POST['apellidos'].strip()
                telefonos = request.POST['telefonos'].strip()
                direccion = request.POST['direccion'].strip()
                email = request.POST['email'].strip()
                mensaje = request.POST['mensaje'].strip()
                tipo_pedido = request.POST['tipo_pedido']
                lista_ids = request.POST['lista_productos_ids'].strip()
                lista_cantidad = request.POST['lista_cantidad'].strip()

                # datos de la venta
                usuario = apps.get_model('auth', 'User').objects.get(pk=1)
                user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)
                punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
                caja = apps.get_model('configuraciones', 'Cajas').objects.get(pk=user_perfil.caja_id)

                if user_perfil.punto_id == 1:
                    # almacen central
                    almacen = apps.get_model('configuraciones', 'Almacenes').objects.get(pk=1)
                else:
                    punto_almacen = apps.get_model('configuraciones', 'PuntosAlmacenes').objects.filter(punto_id=punto)
                    if punto_almacen:
                        punto_a = punto_almacen.first()
                        almacen = punto_a.almacen_id
                    else:
                        almacen = 'sin almacen'

                lugar_id = apps.get_model('ventas', 'Lugares').objects.get(pk=settings.LUGAR_PEDIDO_INTERNET)

                # cliente
                cliente_aux = apps.get_model('clientes', 'Clientes').objects.filter(ci_nit=ci)
                if cliente_aux:
                    cliente_id = cliente_aux.first()
                else:
                    datos = {}
                    datos['id'] = 0
                    datos['apellidos'] = apellidos
                    datos['nombres'] = nombres
                    datos['ci_nit'] = ci
                    datos['telefonos'] = telefonos
                    datos['direccion'] = direccion
                    datos['email'] = email
                    datos['razon_social'] = apellidos
                    datos['factura_a'] = apellidos
                    datos['created_at'] = 'now'
                    datos['updated_at'] = 'now'
                    datos['user_perfil_id'] = user_perfil
                    datos['status_id'] = cliente_controller.status_activo
                    datos['punto_id'] = punto

                    if cliente_controller.save_db(type='add', **datos):
                        cliente_id = apps.get_model('clientes', 'Clientes').objects.get(ci_nit=ci)
                    else:
                        error = 1
                        return False

                campos_add = {}
                campos_add['tipo_operacion'] = 'internet'
                campos_add['pedido_id'] = 0
                campos_add['apellidos'] = apellidos
                campos_add['nombres'] = nombres
                campos_add['ci_nit'] = ci
                campos_add['telefonos'] = telefonos
                campos_add['direccion'] = direccion
                campos_add['mesa'] = ''
                campos_add['observacion'] = mensaje

                campos_add['tipo_venta'] = 'CONTADO'
                campos_add['costo_abc'] = 'A'
                campos_add['fecha'] = 'now'
                campos_add['user_perfil_id_fecha'] = user_perfil.user_perfil_id
                campos_add['subtotal'] = 0
                campos_add['descuento'] = 0
                campos_add['porcentaje_descuento'] = 0
                campos_add['total'] = 0
                campos_add['saldo'] = 0
                campos_add['concepto'] = 'VENTAS INTERNET: CI: ' + ci + ', ' + apellidos + ' ' + nombres
                campos_add['created_at'] = 'now'
                campos_add['updated_at'] = 'now'

                campos_add['almacen_id'] = almacen
                campos_add['caja_id'] = caja
                campos_add['cliente_id'] = cliente_id
                campos_add['lugar_id'] = lugar_id
                campos_add['punto_id'] = punto

                campos_add['status_id'] = venta_controller.status_preventa
                campos_add['user_perfil_id'] = user_perfil

                # detalles de la venta
                detalles = []

                error = 0
                total_pedido = 0

                if lista_cantidad == '':
                    error = 1
                else:
                    division_ids = lista_ids.split('|')
                    division_cant = lista_cantidad.split('|')
                    pos_index = 0

                    # recorremos la lista que envio desde la web
                    for i in range(0, len(division_ids)):
                        p_id = division_ids[i]
                        cant = division_cant[i]

                        # recorremos la session
                        lista_session = request.session['productos_cart']

                        for articulo in lista_session:
                            if int(p_id) == articulo['posicion']:
                                #print('articulo: ', articulo['detalle']['lista_componentes'])
                                dato_detalle = {}
                                dato_detalle['producto_id'] = apps.get_model('productos', 'Productos').objects.get(pk=int(articulo['producto_id']))
                                dato_detalle['cantidad'] = int(cant)
                                dato_detalle['costo'] = Decimal(articulo['costo'])
                                dato_detalle['total'] = int(cant) * Decimal(articulo['costo'])

                                # componentes
                                p_componentes = []
                                if articulo['detalle']['lista_componentes']:
                                    for componente in articulo['detalle']['lista_componentes']:
                                        dato_componente = {}
                                        dato_componente['componente_id'] = int(componente['componente_id'])
                                        dato_componente['activo'] = componente['activo']

                                        p_componentes.append(dato_componente)
                                # asignamos
                                dato_detalle['lista_componentes'] = p_componentes

                                # refrescos
                                p_refrescos = []
                                if articulo['detalle']['lista_refrescos']:
                                    for refresco in articulo['detalle']['lista_refrescos']:
                                        dato_refresco = {}
                                        dato_refresco['refresco_grupo_id'] = refresco['refresco_grupo_id']
                                        dato_refresco['activo'] = refresco['activo']
                                        dato_refresco['precio'] = refresco['precio']

                                        p_refrescos.append(dato_refresco)
                                # asignamos
                                dato_detalle['lista_refrescos'] = p_refrescos

                                # papas
                                p_papas = []
                                if articulo['detalle']['lista_papas']:
                                    for papa in articulo['detalle']['lista_papas']:
                                        dato_papa = {}
                                        dato_papa['papa_grupo_id'] = papa['papa_grupo_id']
                                        dato_papa['activo'] = papa['activo']
                                        dato_papa['precio'] = papa['precio']

                                        p_papas.append(dato_papa)
                                # asignamos
                                dato_detalle['lista_papas'] = p_papas

                                # extras
                                p_extras = []
                                if articulo['detalle']['lista_extras']:
                                    for extra in articulo['detalle']['lista_extras']:
                                        dato_extra = {}
                                        dato_extra['extra_id'] = extra['extra_id']
                                        dato_extra['activo'] = extra['activo']
                                        dato_extra['precio'] = extra['precio']

                                        p_extras.append(dato_extra)
                                # asignamos
                                dato_detalle['lista_extras'] = p_extras

                                # asigamos a la lista de detalles
                                detalles.append(dato_detalle)

                    # datos de la venta
                    campos_add['detalles'] = detalles

                    # creamos la venta
                    if venta_controller.save_db(type='add', **campos_add):
                        error = 0
                        # borramos la session
                        request.session['productos_cart'] = []
                        request.session.modified = True
                    else:
                        error = 1

                context = {
                    'autenticado': autenticado,
                    'total_pedido': total_pedido,
                    'url_carrito': reverse('carrito'),
                    'error': error,
                }

                return render(request, 'pages/carrito_compras_resultado.html', context)

            except Exception as ex:
                print('error: ', str(ex))
                context = {
                    'autenticado': autenticado,
                    'total_pedido': 0,
                    'url_carrito': reverse('carrito'),
                    'error': 1,
                }

                return render(request, 'pages/carrito_compras_resultado.html', context)

    # carrito de compras
    cantidad_cart = 0
    lista_productos = []
    total_pedido = 0
    lista_ids = ''

    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])
        lista = request.session['productos_cart']
        for articulo in lista:
            #print('articulo: ', articulo)
            #producto = apps.get_model('productos', 'Productos').objects.get(pk=int(articulo['producto']))
            producto = articulo['producto_producto']
            posicion = articulo['posicion']
            cantidad = articulo['cantidad']
            costo = articulo['costo']
            total = articulo['total']
            lista_ids += str(posicion)+';'

            dato = {}
            dato['posicion'] = posicion
            dato['producto'] = producto
            dato['producto_id'] = articulo['producto_id']
            dato['cantidad'] = cantidad
            dato['precio'] = costo
            dato['total'] = total
            dato['detalle'] = articulo['detalle']

            total_pedido += Decimal(total)

            lista_productos.append(dato)

        if len(lista_ids) > 0:
            lista_ids = lista_ids[0: len(lista_ids)-1]

    # webpush
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

    # usuarios para la notificacion
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    usuarios_notificacion = apps.get_model('permisos', 'UsersPerfiles').objects.filter(status_id=status_activo, notificacion=1).order_by('user_perfil_id')
    lista_notificacion = ''
    for usuario_notif in usuarios_notificacion:
        lista_notificacion += str(usuario_notif.user_id.id) + '|'

    if len(lista_notificacion) > 0:
        lista_notificacion = lista_notificacion[0:len(lista_notificacion)-1]

    if settings.CURRENT_HOST == '127.0.0.1':
        url_push = '/send_push'
    else:
        url_push = '/' + settings.SUB_URL_EMPRESA + '/send_push'

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'lista_productos': lista_productos,
        'total_pedido': total_pedido,
        'url_carrito': reverse('carrito'),
        'url_webpush': url_push,
        'lista_ids': lista_ids,
        'lista_notificacion': lista_notificacion,
        'vapid_key': vapid_key,
        'vender_fracciones': vender_fracciones,
    }

    return render(request, 'pages/carrito_compras.html', context)


# notificaciones para el usuario
def notificaciones_pagina(request):
    # context = {'abc': 'asdd'}
    # return render(request, 'pages/nada.html', context)

    url_pedidos_cliente = reverse('index')

    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    if autenticado == 'no':
        context = {
            'cantidad': 0,
            'cantidad_rojos': 0,
            'notificaciones': {},
            'autenticado': autenticado,
        }
        return render(request, 'pages/notificaciones_pagina.html', context)

    try:
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)

        notificaciones = []
        cantidad = 0
        cantidad_rojos = 0

        # lista pedidos
        sql = "SELECT v.venta_id, v.apellidos, v.nombres, v.ci_nit, v.fecha, v.total "
        sql += f"FROM ventas v WHERE v.status_id='{settings.STATUS_PREVENTA}' ORDER BY v.fecha DESC "

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                cantidad += 1
                cantidad_rojos += 1
                dato = {}
                dato['tipo'] = 'pedido'
                fecha = get_date_show(fecha=row[4], formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')
                dato['descripcion'] = fecha + ', ' + row[1] + ' ' + row[2] + ', ' + str(row[5]) + ' Bs.'
                dato['url'] = url_pedidos_cliente
                notificaciones.append(dato)

        # context para el html
        context = {
            'notificaciones': notificaciones,
            'cantidad': cantidad,
            'cantidad_rojos': cantidad_rojos,
            'autenticado': autenticado,
        }

        return render(request, 'pages/notificaciones_pagina.html', context)

    except Exception as e:
        print('ERROR ' + str(e))
        context = {
            'cantidad': 0,
            'cantidad_rojos': 0,
            'notificaciones': {},
            'autenticado': autenticado,
        }
        return render(request, 'pages/notificaciones_pagina.html', context)


def sucursales_empresa(request):
    """sucursales de la empresa"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
    }

    return render(request, 'pages/sucursales_empresa.html', context)


def acerca_de(request):
    """acerca la empresa"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
    }

    return render(request, 'pages/acerca_de.html', context)


def contactenos(request):
    """formulario de contacto"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    url_main = reverse('contactenos')

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if operation == 'contacto':
            error = 0
            try:
                nombres = request.POST['nombres'].strip()
                apellidos = request.POST['apellidos'].strip()
                telefonos = request.POST['telefonos'].strip()
                email_cliente = request.POST['email'].strip()
                mensaje = request.POST['mensaje'].strip()

                # Import the email modules we'll need
                from email.message import EmailMessage
                import smtplib

                # Create a text/plain message
                separador = "\n"
                email_content = f"Mensaje: {separador}Nombre: {apellidos} {nombres}{separador}Fonos: {telefonos}{separador}Email: {email_cliente}{separador}Mensaje: {mensaje}"
                msg = EmailMessage()
                msg.set_content(email_content)

                # me == the sender's email address
                # you == the recipient's email address
                msg['Subject'] = 'PVI - mensaje, ' + settings.SUB_URL_EMPRESA
                msg['From'] = settings.EMAIL_CONTACT_FROM
                # msg['To'] = settings.EMAIL_CONTACT_TO
                msg['To'] = 'acc.claros@gmail.com, alan_claros13@hotmail.com'

                # Send the message via our own SMTP server.
                s = smtplib.SMTP(settings.EMAIL_SERVER_NAME)
                s.send_message(msg)
                s.quit()

            except Exception as e:
                print('Error al enviar el mensaje: ' + str(e))
                error = 1

            context_p = {
                'autenticado': autenticado,
                'error': error,
            }

            return render(request, 'pages/contactenos_mail.html', context_p)

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    context = {
        'autenticado': autenticado,
        'url_main': url_main,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
    }

    return render(request, 'pages/contactenos.html', context)


def productos_inicio(request):
    """productos de la pagina de inicio"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    system_settings = get_system_settings()
    vender_fracciones = system_settings['vender_fracciones']

    if 'showpid' in request.GET.keys():
        show_pid = request.GET['showpid'].strip()
        try:
            producto = apps.get_model('productos', 'Productos').objects.get(pk=int(show_pid))
            productos_imagenes = apps.get_model('productos', 'ProductosImagenes').objects.filter(producto_id=producto).order_by('posicion')

            context_p = {
                'imagen': productos_imagenes.first().imagen,
                'producto': producto.producto,
            }

            return render(request, 'pages/productos_solo_imagen.html', context_p)

        except Exception as ex:
            context_p = {
                'imagen': '',
                'producto': ''
            }

            return render(request, 'pages/productos_solo_imagen.html', context_p)

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']

        if operation == 'img_producto':
            p_id = request.POST['id']
            # recuperamos la lista de imagenes
            producto = apps.get_model('productos', 'Productos').objects.get(pk=int(p_id))
            productos_imagenes = apps.get_model('productos', 'ProductosImagenes').objects.filter(producto_id=producto).order_by('posicion')

            context_p = {
                'autenticado': autenticado,
                'productos_imagenes': productos_imagenes,
            }

            return render(request, 'pages/productos_inicio_imagenes.html', context_p)

        if operation == 'add_cart':
            producto_controller = ProductosController()

            p_id = request.POST['producto_id']
            cantidad = request.POST['cantidad_'+p_id]
            producto = apps.get_model('productos', 'Productos').objects.get(pk=int(p_id))
            costo = request.POST['costo_'+p_id]
            total = request.POST['total_'+p_id]

            detalle_producto = producto_controller.datos_producto(int(p_id))
            dato_detalle = {}
            costo_adicional = 0
            # componentes
            p_componentes = []
            if detalle_producto['lista_componentes']:
                for aux_detalle in detalle_producto['lista_componentes']:
                    nombre = 'componente_' + p_id + '_' + str(aux_detalle['componente_id'])
                    nombre2 = 'componente_nombre_' + p_id + '_' + str(aux_detalle['componente_id'])

                    dato_componente = {}
                    dato_componente['componente_id'] = aux_detalle['componente_id']
                    dato_componente['componente'] = request.POST[nombre2]
                    dato_componente['activo'] = int(request.POST[nombre])

                    p_componentes.append(dato_componente)
            # asignamos
            dato_detalle['lista_componentes'] = p_componentes

            # refrescos
            p_refrescos = []
            if detalle_producto['lista_refrescos']:
                for aux_refresco in detalle_producto['lista_refrescos']:
                    nombre = 'refresco_' + p_id + '_' + str(aux_refresco['refresco_grupo_id'])
                    nombre2 = 'refresco_nombre_' + p_id + '_' + str(aux_refresco['refresco_grupo_id'])

                    dato_refresco = {}
                    dato_refresco['refresco_grupo_id'] = aux_refresco['refresco_grupo_id']
                    dato_refresco['refresco'] = request.POST[nombre2]
                    dato_refresco['activo'] = int(request.POST[nombre])
                    if int(request.POST[nombre]) == 1:
                        costo_adicional += aux_refresco['precio']

                    dato_refresco['precio'] = str(aux_refresco['precio'])

                    p_refrescos.append(dato_refresco)
            # asignamos
            dato_detalle['lista_refrescos'] = p_refrescos

            # papas
            p_papas = []
            if detalle_producto['lista_papas']:
                for aux_papa in detalle_producto['lista_papas']:
                    nombre = 'papa_' + p_id + '_' + str(aux_papa['papa_grupo_id'])
                    nombre2 = 'papa_nombre_' + p_id + '_' + str(aux_papa['papa_grupo_id'])

                    dato_papa = {}
                    dato_papa['papa_grupo_id'] = aux_papa['papa_grupo_id']
                    dato_papa['papa'] = request.POST[nombre2]
                    dato_papa['activo'] = int(request.POST[nombre])
                    if int(request.POST[nombre]) == 1:
                        costo_adicional += aux_papa['precio']

                    dato_papa['precio'] = str(aux_papa['precio'])

                    p_papas.append(dato_papa)
            # asignamos
            dato_detalle['lista_papas'] = p_papas

            # extras
            p_extras = []
            if detalle_producto['lista_extras']:
                for aux_extra in detalle_producto['lista_extras']:
                    nombre = 'extra_' + p_id + '_' + str(aux_extra['componente_id'])
                    nombre2 = 'extra_nombre_' + p_id + '_' + str(aux_extra['componente_id'])

                    dato_extra = {}
                    dato_extra['extra_id'] = aux_extra['componente_id']
                    dato_extra['extra'] = request.POST[nombre2]
                    dato_extra['activo'] = int(request.POST[nombre])
                    if int(request.POST[nombre]) == 1:
                        costo_adicional += aux_extra['precio']

                    dato_extra['precio'] = str(aux_extra['precio'])

                    p_extras.append(dato_extra)
            # asignamos
            dato_detalle['lista_extras'] = p_extras

            # verificamos la session
            pos_lista = 0
            if not 'productos_cart' in request.session.keys():
                request.session['productos_cart'] = []
                request.session.modified = True

            # verificamos si existe el producto
            existe_producto = 'no'
            lista_session = request.session['productos_cart']
            pos_lista = len(lista_session) + 1

            # aniadimos en caso que no exista
            if existe_producto == 'no':
                dato = {}
                dato['posicion'] = pos_lista
                dato['producto_id'] = p_id
                dato['producto_producto'] = producto.producto
                dato['cantidad'] = cantidad
                dato['costo'] = costo
                dato['total'] = total
                dato['detalle'] = dato_detalle

                lista_session.append(dato)

            # actualizamos variables de session
            request.session['productos_cart'] = lista_session
            request.session.modified = True

            context_p = {
                'autenticado': autenticado,
                'cantidad_cart': len(lista_session),
                'url_carrito': reverse('carrito'),
            }

            return render(request, 'pages/productos_inicio_cart.html', context_p)

    # session
    if not 'productosinicio' in request.session.keys():
        request.session['productosinicio'] = {}
        request.session['productosinicio']['producto'] = ''
        request.session['productosinicio']['linea'] = 0
        # pagina
        request.session['productosinicio']['pagina'] = 1
        request.session['productosinicio']['pages_list'] = []

    if 'search_producto_x' in request.POST.keys():
        request.session['productosinicio']['producto'] = request.POST['producto'].strip()
        request.session['productosinicio']['linea'] = 0
        # pagina
        request.session['productosinicio']['pagina'] = 1

    if 'search_linea_x' in request.POST.keys():
        request.session['productosinicio']['linea'] = int(request.POST['linea'].strip())
        request.session['productosinicio']['producto'] = ''
        # pagina
        request.session['productosinicio']['pagina'] = 1

    # si seleccionana una pagina
    if 'pagina' in request.POST.keys():
        request.session['productosinicio']['pagina'] = int(request.POST['pagina'])

    # guardamos datos de session
    request.session.modified = True
    # print('session: ', request.session['productosinicio'])

    producto_busqueda = request.session['productosinicio']['producto']
    linea_id = request.session['productosinicio']['linea']
    pagina = request.session['productosinicio']['pagina']

    # lista de productos por proveedor y linea
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    lista_lineas_aux = apps.get_model('configuraciones', 'Lineas').objects.select_related('proveedor_id').filter(status_id=status_activo, linea_principal=1).order_by('proveedor_id__proveedor', 'linea')
    # linea1
    linea1 = lista_lineas_aux.first()
    lista_lineas = []
    for linea in lista_lineas_aux:
        linea_obj = {}
        linea_obj['linea_id'] = linea.linea_id
        linea_obj['linea'] = linea.linea
        linea_obj['espacios'] = ''
        lista_lineas.append(linea_obj)

        # verificamos si tiene lineas inferiores
        lineas_inf1 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea.linea_id).order_by('linea')

        for linea_dato_inf1 in lineas_inf1:
            linea_obj = {}
            linea_obj['linea_id'] = linea_dato_inf1.linea_id
            linea_obj['linea'] = linea_dato_inf1.linea
            linea_obj['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            lista_lineas.append(linea_obj)

            # verificamos lineas inferiores nivel2
            lineas_inf2 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea_dato_inf1.linea_id).order_by('linea')
            for linea_dato_inf2 in lineas_inf2:
                linea_obj2 = {}
                linea_obj2['linea_id'] = linea_dato_inf2.linea_id
                linea_obj2['linea'] = linea_dato_inf2.linea
                linea_obj2['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * 2
                lista_lineas.append(linea_obj2)

                # verificamos lineas inferiores nivel3
                lineas_inf3 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea_dato_inf2.linea_id).order_by('linea')
                for linea_dato_inf3 in lineas_inf3:
                    linea_obj3 = {}
                    linea_obj3['linea_id'] = linea_dato_inf3.linea_id
                    linea_obj3['linea'] = linea_dato_inf3.linea
                    linea_obj3['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * 3
                    lista_lineas.append(linea_obj3)

    # descripcion del producto
    txt_producto = ''

    if producto_busqueda == '':
        if linea_id == 0:
            lista_pro = lista_productos(request, linea_id=linea1.linea_id, producto_nombre='')
            # txt_producto = linea1.proveedor_id.proveedor + ' - ' + linea1.linea
            txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + link_linea(linea1.linea_id)
        else:
            lista_pro = lista_productos(request, linea_id=linea_id, producto_nombre='')
            linea_actual = apps.get_model('configuraciones', 'Lineas').objects.select_related('proveedor_id').get(pk=int(linea_id))
            #txt_producto = linea_actual.proveedor_id.proveedor + ' - ' + linea_actual.linea
            txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + link_linea(linea_actual.linea_id)
    else:
        lista_pro = lista_productos(request, linea_id=0, producto_nombre=producto_busqueda)
        txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + ' / ' + producto_busqueda

    url_main = reverse('productos_inicio')
    url_carrito = reverse('carrito')

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    # detalle del producto
    if 'id' in request.GET.keys() and 'producto' in request.GET.keys():
        producto_controller = ProductosController()

        p_id = request.GET['id']
        # recuperamos datos del producto y sus imagenes
        producto_aux = apps.get_model('productos', 'Productos').objects.get(pk=int(p_id))
        productos_imagenes = apps.get_model('productos', 'ProductosImagenes').objects.filter(producto_id=producto_aux).order_by('posicion')

        producto = {}
        producto['producto_id'] = producto_aux.producto_id
        producto['producto'] = reemplazar_codigo_html(producto_aux.producto)
        producto['codigo'] = producto_aux.codigo
        producto['unidad'] = producto_aux.unidad

        producto['descripcion'] = reemplazar_codigo_html(producto_aux.descripcion1)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion2)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion3)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion4)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion5)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion6)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion7)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion8)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion9)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion10)
        producto['descripcion'] = producto['descripcion'].strip()

        producto['descripcion1'] = reemplazar_codigo_html(producto_aux.descripcion1)
        producto['descripcion2'] = reemplazar_codigo_html(producto_aux.descripcion2)
        producto['descripcion3'] = reemplazar_codigo_html(producto_aux.descripcion3)
        producto['descripcion4'] = reemplazar_codigo_html(producto_aux.descripcion4)
        producto['descripcion5'] = reemplazar_codigo_html(producto_aux.descripcion5)
        producto['descripcion6'] = reemplazar_codigo_html(producto_aux.descripcion6)
        producto['descripcion7'] = reemplazar_codigo_html(producto_aux.descripcion7)
        producto['descripcion8'] = reemplazar_codigo_html(producto_aux.descripcion8)
        producto['descripcion9'] = reemplazar_codigo_html(producto_aux.descripcion9)
        producto['descripcion10'] = reemplazar_codigo_html(producto_aux.descripcion10)

        producto['precio'] = producto_aux.precio_a

        tallas = []

        imagen1 = ''
        if productos_imagenes:
            primera = productos_imagenes.first()
            imagen1 = primera.imagen

        # productos relacionados
        lista_relacionados = apps.get_model('productos', 'ProductosRelacionados').objects.filter(producto_id=producto_aux).order_by('producto_id__producto')

        # listado de retorno
        listado = []
        cant_fila = 3
        cant_actual = 0
        lista_fila = []
        contador = 0

        for producto_r in lista_relacionados:

            if cant_actual < cant_fila:
                dato_producto = {}
                dato_producto['linea'] = producto_r.producto_relacion_id.linea_id.linea
                dato_producto['producto'] = reemplazar_codigo_html(producto_r.producto_relacion_id.producto)
                dato_producto['codigo'] = producto_r.producto_relacion_id.codigo
                dato_producto['unidad'] = producto_r.producto_relacion_id.unidad
                dato_producto['precio'] = producto_r.producto_relacion_id.precio_a
                dato_producto['producto_id'] = producto_r.producto_relacion_id.producto_id

                pi_relacion = apps.get_model('productos', 'ProductosImagenes').objects.filter(producto_id=producto_r.producto_relacion_id).order_by('posicion')
                if pi_relacion:
                    primera_imagen = pi_relacion.first()
                    dato_producto['imagen'] = primera_imagen.imagen
                    dato_producto['imagen_thumb'] = primera_imagen.imagen_thumb
                else:
                    dato_producto['imagen'] = ''
                    dato_producto['imagen_thumb'] = ''

                lista_fila.append(dato_producto)

            # aumentamos la columna
            cant_actual += 1

            if cant_actual == cant_fila:
                listado.append(lista_fila)
                cant_actual = 0
                lista_fila = []

            contador += 1

        # termina los productos
        if cant_actual > 0:
            # no termino de llenarse los datos de la fila
            for i in range(cant_actual, cant_fila):
                dato_producto = {}
                dato_producto['linea'] = ''
                dato_producto['producto'] = ''
                dato_producto['codigo'] = ''
                dato_producto['unidad'] = ''
                dato_producto['precio'] = 0
                dato_producto['producto_id'] = 0
                dato_producto['imagen'] = ''
                dato_producto['imagen_thumb'] = ''
                lista_fila.append(dato_producto)

            # aniadimos a la lista principal
            listado.append(lista_fila)

        # devolvemos los productos
        # return listado

        detalle_producto = producto_controller.datos_producto(int(p_id))

        context_p = {
            'autenticado': autenticado,
            'lista_lineas': lista_lineas,
            'linea_session': request.session['productosinicio']['linea'],
            'producto_session': request.session['productosinicio']['producto'],
            'detalle_producto': detalle_producto,
            'url_main': url_main,
            'url_carrito': url_carrito,
            'url_index': reverse('index'),
            'cantidad_cart': cantidad_cart,
            'txt_producto': txt_producto,
            'vender_fracciones': vender_fracciones,

            'productos_relacionados': listado,

            'producto': producto,
            'imagen1': imagen1,
            'productos_imagenes': productos_imagenes,
            'tallas': tallas,
        }

        return render(request, 'pages/productos_inicio_detalle.html', context_p)

    context = {
        'autenticado': autenticado,
        'lista_lineas': lista_lineas,
        'listado_productos': lista_pro,
        'linea_session': request.session['productosinicio']['linea'],
        'producto_session': request.session['productosinicio']['producto'],
        'url_main': url_main,
        'url_carrito': url_carrito,
        'url_index': reverse('index'),
        'pages_list': request.session['productosinicio']['pages_list'],
        'pagina_actual': request.session['productosinicio']['pagina'],
        'cantidad_cart': cantidad_cart,
        'txt_producto': txt_producto,
        'vender_fracciones': vender_fracciones,
    }

    return render(request, 'pages/productos_inicio.html', context)


def without_permission(request):
    return render(request, 'pages/without_permission.html')


def internal_error(request):
    context = {
        'error': request.session['internal_error'],
    }
    return render(request, 'pages/internal_error.html', context)


def link_linea(linea_id):
    try:
        linea = apps.get_model('configuraciones', 'Lineas').objects.get(pk=int(linea_id))
        retorno = ''
        if linea.linea_principal == 1:
            retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'

        else:
            # linea principal antes
            linea_sup1 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea.linea_superior_id)

            if linea_sup1.linea_principal == 1:
                retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'
            else:
                # otra linea superior antes
                linea_sup2 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea_sup1.linea_superior_id)

                if linea_sup2.linea_principal == 1:
                    retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup2.linea_id) + "'" + ');">' + linea_sup2.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'
                else:
                    linea_sup3 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea_sup2.linea_superior_id)
                    retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup3.linea_id) + "'" + ');">' + linea_sup3.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup2.linea_id) + "'" + ');">' + linea_sup2.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'

        return retorno

    except Exception as ex:
        retorno = ''
        return retorno


def lista_productos(request, linea_id=0, producto_nombre=''):
    producto = reemplazar_codigo_html(producto_nombre.strip())

    """lista de productos segun linea o ubicacion"""
    settings_sistema = get_system_settings()
    cant_per_page = settings_sistema['cant_products_home']

    # verificamos si escribo busqueda o selecciono combo
    sql_add = "AND p.status_id='1' AND l.status_id='1' "

    if linea_id != 0:
        sql_add += f"AND l.linea_id='{linea_id}' "

    if producto != '':
        division = producto.split(' ')
        if len(division) == 1:
            sql_add += f"AND p.producto LIKE '%{producto}%' "
        elif len(division) == 2:
            sql_add += f"AND (p.producto LIKE '%{division[0]}%{division[1]}%' OR p.producto LIKE '%{division[1]}%{division[0]}%' "
            sql_add += ') '
        # if len(division) == 3:
        elif len(division) == 3:
            sql_add += f"AND (p.producto LIKE '%{division[0]}%{division[1]}%{division[2]}%' "
            sql_add += f"OR p.producto LIKE '%{division[0]}%{division[2]}%{division[1]}%' "

            sql_add += f"OR p.producto LIKE '%{division[1]}%{division[0]}%{division[2]}%' "
            sql_add += f"OR p.producto LIKE '%{division[1]}%{division[2]}%{division[0]}%' "

            sql_add += f"OR p.producto LIKE '%{division[2]}%{division[0]}%{division[1]}%' "
            sql_add += f"OR p.producto LIKE '%{division[2]}%{division[1]}%{division[0]}%' "

            sql_add += ') '
        else:
            nuevo_p = '%'
            for i in range(len(division)):
                nuevo_p += division[i] + '%'

            sql_add += f"AND p.producto LIKE '{nuevo_p}' "

    # cantidad de registros
    sql = 'SELECT COUNT(*) AS cant '
    sql += "FROM productos p, lineas l WHERE p.linea_id=l.linea_id " + sql_add

    cant_total = 0
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        cant_total = row[0]

    # si selecciono una linea sumamos los productos de sus sublineas
    if linea_id != 0:
        sql = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{linea_id}' AND status_id='1' "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                # contamos los productos
                sql_p = f"SELECT COUNT(*) AS cant FROM productos WHERE status_id='1' AND linea_id='{row[0]}' "
                with connection.cursor() as cursor2:
                    cursor2.execute(sql_p)
                    row_p = cursor2.fetchone()
                    cant_total += row_p[0]

                # segundo subnivel
                sql_2 = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{row[0]}' AND status_id='1' "
                with connection.cursor() as cursor22:
                    cursor22.execute(sql_2)
                    rows2 = cursor22.fetchall()
                    for row2 in rows2:
                        # contamos los productos
                        sql_p2 = f"SELECT COUNT(*) AS cant FROM productos WHERE status_id='1' AND linea_id='{row2[0]}' "
                        with connection.cursor() as cursor23:
                            cursor23.execute(sql_p2)
                            row_p2 = cursor23.fetchone()
                            cant_total += row_p2[0]

                        # tercer subnivel
                        sql_3 = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{row2[0]}' AND status_id='1' "
                        with connection.cursor() as cursor33:
                            cursor33.execute(sql_3)
                            rows3 = cursor33.fetchall()
                            for row3 in rows3:
                                # contamos los productos
                                sql_p3 = f"SELECT COUNT(*) AS cant FROM productos WHERE status_id='1' AND linea_id='{row3[0]}' "
                                with connection.cursor() as cursor44:
                                    cursor44.execute(sql_p3)
                                    row_p3 = cursor44.fetchone()
                                    cant_total += row_p3[0]

    #print('cantidad total: ', cant_total)
    j = 1
    i = 0
    pages_list = []
    while i < cant_total:
        pages_list.append(j)
        i = i + cant_per_page
        j += 1
        if j > 15:
            break

    request.session['productosinicio']['pages_list'] = pages_list
    request.session.modified = True

    pages_limit_bottom = (int(request.session['productosinicio']['pagina']) - 1) * cant_per_page
    pages_limit_top = cant_per_page

    # listado de productos
    lista_pp = []

    # por busqueda de texto de productos
    if linea_id == 0:
        sql = 'SELECT l.linea, p.producto, p.codigo, p.unidad, p.precio_a, p.producto_id, l.linea_id '
        sql += "FROM productos p, lineas l WHERE p.linea_id=l.linea_id " + sql_add
        sql += "ORDER BY l.linea, p.producto "
        # print('sql: ', sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                # imagen del producto
                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row[5]}' ORDER BY posicion LIMIT 0,1 "
                imagen = ''
                imagen_thumb = ''
                with connection.cursor() as cursor2:
                    cursor2.execute(sql_imagen)
                    row_imagen = cursor2.fetchone()
                    if row_imagen:
                        imagen = row_imagen[0]
                        imagen_thumb = row_imagen[1]

                dato_producto = {}
                dato_producto['linea'] = row[0]
                dato_producto['producto'] = reemplazar_codigo_html(row[1])
                dato_producto['codigo'] = row[2]
                dato_producto['unidad'] = row[3]
                dato_producto['precio'] = row[4]
                dato_producto['imagen'] = imagen
                dato_producto['imagen_thumb'] = imagen_thumb
                dato_producto['producto_id'] = row[5]

                lista_pp.append(dato_producto)

    # seleccion de linea
    if linea_id != 0:
        # entramos un nivel
        sql = 'SELECT l.linea, p.producto, p.codigo, p.unidad, p.precio_a, p.producto_id, l.linea_id '
        sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{linea_id}' AND l.status_id=1 AND p.status_id=1 "
        sql += "ORDER BY l.linea, p.producto "
        with connection.cursor() as cursor22:
            cursor22.execute(sql)
            rows2 = cursor22.fetchall()
            for row2 in rows2:
                # imagen del producto
                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row2[5]}' ORDER BY posicion LIMIT 0,1 "
                imagen = ''
                imagen_thumb = ''
                with connection.cursor() as cursor33:
                    cursor33.execute(sql_imagen)
                    row_imagen3 = cursor33.fetchone()
                    if row_imagen3:
                        imagen = row_imagen3[0]
                        imagen_thumb = row_imagen3[1]

                dato_producto = {}
                dato_producto['linea'] = row2[0]
                dato_producto['producto'] = reemplazar_codigo_html(row2[1])
                dato_producto['codigo'] = row2[2]
                dato_producto['unidad'] = row2[3]
                dato_producto['precio'] = row2[4]
                dato_producto['imagen'] = imagen
                dato_producto['imagen_thumb'] = imagen_thumb
                dato_producto['producto_id'] = row2[5]

                lista_pp.append(dato_producto)

        # lineas inferior segundo nivel
        sql = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{linea_id}' AND status_id=1 "
        with connection.cursor() as cursor10:
            cursor10.execute(sql)
            rows10 = cursor10.fetchall()
            for row10 in rows10:
                # segundo nivel
                sql = 'SELECT l.linea, p.producto, p.codigo, p.unidad, p.precio_a, p.producto_id, l.linea_id '
                sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{row10[0]}' AND l.status_id=1 AND p.status_id=1 "
                sql += "ORDER BY l.linea, p.producto "
                with connection.cursor() as cursor44:
                    cursor44.execute(sql)
                    rows4 = cursor44.fetchall()
                    for row4 in rows4:
                        # imagen del producto
                        sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row4[5]}' ORDER BY posicion LIMIT 0,1 "
                        imagen = ''
                        imagen_thumb = ''
                        with connection.cursor() as cursor55:
                            cursor55.execute(sql_imagen)
                            row_imagen5 = cursor55.fetchone()
                            if row_imagen5:
                                imagen = row_imagen5[0]
                                imagen_thumb = row_imagen5[1]

                        dato_producto = {}
                        dato_producto['linea'] = row4[0]
                        dato_producto['producto'] = reemplazar_codigo_html(row4[1])
                        dato_producto['codigo'] = row4[2]
                        dato_producto['unidad'] = row4[3]
                        dato_producto['precio'] = row4[4]
                        dato_producto['imagen'] = imagen
                        dato_producto['imagen_thumb'] = imagen_thumb
                        dato_producto['producto_id'] = row4[5]

                        lista_pp.append(dato_producto)

                # tercer nivel
                sql = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{row10[0]}' AND status_id=1 "
                with connection.cursor() as cursor20:
                    cursor20.execute(sql)
                    rows20 = cursor20.fetchall()
                    for row20 in rows20:
                        # tercer nivel
                        sql = 'SELECT l.linea, p.producto, p.codigo, p.unidad, p.precio_a, p.producto_id, l.linea_id '
                        sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{row20[0]}' AND l.status_id=1 AND p.status_id=1 "
                        sql += "ORDER BY l.linea, p.producto "
                        with connection.cursor() as cursor66:
                            cursor66.execute(sql)
                            rows6 = cursor66.fetchall()
                            for row6 in rows6:
                                # imagen del producto
                                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row6[5]}' ORDER BY posicion LIMIT 0,1 "
                                imagen = ''
                                imagen_thumb = ''
                                with connection.cursor() as cursor77:
                                    cursor77.execute(sql_imagen)
                                    row_imagen7 = cursor77.fetchone()
                                    if row_imagen7:
                                        imagen = row_imagen7[0]
                                        imagen_thumb = row_imagen7[1]

                                dato_producto = {}
                                dato_producto['linea'] = row6[0]
                                dato_producto['producto'] = reemplazar_codigo_html(row6[1])
                                dato_producto['codigo'] = row6[2]
                                dato_producto['unidad'] = row6[3]
                                dato_producto['precio'] = row6[4]
                                dato_producto['imagen'] = imagen
                                dato_producto['imagen_thumb'] = imagen_thumb
                                dato_producto['producto_id'] = row6[5]

                                lista_pp.append(dato_producto)

    # listado de retorno
    listado = []
    cant_fila = 3
    cant_actual = 0
    lista_fila = []
    contador = 0

    for producto_p in lista_pp:
        if contador >= pages_limit_bottom and contador < (pages_limit_bottom+pages_limit_top):
            if cant_actual < cant_fila:
                lista_fila.append(producto_p)

            # aumentamos la columna
            cant_actual += 1

            if cant_actual == cant_fila:
                listado.append(lista_fila)
                cant_actual = 0
                lista_fila = []

        contador += 1

    # termina los productos
    if cant_actual > 0:
        # no termino de llenarse los datos de la fila
        for i in range(cant_actual, cant_fila):
            dato_producto = {}
            dato_producto['linea'] = ''
            dato_producto['producto'] = ''
            dato_producto['codigo'] = ''
            dato_producto['unidad'] = ''
            dato_producto['precio'] = 0
            dato_producto['producto_id'] = 0
            lista_fila.append(dato_producto)

        # aniadimos a la lista principal
        listado.append(lista_fila)

    # devolvemos los productos
    return listado
