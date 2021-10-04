from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from inventarios.models import Registros, RegistrosDetalles, PlanPagos, PlanPagosDetalles, PlanPagosPagos
from productos.models import Insumos
from permisos.models import UsersPerfiles
from configuraciones.models import Puntos, Almacenes, Cajas
from cajas.models import CajasIngresos
from status.models import Status

from django.db import transaction

from decimal import Decimal

# fechas
from utils.dates_functions import get_date_show, get_date_system, get_date_to_db, get_seconds_date1_sub_date2, add_days_datetime, get_day_from_date
from utils.permissions import get_permissions_user

from controllers.inventarios.StockController import StockController
from controllers.inventarios.PlanPagosController import PlanPagosController
from controllers.cajas.CajasController import CajasController
from controllers.cajas.CajasIngresosController import CajasIngresosController

from utils.validators import validate_number_int, validate_number_decimal, validate_string


class PedidosAlmacenController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Registros'
        self.modelo_id = 'registro_id'
        self.modelo_app = 'inventarios'
        self.modulo_id = settings.MOD_PEDIDOS_ALMACEN

        # variables de session
        self.modulo_session = "pedidos_almacen"
        self.columnas.append('fecha')
        self.columnas.append('almacen_id__almacen')
        self.columnas.append('concepto')

        self.variables_filtros.append('search_fecha_ini')
        self.variables_filtros.append('search_fecha_fin')
        self.variables_filtros.append('search_almacen')
        self.variables_filtros.append('search_concepto')
        self.variables_filtros.append('search_codigo')

        fecha_actual = get_date_system()
        fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
        fecha_ini = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-7, formato='dd-MMM-yyyy')

        self.variables_filtros_defecto['search_fecha_ini'] = fecha_ini
        self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin
        self.variables_filtros_defecto['search_almacen'] = '0'
        self.variables_filtros_defecto['search_concepto'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = "cbo|0|S|almacen|;"
        self.control_form += "cbo|0|S|almacen2|;"
        self.control_form += "cbo|0|S|tipo_movimiento|;"
        self.control_form += "cbo|0|S|costo_abc|;"
        self.control_form += "txt|2|S|concepto|"

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
                fecha_inicio = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=0, formato='dd-MMM-yyyy')
                fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

                self.variables_filtros_values['search_fecha_ini'] = fecha_inicio
                self.variables_filtros_defecto['search_fecha_ini'] = fecha_inicio
                self.variables_filtros_values['search_fecha_fin'] = fecha_fin
                self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin

                # orden por defecto
                self.variable_order_value = self.columnas[0]
                self.variable_order_type_value = 'DESC'
                request.session[self.modulo_session][self.variable_order] = self.variable_order_value
                request.session[self.modulo_session][self.variable_order_type] = self.variable_order_type_value

                # session
                request.session[self.modulo_session]['search_fecha_ini'] = self.variables_filtros_defecto['search_fecha_ini']
                request.session[self.modulo_session]['search_fecha_fin'] = self.variables_filtros_defecto['search_fecha_fin']
                request.session.modified = True

            #print('variable:', self.variable_val)
            # actualizamos a la fecha actual
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True
        else:
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True

        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.inv_pedido, self.inv_entrega, self.inv_devolucion, self.anulado]
        # tipo movimiento
        self.filtros_modulo['tipo_movimiento__in'] = ['CONTADO', 'FACTURA', 'CONSIGNACION', 'PLANPAGO']
        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['registro_id'] = int(self.variables_filtros_values['search_codigo'].strip())
        else:
            # fechas
            if self.variables_filtros_values['search_fecha_ini'].strip() != '' and self.variables_filtros_values['search_fecha_fin'].strip() != '':
                self.filtros_modulo['fecha__gte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_ini'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
                self.filtros_modulo['fecha__lte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_fin'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

            # almacen
            if self.variables_filtros_values['search_almacen'].strip() != "0":
                self.filtros_modulo['almacen2_id'] = int(self.variables_filtros_values['search_almacen'].strip())
            # concepto
            if self.variables_filtros_values['search_concepto'].strip() != "":
                self.filtros_modulo['concepto__icontains'] = self.variables_filtros_values['search_concepto'].strip()

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
        retorno = modelo.objects.select_related('almacen_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]

        return retorno

    def add(self, request):
        """aniadimos un nuevo registro"""
        try:
            # pedido de inventario
            status_registro = self.status_inv_pedido
            almacen1 = validate_number_int('almacen', request.POST['almacen'])
            almacen2 = validate_number_int('almacen2', request.POST['almacen2'])
            tipo_movimiento = validate_string('tipo movimiento', request.POST['tipo_movimiento'], remove_specials='yes')
            costo_abc = validate_string('costo abc', request.POST['costo_abc'])
            concepto = validate_string('concepto', request.POST['concepto'], remove_specials='yes')

            numero_cuotas = validate_number_int('numero cuotas', request.POST['numero_cuotas'], len_zero='yes')
            tipo_pp = validate_string('tipo plan pago', request.POST['tipo_pp'], len_zero='yes')
            fecha_fija = validate_string('fecha fija', request.POST['fecha_fija'])
            dias = validate_number_int('dias', request.POST['dias'], len_zero='yes')

            porcentaje_descuento = validate_number_decimal('porcentaje_descuento', request.POST['porcentaje_descuento'], len_zero='yes')
            descuento = validate_number_decimal('descuento', request.POST['descuento'], len_zero='yes')

            # formato para la fecha fija
            fecha_fija = get_date_to_db(fecha_fija, formato='yyyy-mm-dd HH:ii:ss')

            if almacen1 == '0':
                self.error_operation = 'Debe seleccionar el almacen de origen'
                return False

            if almacen2 == '0':
                self.error_operation = 'Debe seleccionar el almacen de destino'
                return False

            if almacen1 == almacen2:
                self.error_operation = 'Debe seleccionar un almacen diferente de destino'
                return False

            if tipo_movimiento == '0':
                self.error_operation = 'Debe seleccionar el tipo de venta'
                return False

            if costo_abc == '0':
                self.error_operation = 'Debe seleccionar el tipo de costo'
                return False

            if tipo_movimiento == 'PLANPAGO':
                if numero_cuotas == '':
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

            datos = {}
            datos['almacen_id'] = Almacenes.objects.get(pk=int(almacen1))
            datos['almacen2_id'] = int(almacen2)
            datos['punto_id'] = punto
            datos['status_id'] = status_registro
            datos['user_id'] = usuario
            datos['concepto'] = request.POST['concepto'].strip()
            datos['tipo_movimiento'] = tipo_movimiento
            datos['costo_abc'] = costo_abc
            datos['tipo_pp'] = tipo_pp
            datos['fecha_fija'] = fecha_fija
            datos['dias'] = dias
            datos['numero_cuotas'] = numero_cuotas
            datos['porcentaje_descuento'] = porcentaje_descuento
            datos['descuento'] = descuento
            datos['fecha'] = 'now'
            datos['created_at'] = 'now'
            datos['updated_at'] = 'now'
            datos['user_id_fecha'] = usuario.id

            # detalles del registro
            detalles = []
            for i in range(1, 51):
                aux = request.POST['producto_' + str(i)].strip()
                tb2 = request.POST['tb2_' + str(i)].strip()

                #print('aux:', aux)
                #print('tb2:', tb2)
                if aux != '0':
                    # vemos los ids del stock
                    stock_ids = request.POST['stock_ids_'+aux]
                    division = stock_ids.split(',')

                    if stock_ids != '':
                        for s_id in division:
                            aux_cant = 'cantidad_' + s_id
                            aux_costo = 'costo_' + s_id
                            aux_actual = 'actual_' + s_id
                            aux_f_elab = 'f_elab_' + s_id
                            aux_f_venc = 'f_venc_' + s_id
                            aux_lote = 'lote_' + s_id

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
                                dato_detalle['producto_id'] = Insumos.objects.get(pk=int(aux))
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
            datos['detalles'] = detalles
            # verificando que haya detalles
            if len(detalles) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            self.error_operation = ''
            if self.add_db(**datos):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el registro " + str(ex)
            return False

    def add_db(self, **datos):
        """aniadimos a la base de datos"""

        try:
            if len(datos['detalles']) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            stock_controller = StockController()
            caja_controller = CajasController()
            # caja del usuario
            caja_user = None

            with transaction.atomic():
                # verificamos caja activa
                if datos['tipo_movimiento'] == 'CONTADO' or datos['tipo_movimiento'] == 'FACTURA':
                    # cajas activas
                    user_perfil = UsersPerfiles.objects.get(user_id=datos['user_id'])
                    if user_perfil.caja_id == 0:
                        self.error_operation = 'Debe tener una caja asignada activa '
                        return False

                    # recuperamos la caja del usuario
                    caja_user = apps.get_model('configuraciones', 'Cajas').objects.get(pk=user_perfil.caja_id)
                    caja_estado = caja_controller.cash_active(get_date_system(), datos['user_id'])
                    if not caja_estado:
                        self.error_operation = 'Debe tener su caja activa: ' + caja_user.caja
                        return False

                campos_add = {}
                campos_add['almacen_id'] = datos['almacen_id']
                campos_add['almacen2_id'] = datos['almacen2_id']
                campos_add['punto_id'] = datos['punto_id']
                campos_add['status_id'] = datos['status_id']
                campos_add['user_id'] = datos['user_id']
                campos_add['concepto'] = datos['concepto']
                campos_add['tipo_movimiento'] = datos['tipo_movimiento']
                campos_add['costo_abc'] = datos['costo_abc']
                campos_add['fecha'] = datos['fecha']
                campos_add['created_at'] = datos['created_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['user_id_fecha'] = datos['user_id_fecha']

                # registro
                registro_add = Registros.objects.create(**campos_add)
                registro_add.save()

                # detalles
                suma_subtotal = 0
                suma_descuento = 0
                suma_total = 0
                almacen2 = Almacenes.objects.get(pk=datos['almacen2_id'])
                for detalle in datos['detalles']:
                    suma_subtotal += detalle['total']
                    suma_total += detalle['total']
                    detalle_add = RegistrosDetalles.objects.create(registro_id=registro_add, punto_id=datos['punto_id'], descuento=0, porcentaje_descuento=0, insumo_id=detalle['producto_id'], cantidad=detalle['cantidad'], costo=detalle[
                                                                   'costo'], total=detalle['total'], fecha_elaboracion=detalle['fecha_elaboracion'], fecha_vencimiento=detalle['fecha_vencimiento'], lote=detalle['lote'])
                    detalle_add.save()

                    # actualizamos el stock, salida del almacen 1
                    stock_up = stock_controller.update_stock(user=datos['user_id'], almacen=datos['almacen_id'], producto=detalle['producto_id'], cantidad=(0-detalle['cantidad']),
                                                             fecha_elaboracion=detalle['fecha_elaboracion'], fecha_vencimiento=detalle['fecha_vencimiento'], lote=detalle['lote'])
                    if not stock_up:
                        self.error_operation = 'Error al actualizar stock almacen 1'
                        return False

                    # actualizamos el stock, ingreso al almacen 2
                    stock_up = stock_controller.update_stock(user=datos['user_id'], almacen=almacen2, producto=detalle['producto_id'], cantidad=detalle['cantidad'],
                                                             fecha_elaboracion=detalle['fecha_elaboracion'], fecha_vencimiento=detalle['fecha_vencimiento'], lote=detalle['lote'])
                    if not stock_up:
                        self.error_operation = 'Error al actualizar stock almacen 2'
                        return False

                # actualizamos datos
                registro_add.numero_registro = registro_add.registro_id
                registro_add.subtotal = suma_subtotal

                #registro_add.descuento = suma_descuento
                registro_add.porcentaje_descuento = datos['porcentaje_descuento']
                registro_add.descuento = datos['descuento']

                #registro_add.total = suma_total
                registro_add.total = suma_subtotal - datos['descuento']

                registro_add.save()

                # ingreso a caja si es el caso
                if registro_add.tipo_movimiento == 'CONTADO' or registro_add.tipo_movimiento == 'FACTURA':
                    # registramos el ingreso a caja
                    ci_controller = CajasIngresosController()

                    campos_ingreso = {}
                    campos_ingreso['caja_id'] = caja_user
                    campos_ingreso['punto_id'] = datos['punto_id']
                    campos_ingreso['user_id'] = datos['user_id']
                    campos_ingreso['status_id'] = self.status_activo
                    campos_ingreso['fecha'] = datos['fecha']
                    campos_ingreso['concepto'] = 'ingreso de efectivo, pedido almacen: ' + str(registro_add.registro_id)
                    campos_ingreso['monto'] = registro_add.total
                    campos_ingreso['created_at'] = datos['created_at']
                    campos_ingreso['updated_at'] = datos['updated_at']
                    campos_ingreso['registro_id'] = registro_add.registro_id
                    # registramos
                    ci_controller.add_db(**campos_ingreso)

                # plan de pagos si es el caso
                if registro_add.tipo_movimiento == 'PLANPAGO':
                    plan_pago_controller = PlanPagosController()

                    campos_pp = {}
                    campos_pp['registro_id'] = registro_add.registro_id
                    campos_pp['venta_id'] = 0
                    campos_pp['cliente_id'] = 0
                    campos_pp['punto_id'] = registro_add.punto_id.punto_id
                    campos_pp['fecha'] = datos['fecha']
                    campos_pp['concepto'] = registro_add.concepto
                    campos_pp['numero_cuotas'] = int(datos['numero_cuotas'])
                    campos_pp['monto_total'] = registro_add.total
                    campos_pp['cuota_inicial'] = 0
                    campos_pp['saldo'] = registro_add.total
                    campos_pp['mensual_dias'] = datos['tipo_pp']
                    campos_pp['fecha_fija'] = datos['fecha_fija']
                    campos_pp['dias'] = datos['dias']

                    if datos['tipo_pp'] == 'tipo_fecha':
                        campos_pp['dia_mensual'] = int(get_day_from_date(datos['fecha_fija'], formato_ori='dd-MMM-yyyy'))
                        campos_pp['tiempo_dias'] = 0
                    else:
                        campos_pp['dia_mensual'] = 0
                        campos_pp['tiempo_dias'] = int(datos['dias'])

                    campos_pp['status_id'] = self.status_activo
                    campos_pp['user_id'] = datos['user_id']
                    campos_pp['created_at'] = datos['created_at']
                    campos_pp['updated_at'] = datos['updated_at']

                    # registramos el plan de pagos
                    if not plan_pago_controller.add_plan_pago_db(**campos_pp):
                        self.error_operation = 'Error al adicionar el plan de pagos'
                        return False

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add pedido, '+str(ex))
            return False

    def can_anular(self, id, user):
        """verificando si se puede eliminar o no la tabla"""
        # puede anular el usuario con permiso de la sucursal
        usuario_perfil = UsersPerfiles.objects.get(user_id=user)
        punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
        permisos = get_permissions_user(user, settings.MOD_PEDIDOS_ALMACEN)

        # registro
        registro = Registros.objects.get(pk=id)
        if registro.status_id.status_id == self.anulado:
            self.error_operation = 'el registro ya esta anulado'
            return False

        # registro de la misma sucursal
        if registro.punto_id.sucursal_id == punto.sucursal_id:
            # verificamos si es plan de pagos, y no pago ninguna cuota
            if registro.tipo_movimiento == 'PLANPAGO':
                plan_pago = PlanPagos.objects.get(registro_id=registro.registro_id)
                if plan_pago.monto_total == plan_pago.saldo:
                    if permisos.anular:
                        return True

                else:
                    self.error_operation = 'el plan de pagos ya tiene cuotas pendientes'
                    return False
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
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular pedido almacen: ' + str(ex))
            self.error_operation = 'Error al anular el registro, ' + str(ex)
            return False

    def anular_db(self, id, **datos):
        """ anulamos en la bd """
        try:
            stock_controller = StockController()

            with transaction.atomic():
                campos_update = {}
                campos_update['user_id_anula'] = datos['user_id_anula']
                campos_update['motivo_anula'] = datos['motivo_anula']
                campos_update['status_id'] = datos['status_id']
                campos_update['deleted_at'] = datos['deleted_at']

                # registramos
                registro_update = Registros.objects.filter(pk=id)
                registro_update.update(**campos_update)

                # actualizamos los detalles
                registro = Registros.objects.get(pk=id)
                registros_detalles = RegistrosDetalles.objects.filter(registro_id=registro)
                almacen2 = Almacenes.objects.get(pk=registro.almacen2_id)

                for registro_detalle in registros_detalles:
                    # vuelve producto al almacen 1
                    stock_up = stock_controller.update_stock(user=datos['user_id'], almacen=registro.almacen_id, producto=registro_detalle.insumo_id, cantidad=registro_detalle.cantidad,
                                                             fecha_elaboracion=registro_detalle.fecha_elaboracion, fecha_vencimiento=registro_detalle.fecha_vencimiento, lote=registro_detalle.lote)
                    if not stock_up:
                        self.error_operation = 'Error al actualizar stock almacen 1'
                        return False

                    # sale del almacen 2
                    stock_up = stock_controller.update_stock(user=datos['user_id'], almacen=almacen2, producto=registro_detalle.insumo_id, cantidad=(0-registro_detalle.cantidad),
                                                             fecha_elaboracion=registro_detalle.fecha_elaboracion, fecha_vencimiento=registro_detalle.fecha_vencimiento, lote=registro_detalle.lote)
                    if not stock_up:
                        self.error_operation = 'Error al actualizar stock almacen 2'
                        return False

                # anulamos ingreso a caja si es necesario
                if registro.tipo_movimiento == 'CONTADO' or registro.tipo_movimiento == 'FACTURA':
                    # anulamos el registro de caja
                    ci_controller = CajasIngresosController()

                    caja_ingreso = CajasIngresos.objects.get(registro_id=registro.registro_id, status_id=self.status_activo)
                    ci_controller.delete_db(caja_ingreso.caja_ingreso_id, **campos_update)

                # verificamos si tiene plan de pagos
                if registro.tipo_movimiento == 'PLANPAGO':
                    plan_pago_controller = PlanPagosController()

                    if not plan_pago_controller.anular_db(registro_id=registro.registro_id, **datos):
                        self.error_operation = 'No se puedo anular el plan de pagos'
                        return False

                self.error_operation = ''
                return True

        except Exception as ex:
            print('Error anular pedido almacen db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return False
