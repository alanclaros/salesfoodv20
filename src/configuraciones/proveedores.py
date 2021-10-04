from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.ProveedoresController import ProveedoresController

# controlador del modulo
proveedor_controller = ProveedoresController()


# proveedores
# proveedores
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PROVEEDORES, 'lista'), 'without_permission')
def proveedores_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_PROVEEDORES)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = proveedores_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = proveedores_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = proveedores_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    proveedores_lista = proveedor_controller.index(request)
    proveedores_session = request.session[proveedor_controller.modulo_session]
    # print(zonas_session)
    context = {
        'proveedores': proveedores_lista,
        'session': proveedores_session,
        'permisos': permisos,
        'url_main': '',
        'js_file': proveedor_controller.modulo_session,
        'autenticado': 'si',

        'columnas': proveedor_controller.columnas,

        'module_x': settings.MOD_PROVEEDORES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/proveedores.html', context)


# proveedores add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PROVEEDORES, 'adicionar'), 'without_permission')
def proveedores_add(request):
    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if proveedor_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Proveedores!', 'description': 'Se agrego el nuevo proveedor: '+request.POST['proveedor']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Proveedores!', 'description': proveedores_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Proveedores'), request, None, 'proveedor', 'codigo', 'direccion', 'telefonos', 'email', 'nit')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Proveedores'), None, None, 'proveedor', 'codigo', 'direccion', 'telefonos', 'email', 'nit')

    context = {
        'url_main': '',
        'db_tags': db_tags,
        'control_form': proveedor_controller.control_form,
        'js_file': proveedor_controller.modulo_session,
        'autenticado': 'si',

        'module_x': settings.MOD_PROVEEDORES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/proveedores_form.html', context)


# proveedores modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PROVEEDORES, 'modificar'), 'without_permission')
def proveedores_modify(request, proveedor_id):
    # url modulo
    proveedor_check = apps.get_model('configuraciones', 'Proveedores').objects.filter(pk=proveedor_id)
    if not proveedor_check:
        return render(request, 'pages/without_permission.html', {})

    proveedor = apps.get_model('configuraciones', 'Proveedores').objects.get(pk=int(proveedor_id))

    if proveedor.status_id not in [proveedor_controller.status_activo, proveedor_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if proveedor_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Proveedores!', 'description': 'Se modifico el proveedor: '+request.POST['proveedor']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Proveedores!', 'description': proveedor_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Proveedores'), request, proveedor, 'proveedor', 'codigo', 'direccion', 'telefonos', 'email', 'nit')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Proveedores'), None, proveedor, 'proveedor', 'codigo', 'direccion', 'telefonos', 'email', 'nit')

    context = {
        'url_main': '',
        'proveedor': proveedor,
        'db_tags': db_tags,
        'control_form': proveedor_controller.control_form,
        'js_file': proveedor_controller.modulo_session,
        'status_active': proveedor_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_PROVEEDORES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': proveedor_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/proveedores_form.html', context)


# proveedores delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PROVEEDORES, 'eliminar'), 'without_permission')
def proveedores_delete(request, proveedor_id):
    # url modulo
    proveedor_check = apps.get_model('configuraciones', 'Proveedores').objects.filter(pk=proveedor_id)
    if not proveedor_check:
        url = reverse('without_permission')
        return HttpResponseRedirect(url)

    proveedor = apps.get_model('configuraciones', 'Proveedores').objects.get(pk=int(proveedor_id))

    if proveedor.status_id not in [proveedor_controller.status_activo, proveedor_controller.status_inactivo]:
        url = reverse('without_permission')
        return HttpResponseRedirect(url)

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if proveedor_controller.can_delete('proveedor_id', proveedor_id, **proveedor_controller.modelos_eliminar) and proveedor_controller.delete(proveedor_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Proveedores!', 'description': 'Se elimino el proveedor: '+request.POST['proveedor']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Proveedores!', 'description': proveedor_controller.error_operation})

    if proveedor_controller.can_delete('proveedor_id', proveedor_id, **proveedor_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Proveedores!', 'description': 'No puede eliminar este proveedor, ' + proveedor_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Proveedores'), request, proveedor, 'proveedor', 'codigo', 'direccion', 'telefonos', 'email', 'nit')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Proveedores'), None, proveedor, 'proveedor', 'codigo', 'direccion', 'telefonos', 'email', 'nit')

    context = {
        'url_main': '',
        'proveedor': proveedor,
        'db_tags': db_tags,
        'control_form': proveedor_controller.control_form,
        'js_file': proveedor_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': proveedor_controller.error_operation,
        'status_active': proveedor_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_PROVEEDORES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': proveedor_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/proveedores_form.html', context)
