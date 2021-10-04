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
from productos.models import Insumos

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# controlador
from controllers.productos.InsumosController import InsumosController


insumo_controller = InsumosController()


@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_INSUMOS, 'lista'), 'without_permission')
def insumos_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_INSUMOS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'mostrar_imagen']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = insumos_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = insumos_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = insumos_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'mostrar_imagen':
            insumo_imagen = Insumos.objects.get(pk=int(request.POST['id']))
            context_img = {
                'insumo_imagen': insumo_imagen,
                'autenticado': 'si',
            }
            return render(request, 'productos/insumo_imagen_mostrar.html', context_img)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    insumos_lista = insumo_controller.index(request)
    # print(Ciudades)
    insumos_session = request.session[insumo_controller.modulo_session]
    # print(zonas_session)
    context = {
        'insumos': insumos_lista,
        'session': insumos_session,
        'permisos': permisos,
        'url_main': '',
        'js_file': insumo_controller.modulo_session,
        'autenticado': 'si',

        'columnas': insumo_controller.columnas,

        'module_x': settings.MOD_INSUMOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',


    }
    return render(request, 'productos/insumos.html', context)


# insumos add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_INSUMOS, 'adicionar'), 'without_permission')
def insumos_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if insumo_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Insumos!', 'description': 'Se agrego el nuevo insumo: '+request.POST['insumo']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Insumos!', 'description': insumo_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Insumos, request, None, 'insumo', 'codigo', 'posicion', 'precio')
    else:
        db_tags = get_html_column(Insumos, None, None, 'insumo', 'codigo', 'posicion', 'precio')

    context = {
        'url_main': '',
        'operation_x': 'add',
        'db_tags': db_tags,
        'control_form': insumo_controller.control_form,
        'js_file': insumo_controller.modulo_session,
        'autenticado': 'si',
        'columnas': insumo_controller.columnas,

        'module_x': settings.MOD_INSUMOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/insumos_form.html', context)


# insumos modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_INSUMOS, 'modificar'), 'without_permission')
def insumos_modify(request, insumo_id):
    insumo_check = apps.get_model('productos', 'Insumos').objects.filter(pk=insumo_id)
    if not insumo_check:
        return render(request, 'pages/without_permission.html', {})

    insumo = Insumos.objects.get(pk=insumo_id)

    if insumo.status_id not in [insumo_controller.status_activo, insumo_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if insumo_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Insumos!', 'description': 'Se modifico el insumo: '+request.POST['insumo']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Insumos!', 'description': insumo_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Insumos, request, insumo, 'insumo', 'codigo', 'posicion', 'precio')
    else:
        db_tags = get_html_column(Insumos, None, insumo, 'insumo', 'codigo', 'posicion', 'precio')

    context = {
        'url_main': '',
        'operation_x': 'modify',
        'insumo': insumo,
        'db_tags': db_tags,
        'control_form': insumo_controller.control_form,
        'js_file': insumo_controller.modulo_session,
        'autenticado': 'si',
        'status_active': insumo_controller.activo,

        'module_x': settings.MOD_INSUMOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': insumo_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/insumos_form.html', context)


# insumos delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_INSUMOS, 'eliminar'), 'without_permission')
def insumos_delete(request, insumo_id):
    insumo_check = apps.get_model('productos', 'Insumos').objects.filter(pk=insumo_id)
    if not insumo_check:
        return render(request, 'pages/without_permission.html', {})

    insumo = Insumos.objects.get(pk=insumo_id)

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if insumo_controller.can_delete('insumo_id', insumo_id, **insumo_controller.modelos_eliminar) and insumo_controller.delete(insumo_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Insumos!', 'description': 'Se elimino el insumo: '+request.POST['insumo']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Insumos!', 'description': insumo_controller.error_operation})

    if insumo_controller.can_delete('insumo_id', insumo_id, **insumo_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Insumos!', 'description': 'No puede eliminar este insumo, ' + insumo_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Insumos, request, insumo, 'insumo', 'codigo', 'posicion', 'precio')
    else:
        db_tags = get_html_column(Insumos, None, insumo, 'insumo', 'codigo', 'posicion', 'precio')

    context = {
        'url_main': '',
        'operation_x': 'delete',
        'insumo': insumo,
        'db_tags': db_tags,
        'control_form': insumo_controller.control_form,
        'js_file': insumo_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': insumo_controller.error_operation,
        'autenticado': 'si',
        'status_active': insumo_controller.activo,

        'module_x': settings.MOD_INSUMOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': insumo_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/insumos_form.html', context)
