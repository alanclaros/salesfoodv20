from utils.permissions import get_system_settings
from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from configuraciones.models import Sucursales
from decimal import Decimal

from utils.validators import validate_string, validate_number_int, validate_email

# transacciones
from django.db import transaction


class SucursalesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Sucursales'
        self.modelo_id = 'sucursal_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_SUCURSALES

        # variables de session
        self.modulo_session = "sucursales"
        self.columnas.append('zona_id__zona')
        self.columnas.append('sucursal')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_zona')
        self.variables_filtros.append('search_sucursal')

        self.variables_filtros_defecto['search_zona'] = ''
        self.variables_filtros_defecto['search_sucursal'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'configuraciones': 'Puntos'}

        # control del formulario
        self.control_form = "cbo|0|S|zona|Zona;"
        self.control_form += "txt|2|S|sucursal|Sucursal;"
        self.control_form += "txt|2|S|codigo|Codigo;"
        self.control_form += "txt|2|S|empresa|Empresa;"
        self.control_form += "txt|2|S|direccion|Direccion;"
        self.control_form += "txt|2|S|ciudad_rp|Ciudad;"
        self.control_form += "txt|2|S|telefonos|Telefonos;"
        self.control_form += "txt|2|S|actividad|Actividad"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]
        # zona
        if self.variables_filtros_values['search_zona'].strip() != "":
            self.filtros_modulo['zona_id__zona__icontains'] = self.variables_filtros_values['search_zona'].strip()
        # sucursal
        if self.variables_filtros_values['search_sucursal'].strip() != "":
            self.filtros_modulo['sucursal__icontains'] = self.variables_filtros_values['search_sucursal'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def records_count(self):
        """cantidad de registros del modulo"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        cantidad = modelo.objects.select_related('zona_id').filter(**self.filtros_modulo).count()

        return cantidad

    def get_list(self):
        # orden
        orden_enviar = ''
        if self.variable_order_value != '':
            orden_enviar = self.variable_order_value
            if self.variable_order_type_value != '':
                if self.variable_order_type_value == 'DESC':
                    orden_enviar = '-' + orden_enviar

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        retorno = modelo.objects.select_related('zona_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]
        # for sucursal in retorno:
        #    # print(ciudad.__dict__)
        #    print(sucursal.ciudad_id.pais_id.__dict__)

        return retorno

    def is_in_db(self, id, zona_id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['sucursal__iexact'] = nuevo_valor
        filtros['zona_id_id__in'] = [zona_id]
        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        #print('cantidad', cantidad)
        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva zona"""
        try:
            zona_id = validate_number_int('zona', request.POST['zona'])
            ciudad_id = validate_number_int('ciudad', request.POST['ciudad'])
            sucursal_txt = validate_string('sucursal', request.POST['sucursal'])
            codigo_txt = validate_string('codigo', request.POST['codigo'])
            email_txt = validate_email('email', request.POST['email'], len_zero='yes')
            empresa_txt = validate_string('empresa', request.POST['empresa'], remove_specials='yes')
            direccion_txt = validate_string('direccion', request.POST['direccion'], remove_specials='yes')
            ciudad_txt = validate_string('ciudad', request.POST['ciudad_rp'], remove_specials='yes')
            telefonos_txt = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes')
            actividad_txt = validate_string('actividad', request.POST['actividad'], remove_specials='yes')

            datos_mapa = validate_string('datos_mapa', request.POST['datos_mapa'], len_zero='yes')
            ubicacion_mapa = validate_string('ubicacion mapa', request.POST['ubicacion_mapa'], len_zero='yes')

            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            # sucursal y usuario
            ciudad = apps.get_model('configuraciones', 'Ciudades').objects.get(pk=ciudad_id)
            zona = apps.get_model('configuraciones', 'Zonas').objects.get(pk=zona_id)
            usuario = request.user
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)

            if not self.is_in_db(id, zona_id, sucursal_txt):

                with transaction.atomic():
                    # activo
                    if 'activo' in request.POST.keys():
                        status_sucursal = self.status_activo
                    else:
                        status_sucursal = self.status_inactivo

                    if type == 'add':
                        sucursal = Sucursales.objects.create(ciudad_id=ciudad, zona_id=zona, user_perfil_id=user_perfil,
                                                             sucursal=sucursal_txt, codigo=codigo_txt, email=email_txt, empresa=empresa_txt,
                                                             direccion=direccion_txt, ciudad=ciudad_txt, telefonos=telefonos_txt, actividad=actividad_txt,
                                                             datos_mapa=datos_mapa, ubicacion_mapa=ubicacion_mapa, status_id=status_sucursal, created_at='now', updated_at='now')
                        sucursal.save()

                        self.error_operation = ""
                        return True

                    if type == 'modify':
                        sucursal = Sucursales.objects.get(pk=id)
                        # datos
                        sucursal.ciudad_id = ciudad
                        sucursal.zona_id = zona
                        sucursal.status_id = status_sucursal
                        sucursal.sucursal = sucursal_txt
                        sucursal.codigo = codigo_txt
                        sucursal.email = email_txt
                        sucursal.empresa = empresa_txt
                        sucursal.direccion = direccion_txt
                        sucursal.ciudad = ciudad_txt
                        sucursal.telefonos = telefonos_txt
                        sucursal.actividad = actividad_txt
                        sucursal.datos_mapa = datos_mapa
                        sucursal.ubicacion_mapa = ubicacion_mapa
                        sucursal.updated_at = 'now'
                        sucursal.save()

                        self.error_operation = ""
                        return True

                    self.error_operation = 'Operacion no permitida'
                    return False

            else:
                self.error_operation = "Ya existe esta sucursal: " + sucursal_txt
                return False

        except Exception as ex:
            print('ERROR, adicionar sucursal: ' + str(ex))
            self.error_operation = "Error al agregar la sucursal, " + str(ex)
            return False

    # def modify(self, request, id):
    #     """modificamos la sucursal"""
    #     try:
    #         zona_id = validate_number_int('zona', request.POST['zona'])
    #         ciudad_id = validate_number_int('ciudad', request.POST['ciudad'])
    #         sucursal_txt = validate_string('sucursal', request.POST['sucursal'])
    #         codigo_txt = validate_string('codigo', request.POST['codigo'])
    #         email_txt = validate_email('email', request.POST['email'], len_zero='yes')
    #         empresa_txt = validate_string('empresa', request.POST['empresa'], remove_specials='yes')
    #         direccion_txt = validate_string('direccion', request.POST['direccion'], remove_specials='yes')
    #         ciudad_txt = validate_string('ciudad', request.POST['ciudad_rp'], remove_specials='yes')
    #         telefonos_txt = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes')
    #         actividad_txt = validate_string('actividad', request.POST['actividad'], remove_specials='yes')

    #         datos_mapa = validate_string('datos_mapa', request.POST['datos_mapa'], len_zero='yes')
    #         ubicacion_mapa = validate_string('ubicacion mapa', request.POST['ubicacion_mapa'], len_zero='yes')

    #         activo = validate_number_int('activo', request.POST['activo'])

    #         if not self.is_in_db(id, zona_id, sucursal_txt):

    #             with transaction.atomic():
    #                 # sucursal
    #                 sucursal = Sucursales.objects.get(pk=id)

    #                 # ciudad
    #                 ciudad = apps.get_model('configuraciones', 'Ciudades').objects.get(pk=ciudad_id)
    #                 zona = apps.get_model('configuraciones', 'Zonas').objects.get(pk=zona_id)

    #                 # activo
    #                 if activo == 1:
    #                     status_sucursal = self.status_activo
    #                 else:
    #                     status_sucursal = self.status_inactivo

    #                 # datos
    #                 sucursal.ciudad_id = ciudad
    #                 sucursal.zona_id = zona
    #                 sucursal.status_id = status_sucursal
    #                 sucursal.sucursal = sucursal_txt
    #                 sucursal.codigo = codigo_txt
    #                 sucursal.email = email_txt
    #                 sucursal.empresa = empresa_txt
    #                 sucursal.direccion = direccion_txt
    #                 sucursal.ciudad = ciudad_txt
    #                 sucursal.telefonos = telefonos_txt
    #                 sucursal.actividad = actividad_txt
    #                 sucursal.datos_mapa = datos_mapa
    #                 sucursal.ubicacion_mapa = ubicacion_mapa
    #                 sucursal.updated_at = 'now'
    #                 sucursal.save()

    #                 self.error_operation = ""
    #                 return True

    #         else:
    #             self.error_operation = "Ya existe esta sucursal: " + sucursal_txt
    #             return False

    #     except Exception as ex:
    #         print('ERROR, modificar sucursal: ' + str(ex))
    #         self.error_operation = "Error al actualizar la sucursal, " + str(ex)
    #         return False

    # def canDelete(self, id):
    #     """verificando si se puede eliminar o no la tabla"""
    #     tablas = ['socios']
    #     # for tabla in tablas:
    #     #     datos
