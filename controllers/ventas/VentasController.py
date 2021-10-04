from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from ventas.models import Lugares, Ventas, VentasDetalles, VentasDetallesComponentes, VentasDetallesExtras, VentasDetallesInsumos, VentasDetallesPapas, VentasDetallesRefrescos
from productos.models import Componentes, Productos, ProductosComponentes, ProductosInsumos, ProductosPapas, ProductosRefrescos, RefrescosGrupo, PapasGrupo
from clientes.models import Clientes
from permisos.models import UsersPerfiles
from inventarios.models import PlanPagos, PlanPagosDetalles
from cajas.models import Cajas, CajasIngresos
from configuraciones.models import Puntos, Almacenes, PuntosAlmacenes
from status.models import Status
from decimal import Decimal

from django.db import transaction

from decimal import Decimal

# fechas
from utils.dates_functions import get_date_system, get_date_show, get_date_to_db, add_days_datetime, get_seconds_date1_sub_date2, get_day_from_date
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

from controllers.inventarios.StockController import StockController
from controllers.cajas.CajasIngresosController import CajasIngresosController
from controllers.inventarios.PlanPagosController import PlanPagosController
from controllers.productos.ProductosController import ProductosController
from controllers.clientes.ClientesController import ClientesController

# user model
from django.contrib.auth.models import User

from utils.validators import validate_number_int, validate_number_decimal, validate_string

# conexion directa a la base de datos
from django.db import connection


