from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from productos.models import Componentes

# imagenes
from django.core.files.base import ContentFile
from PIL import Image

import random
import os.path as path
import os
from os import remove

from utils.validators import validate_string, validate_number_int, validate_number_decimal

from controllers.SystemController import SystemController


class ComponentesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Componentes'
        self.modelo_id = 'componente_id'
        self.modelo_app = 'productos'
        self.modulo_id = settings.MOD_COMPONENTES

        # variables de session
        self.modulo_session = "componentes"
        self.columnas.append('componente')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_componente')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_componente'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = "ASC"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'productos': 'ProductosComponentes'}

        # control del formulario
        self.control_form = "txt|2|S|componente|Componente;"
        self.control_form += "txt|2|S|codigo|Codigo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # linea
        if self.variables_filtros_values['search_componente'].strip() != "":
            self.filtros_modulo['componente__icontains'] = self.variables_filtros_values['search_componente'].strip()
        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def is_in_db(self, id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['componente__iexact'] = nuevo_valor
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva linea"""
        system_controller = SystemController()
        try:
            componente_txt = validate_string('componente', request.POST['componente'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            posicion = validate_number_int('posicion', request.POST['posicion'], len_zero='yes')
            precio = validate_number_decimal('precio', request.POST['precio'], len_zero='yes')
            # activo = validate_number_int('activo', request.POST['activo'])
            # es_aderezo = validate_number_int('es_aderezo', request.POST['es_aderezo'])
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, componente_txt):
                if 'activo' in request.POST.keys():
                    status_componente = self.status_activo
                else:
                    status_componente = self.status_inactivo

                if 'es_aderezo' in request.POST.keys():
                    es_aderezo = 1
                else:
                    es_aderezo = 0

                aux = {}
                aux['nombre_archivo'] = ''
                aux['nombre_archivo_thumb'] = ''
                if 'imagen1' in request.FILES.keys():
                    uploaded_filename = request.FILES['imagen1'].name.strip()

                    if uploaded_filename != '':
                        #aux = self.nombre_imagen(uploaded_filename)
                        aux = system_controller.nombre_imagen('componentes', uploaded_filename)

                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'componentes', aux['nombre_archivo'])
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'componentes', aux['nombre_archivo_thumb'])

                        fout = open(full_filename, 'wb+')
                        file_content = ContentFile(request.FILES['imagen1'].read())
                        for chunk in file_content.chunks():
                            fout.write(chunk)
                        fout.close()

                        # creamos el thumb
                        imagen = Image.open(full_filename)
                        max_size = (settings.PRODUCTOS_THUMB_WIDTH, settings.PRODUCTOS_THUMB_HEIGHT)
                        imagen.thumbnail(max_size)
                        imagen.save(full_filename_thumb)

                if type == 'add':
                    componente = Componentes.objects.create(componente=componente_txt, codigo=codigo_txt, posicion=posicion, precio=precio, es_aderezo=es_aderezo,
                                                            imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=status_componente, created_at='now', updated_at='now')
                    componente.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    componente = Componentes.objects.get(pk=id)

                    # verificamos imagen
                    if componente.imagen != '':
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'componentes', componente.imagen)
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'componentes', componente.imagen_thumb)

                        if os.path.exists(full_filename):
                            remove(full_filename)
                        if os.path.exists(full_filename_thumb):
                            remove(full_filename_thumb)

                    if aux['nombre_archivo'] != '':
                        # guardamos la nueva imagen
                        componente.imagen = aux['nombre_archivo']
                        componente.imagen_thumb = aux['nombre_archivo_thumb']

                    # datos
                    componente.status_id = status_componente
                    componente.componente = componente_txt
                    componente.codigo = codigo_txt
                    componente.posicion = posicion
                    componente.precio = precio
                    componente.es_aderezo = es_aderezo
                    componente.updated_at = 'now'
                    componente.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este componente: " + componente_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el componente, " + str(ex)
            return False

    # def modify(self, request, id):
    #     """modificamos la linea"""

    #     system_controller = SystemController()
    #     try:
    #         componente_txt = validate_string('componente', request.POST['componente'], remove_specials='yes')
    #         codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
    #         posicion = validate_number_int('posicion', request.POST['posicion'], len_zero='yes')
    #         precio = validate_number_decimal('precio', request.POST['precio'], len_zero='yes')
    #         activo = validate_number_int('activo', request.POST['activo'])
    #         es_aderezo = validate_number_int('es_aderezo', request.POST['es_aderezo'])

    #         if not self.is_in_db(id, componente_txt):
    #             # linea
    #             componente = Componentes.objects.get(pk=id)

    #             # activo
    #             if activo == 1:
    #                 status_componente = self.status_activo
    #             else:
    #                 status_componente = self.status_inactivo

    #             aux = {}
    #             aux['nombre_archivo'] = ''
    #             aux['nombre_archivo_thumb'] = ''
    #             if 'imagen1' in request.FILES.keys():
    #                 uploaded_filename = request.FILES['imagen1'].name.strip()

    #                 if uploaded_filename != '':
    #                     #aux = self.nombre_imagen(uploaded_filename)
    #                     aux = system_controller.nombre_imagen('componentes', uploaded_filename)

    #                     full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'componentes', aux['nombre_archivo'])
    #                     full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'componentes', aux['nombre_archivo_thumb'])

    #                     fout = open(full_filename, 'wb+')
    #                     file_content = ContentFile(request.FILES['imagen1'].read())
    #                     for chunk in file_content.chunks():
    #                         fout.write(chunk)
    #                     fout.close()

    #                     # creamos el thumb
    #                     imagen = Image.open(full_filename)
    #                     max_size = (settings.PRODUCTOS_THUMB_WIDTH, settings.PRODUCTOS_THUMB_HEIGHT)
    #                     imagen.thumbnail(max_size)
    #                     imagen.save(full_filename_thumb)

    #             # verificamos imagen
    #             if aux['nombre_archivo'] != '':
    #                 if componente.imagen != '':
    #                     full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'componentes', componente.imagen)
    #                     full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'componentes', componente.imagen_thumb)

    #                     remove(full_filename)
    #                     remove(full_filename_thumb)

    #                 # guardamos la nueva imagen
    #                 componente.imagen = aux['nombre_archivo']
    #                 componente.imagen_thumb = aux['nombre_archivo_thumb']

    #             # datos
    #             componente.status_id = status_componente
    #             componente.componente = componente_txt
    #             componente.codigo = codigo_txt
    #             componente.posicion = posicion
    #             componente.precio = precio
    #             componente.es_aderezo = es_aderezo
    #             componente.updated_at = 'now'
    #             componente.save()
    #             self.error_operation = ""
    #             return True

    #         else:
    #             self.error_operation = "Ya existe este componente: " + componente_txt
    #             return False

    #     except Exception as ex:
    #         self.error_operation = "Error al actualizar el componente, " + str(ex)
    #         return False
