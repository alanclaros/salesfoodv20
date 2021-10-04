import os
# from pages.views import lista_productos
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings
# reverse url
from django.urls import reverse
from django.http import HttpResponseRedirect

# propios
from configuraciones.models import Almacenes
from inventarios.models import Registros, RegistrosDetalles, PlanPagos, PlanPagosDetalles

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column, get_system_settings
from utils.dates_functions import get_date_to_db, get_date_show, get_date_system

# clases por modulo
from controllers.inventarios.PedidosAlmacenController import PedidosAlmacenController
from controllers.ListasController import ListasController
from controllers.productos.ProductosController import ProductosController


# from controllers.inventarios.MovimientosAlmacenController import MovimientosAlmacenController
# from controllers.inventarios.PedidosAlmacenController import PedidosAlmacenController

from controllers.inventarios.StockController import StockController

# reportes
import io
from django.http import FileResponse
from reportes.inventarios.rptPedidoAlmacen import rptPedidoAlmacen


pedidos_almacen_controller = PedidosAlmacenController()


# pedidos almacen
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PEDIDOS_ALMACEN, 'lista'), 'without_permission')
def pedidos_almacen_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_PEDIDOS_ALMACEN)
    stock_controller = StockController()
    lista_controller = ListasController()

    system_settings = get_system_settings()
    vender_fracciones = system_settings['vender_fracciones']

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'anular', 'print', 'stock_producto']:
            url = reverse('without_permission')
            return HttpResponseRedirect(url)

        if operation == 'add':
            respuesta = pedidos_almacen_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'anular':
            respuesta = pedidos_almacen_nullify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'print':
            if permisos.imprimir:
                try:
                    if not get_user_permission_operation(request.user, settings.MOD_PEDIDOS_ALMACEN, 'imprimir', 'registro_id', int(request.POST['id'].strip()), 'inventarios', 'Registros'):
                        url = reverse('without_permission')
                        return HttpResponseRedirect(url)

                    buffer = io.BytesIO()
                    rptPedidoAlmacen(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='pedido_almacen_'+str(request.POST['id'])+'.pdf')

                except Exception as ex:
                    request.session['internal_error'] = str(ex)
                    request.session.modified = True
                    url = reverse('internal_error')
                    return HttpResponseRedirect(url)

            else:
                url = reverse('without_permission')
                return HttpResponseRedirect(url)

            # stock del producto
        if operation == 'stock_producto':
            producto_id = request.POST['id'].strip()
            almacen_id = request.POST['almacen'].strip()

            stock_producto = stock_controller.stock_producto(producto_id=producto_id, user=request.user, almacen_id=almacen_id)
            # lista de ids
            stock_ids = ''
            for stock in stock_producto:
                stock_ids += str(stock.stock_id) + ','
            if len(stock_ids) > 0:
                stock_ids = stock_ids[0:len(stock_ids)-1]

            context_stock = {
                'stock_producto': stock_producto,
                'stock_ids': stock_ids,
                'producto_id': producto_id,
                'vender_fracciones': vender_fracciones,
                'autenticado': 'si',
                'lbl_lote': settings.PRODUCTOS_LBL_LOTE,
                'stock_js': 'PA',
            }

            if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
                return render(request, 'inventarios/stock_producto_pedido.html', context_stock)
            else:
                if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
                    return render(request, 'inventarios/stock_producto_pedido_sin_fechas_lote.html', context_stock)
                else:
                    if settings.PRODUCTOS_USAR_FECHAS:
                        return render(request, 'inventarios/stock_producto_pedido_solo_fecha.html', context_stock)
                    if settings.PRODUCTOS_USAR_LOTE:
                        return render(request, 'inventarios/stock_producto_pedido_solo_lote.html', context_stock)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    pedidos_lista = pedidos_almacen_controller.index(request)
    pedidos_session = request.session[pedidos_almacen_controller.modulo_session]

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user)

    # print(zonas_session)
    context = {
        'pedidos': pedidos_lista,
        'session': pedidos_session,
        'permisos': permisos,
        'lista_almacenes': lista_almacenes,
        'url_main': '',
        'estado_anulado': pedidos_almacen_controller.anulado,
        'autenticado': 'si',

        'js_file': pedidos_almacen_controller.modulo_session,
        'columnas': pedidos_almacen_controller.columnas,
        'module_x': settings.MOD_PEDIDOS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'inventarios/pedidos_almacen.html', context)


