from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from inventarios.models import PlanPagos, PlanPagosDetalles, PlanPagosPagos, Registros
#from preventas.models import PreVentas, PreVentasDetalles
from productos.models import Productos
from clientes.models import Clientes
from permisos.models import UsersPerfiles
from cajas.models import Cajas
from configuraciones.models import Puntos, Almacenes, PuntosAlmacenes
from status.models import Status
from decimal import Decimal

from django.db import transaction

from decimal import Decimal

# fechas
from utils.dates_functions import get_date_system, get_date_show, get_date_to_db, get_seconds_date1_sub_date2, add_days_datetime, get_day_from_date
from utils.permissions import get_permissions_user

from controllers.inventarios.PlanPagosController import PlanPagosController
from controllers.inventarios.StockController import StockController
from controllers.inventarios.MovimientosAlmacenController import MovimientosAlmacenController

# user model
from django.contrib.auth.models import User

# conexion directa a la base de datos
from django.db import connection

from utils.validators import validate_number_int, validate_string, validate_number_decimal


class PreVentasController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'PreVentas'
        self.modelo_id = 'preventa_id'
        self.modelo_app = 'preventas'
        self.modulo_id = settings.MOD_PREVENTAS

        # variables de session
        self.modulo_session = "preventas"
        self.columna = "fecha"
        self.columna2 = "apellidos"
        self.columna3 = "nombres"
        self.columna4 = "ci_nit"

        fecha_actual = get_date_system()
        fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
        fecha_ini = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-1, formato='dd-MMM-yyyy')

        self.variable, self.variable_defecto = "fecha_ini", fecha_ini
        self.variable2, self.variable2_defecto = "fecha_fin", fecha_fin
        self.variable3, self.variable3_defecto = "apellidos", ''
        self.variable4, self.variable4_defecto = "nombres", ''
        self.variable5, self.variable5_defecto = "codigo", ''
        self.variable6, self.variable6_defecto = "ci_nit", ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "ao_preventas"
        self.variable_order_value = self.columna
        self.variable_order_type = "ao_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = "txt|1|S|ci_nit|;"
        self.control_form += "txt|2|S|apellidos|;"
        self.control_form += "txt|1|S|total|"

    def index(self, request):
        DefaultValues.index(self, request)

        # ultimo acceso
        if 'last_access' in request.session[self.modulo_session].keys():
            # restamos
            resta = get_seconds_date1_sub_date2(fecha1=get_date_system(time='yes'), formato1='yyyy-mm-dd HH:ii:ss', fecha2=request.session[self.modulo_session]['last_access'], formato2='yyyy-mm-dd HH:ii:ss')
            #print('resta:', resta)
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

            #print('variable:', self.variable_val)
            # actualizamos a la fecha actual
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True
        else:
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True

        self.filtros_modulo.clear()
        # punto
        user_perfil = UsersPerfiles.objects.get(user_id=request.user)
        punto_index = Puntos.objects.get(pk=user_perfil.punto_id)
        # punto
        self.filtros_modulo['punto_id'] = punto_index
        # status
        self.filtros_modulo['status_id_id__in'] = [self.preventa, self.preventa_venta, self.anulado]
        # tipo movimiento
        self.filtros_modulo['tipo_preventa__in'] = ['CONTADO', 'FACTURA', 'CONSIGNACION', 'PLANPAGO']
        # codigo
        if self.variable5_val.strip() != "":
            self.filtros_modulo['numero_preventa'] = int(self.variable5_val.strip())

        # fechas
        if self.variable_val.strip() != '' and self.variable2_val.strip() != '':
            self.filtros_modulo['fecha__gte'] = get_date_to_db(fecha=self.variable_val.strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss')
            self.filtros_modulo['fecha__lte'] = get_date_to_db(fecha=self.variable2_val.strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

        # apellidos
        if self.variable3_val.strip() != "":
            self.filtros_modulo['apellidos__icontains'] = self.variable3_val.strip()
        # nombres
        if self.variable4_val.strip() != "":
            self.filtros_modulo['nombres__icontains'] = self.variable4_val.strip()
        # ci_nit
        if self.variable6_val.strip() != "":
            self.filtros_modulo['ci_nit'] = self.variable6_val.strip()

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
        retorno = modelo.objects.select_related('punto_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]

        return retorno

    def add(self, request):
        """aniadimos un nuevo registro"""
        try:
            # control de almacenes
            almacen1= validate_number_int('almacen', request.POST['almacen'])
            tipo_venta= validate_string('tipo venta', request.POST['tipo_venta'], remove_specials='yes')
            costo_abc= validate_string('costo abc', request.POST['costo_abc'], remove_specials='yes')
            concepto= 'ventas del dia'
            apellidos= validate_string('apellidos', request.POST['apellidos'], remove_specials='yes', len_zero='yes')
            nombres = validate_string('nombres', request.POST['nombres'], remove_specials='yes', len_zero='yes')
            ci_nit = validate_string('ci_nit', request.POST['ci_nit'], remove_specials='yes', len_zero='yes')
            telefonos = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes', len_zero='yes')

            numero_cuotas= validate_number_int('numero cuotas', request.POST['numero_cuotas'], len_zero='yes')
            tipo_pp= validate_string('tipo_pp', request.POST['tipo_pp'], remove_specials='yes', len_zero='yes')
            aux_fecha_fija= validate_string('fecha fija', request.POST['fecha_fija'], remove_specials='yes')
            dias= validate_number_int('dias', request.POST['dias'], len_zero='yes')
            
            porcentaje_descuento= validate_number_decimal('porcentaje_descuento', request.POST['porcentaje_descuento'], len_zero='yes')
            descuento= validate_number_decimal('descuento', request.POST['descuento'], len_zero='yes')

            status_venta = self.status_preventa
            # cliente id
            cliente_id = Clientes.objects.get(ci_nit=ci_nit, apellidos=apellidos, nombres=nombres)
            # caso de plan de pago
            fecha_fija = get_date_to_db(fecha=aux_fecha_fija, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss')

            if almacen1 == '0':
                self.error_operation = 'Debe seleccionar el almacen para la preventa'
                return False

            if tipo_venta == '0':
                self.error_operation = 'Debe seleccionar el tipo de venta'
                return False

            if costo_abc == '0':
                self.error_operation = 'Debe seleccionar el tipo de costo'
                return False

            if tipo_venta == 'PLANPAGO':
                if numero_cuotas == 0:
                    self.error_operation = 'Debe indicar el numero de cuotas'
                    return False

                if tipo_pp == 'tipo_dias' and dias == 0:
                    self.error_operation = 'Debe indicar periodo de dias'
                    return False

            if concepto == '':
                self.error_operation = 'Debe indicar el concepto'
                return False

            # punto
            usuario = request.user
            usuario_perfil = UsersPerfiles.objects.get(user_id=usuario)
            punto = Puntos.objects.get(pk=usuario_perfil.punto_id)

            # tipo de operacion, adicion o modificacion
            tipo_operacion = request.POST['tipo_operacion']
            m_venta_id = request.POST['m_id']

            venta_ant = {}
            planpago_ant = {}
            if tipo_operacion == 'modify':
                venta_ant = apps.get_model('preventas', 'PreVentas').objects.get(pk=int(m_venta_id))
                if venta_ant.tipo_preventa == 'PLANPAGO':
                    planpago_ant = PlanPagos.objects.get(preventa_id=venta_ant.preventa_id)

            datos = {}
            datos['tipo_operacion'] = tipo_operacion
            datos['m_venta_id'] = m_venta_id
            datos['apellidos'] = apellidos
            datos['venta_id'] = 0
            datos['registro_id'] = 0
            datos['nombres'] = nombres
            datos['ci_nit'] = ci_nit
            datos['telefonos'] = telefonos
            datos['tipo_preventa'] = tipo_venta
            datos['costo_abc'] = costo_abc

            # tipo de operacion: nuevo o modificar
            if tipo_operacion == 'modify':
                datos['fecha'] = venta_ant.fecha
            else:
                datos['fecha'] = 'now'

            datos['user_id_fecha'] = usuario.id
            datos['subtotal'] = 0
            datos['porcentaje_descuento']= porcentaje_descuento
            datos['descuento']= descuento
            datos['total'] = 0
            datos['saldo'] = 0
            datos['concepto'] = concepto
            datos['created_at'] = 'now'
            datos['updated_at'] = 'now'

            datos['almacen_id'] = Almacenes.objects.get(pk=int(almacen1))
            datos['cliente_id'] = cliente_id
            datos['punto_id'] = punto

            datos['status_id'] = status_venta
            datos['user_id'] = usuario

            # plan de pago
            datos['tipo_pp'] = tipo_pp
            datos['fecha_fija'] = fecha_fija
            datos['dias'] = dias
            datos['numero_cuotas'] = numero_cuotas

            # detalles del registro
            detalles = []
            for i in range(1, 51):
                nombre = 'producto_' + str(i)

                if not nombre in request.POST.keys():
                    continue

                aux = request.POST[nombre].strip()
                tb2 = request.POST['tb2_' + str(i)].strip()

                if aux == '0':
                    continue

                #print('aux:', aux)
                #print('tb2:', tb2)

                # vemos los ids del stock
                stock_ids = request.POST['stock_ids_'+aux]
                if stock_ids == '':
                    continue

                division = stock_ids.split(',')
                #print('stock_ids: ', stock_ids)
                for s_id in division:
                    aux_cant = 'cantidad_' + s_id
                    aux_costo = 'costo_' + s_id
                    aux_actual = 'actual_' + s_id
                    aux_f_elab = 'f_elab_' + s_id
                    aux_f_venc = 'f_venc_' + s_id
                    aux_lote = 'lote_' + s_id

                    if not aux_cant in request.POST.keys():
                        continue

                    cantidad = request.POST[aux_cant].strip()
                    costo = request.POST[aux_costo].strip()
                    actual = request.POST[aux_actual].strip()

                    # fecha elaboracion
                    fecha_elaboracion = request.POST[aux_f_elab].strip()
                    if fecha_elaboracion == '/N':
                        fecha_elaboracion = None
                    else:
                        fecha_elaboracion = get_date_to_db(fecha=fecha_elaboracion, formato_ori='d-M-yy', formato='yyyy-mm-dd HH:ii:ss')

                    # fecha vencimiento
                    fecha_vencimiento = request.POST[aux_f_venc].strip()
                    if fecha_vencimiento == '/N':
                        fecha_vencimiento = None
                    else:
                        fecha_vencimiento = get_date_to_db(fecha=fecha_vencimiento, formato_ori='d-M-yy', formato='yyyy-mm-dd HH:ii:ss')

                    # lote
                    lote = request.POST[aux_lote].strip()
                    cant_valor = 0 if cantidad == '' else Decimal(cantidad)
                    costo_valor = 0 if costo == '' else Decimal(costo)
                    actual_valor = 0 if actual == '' else Decimal(actual)

                    if cant_valor > 0 and costo_valor > 0 and cant_valor <= actual_valor:
                        # registramos la salida
                        dato_detalle = {}
                        dato_detalle['producto_id'] = Productos.objects.get(pk=int(aux))
                        dato_detalle['cantidad'] = cant_valor
                        dato_detalle['costo'] = costo_valor
                        dato_detalle['total'] = cant_valor * costo_valor
                        dato_detalle['fecha_elaboracion'] = fecha_elaboracion
                        dato_detalle['fecha_vencimiento'] = fecha_vencimiento
                        dato_detalle['lote'] = lote

                        detalles.append(dato_detalle)
                    else:
                        if cant_valor > actual_valor:
                            self.error_operation = 'La cantidad no puede ser mayor a ' + str(actual_valor) + ' del producto ' + tb2
                            return False

            # detalles
            #print('detalles: ', detalles)

            datos['detalles'] = detalles
            # verificando que haya detalles
            if len(detalles) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            if self.add_db(**datos):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar la venta, " + str(ex)
            return False

    def add_db(self, **datos):
        """aniadimos a la base de datos"""
        try:
            if len(datos['detalles']) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            with transaction.atomic():
                # tipo de operacion
                venta_ant = {}
                planpago_ant = {}
                if datos['tipo_operacion'] == 'modify':
                    venta_ant = apps.get_model('preventas', 'PreVentas').objects.get(pk=int(datos['m_venta_id']))
                    if venta_ant.tipo_preventa == 'PLANPAGO':
                        planpago_ant = PlanPagos.objects.get(preventa_id=venta_ant.preventa_id)

                campos_add = {}
                campos_add['venta_id'] = 0
                campos_add['registro_id'] = 0
                campos_add['apellidos'] = datos['apellidos']
                campos_add['nombres'] = datos['nombres']
                campos_add['ci_nit'] = datos['ci_nit']
                campos_add['telefonos'] = datos['telefonos']
                campos_add['tipo_preventa'] = datos['tipo_preventa']
                campos_add['costo_abc'] = datos['costo_abc']
                campos_add['fecha'] = datos['fecha']
                campos_add['user_id_fecha'] = datos['user_id_fecha']
                campos_add['subtotal'] = datos['subtotal']
                campos_add['descuento'] = datos['descuento']
                campos_add['porcentaje_descuento'] = datos['porcentaje_descuento']
                campos_add['total'] = datos['total']
                campos_add['saldo'] = datos['saldo']
                campos_add['concepto'] = datos['concepto']
                campos_add['created_at'] = datos['created_at']
                campos_add['updated_at'] = datos['updated_at']

                campos_add['almacen_id'] = datos['almacen_id']
                campos_add['cliente_id'] = datos['cliente_id']
                campos_add['punto_id'] = datos['punto_id']

                campos_add['status_id'] = datos['status_id']
                campos_add['user_id'] = datos['user_id']

                # venta
                preventa_add = apps.get_model('preventas', 'PreVentas').objects.create(**campos_add)
                preventa_add.save()

                # detalles
                suma_subtotal = 0
                suma_descuento = 0
                suma_total = 0

                for detalle in datos['detalles']:
                    suma_subtotal += detalle['total']
                    suma_total += detalle['total']
                    detalle_add = apps.get_model('preventas', 'PreVentasDetalles').objects.create(preventa_id=preventa_add, punto_id=datos['punto_id'], descuento=0, porcentaje_descuento=0, producto_id=detalle['producto_id'], cantidad=detalle['cantidad'], costo=detalle[
                        'costo'], total=detalle['total'], fecha_elaboracion=detalle['fecha_elaboracion'], fecha_vencimiento=detalle['fecha_vencimiento'], lote=detalle['lote'])
                    detalle_add.save()

                # actualizamos datos
                # verficamos si es modificacion o adicion
                if datos['tipo_operacion'] == 'add':
                    preventa_add.numero_preventa = preventa_add.preventa_id
                else:
                    preventa_add.numero_preventa = venta_ant.numero_preventa

                preventa_add.subtotal = suma_subtotal
                
                # preventa_add.descuento = suma_descuento
                preventa_add.porcentaje_descuento= datos['porcentaje_descuento']
                preventa_add.descuento= datos['descuento']
                
                # preventa_add.total = suma_total
                preventa_add.total= suma_subtotal - datos['descuento']
                
                preventa_add.save()

                # plan de pagos si es el caso
                if preventa_add.tipo_preventa == 'PLANPAGO':
                    campos_pp = {}
                    campos_pp['preventa_id'] = preventa_add.preventa_id
                    campos_pp['cliente_id'] = preventa_add.cliente_id.cliente_id
                    campos_pp['punto_id'] = preventa_add.punto_id.punto_id
                    campos_pp['fecha'] = datos['fecha']
                    campos_pp['concepto'] = preventa_add.concepto
                    campos_pp['numero_cuotas'] = int(datos['numero_cuotas'])
                    campos_pp['monto_total'] = preventa_add.total
                    campos_pp['cuota_inicial'] = 0
                    campos_pp['saldo'] = preventa_add.total
                    campos_pp['mensual_dias'] = datos['tipo_pp']

                    campos_pp['fecha_fija'] = datos['fecha_fija']
                    campos_pp['dias'] = datos['dias']

                    if datos['tipo_pp'] == 'tipo_fecha':
                        campos_pp['dia_mensual'] = int(get_day_from_date(datos['fecha_fija'], formato_ori='yyyy-mm-dd HH:ii:ss'))
                        campos_pp['tiempo_dias'] = 0
                    else:
                        campos_pp['dia_mensual'] = 0
                        campos_pp['tiempo_dias'] = int(datos['dias'])

                    campos_pp['status_id'] = Status.objects.get(pk=self.activo)
                    campos_pp['user_id'] = datos['user_id']
                    campos_pp['created_at'] = datos['created_at']
                    campos_pp['updated_at'] = datos['updated_at']

                    plan_pago_controller = PlanPagosController()
                    if not plan_pago_controller.add_plan_pago_db(**campos_pp):
                        self.error_operation = 'Error al agregar el plan de pagos'
                        return False

                # verificamos si es operacion de modificar para anular la anterior
                if datos['tipo_operacion'] == 'modify':
                    status_eliminar = self.status_eliminado
                    venta_ant.status_id = status_eliminar
                    venta_ant.deleted_at = 'now'
                    venta_ant.motivo_anula = 'eliminacion por modificacion de preventa'
                    venta_ant.user_id_anula = datos['user_id'].id
                    venta_ant.save()

                    if venta_ant.tipo_preventa == 'PLANPAGO':
                        planpago_ant.status_id = status_eliminar
                        planpago_ant.deleted_at = 'now'
                        planpago_ant.motivo_anula = 'eliminacion por modificacion de preventa'
                        planpago_ant.user_id_anula = datos['user_id'].id
                        planpago_ant.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add venta, '+str(ex))
            return False

    def can_anular(self, id, user):
        """verificando si se puede anular o no la tabla"""
        # puede anular el usuario con permiso de la sucursal
        usuario_perfil = UsersPerfiles.objects.get(user_id=user)
        punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
        permisos = get_permissions_user(user, settings.MOD_PREVENTAS)

        # registro
        venta = apps.get_model('preventas', 'PreVentas').objects.get(pk=id)
        if venta.status_id.status_id == self.anulado:
            self.error_operation = 'el registro ya esta anulado'
            return False

        # registro de la misma sucursal
        if venta.punto_id.sucursal_id == punto.sucursal_id:
            # verificamos si es plan de pagos, y no pago ninguna cuota
            if venta.tipo_preventa == 'PLANPAGO':
                plan_pago = PlanPagos.objects.get(preventa_id=venta.preventa_id)
                if plan_pago.monto_total == plan_pago.saldo:
                    if permisos.anular:
                        return True
            else:
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
                self.error_operation = 'No tiene permiso para anular esta venta'
                return False

        except Exception as ex:
            print('Error anular venta: ' + str(ex))
            self.error_operation = 'Error al anular la venta, ' + str(ex)
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
                venta_update = apps.get_model('preventas', 'PreVentas').objects.filter(pk=id)
                venta_update.update(**campos_update)

                # actualizamos los detalles
                venta = apps.get_model('preventas', 'PreVentas').objects.get(pk=id)

                # verificamos si tiene plan de pagos
                if venta.tipo_preventa == 'PLANPAGO':
                    plan_pago = PlanPagos.objects.get(preventa_id=venta.preventa_id)
                    plan_pago.user_id_anula = datos['user_id_anula']
                    plan_pago.motivo_anula = datos['motivo_anula']
                    plan_pago.status_id = datos['status_id']
                    plan_pago.deleted_at = datos['deleted_at']
                    plan_pago.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            print('Error anular venta db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return

    # def lista_almacenes(self, user):
    #     """lista de almacenes para el usuario"""
    #     UserPerfil = UsersPerfiles.objects.get(user_id=user)
    #     punto = Puntos.objects.get(pk=UserPerfil.punto_id)
    #
    #     # status activo
    #     status_activo = Status.objects.get(pk=self.activo)
    #
    #     filtros = {}
    #     filtros['status_id'] = status_activo
    #     filtros['almacen_id__status_id'] = status_activo
    #     # almacen central
    #     filtros['almacen_id'] = Almacenes.objects.get(pk=1)
    #
    #     almacenes = []
    #     puntos_almacenes = PuntosAlmacenes.objects.select_related('almacen_id').select_related('punto_id').select_related('punto_id__sucursal_id').filter(**filtros).order_by('almacen_id__almacen')
    #     for punto_almacen in puntos_almacenes:
    #         dato = {}
    #         dato['almacen_id'] = punto_almacen.almacen_id.almacen_id
    #         dato['almacen'] = punto_almacen.almacen_id.almacen
    #         dato['sucursal'] = punto_almacen.punto_id.sucursal_id.sucursal
    #         almacenes.append(dato)
    #
    #     return almacenes

    def get_preventa(self, preventa_id, punto_id, fecha):
        """devolvemos los datos de la preventa"""
        datos = {}
        datos['venta_id'] = preventa_id
        datos['next_id'] = 0
        datos['previous_id'] = 0

        # si manda id 0
        if preventa_id == 0:
            return datos

        # recuperamos datos de la venta
        try:
            venta = apps.get_model('preventas', 'PreVentas').objects.select_related('user_id').select_related('punto_id').get(pk=preventa_id)
            datos['venta_id'] = venta.preventa_id
            datos['registro_id'] = venta.registro_id
            datos['next_id'] = self.get_next_id(venta.preventa_id, punto_id, fecha)
            datos['previous_id'] = self.get_previous_id(venta.preventa_id, punto_id, fecha)
            datos['almacen_id'] = venta.almacen_id.almacen_id
            datos['cliente_id'] = venta.cliente_id.cliente_id
            datos['tipo_preventa'] = venta.tipo_preventa
            datos['costo_abc'] = venta.costo_abc
            datos['apellidos'] = venta.apellidos
            datos['nombres'] = venta.nombres
            datos['ci_nit'] = venta.ci_nit
            datos['telefonos'] = venta.telefonos
            datos['tipo_venta'] = venta.tipo_preventa
            datos['numero_venta'] = venta.numero_preventa
            datos['costo_abc'] = venta.costo_abc
            datos['fecha'] = venta.fecha
            datos['subtotal'] = venta.subtotal
            datos['descuento'] = venta.descuento
            datos['porcentaje_descuento'] = venta.porcentaje_descuento
            datos['total'] = venta.total
            datos['status_id'] = venta.status_id
            datos['user'] = venta.user_id.username
            datos['punto'] = venta.punto_id.punto
            datos['user_id_anula'] = venta.user_id_anula
            datos['user_anula'] = ''

            # plan de pagos
            if venta.tipo_preventa == 'PLANPAGO':
                plan_pago = PlanPagos.objects.get(preventa_id=venta.preventa_id)
                plan_pago_detalle = PlanPagosDetalles.objects.get(plan_pago_id=plan_pago, numero_cuota=1)
                datos['numero_cuotas'] = plan_pago.numero_cuotas
                datos['mensual_dias'] = plan_pago.mensual_dias
                datos['tiempo_dias'] = plan_pago.tiempo_dias
                datos['fecha_fija'] = get_date_show(fecha=plan_pago_detalle.fecha, formato='dd-MMM-yyyy')
            else:
                datos['numero_cuotas'] = 0
                datos['mensual_dias'] = ''
                datos['tiempo_dias'] = 0
                datos['fecha_fija'] = ''

            # verificamos si la venta esta anulada
            if not venta.user_id_anula is None and venta.user_id_anula != 0:
                user_anula = User.objects.get(pk=venta.user_id_anula)
                datos['user_anula'] = user_anula.username

            # detalles de la venta
            ventas_detalles = apps.get_model('preventas', 'PreVentasDetalles').objects.select_related('producto_id').select_related('producto_id__linea_id').filter(preventa_id=venta).order_by('preventa_detalle_id', 'producto_id__producto')
            detalles = []
            for venta_detalle in ventas_detalles:
                dato_detalle = {}
                dato_detalle['producto_id'] = venta_detalle.producto_id.producto_id
                dato_detalle['producto'] = venta_detalle.producto_id.producto
                dato_detalle['producto_linea'] = venta_detalle.producto_id.linea_id.linea + ' ' + venta_detalle.producto_id.producto
                dato_detalle['cantidad'] = venta_detalle.cantidad
                dato_detalle['costo'] = venta_detalle.costo
                dato_detalle['total'] = venta_detalle.total
                dato_detalle['fecha_elaboracion'] = '' if venta_detalle.fecha_elaboracion is None else get_date_show(fecha=venta_detalle.fecha_elaboracion, formato='dd-MMM-yyyy')
                dato_detalle['fecha_vencimiento'] = '' if venta_detalle.fecha_vencimiento is None else get_date_show(fecha=venta_detalle.fecha_vencimiento, formato='dd-MMM-yyyy')

                # para modificacion
                dato_detalle['fecha_elaboracion_mod'] = '/N' if venta_detalle.fecha_elaboracion is None else get_date_show(fecha=venta_detalle.fecha_elaboracion, formato='d-M-yy')
                dato_detalle['fecha_vencimiento_mod'] = '/N' if venta_detalle.fecha_vencimiento is None else get_date_show(fecha=venta_detalle.fecha_vencimiento, formato='d-M-yy')

                dato_detalle['lote'] = '' if venta_detalle.lote == '' else venta_detalle.lote
                detalles.append(dato_detalle)

            # adiciminamos los datos del detalle
            datos['detalles'] = detalles

            return datos

        except Exception as ex:
            print('error al recuperar datos de preventa_id: ' + str(preventa_id) + ', ' + str(ex))
            datos['venta_id'] = -1
            return datos

    def get_last_id(self, punto_id, fecha):
        """ultimo id de venta para la fecha"""
        last_id = 0
        fecha_ini = fecha + ' 00:00:00'
        fecha_fin = fecha + ' 23:59:59'
        status_preventa = "'" + str(self.preventa) + "', '" + str(self.preventa_venta) + "', '" + str(self.anulado) + "'"
        sql = f"SELECT MAX(preventa_id) AS maximo FROM preventas WHERE punto_id='{punto_id}' AND fecha>='{fecha_ini}' AND fecha<='{fecha_fin}' AND status_id IN ({status_preventa}) "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                last_id = 0 if row[0] is None else row[0]

        return last_id

    def get_next_id(self, id, punto_id, fecha):
        """next id de preventa """
        next_id = 0
        fecha_ini = fecha + ' 00:00:00'
        fecha_fin = fecha + ' 23:59:59'
        status_preventa = "'" + str(self.preventa) + "', '" + str(self.preventa_venta) + "', '" + str(self.anulado) + "'"
        sql = f"SELECT MIN(preventa_id) AS maximo FROM preventas WHERE punto_id='{punto_id}' AND fecha>='{fecha_ini}' AND fecha<='{fecha_fin}' AND preventa_id>'{id}' AND status_id IN ({status_preventa}) "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                if row[0]:
                    next_id = row[0]

        return next_id

    def get_previous_id(self, id, punto_id, fecha):
        """next id de preventa """
        previous_id = 0
        fecha_ini = fecha + ' 00:00:00'
        fecha_fin = fecha + ' 23:59:59'
        status_preventa = "'" + str(self.preventa) + "', '" + str(self.preventa_venta) + "', '" + str(self.anulado) + "'"
        sql = f"SELECT MAX(preventa_id) AS maximo FROM preventas WHERE punto_id='{punto_id}' AND fecha>='{fecha_ini}' AND fecha<='{fecha_fin}' AND preventa_id<'{id}' AND status_id IN ({status_preventa}) "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                if row[0]:
                    previous_id = row[0]

        return previous_id

    def lista_pedidos(self, request, almacen_id):
        """pedido de inventario, recuperamos todas las preventas en estado preventa"""
        try:
            status_preventa = self.status_preventa
            status_activo = self.status_activo
            # almacen
            almacen_pedido = Almacenes.objects.get(pk=almacen_id, status_id=status_activo)
            # punto
            user_perfil = UsersPerfiles.objects.get(user_id=request.user)
            punto_pedido = Puntos.objects.get(pk=user_perfil.punto_id)

            filtros = {}
            filtros['status_id'] = status_preventa
            filtros['almacen_id'] = almacen_pedido
            filtros['registro_id'] = 0
            filtros['punto_id'] = punto_pedido

            preventas = apps.get_model('preventas', 'PreVentas').objects.filter(**filtros).select_related('almacen_id').order_by('fecha')
            lista = []
            for preventa in preventas:
                datos = {}
                datos['preventa_id'] = preventa.preventa_id
                datos['numero_preventa'] = preventa.numero_preventa
                datos['apellidos'] = preventa.apellidos
                datos['nombres'] = preventa.nombres
                datos['ci_nit'] = preventa.ci_nit
                datos['numero_preventa'] = preventa.numero_preventa
                datos['fecha'] = preventa.fecha
                datos['total'] = preventa.total

                # detalles
                preventa_detalle = apps.get_model('preventas', 'PreVentasDetalles').objects.select_related('producto_id').select_related('producto_id__linea_id').filter(preventa_id=preventa).order_by('preventa_detalle_id')
                detalle_preventa = []
                for detalle in preventa_detalle:
                    datos_detalle = {}
                    datos_detalle['producto'] = detalle.producto_id.linea_id.linea + ' - ' + detalle.producto_id.producto
                    datos_detalle['producto_id'] = detalle.producto_id.producto_id
                    datos_detalle['cantidad'] = detalle.cantidad
                    datos_detalle['costo'] = detalle.costo
                    datos_detalle['total'] = detalle.total
                    datos_detalle['fecha_elaboracion'] = detalle.fecha_elaboracion
                    datos_detalle['fecha_vencimiento'] = detalle.fecha_vencimiento
                    datos_detalle['lote'] = detalle.lote
                    detalle_preventa.append(datos_detalle)

                # aniadimos los detalles
                datos['detalle'] = detalle_preventa
                # aniadimos los registros
                lista.append(datos)

            self.error_operation = ''
            return lista

        except Exception as ex:
            self.error_operation = 'Error al recuperar los pedidos, ' + str(ex)
            print('ERROR pedido inventario: ' + str(ex))
            return []

    def pedido_inventario(self, request):
        """aniadimos un nuevo registro de pedido"""
        try:
            cant_pedidos = int(request.POST['cant_pedidos'].strip())
            cant_productos = int(request.POST['cant_productos_pedido'].strip())

            lista_pedidos_id = []
            for i in range(1, cant_pedidos+1):
                nombre = 'pedido_' + str(i)
                if nombre in request.POST.keys():
                    pedido_id = request.POST['pedido_id_'+str(i)]
                    lista_pedidos_id.append(pedido_id)

            # cantidad de pedidos
            if len(lista_pedidos_id) == 0:
                self.error_operation = 'Debe seleccionar al menos un pedido'
                return False

            # productos para el pedido a almacen
            lista_productos = []
            for i in range(1, cant_productos+1):
                producto_pedido_id = request.POST['producto_pedido_'+str(i)]

                aux_f = request.POST['producto_fecha_elab_'+str(i)]
                if aux_f == '/N':
                    fecha_elaboracion = None
                else:
                    fecha_elaboracion = get_date_to_db(fecha=aux_f, formato_ori='d-M-yy', formato='yyyy-mm-dd HH:ii:ss')

                aux_f = request.POST['producto_fecha_venc_'+str(i)]
                if aux_f == '/N':
                    fecha_vencimiento = None
                else:
                    fecha_vencimiento = get_date_to_db(fecha=aux_f, formato_ori='d-M-yy', formato='yyyy-mm-dd HH:ii:ss')

                lote = request.POST['producto_lote_'+str(i)]
                print('antes cantidad...')
                cantidad = Decimal(request.POST['producto_pedido_cant_'+str(i)])
                print('despues cantidad...', cantidad)

                if cantidad > 0:
                    dato_pedido = {}
                    dato_pedido['producto_pedido_id'] = producto_pedido_id
                    dato_pedido['fecha_elaboracion'] = fecha_elaboracion
                    dato_pedido['fecha_vencimiento'] = fecha_vencimiento
                    dato_pedido['lote'] = lote
                    dato_pedido['cantidad'] = cantidad

                    lista_productos.append(dato_pedido)

            # cantidad de productos en el pedido con cantidad mayor a cero
            if len(lista_productos) == 0:
                self.error_operation = 'Debe tener cantidades en los productos'
                return False

            # punto
            usuario = request.user
            usuario_perfil = UsersPerfiles.objects.get(user_id=usuario)
            punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
            status_activo = self.status_activo

            punto_almacenes = PuntosAlmacenes.objects.filter(status_id=status_activo, punto_id=punto)
            punto_almacen = punto_almacenes.first()

            # almacen central
            almacen1 = 1
            almacen2 = punto_almacen.almacen_id.almacen_id

            datos = {}
            # preventas
            datos['preventas_ids'] = lista_pedidos_id
            datos['almacen_id'] = Almacenes.objects.get(pk=int(almacen1))
            datos['almacen2_id'] = int(almacen2)
            datos['punto_id'] = punto
            datos['status_id'] = status_activo
            datos['user_id'] = usuario
            datos['concepto'] = 'pedido de inventario para el almacen ' + str(almacen2)
            datos['tipo_movimiento'] = 'MOVIMIENTO'
            datos['costo_abc'] = ''
            datos['fecha'] = 'now'
            datos['created_at'] = 'now'
            datos['updated_at'] = 'now'
            datos['user_id_fecha'] = usuario.id

            # detalle
            detalles = []
            for producto in lista_productos:
                # registramos la salida
                dato_detalle = {}
                dato_detalle['producto_id'] = Productos.objects.get(pk=int(producto['producto_pedido_id']))
                dato_detalle['cantidad'] = producto['cantidad']
                dato_detalle['costo'] = 0
                dato_detalle['total'] = 0
                dato_detalle['fecha_elaboracion'] = producto['fecha_elaboracion']
                dato_detalle['fecha_vencimiento'] = producto['fecha_vencimiento']
                dato_detalle['lote'] = producto['lote']

                detalles.append(dato_detalle)

            # detalles
            datos['detalles'] = detalles

            if self.pedido_inventario_db(**datos):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            print('ERROR: ', str(ex))
            self.error_operation = "Error al agregar el pedido, " + str(ex)
            return False

    def pedido_inventario_db(self, **datos):
        """aniadimos a la base de datos"""
        try:
            if len(datos['detalles']) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            movimiento_controller = MovimientosAlmacenController()
            with transaction.atomic():
                if not movimiento_controller.add_db(**datos):
                    self.error_operation = 'Error al registrar el movimiento'
                    return False

                # recuperamos el registro
                registro_movimiento = Registros.objects.get(fecha=datos['fecha'], tipo_movimiento='MOVIMIENTO')

                # actualizamos las preventas
                for p_id in datos['preventas_ids']:
                    preventa = apps.get_model('preventas', 'PreVentas').objects.get(pk=p_id)
                    preventa.registro_id = registro_movimiento.registro_id
                    preventa.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add pedido inventario, '+str(ex))
