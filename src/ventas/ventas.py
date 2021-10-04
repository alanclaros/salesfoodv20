import os
from productos.models import Productos
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
# settings de la app
from django.conf import settings
# reverse url
from django.apps import apps

# propios
from configuraciones.models import Puntos
from permisos.models import UsersPerfiles
from ventas.models import Ventas, VentasDetalles
from cajas.models import Cajas

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column, get_system_settings
from utils.dates_functions import get_date_show, get_date_system

# clases por modulo
from controllers.ventas.VentasController import VentasController
from controllers.inventarios.StockController import StockController
from controllers.clientes.ClientesController import ClientesController
from controllers.cajas.CajasController import CajasController
from controllers.ListasController import ListasController
from controllers.productos.ProductosController import ProductosController
# from controllers.preventas.PreVentasController import PreVentasController
# from controllers.ventas.PlanPagosController import PlanPagosController
# from controllers.pedidos.PedidosController import PedidosController

# reportes
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportes.ventas.rptVenta import rptVenta
# from reportes.ventas.rptPlanPago import rptPlanPago
# from reportes.ventas.rptPlanPagoPagos import rptPlanPagoPagos
# from reportes.ventas.rptPlanPagoCuota import rptPlanPagoCuota

from utils.validators import validate_number_int, validate_string


