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
from productos.models import Componentes

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# controlador
from controllers.productos.ComponentesController import ComponentesController


componente_controller = ComponentesController()


@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_COMPONENTES, 'lista'), 'without_permission')
def componentes_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_COMPONENTES)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'mostrar_imagen']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = componentes_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = componentes_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = componentes_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'mostrar_imagen':
            componente_imagen = Componentes.objects.get(pk=int(request.POST['id']))
            context_img = {
                'componente_imagen': componente_imagen,
                'autenticado': 'si',
            }
            return render(request, 'productos/componente_imagen_mostrar.html', context_img)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    componentes_lista = componente_controller.index(request)
    # print(Ciudades)
    componentes_session = request.session[componente_controller.modulo_session]
    # print(zonas_session)
    context = {
        'componentes': componentes_lista,
        'session': componentes_session,
        'permisos': permisos,
        'url_main': '',
        'js_file': componente_controller.modulo_session,
        'autenticado': 'si',

        'columnas': componente_controller.columnas,

        'module_x': settings.MOD_COMPONENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',


    }
    return render(request, 'productos/componentes.html', context)


# componentes add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_COMPONENTES, 'adicionar'), 'without_permission')
def componentes_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if componente_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Componentes!', 'description': 'Se agrego el nuevo componente: '+request.POST['componente']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Componentes!', 'description': componente_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Componentes, request, None, 'componente', 'codigo', 'posicion', 'precio')
    else:
        db_tags = get_html_column(Componentes, None, None, 'componente', 'codigo', 'posicion', 'precio')

    context = {
        'url_main': '',
        'operation_x': 'add',
        'db_tags': db_tags,
        'control_form': componente_controller.control_form,
        'js_file': componente_controller.modulo_session,
        'autenticado': 'si',
        'columnas': componente_controller.columnas,

        'module_x': settings.MOD_COMPONENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/componentes_form.html', context)


# insumos modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_COMPONENTES, 'modificar'), 'without_permission')
def componentes_modify(request, componente_id):
    componente_check = apps.get_model('productos', 'Componentes').objects.filter(pk=componente_id)
    if not componente_check:
        return render(request, 'pages/without_permission.html', {})

    componente = Componentes.objects.get(pk=componente_id)

    if componente.status_id not in [componente_controller.status_activo, componente_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if componente_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Componentes!', 'description': 'Se modifico el componente: '+request.POST['componente']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Componentes!', 'description': componente_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Componentes, request, componente, 'componente', 'codigo', 'posicion', 'precio')
    else:
        db_tags = get_html_column(Componentes, None, componente, 'componente', 'codigo', 'posicion', 'precio')

    context = {
        'url_main': '',
        'operation_x': 'modify',
        'componente': componente,
        'db_tags': db_tags,
        'control_form': componente_controller.control_form,
        'js_file': componente_controller.modulo_session,
        'autenticado': 'si',
        'status_active': componente_controller.activo,

        'module_x': settings.MOD_COMPONENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': componente_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/componentes_form.html', context)


# componentes delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_COMPONENTES, 'eliminar'), 'without_permission')
def componentes_delete(request, componente_id):
    componente_check = apps.get_model('productos', 'Componentes').objects.filter(pk=componente_id)
    if not componente_check:
        url = reverse('without_permission')
        return HttpResponseRedirect(url)

    componente = Componentes.objects.get(pk=componente_id)

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if componente_controller.can_delete('componente_id', componente_id, **componente_controller.modelos_eliminar) and componente_controller.delete(componente_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Componentes!', 'description': 'Se elimino el componente: '+request.POST['componente']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Componentes!', 'description': componente_controller.error_operation})

    if componente_controller.can_delete('componente_id', componente_id, **componente_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Componentes!', 'description': 'No puede eliminar este componente, ' + componente_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(Componentes, request, componente, 'componente', 'codigo', 'posicion', 'precio')
    else:
        db_tags = get_html_column(Componentes, None, componente, 'componente', 'codigo', 'posicion', 'precio')

    context = {
        'url_main': '',
        'operation_x': 'delete',
        'componente': componente,
        'db_tags': db_tags,
        'control_form': componente_controller.control_form,
        'js_file': componente_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': componente_controller.error_operation,
        'autenticado': 'si',
        'status_active': componente_controller.activo,

        'module_x': settings.MOD_COMPONENTES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': componente_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'productos/componentes_form.html', context)
