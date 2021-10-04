from utils.dates_functions import add_months_datetime, add_days_datetime
from django.apps import apps
from django.conf import settings


class PlanPagosController():

    def add_plan_pago_db(self, **datos):
        try:
            # print('datos: ', datos)
            campos_pp = {}
            if 'registro_id' in datos.keys():
                campos_pp['registro_id'] = datos['registro_id']
            else:
                campos_pp['registro_id'] = 0

            if 'venta_id' in datos.keys():
                campos_pp['venta_id'] = datos['venta_id']
            else:
                campos_pp['venta_id'] = 0

            if 'preventa_id' in datos.keys():
                campos_pp['preventa_id'] = datos['preventa_id']
            else:
                campos_pp['preventa_id'] = 0

            if 'cliente_id' in datos.keys():
                campos_pp['cliente_id'] = datos['cliente_id']
            else:
                campos_pp['cliente_id'] = 0

            campos_pp['punto_id'] = datos['punto_id']
            campos_pp['fecha'] = datos['fecha']
            campos_pp['concepto'] = datos['concepto']
            campos_pp['numero_cuotas'] = datos['numero_cuotas']
            campos_pp['monto_total'] = datos['monto_total']
            campos_pp['cuota_inicial'] = datos['cuota_inicial']
            campos_pp['saldo'] = datos['saldo']
            campos_pp['mensual_dias'] = datos['mensual_dias']

            if datos['mensual_dias'] == 'tipo_fecha':
                campos_pp['dia_mensual'] = datos['dia_mensual']
                campos_pp['tiempo_dias'] = 0
            else:
                campos_pp['dia_mensual'] = 0
                campos_pp['tiempo_dias'] = int(datos['dias'])

            campos_pp['status_id'] = datos['status_id']
            campos_pp['user_perfil_id'] = datos['user_perfil_id']
            campos_pp['created_at'] = datos['created_at']
            campos_pp['updated_at'] = datos['updated_at']

            # registramos el plan de pagos
            pp_add = apps.get_model('inventarios', 'PlanPagos').objects.create(**campos_pp)
            pp_add.save()

            # registramos los detalles
            cuota = pp_add.monto_total // pp_add.numero_cuotas
            saldo = pp_add.monto_total
            num_cuota = 1
            aux_fecha = datos['fecha_fija']

            # status cuota pendiente
            status_cuota_pendiente = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_CUOTA_PENDIENTE))

            while num_cuota < pp_add.numero_cuotas:
                # creamos el detalle
                campos_pp_detalle = {}
                campos_pp_detalle['plan_pago_id'] = pp_add
                campos_pp_detalle['numero_cuota'] = num_cuota

                if num_cuota == 1:
                    campos_pp_detalle['fecha'] = aux_fecha
                else:
                    if datos['mensual_dias'] == 'tipo_fecha':
                        aux_fecha = add_months_datetime(fecha=aux_fecha, formato_ori='yyyy-mm-dd HH:ii:ss', meses=1, formato='yyyy-mm-dd HH:ii:ss')
                        campos_pp_detalle['fecha'] = aux_fecha
                    else:
                        aux_fecha = add_days_datetime(fecha=aux_fecha, formato_ori='yyyy-mm-dd HH:ii:ss', dias=int(datos['dias']), formato='yyyy-mm-dd HH:ii:ss')
                        campos_pp_detalle['fecha'] = aux_fecha

                campos_pp_detalle['monto'] = cuota
                campos_pp_detalle['saldo'] = saldo - cuota
                campos_pp_detalle['status_id'] = status_cuota_pendiente
                campos_pp_detalle['user_perfil_id'] = pp_add.user_perfil_id
                campos_pp_detalle['created_at'] = datos['created_at']
                campos_pp_detalle['updated_at'] = datos['updated_at']

                # print('campos detalle: ', campos_pp_detalle)
                # detalle del plan de pagos
                pp_detalle_add = apps.get_model('inventarios', 'PlanPagosDetalles').objects.create(**campos_pp_detalle)
                pp_detalle_add.save()

                saldo -= cuota
                num_cuota += 1

            # ultima cuota
            campos_pp_detalle = {}
            campos_pp_detalle['plan_pago_id'] = pp_add
            campos_pp_detalle['numero_cuota'] = num_cuota

            if datos['mensual_dias'] == 'tipo_fecha':
                aux_fecha = add_months_datetime(fecha=aux_fecha, formato_ori='yyyy-mm-dd', meses=1, formato='yyyy-mm-dd')
                campos_pp_detalle['fecha'] = aux_fecha
            else:
                aux_fecha = add_days_datetime(fecha=aux_fecha, formato_ori='yyyy-mm-dd', dias=int(datos['dias']), formato='yyyy-mm-dd')
                campos_pp_detalle['fecha'] = aux_fecha

            campos_pp_detalle['monto'] = saldo
            campos_pp_detalle['saldo'] = 0
            campos_pp_detalle['status_id'] = status_cuota_pendiente
            campos_pp_detalle['user_perfil_id'] = pp_add.user_perfil_id
            campos_pp_detalle['created_at'] = datos['created_at']
            campos_pp_detalle['updated_at'] = datos['updated_at']

            # detalle del plan de pagos
            pp_detalle_add = apps.get_model('inventarios', 'PlanPagosDetalles').objects.create(**campos_pp_detalle)
            pp_detalle_add.save()

            return True

        except Exception as ex:
            print('Error al adicionar el plan de pago, ' + str(ex))
            return False

    def anular_db(self, registro_id=0, venta_id=0, preventa_id=0, **datos):

        try:
            if registro_id > 0:
                plan_pago = apps.get_model('inventarios', 'PlanPagos').objects.get(registro_id=registro_id)

            if venta_id > 0:
                plan_pago = apps.get_model('inventarios', 'PlanPagos').objects.get(venta_id=venta_id)

            if preventa_id > 0:
                plan_pago = apps.get_model('inventarios', 'PlanPagos').objects.get(preventa_id=preventa_id)

            plan_pago.user_perfil_id_anula = datos['user_perfil_id_anula']
            plan_pago.motivo_anula = datos['motivo_anula']
            plan_pago.status_id = datos['status_id']
            plan_pago.deleted_at = datos['deleted_at']
            plan_pago.save()

            return True

        except Exception as ex:
            print('Error al anular el plan de pago, ' + str(ex))
            return False
