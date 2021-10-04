from utils.permissions import get_system_settings
from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from configuraciones.models import Zonas
# from status.models import Status

from utils.validators import validate_string, validate_number_int


class ZonasController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Zonas'
        self.modelo_id = 'zona_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_ZONAS

        # variables de session
        self.modulo_session = "zonas"
        self.columnas.append('zona')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_zona')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_zona'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'configuraciones': 'Sucursales'}

        # control del formulario
        self.control_form = "txt|2|S|zona|Zona;"
        self.control_form += "txt|2|S|codigo|Codigo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]
        # zona
        if self.variables_filtros_values['search_zona'].strip() != "":
            self.filtros_modulo['zona__icontains'] = self.variables_filtros_values['search_zona'].strip()
        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def is_in_db(self, id, ciudad_id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['zona__iexact'] = nuevo_valor
        filtros['ciudad_id_id__in'] = [ciudad_id]
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva zona"""
        try:
            ciudad_id = validate_number_int('ciudad', request.POST['ciudad'])
            zona_txt = validate_string('zona', request.POST['zona'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            id = validate_number_int('id', request.POST['id'], len_zero='yes')
            ciudad = apps.get_model('configuraciones', 'Ciudades').objects.get(pk=int(ciudad_id))

            if not self.is_in_db(id, ciudad_id, zona_txt):

                if 'activo' in request.POST.keys():
                    status_zona = self.status_activo
                else:
                    status_zona = self.status_inactivo

                if type == 'add':
                    usuario = request.user
                    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)

                    zona = Zonas.objects.create(ciudad_id=ciudad, user_perfil_id=user_perfil, zona=zona_txt, codigo=codigo_txt,
                                                status_id=status_zona, created_at='now', updated_at='now')
                    zona.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    zona = Zonas.objects.get(pk=int(id))
                    # datos
                    zona.ciudad_id = ciudad
                    zona.status_id = status_zona
                    zona.zona = zona_txt
                    zona.codigo = codigo_txt
                    zona.updated_at = 'now'
                    zona.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operacion no permitida'
                return False

            else:
                self.error_operation = "Ya existe esta zona: " + zona_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar la zona, " + str(ex)
            return False

    # def modify(self, request, id):
    #     """modificamos la ciudad"""
    #     try:
    #         ciudad_id = validate_number_int('ciudad', request.POST['ciudad'])
    #         zona_txt = validate_string('zona', request.POST['zona'], remove_specials='yes')
    #         codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
    #         activo = validate_number_int('activo', request.POST['activo'])

    #         if not self.is_in_db(id, ciudad_id, zona_txt):
    #             # zona
    #             zona = Zonas.objects.get(pk=int(id))
    #             # ciudad
    #             ciudad = apps.get_model('configuraciones', 'Ciudades').objects.get(pk=ciudad_id)
    #             # activo
    #             if activo == 1:
    #                 status_zona = self.status_activo
    #             else:
    #                 status_zona = self.status_inactivo

    #             # datos
    #             zona.ciudad_id = ciudad
    #             zona.status_id = status_zona
    #             zona.zona = zona_txt
    #             zona.codigo = codigo_txt
    #             zona.updated_at = 'now'
    #             zona.save()
    #             self.error_operation = ""
    #             return True

    #         else:
    #             self.error_operation = "Ya existe esta zona: " + zona_txt
    #             return False

    #     except Exception as ex:
    #         self.error_operation = "Error al actualizar la zona, " + str(ex)
    #         return False
