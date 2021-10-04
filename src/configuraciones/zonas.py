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
from controllers.configuraciones.ZonasController import ZonasController
from controllers.ListasController import ListasController

# controlador del modulo
zona_controller = ZonasController()


# zonas
# zonas
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ZONAS, 'lista'), 'without_permission')
def zonas_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_ZONAS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = zonas_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = zonas_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = zonas_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    zonas_lista = zona_controller.index(request)
    zonas_session = request.session[zona_controller.modulo_session]

    context = {
        'zonas': zonas_lista,
        'session': zonas_session,
        'permisos': permisos,
        'url_main': '',
        'js_file': zona_controller.modulo_session,
        'autenticado': 'si',

        'columnas': zona_controller.columnas,

        'module_x': settings.MOD_ZONAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/zonas.html', context)


# zonas add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ZONAS, 'adicionar'), 'without_permission')
def zonas_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if zona_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Zonas!', 'description': 'Se agrego la nueva zona: '+request.POST['zona']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Zonas!', 'description': zona_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Zonas'), request, None, 'zona', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Zonas'), None, None, 'zona', 'codigo')

    context = {
        'url_main': '',
        'db_tags': db_tags,
        'control_form': zona_controller.control_form,
        'js_file': zona_controller.modulo_session,
        'ciudad': 1,  # sin administracion de cuidades por el momento
        'autenticado': 'si',

        'module_x': settings.MOD_ZONAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/zonas_form.html', context)


# zonas modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ZONAS, 'modificar'), 'without_permission')
def zonas_modify(request, zona_id):
    # url modulo
    zona_check = apps.get_model('configuraciones', 'Zonas').objects.filter(pk=zona_id)
    if not zona_check:
        return render(request, 'pages/without_permission.html', {})

    zona = apps.get_model('configuraciones', 'Zonas').objects.get(pk=zona_id)

    if zona.status_id not in [zona_controller.status_activo, zona_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if zona_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Zonas!', 'description': 'Se modifico la zona: '+request.POST['zona']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Zonas!', 'description': zona_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Zonas'), request, zona, 'zona', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Zonas'), None, zona, 'zona', 'codigo')

    context = {
        'url_main': '',
        'zona': zona,
        'db_tags': db_tags,
        'control_form': zona_controller.control_form,
        'js_file': zona_controller.modulo_session,
        'ciudad': 1,
        'status_active': zona_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_ZONAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': zona_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/zonas_form.html', context)


# zonas delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_ZONAS, 'eliminar'), 'without_permission')
def zonas_delete(request, zona_id):
    # url modulo
    zona_check = apps.get_model('configuraciones', 'Zonas').objects.filter(pk=zona_id)
    if not zona_check:
        return render(request, 'pages/without_permission.html', {})

    zona = apps.get_model('configuraciones', 'Zonas').objects.get(pk=zona_id)

    if zona.status_id not in [zona_controller.status_activo, zona_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if zona_controller.can_delete('zona_id', zona_id, **zona_controller.modelos_eliminar) and zona_controller.delete(zona_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Zonas!', 'description': 'Se elimino la zona: '+request.POST['zona']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Zonas!', 'description': zona_controller.error_operation})

    if zona_controller.can_delete('zona_id', zona_id, **zona_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Zonas!', 'description': 'No puede eliminar esta zona, ' + zona_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Zonas'), request, zona, 'zona', 'codigo')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Zonas'), None, zona, 'zona', 'codigo')

    context = {
        'url_main': '',
        'zona': zona,
        'db_tags': db_tags,
        'control_form': zona_controller.control_form,
        'js_file': zona_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': zona_controller.error_operation,
        'ciudad': 1,
        'status_active': zona_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_ZONAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': zona_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/zonas_form.html', context)