# ventas
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'lista'), 'without_permission')
def ventas_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_VENTAS)
    ventas_controller = VentasController()
    stock_controller = StockController()
    cliente_controller = ClientesController()
    caja_controller = CajasController()
    lista_controller = ListasController()
    producto_controller = ProductosController()

    # system settings
    system_settings = get_system_settings()
    vender_fracciones = system_settings['vender_fracciones']

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']

        if not operation in ['', 'add', 'modify', 'anular', 'print', 'stock_producto', 'nuevo_cliente', 'buscar_cliente', 'guardar_nc']:
            return render(request, 'pages/without_permission.html')

        # guardar nuevo cliente
        if operation == 'guardar_nc':
            try:
                n_ci_nit = validate_string('ci/nit', request.POST['ci_nit'], remove_specials='yes', len_zero='yes')
                n_apellidos = validate_string('apellidos', request.POST['apellidos'], remove_specials='yes', len_zero='yes')
                n_nombres = validate_string('nombres', request.POST['nombres'], remove_specials='yes', len_zero='yes')
                n_telefonos = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes', len_zero='yes')
                n_direccion = validate_string('direccion', request.POST['direccion'], remove_specials='yes', len_zero='yes')

                if n_ci_nit == '' or n_apellidos == '' or n_nombres == '':
                    context = {
                        'adicionado': 0,
                        'error': 1,
                        'error_message': 'Debe llenar todos los datos, CI/NIT, Apellidos, Nombres',
                        'autenticado': 'si',
                    }
                    return render(request, 'ventas/ventas_nuevo_cliente.html', context)

                usuario_perfil = UsersPerfiles.objects.get(user_id=request.user)
                Punto = Puntos.objects.get(pk=usuario_perfil.punto_id)

                datos = {}
                datos['id'] = 0
                datos['ci_nit'] = n_ci_nit
                datos['apellidos'] = n_apellidos
                datos['nombres'] = n_nombres
                datos['telefonos'] = n_telefonos
                datos['direccion'] = n_direccion
                datos['email'] = ''
                datos['razon_social'] = n_apellidos
                datos['factura_a'] = n_apellidos
                datos['created_at'] = 'now'
                datos['updated_at'] = 'now'
                datos['user_perfil_id'] = usuario_perfil
                datos['punto_id'] = Punto
                datos['status_id'] = ventas_controller.status_activo

                if cliente_controller.save_db(type='add', **datos):
                    context = {
                        'adicionado': 1,
                        'error': 0,
                        'error_message': '',
                        'ci_nit': datos['ci_nit'],
                        'apellidos': datos['apellidos'],
                        'nombres': datos['nombres'],
                        'telefonos': datos['telefonos'],
                        'direccion': datos['direccion'],
                        'autenticado': 'si',
                        'ventana_js': 'Venta',
                    }
                else:
                    context = {
                        'adicionado': 0,
                        'error': 1,
                        'error_message': cliente_controller.error_operation,
                        'autenticado': 'si',
                        'ventana_js': 'Venta',
                    }

                return render(request, 'ventas/ventas_nuevo_cliente.html', context)

            except Exception as ex:
                context = {
                    'adicionado': 0,
                    'error': 1,
                    'error_message': 'error al adicionar cliente ' + str(ex),
                    'autenticado': 'si',
                    'ventana_js': 'Venta',
                }
                return render(request, 'ventas/ventas_nuevo_cliente.html', context)

        # nuevo cliente
        if operation == 'nuevo_cliente':
            context_nuevo = {
                'operation_x': 'add_cliente',
                'autenticado': 'si',
                'ventana_js': 'Venta',
            }
            return render(request, 'ventas/ventas_nuevo_cliente.html', context_nuevo)

        # buscar cliente
        if operation == 'buscar_cliente':
            datos_cliente = cliente_controller.buscar_cliente(ci_nit=request.POST['ci_nit'], apellidos=request.POST['apellidos'], nombres=request.POST['nombres'])
            # print(datos_cliente)
            context_buscar = {
                'clientes': datos_cliente,
                'autenticado': 'si',
                'ventana_js': 'Venta',
            }
            return render(request, 'ventas/clientes_buscar.html', context_buscar)

        if operation == 'add':
            # verificamos que tenga caja activa
            cajas_lista = caja_controller.cash_active(get_date_system(), request.user)
            if cajas_lista:
                respuesta = ventas_add(request)
                if not type(respuesta) == bool:
                    return respuesta
            else:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'Debe tener una caja activa para hacer ventas'})

        if operation == 'modify':
            # verificamos que tenga caja activa
            cajas_lista = caja_controller.cash_active(get_date_system(), request.user)
            if cajas_lista:
                respuesta = ventas_add(request)
                if not type(respuesta) == bool:
                    return respuesta
            else:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'Debe tener una caja activa para hacer ventas'})

        if operation == 'anular':
            respuesta = ventas_nullify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        # stock del producto
        if operation == 'stock_producto':
            producto_id = request.POST['id'].strip()
            almacen_id = request.POST['almacen'].strip()
            numero_registro = request.POST['numero_registro'].strip()

            producto = Productos.objects.get(pk=int(producto_id))
            detalle_producto = producto_controller.datos_producto(producto_id)

            #stock_producto = stock_controller.stock_producto(producto_id=producto_id, user=request.user, almacen_id=almacen_id)
            stock_producto = stock_controller.stock_producto_insumo(producto_id=producto_id, almacen_id=almacen_id)
            # lista de ids
            context_stock = {
                'stock_producto': stock_producto,
                'producto': producto,
                'detalle_producto': detalle_producto,
                'numero_registro': numero_registro,
                'stock_js': 'Venta',
                'producto_id': producto_id,
                'vender_fracciones': vender_fracciones,
                'autenticado': 'si',
                'lbl_lote': settings.PRODUCTOS_LBL_LOTE,
            }

            return render(request, 'ventas/stock_venta.html', context_stock)

        if operation == 'print':
            if permisos.imprimir:
                try:
                    if not get_user_permission_operation(request.user, settings.MOD_VENTAS, 'imprimir', 'venta_id', int(request.POST['id'].strip()), 'ventas', 'Ventas'):
                        return render(request, 'pages/without_permission.html')

                    buffer = io.BytesIO()
                    rptVenta(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
                    return FileResponse(buffer, filename='ventas_'+str(request.POST['id'])+'.pdf')

                except Exception as ex:
                    request.session['internal_error'] = str(ex)
                    request.session.modified = True

                    context_internal = {'error': str(ex)}
                    return render(request, 'pages/internal_error.html', context_internal)
            else:
                return render(request, 'pages/without_permission.html')

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    ventas_lista = ventas_controller.index(request)
    ventas_session = request.session[ventas_controller.modulo_session]

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user)

    # print(zonas_session)
    context = {
        'ventas': ventas_lista,
        'session': ventas_session,
        'permisos': permisos,
        'lista_almacenes': lista_almacenes,
        'url_main': '',
        'estado_anulado': ventas_controller.anulado,
        'autenticado': 'si',

        'js_file': ventas_controller.modulo_session,
        'columnas': ventas_controller.columnas,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/ventas.html', context)


# ventas add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'adicionar'), 'without_permission')
def ventas_add(request):
    # # url modulo
    ventas_controller = VentasController()
    producto_controller = ProductosController()

    caja_controller = CajasController()
    lista_controller = ListasController()

    permisos = get_permissions_user(request.user, settings.MOD_VENTAS)
    system_settings = get_system_settings()
    vender_fracciones = system_settings['vender_fracciones']

    # status activo
    user_perfil = UsersPerfiles.objects.get(user_id=request.user)
    fecha_actual = get_date_show(fecha=get_date_system(), formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

    # verificamos caja activa
    cajas_lista = caja_controller.cash_active(get_date_system(), request.user)
    if not cajas_lista:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'debe tener una caja activa'}
        request.session.modified = True
        return False

    # guardamos
    if 'add_x' in request.POST.keys():

        if ventas_controller.save(request, type='add'):
            existe_error = False
            error_operation = ''

            if request.POST['tipo_operacion'] == 'add':
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Ventas!', 'description': 'Se agrego la nueva venta correctamente'})

            if request.POST['tipo_operacion'] == 'modify':
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Ventas!', 'description': 'Se modifico la venta correctamente'})
        else:
            # error al adicionar
            existe_error = True
            error_operation = ventas_controller.error_operation

            if request.POST['tipo_operacion'] == 'add':
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'Error al adicionar la venta, ' + ventas_controller.error_operation})

            if request.POST['tipo_operacion'] == 'modify':
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'Error al modificar la venta, ' + ventas_controller.error_operation})

        # print(request.POST.keys())

        if request.POST['tipo_operacion'] == 'modify':
            last_id = int(request.POST['m_venta_id'])
        else:
            # ultima venta
            last_id = ventas_controller.get_last_id(user_perfil.punto_id, get_date_system())

        datos_venta = ventas_controller.get_venta(last_id, user_perfil.punto_id, get_date_system())
        context = {
            'existe_error': existe_error,
            'error_operation': error_operation,
            'last_id': last_id,
            'datos_venta': datos_venta,
            'fecha_actual': fecha_actual,
            'estado_anulado': ventas_controller.anulado,
            'estado_pedido': ventas_controller.preventa,
            'permisos': permisos,
            'operation_x': 'add_venta',
            'autenticado': 'si',
        }

        return render(request, 'ventas/ventas_dia.html', context)

    #print('request...', request.POST.keys())
    if 'operation_x2' in request.POST.keys():
        operation = request.POST['operation_x2']
        if operation == 'load_id_x':
            id_request = 0 if request.POST['load_id'].strip() == '' else int(request.POST['load_id'].strip())
            datos_venta = ventas_controller.get_venta(id_request, user_perfil.punto_id, get_date_system())
            context = {
                'existe_error': False,
                'error_operation': '',
                'datos_venta': datos_venta,
                'fecha_actual': fecha_actual,
                'operation_x': 'load_id',
                'estado_anulado': ventas_controller.anulado,
                'estado_pedido': ventas_controller.preventa,
                'permisos': permisos,
                'autenticado': 'si',
            }

            return render(request, 'ventas/ventas_dia.html', context)

        if operation == 'anular_x':
            id_venta = 0 if request.POST['venta_id'].strip() == '' else int(request.POST['venta_id'].strip())

            if ventas_controller.can_anular(id_venta, request.user) and ventas_controller.anular(request, id_venta):
                datos_venta = ventas_controller.get_venta(id_venta, user_perfil.punto_id, get_date_system())
                context = {
                    'existe_error': False,
                    'error_operation': '',
                    'datos_venta': datos_venta,
                    'fecha_actual': fecha_actual,
                    'estado_anulado': ventas_controller.anulado,
                    'estado_pedido': ventas_controller.preventa,
                    'operation_x': 'anular',
                    'permisos': permisos,
                    'autenticado': 'si',
                }

                return render(request, 'ventas/ventas_dia.html', context)

            else:
                datos_venta = ventas_controller.get_venta(id_venta, user_perfil.punto_id, get_date_system())
                context = {
                    'existe_error': True,
                    'error_operation': 'No puede anular esta venta',
                    'datos_venta': datos_venta,
                    'fecha_actual': fecha_actual,
                    'estado_anulado': ventas_controller.anulado,
                    'estado_pedido': ventas_controller.preventa,
                    'permisos': permisos,
                    'operation_x': 'anular',
                    'autenticado': 'si',
                }

                return render(request, 'ventas/ventas_dia.html', context)

        # if operation == 'load_preventa_data':
        #     # carga de datos de preventa
        #     preventa_id = request.POST['preventa_id']
        #     datos_preventa = preventas_controller.get_preventa(preventa_id, user_perfil.punto_id, get_date_system())
        #     context_p = {
        #         'datos_venta': datos_preventa,
        #         'operation_x': 'datos_preventa',
        #         'permisos': permisos,
        #         'autenticado': 'si',
        #     }
        #     return render(request, 'ventas/datos_preventa.html', context_p)

        # if operation == 'load_lista_preventa':
        #     # lista de preventas
        #     lista_preventas = ventas_controller.get_preventas(user_perfil.punto_id)
        #     context_pp = {
        #         'lista_preventas': lista_preventas,
        #         'operation_x': 'lista_preventa',
        #         'autenticado': 'si',
        #     }
        #     return render(request, 'ventas/lista_preventas.html', context_pp)

    # lista de productos
    lista_productos = producto_controller.lista_productos(punto_id=user_perfil.punto_id, combos=1)
    # restricciones de columna
    db_tags = {}
    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user)

    # lista lugarres
    lista_lugares = lista_controller.get_lista_lugares(user=request.user)

    # lista de preventas
    lista_preventas = ventas_controller.get_preventas(user_perfil.punto_id)

    # ultima venta
    operation_x = request.POST['operation_x']
    if operation_x == 'modify':
        last_id = int(request.POST['id'])
    else:
        last_id = ventas_controller.get_last_id(user_perfil.punto_id, get_date_system())

    datos_venta = ventas_controller.get_venta(last_id, user_perfil.punto_id, get_date_system())

    # caja del usuario
    caja_usuario = cajas_lista[0]

    # verificamos si es un pedido
    # if 'pedido_id' in request.POST.keys():
    #     pedido_id = request.POST['pedido_id'].strip()
    #     # recuperamos datos del pedido
    #     pedido_controller = PedidosController()
    #     pedido = pedido_controller.get_pedido(pedido_id)
    #     cant_detalles = len(pedido['detalles'])
    # else:
    #     pedido_id = 0
    #     pedido = {}
    #     cant_detalles = 0

    pedido_id = 0
    pedido = {}
    cant_detalles = 0

    # cantidad de filas
    filas = []
    for i in range(1, 51):
        filas.append(i)

    context = {
        'pedido_id': pedido_id,
        'pedido': pedido,
        'cant_detalles': cant_detalles,

        'url_main': '',
        'url_add': '',
        'permisos': permisos,
        'lista_lugares': lista_lugares,
        'lista_productos': lista_productos,
        'lista_almacenes': lista_almacenes,
        'lista_preventas': lista_preventas,
        'cajas_lista': cajas_lista,
        'caja_usuario': caja_usuario,
        'estado_recibe': ventas_controller.apertura_recibe,
        'filas': filas,
        'db_tags': db_tags,
        'control_form': ventas_controller.control_form,
        'js_file': ventas_controller.modulo_session,
        'datos_venta': datos_venta,
        'fecha_actual': fecha_actual,
        'estado_anulado': ventas_controller.anulado,
        'estado_pedido': ventas_controller.preventa,
        'vender_fracciones': vender_fracciones,

        'productos_precios_abc': settings.PRODUCTOS_PRECIOS_ABC,

        'autenticado': 'si',
        'lbl_lote': settings.PRODUCTOS_LBL_LOTE,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    # if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
    #     return render(request, 'ventas/ventas_form.html', context)
    # else:
    #     if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
    #         return render(request, 'ventas/ventas_form_sin_fechas_lote.html', context)
    #     else:
    #         if settings.PRODUCTOS_USAR_FECHAS:
    #             return render(request, 'ventas/ventas_form_solo_fecha.html', context)
    #         if settings.PRODUCTOS_USAR_LOTE:
    #             return render(request, 'ventas/ventas_form_solo_lote.html', context)
    return render(request, 'ventas/ventas_form_sin_fechas_lote.html', context)


# ventas anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_nullify(request, venta_id):
    # check
    venta_check = apps.get_model('ventas', 'Ventas').objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html')

    venta = Ventas.objects.get(pk=venta_id)
    ventas_controller = VentasController()

    # verificamos el estado
    if venta.status_id.status_id == ventas_controller.anulado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro ya esta anulado'}
        request.session.modified = True
        return False

    # confirma eliminacion
    if 'anular_x' in request.POST.keys():
        if ventas_controller.can_anular(venta_id, request.user) and ventas_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo la venta: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': ventas_controller.error_operation})

    if ventas_controller.can_anular(venta_id, request.user):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular esta venta, ' + ventas_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # venta
    venta = Ventas.objects.select_related('almacen_id').select_related('caja_id').get(pk=venta_id)
    # plan de pagos
    plan_pago = {}
    if venta.tipo_venta == 'PLANPAGO':
        plan_pago = apps.get_model('inventarios', 'PlanPagos').objects.get(venta_id=venta.venta_id)

    # detalles
    detalles = VentasDetalles.objects.select_related('producto_id').select_related('producto_id__linea_id').filter(venta_id=venta).order_by('venta_detalle_id')

    context = {
        'url_main': '',
        'venta': venta,
        'plan_pago': plan_pago,
        'detalles': detalles,
        'db_tags': db_tags,
        'control_form': ventas_controller.control_form,
        'js_file': ventas_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': ventas_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/ventas_anular.html', context)
