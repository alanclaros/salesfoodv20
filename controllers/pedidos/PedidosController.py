from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from productos.models import Productos
from permisos.models import UsersPerfiles
from configuraciones.models import Puntos, Lineas
from pedidos.models import Pedidos, PedidosDetalles
from status.models import Status
from decimal import Decimal

from django.db import transaction
from utils.permissions import get_permissions_user
from utils.dates_functions import get_date_to_db, get_date_show, get_date_system, add_days_datetime, get_seconds_date1_sub_date2

# conexion directa a la base de datos
from django.db import connection

from utils.validators import validate_number_int, validate_string


class PedidosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Pedidos'
        self.modelo_id = 'pedido_id'
        self.modelo_app = 'pedidos'
        self.modulo_id = settings.MOD_PEDIDOS

        # variables de session
        self.modulo_session = "pedidos"
        self.columna = "apellidos"
        self.columna2 = "nombres"
        self.columna3 = "telefonos"
        self.columna4 = "total"

        fecha_actual = get_date_system()
        fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
        fecha_ini = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-1, formato='dd-MMM-yyyy')

        self.variable, self.variable_defecto = "fecha_ini", fecha_ini
        self.variable2, self.variable2_defecto = "fecha_fin", fecha_fin

        self.variable3, self.variable3_defecto = "apellidos", ''
        self.variable4, self.variable4_defecto = "nombres", ''
        self.variable5, self.variable5_defecto = "anulados", '0'
        self.variable6, self.variable6_defecto = "telefonos", ''
        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "ao_pedidos"
        self.variable_order_value = self.columna
        self.variable_order_type = "ao_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = ""

    def index(self, request):
        DefaultValues.index(self, request)

        # ultimo acceso
        if 'last_access' in request.session[self.modulo_session].keys():
            # restamos
            resta = get_seconds_date1_sub_date2(fecha1=get_date_system(time='yes'), formato1='yyyy-mm-dd HH:ii:ss', fecha2=request.session[self.modulo_session]['last_access'], formato2='yyyy-mm-dd HH:ii:ss')
            # print('resta:', resta)
            if resta > 14400:  # 4 horas (4x60x60)
                # print('modificando')
                fecha_actual = get_date_system()
                fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
                fecha_ini = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-1, formato='dd-MMM-yyyy')

                self.variable_val = fecha_ini
                self.variable_defecto = fecha_ini
                self.variable2_val = fecha_fin
                self.variable2_defecto = fecha_fin

                # orden por defecto
                self.variable_order_value = self.columna
                self.variable_order_type_value = 'DESC'
                request.session[self.modulo_session][self.variable_order] = self.variable_order_value
                request.session[self.modulo_session][self.variable_order_type] = self.variable_order_type_value

                # session
                request.session[self.modulo_session][self.variable] = self.variable_defecto
                request.session[self.modulo_session][self.variable2] = self.variable2_defecto
                request.session.modified = True

            # print('variable:', self.variable_val)
            # actualizamos a la fecha actual
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True
        else:
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True

        self.filtros_modulo.clear()
        # estado, anulados o no
        if self.variable5_val.strip() == "1":
            self.filtros_modulo['status_id_id'] = self.anulado
        else:
            # status
            self.filtros_modulo['status_id_id__in'] = [self.activo, self.contado, self.consignacion, self.plan_pago, self.factura]

        # fechas
        if self.variable_val.strip() != '' and self.variable2_val.strip() != '':
            self.filtros_modulo['created_at__gte'] = get_date_to_db(fecha=self.variable_val.strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss')
            self.filtros_modulo['created_at__lte'] = get_date_to_db(fecha=self.variable2_val.strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

        # apellidos
        if self.variable3_val.strip() != "":
            self.filtros_modulo['apellidos__icontains'] = self.variable3_val.strip()

        # nombres
        if self.variable4_val.strip() != "":
            self.filtros_modulo['nombres__icontains'] = self.variable4_val.strip()

        # telefonos
        if self.variable6_val.strip() != "":
            self.filtros_modulo['telefonos__icontains'] = self.variable6_val.strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def get_list(self):
        # orden
        orden_enviar = ''
        if self.variable_order_value != '':
            orden_enviar = self.variable_order_value
            if self.variable_order_type_value != '':
                if self.variable_order_type_value == 'DESC':
                    orden_enviar = '-' + orden_enviar
        # print(orden_enviar)

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        retorno = modelo.objects.filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]

        return retorno

    def get_pedido(self, pedido_id):
        """devuelve datos del pedido"""
        pedido_retorno = {}
        try:
            pedido = Pedidos.objects.get(pk=int(pedido_id))
            pedido_retorno = pedido.__dict__

            # detalles
            detalles = []
            pedido_detalles = PedidosDetalles.objects.select_related('producto_id').filter(pedido_id=pedido, status_id=self.status_activo).order_by('producto_id__producto')

            for detalle in pedido_detalles:
                dato = {}
                dato['producto_id'] = detalle.producto_id.producto_id
                dato['producto'] = detalle.producto_id.producto
                dato['cantidad'] = int(detalle.cantidad)
                dato['costo'] = detalle.costo
                dato['descuento'] = detalle.descuento
                dato['total'] = detalle.total
                dato['talla'] = detalle.talla

                detalles.append(dato)

            pedido_retorno['detalles'] = detalles

        except Exception as ex:
            print('Error al recuperar el pedido: ' + str(ex))
            pedido_retorno = {}

        return pedido_retorno

    def pedidos_cliente_marcar(self, request, id):
        """marcamos el pedido"""

        try:
            # estado
            status_pedido = Status.objects.get(pk=int(request.POST['tipo_venta']))
            pedido = Pedidos.objects.get(pk=int(id))

            # datos
            datos = {}
            datos['status_id'] = status_pedido
            datos['updated_at'] = 'now'

            if self.pedidos_cliente_marcar_db(id, **datos):
                self.error_operation = ""
                return True
            else:
                self.error_operation = 'error al marcar el pedido'
                return False
        except:
            self.error_operation = "Error al actualizar el pedido"
            return False

    def pedidos_cliente_marcar_db(self, id, **datos):
        """actualizamos a la base de datos"""

        try:
            with transaction.atomic():
                campos_update = {}
                campos_update['status_id'] = datos['status_id']
                campos_update['updated_at'] = datos['updated_at']

                pedido_update = Pedidos.objects.filter(pk=id)
                pedido_update.update(**campos_update)

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR pedido marcar, ' + str(ex))
            return False

    def can_anular(self, id, user):
        """verificando si se puede eliminar o no la tabla"""
        # puede anular el usuario con permiso de la sucursal
        usuario_perfil = UsersPerfiles.objects.get(user_id=user)
        punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
        permisos = get_permissions_user(user, settings.MOD_PEDIDOS)

        # pedido
        pedido = Pedidos.objects.get(pk=id)
        if pedido.status_id.status_id == self.anulado:
            self.error_operation = 'el registro ya esta anulado'
            return False

        if permisos.anular:
            return True

        return False

    def anular(self, request, id):
        """anulando el registro"""
        try:
            if self.can_anular(id, request.user):

                status_anular = self.status_anulado
                motivo_a = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')

                campos_update = {}
                # para actualizar el stock
                campos_update['user_id'] = request.user
                campos_update['user_id_anula'] = request.user.id
                campos_update['motivo_anula'] = motivo_a
                campos_update['status_id'] = status_anular
                campos_update['deleted_at'] = 'now'

                if self.anular_db(id, **campos_update):
                    self.error_operation = ''
                    return True
                else:
                    return False

            else:
                self.error_operation = 'No tiene permiso para anular este pedido'
                return False

        except Exception as ex:
            print('Error anular pedido: ' + str(ex))
            self.error_operation = 'Error al anular el pedido, ' + str(ex)
            return False

    def anular_db(self, id, **datos):
        """ anulamos en la bd """
        try:
            with transaction.atomic():
                campos_update = {}
                campos_update['user_id_anula'] = datos['user_id_anula']
                campos_update['motivo_anula'] = datos['motivo_anula']
                campos_update['status_id'] = datos['status_id']
                campos_update['deleted_at'] = datos['deleted_at']

                # registramos
                pedido_update = Pedidos.objects.filter(pk=id)
                pedido_update.update(**campos_update)

                self.error_operation = ''
                return True

        except Exception as ex:
            print('Error anular pedido db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return False
