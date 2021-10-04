from utils.permissions import get_system_settings
from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from configuraciones.models import Proveedores

from utils.validators import validate_number_int, validate_string, validate_email


class ProveedoresController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Proveedores'
        self.modelo_id = 'proveedor_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_PROVEEDORES

        # variables de session
        self.modulo_session = "proveedores"
        self.columnas.append('proveedor')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_proveedor')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_proveedor'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'configuraciones': 'Lineas'}

        # control del formulario
        self.control_form = "txt|2|S|proveedor|Proveedor;"
        self.control_form += "txt|2|S|codigo|Codigo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # proveedor
        if self.variables_filtros_values['search_proveedor'].strip() != "":
            self.filtros_modulo['proveedor__icontains'] = self.variables_filtros_values['search_proveedor'].strip()
        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

        # print('filtros: ', self.filtros_modulo)
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
        filtros['proveedor__iexact'] = nuevo_valor
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nuevo proveedor"""
        try:
            proveedor_txt = validate_string('proveedor', request.POST['proveedor'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            direccion_txt = validate_string('direccion', request.POST['direccion'], remove_specials='yes', len_zero='yes')
            telefonos_txt = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes', len_zero='yes')
            email_txt = validate_email('correo', request.POST['email'], len_zero='yes')
            nit_txt = validate_string('nit', request.POST['nit'], remove_specials='yes', len_zero='yes')
            #activo = validate_number_int('activo', request.POST['activo'])
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, proveedor_txt):
                if 'activo' in request.POST.keys():
                    status_proveedor = self.status_activo
                else:
                    status_proveedor = self.status_inactivo

                if type == 'add':
                    proveedor = Proveedores.objects.create(proveedor=proveedor_txt, codigo=codigo_txt, status_id=status_proveedor,
                                                           direccion=direccion_txt, telefonos=telefonos_txt, email=email_txt,
                                                           nit=nit_txt, created_at='now', updated_at='now')
                    proveedor.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    proveedor = Proveedores.objects.get(pk=int(id))
                    proveedor.status_id = status_proveedor
                    proveedor.proveedor = proveedor_txt
                    proveedor.codigo = codigo_txt
                    proveedor.direccion = direccion_txt
                    proveedor.telefonos = telefonos_txt
                    proveedor.email = email_txt
                    proveedor.nit = nit_txt
                    proveedor.updated_at = 'now'
                    proveedor.save()
                    self.error_operation = ""
                    return True

                # default
                self.error_operation = 'operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este proveedor: " + proveedor_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el proveedor, " + str(ex)
            return False

    # def modify(self, request, id):
    #     """modificamos el proveedor"""
    #     try:
    #         proveedor_txt = validate_string('proveedor', request.POST['proveedor'], remove_specials='yes')
    #         codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
    #         direccion_txt = validate_string('direccion', request.POST['direccion'], remove_specials='yes', len_zero='yes')
    #         telefonos_txt = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes', len_zero='yes')
    #         email_txt = validate_email('email', request.POST['email'], len_zero='yes')
    #         nit_txt = validate_string('nit', request.POST['nit'], remove_specials='yes', len_zero='yes')
    #         activo = validate_number_int('activo', request.POST['activo'])

    #         if not self.is_in_db(id, proveedor_txt):

    #             # proveedor
    #             proveedor = Proveedores.objects.get(pk=int(id))

    #             # activo
    #             if activo == 1:
    #                 status_proveedor = self.status_activo
    #             else:
    #                 status_proveedor = self.status_inactivo

    #             # datos
    #             proveedor.status_id = status_proveedor
    #             proveedor.proveedor = proveedor_txt
    #             proveedor.codigo = codigo_txt
    #             proveedor.direccion = direccion_txt
    #             proveedor.telefonos = telefonos_txt
    #             proveedor.email = email_txt
    #             proveedor.nit = nit_txt
    #             proveedor.updated_at = 'now'
    #             proveedor.save()
    #             self.error_operation = ""
    #             return True

    #         else:
    #             self.error_operation = "Ya existe este proveedor: " + proveedor_txt
    #             return False
    #     except Exception as ex:
    #         self.error_operation = "Error al actualizar el proveedor, " + str(ex)
    #         return False

    # def canDelete(self, id):
    #     """verificando si se puede eliminar o no la tabla"""
    #     tablas = ['socios']
    #     # for tabla in tablas:
    #     #     datos
