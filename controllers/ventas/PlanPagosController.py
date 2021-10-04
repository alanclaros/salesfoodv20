from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from inventarios.models import PlanPagos, PlanPagosDetalles, PlanPagosPagos
from permisos.models import UsersPerfiles
from cajas.models import Cajas, CajasIngresos
from configuraciones.models import Puntos

from status.models import Status
from decimal import Decimal

from django.db import transaction

from decimal import Decimal

# fechas
from utils.dates_functions import get_date_show, get_date_system, get_seconds_date1_sub_date2, get_day_from_date
from utils.permissions import get_permissions_user, get_system_settings

from controllers.cajas.CajasIngresosController import CajasIngresosController

from utils.validators import validate_string, validate_number_int, validate_number_decimal

# conexion directa a la base de datos
from django.db import connection


class PlanPagosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'PlanPagos'
        self.modelo_id = 'plan_pago_id'
        self.modelo_app = 'ventas'
        self.modulo_id = settings.MOD_PLAN_PAGOS

        # variables de session
        self.modulo_session = "plan_pagos"
        self.columnas.append('fecha')
        self.columnas.append('venta')
        self.columnas.append('total')
        self.columnas.append('saldo')

        self.variables_filtros.append('search_tipo_plan_pago')
        self.variables_filtros.append('search_concepto')
        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_ci_nit')
        self.variables_filtros.append('search_codigo')
        self.variables_filtros.append('search_activos')
        self.variables_filtros.append('search_anulados')
        self.variables_filtros.append('search_almacen2')

        self.variables_filtros_defecto['search_tipo_plan_pago'] = 'venta'
        self.variables_filtros_defecto['search_concepto'] = ''
        self.variables_filtros_defecto['search_apellidos'] = ''
        self.variables_filtros_defecto['search_nombres'] = ''
        self.variables_filtros_defecto['search_ci_nit'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''
        self.variables_filtros_defecto['search_activos'] = '1'
        self.variables_filtros_defecto['search_anulados'] = '0'
        self.variables_filtros_defecto['search_almacen2'] = '0'

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = 'DESC'

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = ""
        # sql_add
        self.sql_venta = ""
        self.sql_inventario = ""
        self.sql_cantidad = ''
        self.sql_add = ''

    def index(self, request):
        DefaultValues.index(self, request)

        self.filtros_modulo.clear()
        # consulta
        self.sql_venta = ''
        self.sql_inventario = ''
        self.sql_add = ''

        if self.variables_filtros_values['search_codigo'].strip() != '':
            self.sql_add += f"AND p.plan_pago_id='{self.variables_filtros_values['search_codigo'].strip()}' "
        else:
            # anulados
            if 'search_anulados' in request.POST.keys() or self.variables_filtros_values['search_anulados'] == '1':
                self.variables_filtros_values['search_anulados'] = '1'
                self.sql_add += f"AND p.status_id='{self.anulado}' "
            else:
                self.variables_filtros_values['search_anulados'] = '0'
                self.sql_add += f"AND p.status_id='{self.activo}' "

            # activos
            if 'search_activos' in request.POST.keys() or self.variables_filtros_values['search_activos'] == '1':
                self.variables_filtros_values['search_activos'] = '1'
                self.sql_add += "AND p.saldo>0 "
            else:
                self.variables_filtros_values['search_activos'] = '0'
                self.sql_add += "AND p.saldo=0 "

            if self.variables_filtros_values['search_tipo_plan_pago'].strip() == 'venta':
                # de ventas
                # apellidos
                if self.variables_filtros_values['search_apellidos'].strip() != "":
                    self.sql_add += f"AND c.apellidos LIKE '%{self.variables_filtros_values['search_apellidos'].strip()}%' "
                # nombres
                if self.variables_filtros_values['search_nombres'].strip() != "":
                    self.sql_add += f"AND c.nombres LIKE '%{self.variables_filtros_values['search_nombres'].strip()}%' "
                # ci_nit
                if self.variables_filtros_values['search_ci_nit'].strip() != "":
                    self.sql_add += f"AND c.ci_nit LIKE '%{self.variables_filtros_values['search_ci_nit'].strip()}%' "
            else:
                # plan pago inventarios
                self.sql_add += f"AND r.almacen2_id='{self.variables_filtros_values['search_almacen2']}' "

                if self.variables_filtros_values['search_concepto'].strip() != '':
                    division = self.variables_filtros_values['search_concepto'].strip().split(' ')
                    if len(division) == 1:
                        self.sql_add += f"AND r.concepto LIKE '%{self.variables_filtros_values['search_concepto'].strip()}%' "
                    elif len(division) == 2:
                        self.sql_add += f"AND (r.concepto LIKE '%{division[0]}%{division[1]}%' OR r.concepto LIKE '%{division[1]}%{division[0]}%' "
                        self.sql_add += ') '
                    # if len(division) == 3:
                    else:
                        self.sql_add += f"AND (r.concepto LIKE '%{division[0]}%{division[1]}%{division[2]}' "
                        self.sql_add += f"OR r.concepto LIKE '%{division[0]}%{division[2]}%{division[1]}' "

                        self.sql_add += f"OR r.concepto LIKE '%{division[1]}%{division[0]}%{division[2]}' "
                        self.sql_add += f"OR r.concepto LIKE '%{division[1]}%{division[2]}%{division[0]}' "

                        self.sql_add += f"OR r.concepto LIKE '%{division[2]}%{division[0]}%{division[1]}' "
                        self.sql_add += f"OR r.concepto LIKE '%{division[2]}%{division[1]}%{division[0]}' "

                        self.sql_add += ') '

        # tipo de plan de pago
        if self.variables_filtros_values['search_tipo_plan_pago'].strip() == 'venta':
            self.sql_venta = "SELECT p.fecha, p.concepto, p.numero_cuotas, p.monto_total, p.saldo, p.mensual_dias, p.dia_mensual, p.tiempo_dias, p.user_perfil_id_anula, p.motivo_anula, "
            self.sql_venta += "c.apellidos, c.nombres, c.ci_nit, v.numero_venta, p.plan_pago_id, p.status_id "

            self.sql_cantidad = "SELECT COUNT(*) AS cantidad "

            aux = ''
            aux += "FROM plan_pagos p, ventas v, clientes c "
            aux += "WHERE p.venta_id=v.venta_id AND v.cliente_id=c.cliente_id "
            aux += self.sql_add

            self.sql_venta += aux
            self.sql_cantidad += aux

            self.sql_venta += "ORDER BY p.fecha, c.apellidos, c.nombres "
            #print('venta: ', self.sql_venta)

        else:
            # plan de pago de inventario
            self.sql_inventario = "SELECT p.fecha, p.concepto, p.numero_cuotas, p.monto_total, p.saldo, p.mensual_dias, p.dia_mensual, p.tiempo_dias, p.user_perfil_id_anula, p.motivo_anula, "
            self.sql_inventario += "r.concepto, a.almacen, r.numero_registro, p.plan_pago_id, p.status_id "

            self.sql_cantidad = "SELECT COUNT(*) AS cantidad "

            aux = ''
            aux += "FROM plan_pagos p, registros r, almacenes a "
            aux += "WHERE p.registro_id=r.registro_id AND r.almacen2_id=a.almacen_id "
            aux += self.sql_add

            self.sql_inventario += aux
            self.sql_cantidad += aux

            self.sql_inventario += "ORDER BY p.fecha, r.concepto "
            #print('inventario: ', self.sql_inventario)

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def records_count(self):
        """cantidad de registros del modulo"""
        cantidad = 0
        with connection.cursor() as cursor:
            cursor.execute(self.sql_cantidad)
            row = cursor.fetchone()
            if row:
                cantidad = row[0]

        return cantidad

    def pagination(self):
        settings_sistema = get_system_settings()
        cant_per_page = settings_sistema['cant_per_page']
        self.pages_list = []
        cant_total = self.records_count()
        j = 1
        i = 0
        while i < cant_total:
            self.pages_list.append(j)
            i = i + cant_per_page
            j += 1
            if j > 15:
                break

        self.pages_limit_botton = (int(self.variable_page_val) - 1) * cant_per_page
        self.pages_limit_top = self.pages_limit_botton + cant_per_page

    def get_list(self):
        retorno = []

        if self.variables_filtros_values['search_tipo_plan_pago'] == 'venta':
            sql_mandar = self.sql_venta
            sql_mandar += f"LIMIT {self.pages_limit_botton},{self.pages_limit_top} "

            with connection.cursor() as cursor:
                cursor.execute(sql_mandar)
                rows = cursor.fetchall()
                for row in rows:
                    datos = {}
                    datos['fecha'] = row[0]
                    datos['concepto'] = row[1]
                    datos['numero_cuotas'] = row[2]
                    datos['monto_total'] = row[3]
                    datos['saldo'] = row[4]
                    datos['mensual_dias'] = row[5]
                    datos['dia_mensual'] = row[6]
                    datos['tiempo_dias'] = row[7]
                    datos['user_id_anula'] = row[8]
                    datos['motivo_anula'] = row[9]
                    datos['detalle'] = row[10] + ' ' + row[11] + ', CI/NIT: ' + row[12] + f" (V:{row[13]})"
                    datos['plan_pago_id'] = row[14]
                    datos['status_id'] = row[15]
                    retorno.append(datos)

        else:
            sql_mandar = self.sql_inventario
            sql_mandar += f"LIMIT {self.pages_limit_botton},{self.pages_limit_top} "
            with connection.cursor() as cursor:
                cursor.execute(sql_mandar)
                rows = cursor.fetchall()
                for row in rows:
                    datos = {}
                    datos['fecha'] = row[0]
                    datos['concepto'] = row[1]
                    datos['numero_cuotas'] = row[2]
                    datos['monto_total'] = row[3]
                    datos['saldo'] = row[4]
                    datos['mensual_dias'] = row[5]
                    datos['dia_mensual'] = row[6]
                    datos['tiempo_dias'] = row[7]
                    datos['user_id_anula'] = row[8]
                    datos['motivo_anula'] = row[9]
                    datos['detalle'] = row[10] + f" A:{row[11]} (I:{row[12]}) "
                    datos['plan_pago_id'] = row[13]
                    datos['status_id'] = row[14]
                    retorno.append(datos)

        return retorno

    def add_pago(self, request, plan_pago_id):
        """aniadimos un nuevo pago"""
        try:
            # control de almacenes
            monto = validate_number_decimal('monto', request.POST['monto'])
            observacion = validate_string('observacion', request.POST['observacion'], remove_specials='yes')
            aux_caja = validate_number_int('caja', request.POST['caja'])

            if monto <= 0:
                self.error_operation = 'Debe ingresar un monto valido'
                return False

            # caja
            caja_id = Cajas.objects.get(pk=aux_caja)
            # estado
            status_cuota = self.status_cuota_pagada
            # usuario
            usuario = request.user
            user_perfil = UsersPerfiles.objects.get(user_id=usuario)
            punto = Puntos.objects.get(pk=user_perfil.punto_id)
            # plan de pago
            plan_pago = PlanPagos.objects.get(pk=int(plan_pago_id))

            datos = {}
            datos['monto'] = monto
            datos['observacion'] = observacion
            datos['caja_id'] = caja_id
            datos['punto_id'] = punto
            datos['plan_pago'] = plan_pago
            datos['status_id'] = status_cuota
            datos['user_perfil_id'] = user_perfil
            datos['fecha'] = 'now'
            datos['created_at'] = 'now'
            datos['updated_at'] = 'now'

            if self.add_pago_db(**datos):
                self.error_operation = ""
                return True
            else:
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el pago, " + str(ex)
            return False

    def add_pago_db(self, **datos):
        """aniadimos a la base de datos"""
        try:
            # transaccion
            with transaction.atomic():
                # actualizamos el saldo del plan de pagos
                #plan_pago= PlanPagos.objects.get(pk=datos['plan'])
                if datos['plan_pago'].saldo - datos['monto'] < 0:
                    datos['plan_pago'].saldo = 0
                    datos['monto'] = datos['plan_pago'].saldo
                else:
                    datos['plan_pago'].saldo = datos['plan_pago'].saldo - datos['monto']

                datos['plan_pago'].updated_at = datos['updated_at']
                datos['plan_pago'].save()

                campos_add = {}
                campos_add['monto'] = datos['monto']
                campos_add['saldo'] = datos['plan_pago'].saldo
                campos_add['persona_paga'] = datos['observacion']
                campos_add['fecha'] = datos['fecha']
                campos_add['numero_cuota'] = self.get_numero_cuota(datos['plan_pago'].plan_pago_id)
                campos_add['user_perfil_id_paga'] = 0  # usuario del almacen al que se vende
                campos_add['cliente_id_paga'] = datos['plan_pago'].cliente_id
                campos_add['created_at'] = datos['created_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['plan_pago_id'] = datos['plan_pago']
                campos_add['user_perfil_id'] = datos['user_perfil_id']
                campos_add['status_id'] = datos['status_id']

                # nuevo registro
                pp_add = PlanPagosPagos.objects.create(**campos_add)
                pp_add.save()

                # ingreso a caja
                status_activo = self.status_activo
                ci_controller = CajasIngresosController()

                campos_ingreso = {}
                campos_ingreso['caja_id'] = datos['caja_id']
                campos_ingreso['punto_id'] = datos['punto_id']
                campos_ingreso['user_perfil_id'] = datos['user_perfil_id']
                campos_ingreso['status_id'] = status_activo
                campos_ingreso['fecha'] = datos['fecha']
                campos_ingreso['concepto'] = 'ingreso de efectivo, plan pago: ' + str(datos['plan_pago'].plan_pago_id)
                campos_ingreso['monto'] = pp_add.monto
                campos_ingreso['created_at'] = datos['created_at']
                campos_ingreso['updated_at'] = datos['updated_at']
                campos_ingreso['venta_plan_pago_id'] = pp_add.plan_pago_pago_id
                # registramos
                ci_controller.add_db(**campos_ingreso)

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add pago de plan de pago, '+str(ex))
            return False

    def can_anular(self, id, user):
        """verificando si se puede eliminar o no la tabla"""
        # puede anular el usuario con permiso de la sucursal
        usuario_perfil = UsersPerfiles.objects.get(user_id=user)
        punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
        permisos = get_permissions_user(user, settings.MOD_PLAN_PAGOS)

        # registro
        plan_pago_pago = PlanPagosPagos.objects.get(pk=id)
        if plan_pago_pago.status_id.status_id == self.anulado:
            self.error_operation = 'el registro ya esta anulado'
            return False

        # registro de la misma sucursal
        plan_pago = PlanPagos.objects.get(pk=plan_pago_pago.plan_pago_id.plan_pago_id)
        plan_pago_punto = Puntos.objects.get(pk=plan_pago.punto_id)
        if plan_pago_punto.sucursal_id == punto.sucursal_id:
            # verificamos si es plan de pagos, y no pago ninguna cuota
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
                user_perfil = UsersPerfiles.objects.get(user_id=request.user)
                campos_update['user_perfil_id'] = user_perfil
                campos_update['user_perfil_id_anula'] = user_perfil.user_perfil_id
                campos_update['motivo_anula'] = motivo_a
                campos_update['status_id'] = status_anular
                campos_update['deleted_at'] = 'now'

                if self.anular_db(id, **campos_update):
                    self.error_operation = ''
                    return True
                else:
                    return False

            else:
                self.error_operation = 'No tiene permiso para anular este pago'
                return False

        except Exception as ex:
            print('Error anular pago: ' + str(ex))
            self.error_operation = 'Error al anular el pago, ' + str(ex)
            return False

    def anular_db(self, id, **datos):
        """ anulamos en la bd """
        try:
            with transaction.atomic():
                campos_update = {}
                campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                campos_update['motivo_anula'] = datos['motivo_anula']
                campos_update['status_id'] = datos['status_id']
                campos_update['deleted_at'] = datos['deleted_at']

                # registramos
                pp_pago_update = PlanPagosPagos.objects.filter(pk=id)
                pp_pago_update.update(**campos_update)

                # anulamos el registro de caja
                ci_controller = CajasIngresosController()
                status_activo = self.status_activo
                caja_ingreso = CajasIngresos.objects.get(venta_plan_pago_id=id, status_id=status_activo)
                ci_controller.delete_db(caja_ingreso.caja_ingreso_id, **campos_update)

                # actaulizamos el plan de pagos
                pp_pago = PlanPagosPagos.objects.get(pk=id)
                plan_pago = PlanPagos.objects.get(pk=pp_pago.plan_pago_id.plan_pago_id)
                plan_pago.saldo = plan_pago.saldo + pp_pago.monto
                plan_pago.updated_at = 'now'
                plan_pago.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            print('Error anular pago de plan pago db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return

    def get_detalles(self, plan_pago_id):
        """devolvemos los detalles del plan de pagos"""

        plan_pagos_detalles = []
        try:
            plan_pago = PlanPagos.objects.get(pk=int(plan_pago_id))
            status_cuota_pendiente = self.status_cuota_pendiente

            plan_pagos_detalles = PlanPagosDetalles.objects.filter(plan_pago_id=plan_pago, status_id=status_cuota_pendiente).order_by('fecha')

            return plan_pagos_detalles

        except Exception as e:
            print('error al recuperar plan pagos detalles: ' + str(plan_pago_id) + ', ' + str(e))
            return plan_pagos_detalles

    def get_pagos_realizados(self, plan_pago_id):
        """devolvemos los pagos realizados del plan de pagos"""

        pagos = []
        try:
            plan_pago = PlanPagos.objects.get(pk=int(plan_pago_id))
            #status_activo = Status.objects.get(pk=self.activo)
            status_cuota_pagada = Status.objects.get(pk=self.cuota_pagada)

            pagos = PlanPagosPagos.objects.filter(plan_pago_id=plan_pago).order_by('fecha')

            return pagos

        except Exception as e:
            print('error al recuperar los pagos del plan pagos: ' + str(plan_pago_id) + ', ' + str(e))
            return pagos

    def get_numero_cuota(self, plan_pago_id):
        """devuelve el numero de cuota que esta pagando"""
        plan_pago = PlanPagos.objects.get(pk=int(plan_pago_id))
        status_cuota_pagada = Status.objects.get(pk=self.cuota_pagada)
        listado = PlanPagosPagos.objects.filter(plan_pago_id=plan_pago, status_id=status_cuota_pagada)

        cantidad = 0

        if listado:
            cantidad = listado.count() + 1
        else:
            cantidad = 1

        return cantidad
