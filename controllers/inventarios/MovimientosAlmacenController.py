from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from inventarios.models import Registros, RegistrosDetalles
# from preventas.models import PreVentas
from productos.models import Insumos
from permisos.models import UsersPerfiles
from configuraciones.models import Puntos, Almacenes

from django.db import transaction

from decimal import Decimal

# fechas
from utils.dates_functions import get_date_show, get_date_to_db, get_date_system, add_days_datetime, get_seconds_date1_sub_date2
from utils.permissions import get_permissions_user

from controllers.inventarios.StockController import StockController
from utils.validators import validate_string, validate_number_int


class MovimientosAlmacenController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Registros'
        self.modelo_id = 'registro_id'
        self.modelo_app = 'inventarios'
        self.modulo_id = settings.MOD_MOVIMIENTOS_ALMACEN

        # variables de session
        self.modulo_session = "movimientos_almacen"
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
        self.variable_order_type_value = "DESC"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = "cbo|0|S|almacen|Almacen;"
        self.control_form += "cbo|0|S|almacen2|Almacen2;"
        self.control_form += "txt|2|S|concepto|Concepto"

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
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.anulado]
        # tipo movimiento
        self.filtros_modulo['tipo_movimiento'] = 'MOVIMIENTO'
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
                self.filtros_modulo['almacen_id'] = int(self.variables_filtros_values['search_almacen'].strip())
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

    def permission_operation(self, user_perfil, almacen):
        """add ingreso almacen"""
        try:
            if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                punto_user = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
                if almacen.sucursal_id == punto_user.sucursal_id:
                    return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                punto_user = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
                puntos_almacenes = apps.get_model('configuraciones', 'PuntosAlmacenes').objects.filter(punto_id=punto_user)
                for punto_almacen in puntos_almacenes:
                    if almacen == punto_almacen.almacen_id:
                        return True

            return False

        except Exception as ex:
            print('Error in permission add, ', str(ex))
            return False

    def permission_registro(self, user_perfil, registro):
        """add ingreso almacen"""
        try:
            if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                if user_perfil.punto_id.sucursal_id == registro.punto_id.sucursal_id:
                    return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                if user_perfil.punto_id == registro.punto_id:
                    return True

            return False

        except Exception as ex:
            print('Error in permission add, ', str(ex))
            return False

    def save(self, request, type='add'):
        """aniadimos un nuevo registro"""
        try:
            # activo
            status_registro = self.status_activo
            almacen1 = validate_number_int('almacen', request.POST['almacen'])
            almacen2 = validate_number_int('almacen2', request.POST['almacen2'])
            concepto = validate_string('concepto', request.POST['concepto'], remove_specials='yes')

            if almacen1 == '0':
                self.error_operation = 'Debe seleccionar el almacen de origen'
                return False

            if almacen2 == '0':
                self.error_operation = 'Debe seleccionar el almacen de destino'
                return False

            if almacen1 == almacen2:
                self.error_operation = 'Debe seleccionar un almacen diferente de destino'
                return False

            # punto
            usuario = request.user
            usuario_perfil = UsersPerfiles.objects.get(user_id=usuario)
            punto = Puntos.objects.get(pk=usuario_perfil.punto_id)

            almacen_origen = Almacenes.objects.get(pk=int(almacen1))
            if not self.permission_operation(usuario_perfil, almacen_origen):
                self.error_operation = 'solo puede realizar ingresos a su almacen'
                return False

            datos = {}
            datos['almacen_id'] = almacen_origen
            datos['almacen2_id'] = almacen2
            datos['punto_id'] = punto
            datos['status_id'] = status_registro
            datos['user_perfil_id'] = usuario_perfil
            datos['concepto'] = concepto
            datos['tipo_movimiento'] = 'MOVIMIENTO'
            datos['costo_abc'] = ''
            datos['fecha'] = 'now'
            datos['created_at'] = 'now'
            datos['updated_at'] = 'now'
            datos['user_perfil_id_fecha'] = usuario_perfil.user_perfil_id

            # detalles del registro
            detalles = []
            for i in range(1, 51):
                aux = request.POST['producto_' + str(i)].strip()
                tb2 = request.POST['tb2_' + str(i)].strip()

                #print('aux:', aux)
                #print('tb2:', tb2)
                if aux != '0':
                    # vemos los ids del stock
                    stock_ids = request.POST['stock_ids_'+aux].strip()
                    division = stock_ids.split(',')

                    if stock_ids != '':
                        for s_id in division:
                            aux_cant = 'cantidad_' + s_id
                            aux_actual = 'actual_' + s_id
                            aux_f_elab = 'f_elab_' + s_id
                            aux_f_venc = 'f_venc_' + s_id
                            aux_lote = 'lote_' + s_id

                            cantidad = request.POST[aux_cant].strip()
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
                            actual_valor = 0 if actual == '' else Decimal(actual)

                            if cant_valor > 0 and cant_valor <= actual_valor:
                                # registramos la salida
                                dato_detalle = {}
                                dato_detalle['producto_id'] = Insumos.objects.get(pk=int(aux))
                                dato_detalle['cantidad'] = cant_valor
                                dato_detalle['costo'] = 0
                                dato_detalle['total'] = 0
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

            if self.save_db(type, **datos):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el registro, " + str(ex)
            return False

    def save_db(self, type='add', **datos):
        """aniadimos a la base de datos"""
        # transacion_list=[]

        try:
            if len(datos['detalles']) == 0:
                self.error_operation = 'debe registrar al menos un producto'
                return False

            if not self.permission_operation(datos['user_perfil_id'], datos['almacen_id']):
                self.error_operation = 'solo puede realizar ingresos a su almacen'
                return False

            stock_controller = StockController()

            with transaction.atomic():
                campos_add = {}
                campos_add['almacen_id'] = datos['almacen_id']
                campos_add['almacen2_id'] = datos['almacen2_id']
                campos_add['punto_id'] = datos['punto_id']
                campos_add['status_id'] = datos['status_id']
                campos_add['user_perfil_id'] = datos['user_perfil_id']
                campos_add['concepto'] = datos['concepto']
                campos_add['tipo_movimiento'] = datos['tipo_movimiento']
                campos_add['costo_abc'] = datos['costo_abc']
                campos_add['fecha'] = datos['fecha']
                campos_add['created_at'] = datos['created_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['user_perfil_id_fecha'] = datos['user_perfil_id_fecha']

                # registro
                registro_add = Registros.objects.create(**campos_add)
                registro_add.save()

                # transaction_model={}
                # transaction_model['app']= 'inventarios'
                # transaction_model['model']= 'Registros'
                # transaction_model['id']= registro_add.registro_id
                # transacion_list.append(transaction_model)

                # detalles
                suma_subtotal = 0
                suma_descuento = 0
                suma_total = 0
                almacen2_object = Almacenes.objects.get(pk=datos['almacen2_id'])
                for detalle in datos['detalles']:
                    suma_subtotal += detalle['total']
                    suma_total += detalle['total']
                    detalle_add = RegistrosDetalles.objects.create(registro_id=registro_add, punto_id=datos['punto_id'], descuento=0, porcentaje_descuento=0, insumo_id=detalle['producto_id'], cantidad=detalle['cantidad'], costo=detalle[
                                                                   'costo'], total=detalle['total'], fecha_elaboracion=detalle['fecha_elaboracion'], fecha_vencimiento=detalle['fecha_vencimiento'], lote=detalle['lote'])
                    detalle_add.save()

                    # transaction_model={}
                    # transaction_model['app']= 'inventarios'
                    # transaction_model['model']= 'RegistrosDetalles'
                    # transaction_model['id']= detalle_add.registro_detalle_id
                    # transacion_list.append(transaction_model)

                    # actualizamos el stock, salida del almacen 1
                    stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=datos['almacen_id'], producto=detalle['producto_id'], cantidad=(0-detalle['cantidad']),
                                                             fecha_elaboracion=detalle['fecha_elaboracion'], fecha_vencimiento=detalle['fecha_vencimiento'], lote=detalle['lote'])
                    if not stock_up:
                        self.error_operation = 'Error al actualizar stock almacen 1'
                        return False

                    # actualizamos el stock, ingreso al almacen 2
                    stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=almacen2_object, producto=detalle['producto_id'], cantidad=detalle['cantidad'],
                                                             fecha_elaboracion=detalle['fecha_elaboracion'], fecha_vencimiento=detalle['fecha_vencimiento'], lote=detalle['lote'])
                    if not stock_up:
                        self.error_operation = 'Error al actualizar stock almacen 2'
                        return False

                # actualizamos datos
                registro_add.numero_registro = registro_add.registro_id
                registro_add.subtotal = suma_subtotal
                registro_add.descuento = suma_descuento
                registro_add.total = suma_total
                registro_add.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add ingreso, '+str(ex))
            return False

    def can_anular(self, id, usuario_perfil):
        """verificando si se puede eliminar o no la tabla"""
        try:
            # puede anular el usuario con permiso de la sucursal
            punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
            permisos = get_permissions_user(usuario_perfil.user_id, settings.MOD_MOVIMIENTOS_ALMACEN)

            # registro
            registro = Registros.objects.get(pk=id)
            if registro.status_id.status_id == self.anulado:
                self.error_operation = 'el registro ya esta anulado'
                return False

            if not self.permission_registro(usuario_perfil, registro):
                self.error_operation = 'no tiene permiso para anular este registro'
                return False

            if permisos.anular:
                return True

            return False

        except Exception as ex:
            print('error can anular: ', str(ex))
            return False

    def anular(self, request, id):
        """anulando el registro"""
        try:
            usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            if self.can_anular(id, usuario_perfil):

                status_anular = self.status_anulado
                motivo_a = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')

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
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular ingreso almacen: ' + str(ex))
            self.error_operation = 'Error al anular el registro, ' + str(ex)
            return False

    def anular_db(self, id, **datos):
        """ anulamos en la bd """
        try:
            if self.can_anular(id, datos['user_perfil_id']):
                stock_controller = StockController()

                with transaction.atomic():
                    campos_update = {}
                    campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
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
                        stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=registro.almacen_id, producto=registro_detalle.insumo_id, cantidad=registro_detalle.cantidad,
                                                                 fecha_elaboracion=registro_detalle.fecha_elaboracion, fecha_vencimiento=registro_detalle.fecha_vencimiento, lote=registro_detalle.lote)
                        if not stock_up:
                            self.error_operation = 'Error al actualizar stock almacen 1'
                            return False

                        # sale del almacen 2
                        stock_up = stock_controller.update_stock(user_perfil=datos['user_perfil_id'], almacen=almacen2, producto=registro_detalle.insumo_id, cantidad=(0-registro_detalle.cantidad),
                                                                 fecha_elaboracion=registro_detalle.fecha_elaboracion, fecha_vencimiento=registro_detalle.fecha_vencimiento, lote=registro_detalle.lote)
                        if not stock_up:
                            self.error_operation = 'Error al actualizar stock almacen 2'
                            return False

                    # verificamos las preventas si que hubiese
                    lista_models = apps.get_models()
                    existe = 'no'
                    for model in lista_models:
                        # print('modelo: ', model.__name__)
                        if model.__name__ == 'PreVentas':
                            existe = 'si'

                    if existe == 'si':
                        preventas_lista = apps.get_model('preventas', 'Preventas').objects.filter(registro_id=registro.registro_id)
                        for preventa in preventas_lista:
                            preventa.registro_id = 0
                            preventa.updated_at = 'now'
                            preventa.save()

                    self.error_operation = ''
                    return True

            else:
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular ingreso almacen db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return False