# pedidos almacen add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PEDIDOS_ALMACEN, 'adicionar'), 'without_permission')
def pedidos_almacen_add(request):
    producto_controller = ProductosController()
    lista_controller = ListasController()

    # guardamos
    if 'add_x' in request.POST.keys():
        if pedidos_almacen_controller.add(request):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Pedidos Almacen!', 'description': 'Se agrego el pedido'}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Pedidos Almacen!', 'description': pedidos_almacen_controller.error_operation})

    # lista de productos
    #lista_productos = producto_controller.lista_productos(combos=1)
    lista_productos = producto_controller.lista_insumos()

    # restricciones de columna
    db_tags = {}

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(user=request.user, module='almacen1')

    # lista de almacenes destino
    lista_almacenes_destino = lista_controller.get_lista_almacenes(request.user)

    # cantidad de filas, 51 para que llegue a 50
    filas = []
    for i in range(1, 51):
        filas.append(i)

    fecha_actual = get_date_system()
    fecha_actual = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

    context = {
        'url_main': '',
        'lista_productos': lista_productos,
        'lista_almacenes': lista_almacenes,
        'lista_almacenes_destino': lista_almacenes_destino,
        'filas': filas,
        'db_tags': db_tags,
        'control_form': pedidos_almacen_controller.control_form,
        'js_file': pedidos_almacen_controller.modulo_session,
        'fecha_actual': fecha_actual,

        'productos_precios_abc': settings.PRODUCTOS_PRECIOS_ABC,
        'lbl_lote': settings.PRODUCTOS_LBL_LOTE,

        'autenticado': 'si',

        'module_x': settings.MOD_PEDIDOS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
        return render(request, 'inventarios/pedidos_almacen_form.html', context)
    else:
        if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
            return render(request, 'inventarios/pedidos_almacen_form_sin_fechas_lote.html', context)
        else:
            if settings.PRODUCTOS_USAR_FECHAS:
                return render(request, 'inventarios/pedidos_almacen_form_solo_fecha.html', context)
            if settings.PRODUCTOS_USAR_LOTE:
                return render(request, 'inventarios/pedidos_almacen_form_solo_lote.html', context)


# pedidos almacen anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PEDIDOS_ALMACEN, 'anular'), 'without_permission')
def pedidos_almacen_nullify(request, registro_id):
    # url modulo
    registro_check = Registros.objects.filter(pk=registro_id)
    if not registro_check:
        url = reverse('without_permission')
        return HttpResponseRedirect(url)

    registro = Registros.objects.get(pk=registro_id)
    lista_controller = ListasController()

    if registro.status_id.status_id == pedidos_almacen_controller.anulado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Pedidos Almacen!', 'description': 'El registro ya esta anulado'}
        request.session.modified = True
        return False

    # verificamos tipo de movimiento
    if not registro.tipo_movimiento in ['CONTADO', 'FACTURA', 'CONSIGNACION', 'PLANPAGO']:
        url = reverse('without_permission')
        return HttpResponseRedirect(url)

    # confirma eliminacion
    if 'anular_x' in request.POST.keys():
        if pedidos_almacen_controller.can_anular(registro_id, request.user) and pedidos_almacen_controller.anular(request, registro_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Pedidos Almacen!', 'description': 'Se anulo el registro: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Pedidos Almacen!', 'description': pedidos_almacen_controller.error_operation})

    if pedidos_almacen_controller.can_anular(registro_id, request.user):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Pedidos Almacen!', 'description': 'No puede anular este registro, ' + pedidos_almacen_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(user=request.user, module='almacen1')

    # lista de almacenes destino
    lista_almacenes_destino = lista_controller.get_lista_almacenes(request.user)

    # detalles
    detalles = RegistrosDetalles.objects.filter(registro_id=registro).order_by('registro_detalle_id')

    # verificamos si tiene plan de pagos
    if registro.tipo_movimiento == 'PLANPAGO':
        plan_pagos = PlanPagos.objects.get(registro_id=registro.registro_id)
        fecha_actual = get_date_show(plan_pagos.fecha, 'dd-MMM-yyyy')
    else:
        plan_pagos = {}
        fecha_actual = ''

    context = {
        'url_main': '',
        'plan_pagos': plan_pagos,
        'fecha_actual': fecha_actual,
        'registro': registro,
        'detalles': detalles,
        'lista_almacenes': lista_almacenes,
        'lista_almacenes_destino': lista_almacenes_destino,
        'db_tags': db_tags,
        'control_form': pedidos_almacen_controller.control_form,
        'js_file': pedidos_almacen_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': pedidos_almacen_controller.error_operation,
        'autenticado': 'si',
        'lbl_lote': settings.PRODUCTOS_LBL_LOTE,

        'module_x': settings.MOD_PEDIDOS_ALMACEN,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': registro_id,
        'id2': '',
        'id3': '',
    }

    if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
        return render(request, 'inventarios/pedidos_almacen_form.html', context)
    else:
        if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
            return render(request, 'inventarios/pedidos_almacen_form_sin_fechas_lote.html', context)
        else:
            if settings.PRODUCTOS_USAR_FECHAS:
                return render(request, 'inventarios/pedidos_almacen_form_solo_fecha.html', context)
            if settings.PRODUCTOS_USAR_LOTE:
                return render(request, 'inventarios/pedidos_almacen_form_solo_lote.html', context)