class VentasController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Ventas'
        self.modelo_id = 'venta_id'
        self.modelo_app = 'ventas'
        self.modulo_id = settings.MOD_VENTAS

        # variables de session
        self.modulo_session = "ventas"
        self.columnas.append('fecha')
        self.columnas.append('apellidos')
        self.columnas.append('nombres')
        self.columnas.append('ci_nit')

        self.variables_filtros.append('search_fecha_ini')
        self.variables_filtros.append('search_fecha_fin')
        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_codigo')
        self.variables_filtros.append('search_ci_nit')

        fecha_actual = get_date_system()
        fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
        fecha_ini = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-1, formato='dd-MMM-yyyy')

        self.variables_filtros_defecto['search_fecha_ini'] = fecha_ini
        self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin
        self.variables_filtros_defecto['search_apellidos'] = ''
        self.variables_filtros_defecto['search_nombres'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''
        self.variables_filtros_defecto['search_ci_nit'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = 'DESC'

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = "txt|1|S|ci_nit|CI/NIT;"
        self.control_form += "txt|2|S|apellidos|Apellidos;"
        self.control_form += "txt|1|S|total|Total"

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
        self.filtros_modulo['status_id_id__in'] = [self.contado, self.consignacion, self.plan_pago, self.factura, self.anulado, self.preventa]
        # tipo movimiento
        self.filtros_modulo['tipo_venta__in'] = ['CONTADO', 'FACTURA', 'CONSIGNACION', 'PLANPAGO']

        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['venta_id'] = int(self.variables_filtros_values['search_codigo'].strip())
        else:
            # fechas
            if self.variables_filtros_values['search_fecha_ini'].strip() != '' and self.variables_filtros_values['search_fecha_fin'].strip() != '':
                self.filtros_modulo['fecha__gte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_ini'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
                self.filtros_modulo['fecha__lte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_fin'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

            # apellidos
            if self.variables_filtros_values['search_apellidos'].strip() != "":
                self.filtros_modulo['apellidos__icontains'] = self.variables_filtros_values['search_apellidos'].strip()
            # nombres
            if self.variables_filtros_values['search_nombres'].strip() != "":
                self.filtros_modulo['nombres__icontains'] = self.variables_filtros_values['search_nombres'].strip()
            # ci_nit
            if self.variables_filtros_values['search_ci_nit'].strip() != "":
                self.filtros_modulo['ci_nit'] = self.variables_filtros_values['search_ci_nit'].strip()

        #print('filtros: ', self.filtros_modulo)

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

    def save(self, request, type='add'):
        """aniadimos un nuevo registro"""

        producto_controller = ProductosController()
        cliente_controller = ClientesController()
        try:
            almacen1 = validate_number_int('almacen', request.POST['almacen'])
            tipo_venta = validate_string('tipo venta', request.POST['tipo_venta'], remove_specials='yes')
            caja_aux = validate_number_int('caja', request.POST['caja'])
            costo_abc = validate_string('costo abc', request.POST['costo_abc'], remove_specials='yes')
            concepto = 'ventas del dia'
            apellidos = validate_string('apellidos', request.POST['apellidos'], remove_specials='yes', len_zero='yes')
            nombres = validate_string('nombres', request.POST['nombres'], remove_specials='yes', len_zero='yes')
            ci_nit = validate_string('ci_nit', request.POST['ci_nit'], remove_specials='yes', len_zero='yes')
            telefonos = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes', len_zero='yes')
            direccion = validate_string('direccion', request.POST['direccion'], remove_specials='yes', len_zero='yes')
            observacion = validate_string('observacion', request.POST['observacion'], remove_specials='yes', len_zero='yes')
            lugar = validate_number_int('lugar', request.POST['lugar'])
            mesa = validate_string('mesa', request.POST['mesa'], remove_specials='yes', len_zero='yes')

            # caso de plan de pago
            numero_cuotas = validate_number_int('numero cuotas', request.POST['numero_cuotas'], len_zero='yes')
            tipo_pp = validate_string('tipo plan pago', request.POST['tipo_pp'], remove_specials='yes', len_zero='yes')
            fecha_fija_aux = validate_string('fecha fija', request.POST['fecha_fija'], remove_specials='yes')
            dias = validate_number_int('dias', request.POST['dias'], len_zero='yes')

            porcentaje_descuento = validate_number_decimal('porcentaje_descuento', request.POST['porcentaje_descuento'], len_zero='yes')
            descuento = validate_number_decimal('descuento', request.POST['descuento'], len_zero='yes')

            caja_id = Cajas.objects.get(pk=caja_aux)

            # cliente
            cliente_id = Clientes.objects.get(ci_nit=ci_nit)

            # lugar id
            lugar_id = Lugares.objects.get(pk=lugar)

            fecha_fija = get_date_to_db(fecha=fecha_fija_aux, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss')

            status_venta = self.status_contado
            if tipo_venta == 'CONSIGNACION':
                status_venta = self.status_consignacion
            if tipo_venta == 'PLANPAGO':
                status_venta = self.status_plan_pago
            if tipo_venta == 'FACTURA':
                status_venta = self.status_factura

            if almacen1 == 0:
                self.error_operation = 'Debe seleccionar el almacen para la venta'
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

            # verificamos si viene de un pedido o no
            pedido_id = request.POST['pedido_id'].strip()

            # punto
            usuario = request.user
            usuario_perfil = UsersPerfiles.objects.get(user_id=usuario)
            punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
            almacen = Almacenes.objects.get(pk=almacen1)

            # verificamos si es de preventa o no
            from_preventa = validate_string('de preventa', request.POST['from_preventa'], remove_specials='yes')
            from_preventa_id = validate_number_int('preventa id', request.POST['from_preventa_id'], len_zero='yes')

            datos = {}
            datos['tipo_operacion'] = request.POST['tipo_operacion']
            datos['m_venta_id'] = request.POST['m_venta_id']
            datos['from_preventa'] = from_preventa
            datos['from_preventa_id'] = from_preventa_id
            datos['pedido_id'] = pedido_id
            datos['apellidos'] = apellidos
            datos['nombres'] = nombres
            datos['ci_nit'] = ci_nit
            datos['telefonos'] = telefonos
            datos['direccion'] = direccion
            datos['observacion'] = observacion
            datos['mesa'] = mesa
            datos['tipo_venta'] = tipo_venta
            datos['costo_abc'] = costo_abc
            datos['fecha'] = 'now'
            datos['user_perfil_id_fecha'] = usuario_perfil.user_perfil_id
            datos['subtotal'] = 0
            datos['porcentaje_descuento'] = porcentaje_descuento
            datos['descuento'] = descuento
            datos['total'] = 0
            datos['saldo'] = 0
            datos['concepto'] = concepto
            datos['created_at'] = 'now'
            datos['updated_at'] = 'now'

            datos['almacen_id'] = almacen
            datos['caja_id'] = caja_id
            datos['cliente_id'] = cliente_id
            datos['lugar_id'] = lugar_id
            datos['punto_id'] = punto

            datos['status_id'] = status_venta
            datos['user_perfil_id'] = usuario_perfil

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

                # datos de productos
                s_id = str(i)
                aux_cant = 'cantidad_' + s_id
                aux_costo = 'costo_' + s_id

                if not aux_cant in request.POST.keys():
                    continue

                cantidad = request.POST[aux_cant].strip()
                costo = request.POST[aux_costo].strip()

                cant_valor = 0 if cantidad == '' else Decimal(cantidad)
                costo_valor = 0 if costo == '' else Decimal(costo)

                if cant_valor > 0 and costo_valor > 0:
                    # datos del producto
                    detalle_producto = producto_controller.datos_producto(int(aux))

                    dato_detalle = {}
                    dato_detalle['producto_id'] = Productos.objects.get(pk=int(aux))
                    dato_detalle['cantidad'] = cant_valor
                    dato_detalle['costo'] = costo_valor

                    # costo adicional, refrescos, papas, extras
                    costo_adicional = 0

                    # componentes
                    p_componentes = []
                    if detalle_producto['lista_componentes']:
                        for aux_detalle in detalle_producto['lista_componentes']:
                            nombre = 'componente_' + str(i) + '_' + str(aux_detalle['componente_id'])

                            dato_componente = {}
                            dato_componente['componente_id'] = aux_detalle['componente_id']
                            dato_componente['activo'] = int(request.POST[nombre])

                            p_componentes.append(dato_componente)
                    # asignamos
                    dato_detalle['lista_componentes'] = p_componentes

                    # refrescos
                    p_refrescos = []
                    if detalle_producto['lista_refrescos']:
                        for aux_refresco in detalle_producto['lista_refrescos']:
                            nombre = 'refresco_' + str(i) + '_' + str(aux_refresco['refresco_grupo_id'])

                            dato_refresco = {}
                            dato_refresco['refresco_grupo_id'] = aux_refresco['refresco_grupo_id']
                            dato_refresco['activo'] = int(request.POST[nombre])
                            if int(request.POST[nombre]) == 1:
                                costo_adicional += aux_refresco['precio']

                            dato_refresco['precio'] = aux_refresco['precio']

                            p_refrescos.append(dato_refresco)
                    # asignamos
                    dato_detalle['lista_refrescos'] = p_refrescos

                    # papas
                    p_papas = []
                    if detalle_producto['lista_papas']:
                        for aux_papa in detalle_producto['lista_papas']:
                            nombre = 'papa_' + str(i) + '_' + str(aux_papa['papa_grupo_id'])

                            dato_papa = {}
                            dato_papa['papa_grupo_id'] = aux_papa['papa_grupo_id']
                            dato_papa['activo'] = int(request.POST[nombre])
                            if int(request.POST[nombre]) == 1:
                                costo_adicional += aux_papa['precio']

                            dato_papa['precio'] = aux_papa['precio']

                            p_papas.append(dato_papa)
                    # asignamos
                    dato_detalle['lista_papas'] = p_papas

                    # extras
                    p_extras = []
                    if detalle_producto['lista_extras']:
                        for aux_extra in detalle_producto['lista_extras']:
                            nombre = 'extra_' + str(i) + '_' + str(aux_extra['componente_id'])

                            dato_extra = {}
                            dato_extra['extra_id'] = aux_extra['componente_id']
                            dato_extra['activo'] = int(request.POST[nombre])
                            if int(request.POST[nombre]) == 1:
                                costo_adicional += aux_extra['precio']

                            dato_extra['precio'] = aux_extra['precio']

                            p_extras.append(dato_extra)
                    # asignamos
                    dato_detalle['lista_extras'] = p_extras

                    #dato_detalle['total'] = (cant_valor * costo_valor) + costo_adicional
                    # costo adicional ya sumado en el costo por JS
                    dato_detalle['total'] = cant_valor * costo_valor

                    detalles.append(dato_detalle)

            # detalles
            #print('detalles: ', detalles)

            datos['detalles'] = detalles
            # verificando que haya detalles
            if len(detalles) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            if self.save_db(type, **datos):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar la venta, " + str(ex)
            return False

    def save_db(self, type='add', **datos):
        """aniadimos a la base de datos"""
        try:
            if len(datos['detalles']) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            stock_controller = StockController()

            with transaction.atomic():
                campos_add = {}
                campos_add['apellidos'] = datos['apellidos']
                campos_add['nombres'] = datos['nombres']
                campos_add['ci_nit'] = datos['ci_nit']
                campos_add['telefonos'] = datos['telefonos']
                campos_add['direccion'] = datos['direccion']
                campos_add['mesa'] = datos['mesa']
                campos_add['observacion'] = datos['observacion']

                campos_add['tipo_venta'] = datos['tipo_venta']
                campos_add['costo_abc'] = datos['costo_abc']
                campos_add['fecha'] = datos['fecha']
                campos_add['user_perfil_id_fecha'] = datos['user_perfil_id_fecha']
                campos_add['subtotal'] = datos['subtotal']
                campos_add['descuento'] = datos['descuento']
                campos_add['porcentaje_descuento'] = datos['porcentaje_descuento']
                campos_add['total'] = datos['total']
                campos_add['saldo'] = datos['saldo']
                campos_add['concepto'] = datos['concepto']
                campos_add['created_at'] = datos['created_at']
                campos_add['updated_at'] = datos['updated_at']

                campos_add['almacen_id'] = datos['almacen_id']
                campos_add['caja_id'] = datos['caja_id']
                campos_add['cliente_id'] = datos['cliente_id']
                campos_add['lugar_id'] = datos['lugar_id']
                campos_add['punto_id'] = datos['punto_id']

                campos_add['status_id'] = datos['status_id']
                campos_add['user_perfil_id'] = datos['user_perfil_id']

                # venta
                if datos['tipo_operacion'] == 'add' or datos['tipo_operacion'] == 'internet':
                    venta_add = Ventas.objects.create(**campos_add)
                    venta_add.save()

                elif datos['tipo_operacion'] == 'modify':
                    venta_ant = Ventas.objects.get(pk=int(datos['m_venta_id']))

                    # leemos detalles
                    ventas_detalles = VentasDetalles.objects.filter(venta_id=venta_ant)

                    # devolvemos stock
                    for ven_det in ventas_detalles:
                        producto_insumos = ProductosInsumos.objects.filter(producto_id=ven_det.producto_id)
                        for pr_insumo in producto_insumos:
                            # devolvemos el stock
                            stock_up = stock_controller.update_stock(user_perfil=venta_ant.user_perfil_id, almacen=venta_ant.almacen_id, producto=pr_insumo.insumo_id, cantidad=(ven_det.cantidad * pr_insumo.cantidad))
                            if not stock_up:
                                self.error_operation = 'Error al actualizar stock almacen'
                                return False

                    # detalles insumos
                    for ven_det in ventas_detalles:
                        ventas_detalles_insumos = VentasDetallesInsumos.objects.filter(venta_detalle_id=ven_det)
                        ventas_detalles_componentes = VentasDetallesComponentes.objects.filter(venta_detalle_id=ven_det)
                        ventas_detalles_extras = VentasDetallesExtras.objects.filter(venta_detalle_id=ven_det)
                        ventas_detalles_refrescos = VentasDetallesRefrescos.objects.filter(venta_detalle_id=ven_det)
                        ventas_detalles_papas = VentasDetallesPapas.objects.filter(venta_detalle_id=ven_det)

                        if ventas_detalles_insumos:
                            ventas_detalles_insumos.delete()

                        if ventas_detalles_componentes:
                            ventas_detalles_componentes.delete()

                        if ventas_detalles_extras:
                            ventas_detalles_extras.delete()

                        if ventas_detalles_refrescos:
                            ventas_detalles_refrescos.delete()

                        if ventas_detalles_papas:
                            ventas_detalles_papas.delete()

                    # borramos los detalles
                    if ventas_detalles:
                        ventas_detalles.delete()

                    # tipo de pago
                    if venta_ant.tipo_venta == 'CONTADO' or venta_ant.tipo_venta == 'FACTURA':
                        # eliminamos el registro de caja
                        caja_ingreso = CajasIngresos.objects.filter(venta_id=venta_ant.venta_id)
                        if caja_ingreso:
                            caja_ingreso.delete()

                    if venta_ant.tipo_venta == 'PLANPAGO':
                        plan_pago = PlanPagos.objects.filter(venta_id=venta_ant.venta_id)
                        for p_pago in plan_pago:
                            plan_pago_detalles = PlanPagosDetalles.objects.filter(plan_pago_id=p_pago)

                            if plan_pago_detalles:
                                plan_pago_detalles.delete()

                        if plan_pago:
                            plan_pago.delete()

                    # actualizmos la venta
                    venta_update = Ventas.objects.filter(pk=int(datos['m_venta_id']))
                    venta_update.update(**campos_add)

                    venta_add = Ventas.objects.get(pk=int(datos['m_venta_id']))

                else:
                    self.error_operation = 'OPERACION NO PERMITIDA'
                    return False

                # detalles
                suma_subtotal = 0
                suma_descuento = 0
                suma_total = 0

                for detalle in datos['detalles']:
                    suma_subtotal += detalle['total']
                    suma_total += detalle['total']
                    detalle_add = VentasDetalles.objects.create(venta_id=venta_add, punto_id=datos['punto_id'], descuento=0, porcentaje_descuento=0, producto_id=detalle['producto_id'], cantidad=detalle['cantidad'], costo=detalle[
                        'costo'], total=detalle['total'])
                    detalle_add.save()

                    # componentes
                    for componente_lista in detalle['lista_componentes']:
                        cantidad = componente_lista['activo']
                        componente = Componentes.objects.get(pk=int(componente_lista['componente_id']))
                        detalle_componente = VentasDetallesComponentes.objects.create(venta_detalle_id=detalle_add, punto_id=datos['punto_id'], producto_id=detalle['producto_id'], componente_id=componente,
                                                                                      cantidad=cantidad, costo=0, descuento=0, porcentaje_descuento=0, total=0)
                        detalle_componente.save()

                    # extras
                    for extra_lista in detalle['lista_extras']:
                        if extra_lista['activo'] == 1:
                            costo = extra_lista['precio']
                            componente = Componentes.objects.get(pk=int(extra_lista['extra_id']))
                            detalle_extra = VentasDetallesExtras.objects.create(venta_detalle_id=detalle_add, punto_id=datos['punto_id'], producto_id=detalle['producto_id'], componente_id=componente,
                                                                                cantidad=1, costo=costo, porcentaje_descuento=0, descuento=0, total=costo)
                            detalle_extra.save()

                    # refrescos
                    for refresco_lista in detalle['lista_refrescos']:
                        if refresco_lista['activo'] == 1:
                            #producto_refresco = ProductosRefrescos.objects.get(pk=refresco_lista['producto_refresco_id'])
                            producto_refresco = RefrescosGrupo.objects.get(pk=refresco_lista['refresco_grupo_id'])
                            costo = refresco_lista['precio']

                            detalle_refresco = VentasDetallesRefrescos.objects.create(venta_detalle_id=detalle_add, punto_id=datos['punto_id'], producto_id=detalle['producto_id'],
                                                                                      componente_id=producto_refresco.componente_id, insumo_id=producto_refresco.insumo_id, cantidad=1, costo=costo, porcentaje_descuento=0, descuento=0, total=costo)
                            detalle_refresco.save()

                    # papas
                    for papa_lista in detalle['lista_papas']:
                        if papa_lista['activo'] == 1:
                            #producto_papa = ProductosPapas.objects.get(pk=papa_lista['producto_papa_id'])
                            producto_papa = PapasGrupo.objects.get(pk=papa_lista['papa_grupo_id'])
                            costo = papa_lista['precio']

                            detalle_papa = VentasDetallesPapas.objects.create(venta_detalle_id=detalle_add, punto_id=datos['punto_id'], producto_id=detalle['producto_id'],
                                                                              componente_id=producto_papa.componente_id, insumo_id=producto_papa.insumo_id, cantidad=1, costo=costo, porcentaje_descuento=0, descuento=0, total=costo)
                            detalle_papa.save()

                    # actualizamos el stock, salida del almacen 1
                    if datos['tipo_operacion'] in ['add', 'modify']:
                        producto_insumos = ProductosInsumos.objects.filter(producto_id=detalle['producto_id'])
                        for pr_insumo in producto_insumos:
                            detalle_insumo = VentasDetallesInsumos.objects.create(venta_detalle_id=detalle_add, punto_id=datos['punto_id'], producto_id=detalle['producto_id'], insumo_id=pr_insumo.insumo_id,
                                                                                  cantidad=pr_insumo.cantidad, costo=pr_insumo.insumo_id.precio, descuento=0, porcentaje_descuento=0, total=(pr_insumo.cantidad * pr_insumo.insumo_id.precio))
                            detalle_insumo.save()

                            stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'],
                                                                     producto=pr_insumo.insumo_id, cantidad=(0-(detalle['cantidad'] * pr_insumo.cantidad)))
                            if not stock_up:
                                self.error_operation = 'Error al actualizar stock almacen'
                                return False

                # actualizamos datos
                venta_add.numero_venta = venta_add.venta_id
                venta_add.subtotal = suma_subtotal

                #venta_add.descuento = suma_descuento
                venta_add.porcentaje_descuento = datos['porcentaje_descuento']
                venta_add.descuento = datos['descuento']

                #venta_add.total = suma_total
                venta_add.total = suma_subtotal - datos['descuento']

                venta_add.save()

                # solo registramos ingreso de caja de ventas al contado y factura
                if venta_add.tipo_venta == 'CONTADO' or venta_add.tipo_venta == 'FACTURA':
                    if datos['tipo_operacion'] in ['add', 'modify']:
                        ci_controller = CajasIngresosController()

                        campos_ingreso = {}
                        campos_ingreso['caja_id'] = datos['caja_id']
                        campos_ingreso['punto_id'] = datos['punto_id']
                        campos_ingreso['user_perfil_id'] = datos['user_perfil_id']
                        campos_ingreso['status_id'] = self.status_activo
                        campos_ingreso['fecha'] = datos['fecha']
                        campos_ingreso['concepto'] = 'ingreso de efectivo, venta: ' + str(venta_add.venta_id)
                        campos_ingreso['monto'] = venta_add.total
                        campos_ingreso['created_at'] = datos['created_at']
                        campos_ingreso['updated_at'] = datos['updated_at']
                        campos_ingreso['venta_id'] = venta_add.venta_id
                        # registramos
                        ci_controller.add_db(**campos_ingreso)

                # plan de pagos si es el caso
                if venta_add.tipo_venta == 'PLANPAGO':
                    campos_pp = {}
                    campos_pp['registro_id'] = 0
                    campos_pp['venta_id'] = venta_add.venta_id
                    campos_pp['cliente_id'] = venta_add.cliente_id.cliente_id
                    campos_pp['punto_id'] = venta_add.punto_id.punto_id
                    campos_pp['fecha'] = datos['fecha']
                    campos_pp['concepto'] = venta_add.concepto
                    campos_pp['numero_cuotas'] = int(datos['numero_cuotas'])
                    campos_pp['monto_total'] = venta_add.total
                    campos_pp['cuota_inicial'] = 0
                    campos_pp['saldo'] = venta_add.total
                    campos_pp['mensual_dias'] = datos['tipo_pp']

                    campos_pp['fecha_fija'] = datos['fecha_fija']
                    campos_pp['dias'] = datos['dias']

                    if datos['tipo_pp'] == 'tipo_fecha':
                        campos_pp['dia_mensual'] = int(get_day_from_date(datos['fecha_fija'], formato_ori='yyyy-mm-dd HH:ii:ss'))
                        campos_pp['tiempo_dias'] = 0
                    else:
                        campos_pp['dia_mensual'] = 0
                        campos_pp['tiempo_dias'] = int(datos['dias'])

                    campos_pp['status_id'] = self.status_activo
                    campos_pp['user_perfil_id'] = datos['user_perfil_id']
                    campos_pp['created_at'] = datos['created_at']
                    campos_pp['updated_at'] = datos['updated_at']

                    plan_pago_controller = PlanPagosController()
                    if not plan_pago_controller.add_plan_pago_db(**campos_pp):
                        self.error_operation = 'Error al agregar el plan de pagos'
                        return False

                if int(datos['pedido_id']) != 0:
                    # marcamos el pedido
                    pedido = apps.get_model('pedidos', 'Pedidos').objects.get(pk=int(datos['pedido_id']))
                    pedido.venta_id = venta_add.venta_id
                    pedido.cliente_id = venta_add.cliente_id.cliente_id
                    pedido.updated_at = datos['updated_at']
                    pedido.status_id = venta_add.status_id
                    pedido.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add venta db, '+str(ex))
            return False

    def can_anular(self, id, user):
        """verificando si se puede eliminar o no la tabla"""
        # puede anular el usuario con permiso de la sucursal
        usuario_perfil = UsersPerfiles.objects.get(user_id=user)
        punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
        permisos = get_permissions_user(user, settings.MOD_VENTAS)

        # registro
        venta = Ventas.objects.get(pk=id)
        if venta.status_id.status_id == self.anulado:
            self.error_operation = 'el registro ya esta anulado'
            return False

        # registro de la misma sucursal
        if venta.punto_id.sucursal_id == punto.sucursal_id:
            # verificamos si es plan de pagos, y no pago ninguna cuota
            if venta.tipo_venta == 'PLANPAGO':
                plan_pago = apps.get_model('inventarios', 'PlanPagos').objects.get(venta_id=venta.venta_id)
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
                usuario_perfil = UsersPerfiles.objects.get(user_id=request.user)
                status_anular = self.status_anulado
                motivo_a = validate_string('motivo anulacion', request.POST['motivo_anula'], remove_specials='yes')

                campos_update = {}
                # para actualizar el stock
                campos_update['user_perfil_id'] = usuario_perfil
                campos_update['user_perfil_id_anula'] = usuario_perfil.user_perfil_id
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
            self.error_operation = 'Error al anular la venta db, ' + str(ex)
            return False

    def anular_db(self, id, **datos):
        """ anulamos en la bd """
        try:
            stock_controller = StockController()
            ci_controller = CajasIngresosController()

            with transaction.atomic():
                venta_aux = Ventas.objects.get(pk=id)
                estado_ini = venta_aux.status_id

                campos_update = {}
                campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                campos_update['motivo_anula'] = datos['motivo_anula']
                campos_update['status_id'] = datos['status_id']
                campos_update['deleted_at'] = datos['deleted_at']

                # registramos
                venta_update = Ventas.objects.filter(pk=id)
                venta_update.update(**campos_update)

                # actualizamos los detalles
                venta = Ventas.objects.get(pk=id)
                ventas_detalles = VentasDetalles.objects.filter(venta_id=venta)

                # devolvemos stock, solo en caso que no sea pedido
                print('de venta: ', estado_ini, ' clase: ', self.status_preventa)
                if estado_ini != self.status_preventa:
                    for ven_det in ventas_detalles:
                        producto_insumos = ProductosInsumos.objects.filter(producto_id=ven_det.producto_id)
                        for pr_insumo in producto_insumos:
                            # devolvemos el stock
                            stock_up = stock_controller.update_stock(user_perfil=venta.user_perfil_id, almacen=venta.almacen_id, producto=pr_insumo.insumo_id, cantidad=(ven_det.cantidad * pr_insumo.cantidad))
                            if not stock_up:
                                self.error_operation = 'Error al actualizar stock almacen'
                                return False

                # verificamos si tiene plan de pagos
                if venta.tipo_venta == 'PLANPAGO':
                    plan_pago_controller = PlanPagosController()
                    if not plan_pago_controller.anular_db(venta_id=venta.venta_id, **campos_update):
                        self.error_operation = 'Error al anular el plan de pagos'
                        return False

                    # plan_pago = PlanPagos.objects.get(venta_id=venta.venta_id)
                    # plan_pago.user_id_anula = datos['user_id_anula']
                    # plan_pago.motivo_anula = datos['motivo_anula']
                    # plan_pago.status_id = datos['status_id']
                    # plan_pago.deleted_at = datos['deleted_at']
                    # plan_pago.save()

                # anulamos el registro de caja en caso contado y factura
                if estado_ini != self.status_preventa and (venta.tipo_venta == 'CONTADO' or venta.tipo_venta == 'FACTURA'):
                    caja_ingreso = CajasIngresos.objects.get(venta_id=venta.venta_id, status_id=self.status_activo)

                    if not ci_controller.delete_db(caja_ingreso.caja_ingreso_id, **campos_update):
                        self.error_operation = 'Error al anular el ingreso a caja'
                        return False

                # verificamos si proviene de alguna preventa
                # verificamos si es de una preventa
                lista_models = apps.get_models()
                existe = 'no'
                for model in lista_models:
                    # print('modelo: ', model.__name__)
                    if model.__name__ == 'PreVentas':
                        existe = 'si'

                if existe == 'si':
                    # status_preventa_venta = Status.objects.get(pk=self.preventa_venta)
                    # status_preventa = Status.objects.get(pk=self.preventa)
                    preventa_filtro = apps.get_model('preventas', 'PreVentas').objects.filter(status_id=self.status_preventa_venta, venta_id=venta.venta_id)
                    if preventa_filtro:
                        #preventa = PreVentas.objects.get(status_id=status_preventa_venta, venta_id=venta.venta_id)
                        preventa = preventa_filtro.first()
                        if preventa:
                            preventa.venta_id = 0
                            preventa.status_id = self.status_preventa
                            preventa.updated_at = 'now'
                            preventa.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            print('Error anular venta db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return

    def get_venta(self, venta_id, punto_id, fecha):
        """devolvemos los datos de la venta"""
        datos = {}
        datos['venta_id'] = venta_id
        datos['next_id'] = 0
        datos['previous_id'] = 0

        producto_controller = ProductosController()

        # si manda id 0
        if venta_id == 0:
            return datos

        # recuperamos datos de la venta
        try:
            venta = Ventas.objects.select_related('user_perfil_id').select_related('punto_id').get(pk=venta_id)

            datos['venta_id'] = venta.venta_id
            datos['almacen_id'] = venta.almacen_id.almacen_id
            datos['cliente_id'] = venta.cliente_id.cliente_id
            datos['lugar_id'] = venta.lugar_id.lugar_id
            datos['next_id'] = self.get_next_id(venta.venta_id, punto_id, fecha)
            datos['previous_id'] = self.get_previous_id(venta.venta_id, punto_id, fecha)
            datos['apellidos'] = venta.apellidos
            datos['nombres'] = venta.nombres
            datos['ci_nit'] = venta.ci_nit
            datos['telefonos'] = venta.telefonos
            datos['direccion'] = venta.direccion
            datos['mesa'] = venta.mesa
            datos['observacion'] = venta.observacion
            datos['tipo_venta'] = venta.tipo_venta
            datos['numero_venta'] = venta.numero_venta
            datos['costo_abc'] = venta.costo_abc
            datos['fecha'] = venta.fecha
            datos['subtotal'] = venta.subtotal
            datos['descuento'] = venta.descuento
            datos['porcentaje_descuento'] = venta.porcentaje_descuento
            datos['total'] = venta.total
            datos['status_id'] = venta.status_id
            datos['user'] = venta.user_perfil_id.user_id.username
            datos['punto'] = venta.punto_id.punto
            datos['user_perfil_id_anula'] = venta.user_perfil_id_anula
            datos['user_anula'] = ''

            # plan de pagos
            if venta.tipo_venta == 'PLANPAGO':
                plan_pago = PlanPagos.objects.get(venta_id=venta.venta_id)
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
            if not venta.user_perfil_id_anula is None and venta.user_perfil_id_anula != 0:
                user_anula = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=venta.user_perfil_id_anula)
                datos['user_anula'] = user_anula.user_id.username

            # detalles de la venta
            ventas_detalles = VentasDetalles.objects.select_related('producto_id').select_related('producto_id__linea_id').filter(venta_id=venta).order_by('venta_detalle_id', 'producto_id__producto')
            detalles = []
            for venta_detalle in ventas_detalles:
                dato_detalle = {}
                dato_detalle['producto_id'] = venta_detalle.producto_id.producto_id
                dato_detalle['producto'] = venta_detalle.producto_id.producto
                dato_detalle['cantidad'] = venta_detalle.cantidad
                dato_detalle['costo'] = venta_detalle.costo
                dato_detalle['total'] = venta_detalle.total

                # componentes
                detalles_componentes = VentasDetallesComponentes.objects.filter(venta_detalle_id=venta_detalle)
                componentes_ids = ''
                for dc in detalles_componentes:
                    componentes_ids += str(dc.componente_id.componente_id) + '|'
                if len(componentes_ids) > 0:
                    componentes_ids = componentes_ids[0:len(componentes_ids)-1]

                # extras
                detalles_extras = VentasDetallesExtras.objects.filter(venta_detalle_id=venta_detalle)
                extras_ids = ''
                for de in detalles_extras:
                    extras_ids += str(de.componente_id.componente_id) + '|'
                if len(extras_ids) > 0:
                    extras_ids = extras_ids[0:len(extras_ids)-1]

                # refrescos
                lista_refrescos = producto_controller.lista_refrescos()
                detalles_refrescos = VentasDetallesRefrescos.objects.filter(venta_detalle_id=venta_detalle)
                retorno_refresco = []
                for li_re in lista_refrescos:
                    dato_r = {}
                    dato_r['insumo_id'] = li_re['insumo_id']
                    dato_r['componente_id'] = li_re['componente_id']
                    dato_r['insumo'] = li_re['insumo']
                    dato_r['componente'] = li_re['componente']
                    dato_r['refresco_grupo_id'] = li_re['refresco_grupo_id']

                    cantidad = 0
                    for det_re in detalles_refrescos:
                        if li_re['insumo_id'] == det_re.insumo_id and li_re['componente_id'] == det_re.componente_id:
                            cantidad = int(det_re.cantidad)

                    dato_r['cantidad'] = cantidad
                    retorno_refresco.append(dato_r)

                #print('retorno refresco: ', retorno_refresco)

                refrescos_ids = ''
                for dr in lista_refrescos:
                    refrescos_ids += str(dr['refresco_grupo_id']) + '|'
                if len(refrescos_ids) > 0:
                    refrescos_ids = refrescos_ids[0:len(refrescos_ids)-1]

                # papas
                lista_papas = producto_controller.lista_papas()
                detalles_papas = VentasDetallesPapas.objects.filter(venta_detalle_id=venta_detalle)
                retorno_papa = []
                for li_pa in lista_papas:
                    dato_p = {}
                    dato_p['insumo_id'] = li_pa['insumo_id']
                    dato_p['componente_id'] = li_pa['componente_id']
                    dato_p['insumo'] = li_pa['insumo']
                    dato_p['componente'] = li_pa['componente']
                    dato_p['papa_grupo_id'] = li_pa['papa_grupo_id']

                    cantidad = 0
                    for det_pa in detalles_papas:
                        if li_pa['insumo_id'] == det_pa.insumo_id and li_pa['componente_id'] == det_pa.componente_id:
                            cantidad = int(det_pa.cantidad)

                    dato_p['cantidad'] = cantidad
                    retorno_papa.append(dato_p)

                papas_ids = ''
                for dp in lista_papas:
                    papas_ids += str(dp['papa_grupo_id']) + '|'
                if len(papas_ids) > 0:
                    papas_ids = papas_ids[0:len(papas_ids)-1]

                dato_detalle['lista_componentes'] = detalles_componentes
                dato_detalle['lista_extras'] = detalles_extras
                dato_detalle['lista_refrescos'] = retorno_refresco
                dato_detalle['lista_papas'] = retorno_papa

                dato_detalle['componentes_ids'] = componentes_ids
                dato_detalle['extras_ids'] = extras_ids
                dato_detalle['refrescos_ids'] = refrescos_ids
                dato_detalle['papas_ids'] = papas_ids

                detalles.append(dato_detalle)

            # adiciminamos los datos del detalle
            datos['detalles'] = detalles

            return datos

        except Exception as ex:
            print('error al recuperar datos de venta_id: ' + str(venta_id) + ', ' + str(ex))
            datos['venta_id'] = -1
            return datos

    def get_last_id(self, punto_id, fecha):
        """ultimo id de venta para la fecha"""
        last_id = 0
        fecha_ini = fecha + ' 00:00:00'
        fecha_fin = fecha + ' 23:59:59'
        sql = f"SELECT MAX(venta_id) AS maximo FROM ventas WHERE punto_id='{punto_id}' AND fecha>='{fecha_ini}' AND fecha<='{fecha_fin}' "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                last_id = 0 if row[0] is None else row[0]

        return last_id

    def get_next_id(self, id, punto_id, fecha):
        """next id de venta """
        next_id = 0
        fecha_ini = fecha + ' 00:00:00'
        fecha_fin = fecha + ' 23:59:59'
        sql = f"SELECT MIN(venta_id) AS maximo FROM ventas WHERE punto_id='{punto_id}' AND fecha>='{fecha_ini}' AND fecha<='{fecha_fin}' AND venta_id>'{id}' "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                if row[0]:
                    next_id = row[0]

        return next_id

    def get_previous_id(self, id, punto_id, fecha):
        """next id de venta """
        previous_id = 0
        fecha_ini = fecha + ' 00:00:00'
        fecha_fin = fecha + ' 23:59:59'
        sql = f"SELECT MAX(venta_id) AS maximo FROM ventas WHERE punto_id='{punto_id}' AND fecha>='{fecha_ini}' AND fecha<='{fecha_fin}' AND venta_id<'{id}' "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                if row[0]:
                    previous_id = row[0]

        return previous_id

    def get_preventas(self, punto_id, fecha=''):
        """get preventas for day"""
        punto = Puntos.objects.get(pk=punto_id)
        status_preventa = self.status_preventa

        filtros = {}
        filtros['punto_id'] = punto
        filtros['status_id'] = status_preventa
        filtros['registro_id__gt'] = 0
        if fecha != '':
            filtros['fecha__gte'] = get_date_to_db(fecha=fecha, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd')+' 00:00:00'
            filtros['fecha__lte'] = get_date_to_db(fecha=fecha, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd')+' 23:59:59'

        lista_models = apps.get_models()
        existe = 'no'
        for model in lista_models:
            # print('modelo: ', model.__name__)
            if model.__name__ == 'PreVentas':
                existe = 'si'

        if existe == 'si':
            preventas = apps.get_model('preventas', 'PreVentas').objects.select_related('almacen_id').filter(**filtros).order_by('numero_preventa')
        else:
            preventas = {}

        return preventas
