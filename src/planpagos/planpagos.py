import os
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
# settings de la app
from django.conf import settings
# reverse url
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.apps import apps

# propios
from inventarios.models import PlanPagos, PlanPagosDetalles
from status.models import Status
from cajas.models import Cajas

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column, get_system_settings
from utils.dates_functions import get_date_show, get_date_system

# clases por modulo
from controllers.cajas.CajasController import CajasController
from controllers.ListasController import ListasController
from controllers.ventas.PlanPagosController import PlanPagosController
from controllers.ventas.VentasController import VentasController

# reportes
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportes.ventas.rptPlanPago import rptPlanPago
from reportes.ventas.rptPlanPagoPagos import rptPlanPagoPagos
from reportes.ventas.rptPlanPagoCuota import rptPlanPagoCuota

from utils.validators import validate_number_int, validate_string


# plan pagos
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PLAN_PAGOS, 'lista'), 'without_permission')
def plan_pagos_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_PLAN_PAGOS)
    pp_controller = PlanPagosController()

    lista_controller = ListasController()
    url_main = ''

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']

        if not operation in ['', 'detail', 'imprimir_plan_pago', 'imprimir_pagos', 'imprimir_cuota']:
            return render(request, 'pages/without_permission.html')

        # detalle del cliente
        if operation == 'detail':
            respuesta = plan_pagos_detail_index(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'imprimir_plan_pago':
            if permisos.imprimir:
                buffer = io.BytesIO()
                rptPlanPago(buffer, request.user, int(request.POST['id']), crear_pdf='si')

                buffer.seek(0)
                return FileResponse(buffer, filename='plan_pagos.pdf')
            else:
                return render(request, 'pages/without_permission.html')

        if operation == 'imprimir_pagos':
            if permisos.imprimir:
                buffer = io.BytesIO()
                rptPlanPagoPagos(buffer, request.user, int(request.POST['id']), crear_pdf='si')

                buffer.seek(0)
                return FileResponse(buffer, filename='plan_pagos_pagos.pdf')
            else:
                return render(request, 'pages/without_permission.html')

        if operation == 'imprimir_cuota':
            if permisos.imprimir:
                buffer = io.BytesIO()
                rptPlanPagoCuota(buffer, request.user, int(request.POST['id']), crear_pdf='si')

                buffer.seek(0)
                return FileResponse(buffer, filename='plan_pagos_cuota.pdf')
            else:
                return render(request, 'pages/without_permission.html')

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    planes_pagos_lista = pp_controller.index(request)
    planes_pagos_session = request.session[pp_controller.modulo_session]
    #print('session: ', planes_pagos_session)

    # lista de almacenes
    lista_almacenes = lista_controller.get_lista_almacenes(request.user)

    # print(zonas_session)
    context = {
        'planes_pagos': planes_pagos_lista,
        'session': planes_pagos_session,
        'permisos': permisos,
        'url_main': url_main,
        'lista_almacenes': lista_almacenes,
        'js_file': pp_controller.modulo_session,
        'estado_anulado': pp_controller.anulado,
        'autenticado': 'si',

        'module_x': settings.MOD_PLAN_PAGOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/plan_pagos.html', context)


# plan pagos detail
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PLAN_PAGOS, 'modificar'), 'without_permission')
def plan_pagos_detail_index(request, plan_pago_id):
    # # url modulo
    pp_controller = PlanPagosController()
    caja_controller = CajasController()

    pp_check = apps.get_model('inventarios', 'PlanPagos').objects.filter(pk=plan_pago_id)
    if not pp_check:
        return render(request, 'pages/without_permission.html')

    plan_pago = PlanPagos.objects.get(pk=plan_pago_id)

    if plan_pago.preventa_id > 0:
        return render(request, 'pages/without_permission.html')

    # status activo
    fecha_actual = get_date_show(fecha=get_date_system(), formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

    # guardamos
    if 'cobrar_cuota_x' in request.POST.keys():
        pp_id = request.POST['id']
        if pp_controller.add_pago(request, pp_id):
            # request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Plan de Pagos!', 'description': 'Se agrego el pago correctamente'}
            # request.session.modified = True
            # return True
            plan_pago = PlanPagos.objects.get(pk=plan_pago_id)
            messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Plan de Pagos!', 'description': 'Se agrego el pago correctamente'})
        else:
            # error al adicionar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Plan de Pagos!', 'description': 'Error al adicionar el pago, ' + pp_controller.error_operation})

    #print('request...', request.POST.keys())
    if 'operation_x2' in request.POST.keys():
        operation = request.POST['operation_x2']
        if operation == 'anular':
            cuota_id = request.POST['id2'].strip()

            if pp_controller.anular(request, cuota_id):
                # request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Plan de Pagos!', 'description': 'Se anulo el pago correctamente'}
                # request.session.modified = True
                # return True
                plan_pago = PlanPagos.objects.get(pk=plan_pago_id)
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Plan de Pagos!', 'description': 'Se anulo el pago correctamente'})
            else:
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Plan de Pagos!', 'description': 'Error al anular el pago, ' + pp_controller.error_operation})

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # lista del plan de pagos
    detalles = pp_controller.get_detalles(plan_pago_id=plan_pago_id)
    # restricciones de columna
    db_tags = {}
    # lista de pagos realizados
    pagos = pp_controller.get_pagos_realizados(plan_pago_id=plan_pago_id)

    # cajas activas
    cajas_lista = caja_controller.cash_active(get_date_system(), request.user)
    if cajas_lista:
        caja_usuario = cajas_lista[0]
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Plan de Pagos!', 'description': 'Debe tener una caja activa para realizar pagos'})
        caja_usuario = {}

    # permisos
    permisos = get_permissions_user(request.user, settings.MOD_PLAN_PAGOS)

    context = {
        'url_main': '',
        'url_detail': '',
        'permisos': permisos,
        'caja_usuario': caja_usuario,
        'plan_pago': plan_pago,
        'detalles': detalles,
        'pagos': pagos,
        'db_tags': db_tags,
        'control_form': pp_controller.control_form,
        'js_file': pp_controller.modulo_session,
        'fecha_actual': fecha_actual,
        'estado_anulado': pp_controller.anulado,
        'estado_recibe': pp_controller.apertura_recibe,
        'autenticado': 'si',

        'module_x': settings.MOD_PLAN_PAGOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'detail',
        'operation_x2': '',
        'operation_x3': '',

        'id': plan_pago_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/plan_pagos_detail.html', context)
