from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from productos.models import Insumos

# imagenes
from django.core.files.base import ContentFile
from PIL import Image

import random
import os.path as path
import os
from os import remove

from utils.validators import validate_string, validate_number_int, validate_number_decimal

from controllers.SystemController import SystemController


class InsumosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Insumos'
        self.modelo_id = 'insumo_id'
        self.modelo_app = 'productos'
        self.modulo_id = settings.MOD_INSUMOS

        # variables de session
        self.modulo_session = "insumos"
        self.columnas.append('insumo')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_insumo')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_insumo'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = "ASC"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'productos': 'ProductosInsumos'}

        # control del formulario
        self.control_form = "txt|2|S|insumo|Insumo;"
        self.control_form += "txt|2|S|codigo|Codigo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # linea
        if self.variables_filtros_values['search_insumo'].strip() != "":
            self.filtros_modulo['insumo__icontains'] = self.variables_filtros_values['search_insumo'].strip()
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
        filtros['insumo__iexact'] = nuevo_valor
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos un nuevo insumo"""

        system_controller = SystemController()
        try:
            insumo_txt = validate_string('insumo', request.POST['insumo'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            posicion = validate_number_int('posicion', request.POST['posicion'], len_zero='yes')
            precio = validate_number_decimal('precio', request.POST['precio'], len_zero='yes')
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, insumo_txt):
                if 'activo' in request.POST.keys():
                    status_insumo = self.status_activo
                else:
                    status_insumo = self.status_inactivo

                aux = {}
                aux['nombre_archivo'] = ''
                aux['nombre_archivo_thumb'] = ''
                if 'imagen1' in request.FILES.keys():
                    uploaded_filename = request.FILES['imagen1'].name.strip()

                    if uploaded_filename != '':
                        #aux = self.nombre_imagen(uploaded_filename)
                        aux = system_controller.nombre_imagen('insumos', uploaded_filename)

                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'insumos', aux['nombre_archivo'])
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'insumos', aux['nombre_archivo_thumb'])

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
                    insumo = Insumos.objects.create(insumo=insumo_txt, codigo=codigo_txt, posicion=posicion, precio=precio,
                                                    imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=status_insumo, created_at='now', updated_at='now')
                    insumo.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    insumo = Insumos.objects.get(pk=id)

                    # verificamos imagen
                    if insumo.imagen != '':
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'insumos', insumo.imagen)
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'insumos', insumo.imagen_thumb)

                        if os.path.exists(full_filename):
                            remove(full_filename)
                        if os.path.exists(full_filename_thumb):
                            remove(full_filename_thumb)

                    if aux['nombre_archivo'] != '':
                        # guardamos la nueva imagen
                        insumo.imagen = aux['nombre_archivo']
                        insumo.imagen_thumb = aux['nombre_archivo_thumb']

                    insumo.status_id = status_insumo
                    insumo.insumo = insumo_txt
                    insumo.codigo = codigo_txt
                    insumo.posicion = posicion
                    insumo.precio = precio
                    insumo.updated_at = 'now'
                    insumo.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este insumo: " + insumo_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el insumo, " + str(ex)
            return False

    # def modify(self, request, id):
    #     """modificamos la linea"""

    #     system_controller = SystemController()
    #     try:
    #         insumo_txt = validate_string('insumo', request.POST['insumo'], remove_specials='yes')
    #         codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
    #         posicion = validate_number_int('posicion', request.POST['posicion'], len_zero='yes')
    #         precio = validate_number_decimal('precio', request.POST['precio'], len_zero='yes')
    #         activo = validate_number_int('activo', request.POST['activo'])

    #         if not self.is_in_db(id, insumo_txt):
    #             # linea
    #             insumo = Insumos.objects.get(pk=id)

    #             # activo
    #             if activo == 1:
    #                 status_insumo = self.status_activo
    #             else:
    #                 status_insumo = self.status_inactivo

    #             aux = {}
    #             aux['nombre_archivo'] = ''
    #             aux['nombre_archivo_thumb'] = ''
    #             if 'imagen1' in request.FILES.keys():
    #                 uploaded_filename = request.FILES['imagen1'].name.strip()

    #                 if uploaded_filename != '':
    #                     #aux = self.nombre_imagen(uploaded_filename)
    #                     aux = system_controller.nombre_imagen('insumos', uploaded_filename)

    #                     full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'insumos', aux['nombre_archivo'])
    #                     full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'insumos', aux['nombre_archivo_thumb'])

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
    #                 if insumo.imagen != '':
    #                     full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'insumos', insumo.imagen)
    #                     full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'insumos', insumo.imagen_thumb)

    #                     remove(full_filename)
    #                     remove(full_filename_thumb)

    #                 # guardamos la nueva imagen
    #                 insumo.imagen = aux['nombre_archivo']
    #                 insumo.imagen_thumb = aux['nombre_archivo_thumb']

    #             # datos
    #             insumo.status_id = status_insumo
    #             insumo.insumo = insumo_txt
    #             insumo.codigo = codigo_txt
    #             insumo.posicion = posicion
    #             insumo.precio = precio
    #             insumo.updated_at = 'now'
    #             insumo.save()
    #             self.error_operation = ""
    #             return True

    #         else:
    #             self.error_operation = "Ya existe este insumo: " + insumo_txt
    #             return False

    #     except Exception as ex:
    #         self.error_operation = "Error al actualizar el insumo, " + str(ex)
    #         return False
