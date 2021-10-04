from django.db import models
from django.conf import settings

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome
from configuraciones.models import Puntos, Almacenes
from permisos.models import UsersPerfiles
from productos.models import Insumos


class Registros(models.Model):
    registro_id = models.AutoField(primary_key=True, db_column='registro_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    almacen2_id = models.IntegerField(blank=False, null=False, default=0)
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    tipo_movimiento = models.CharField(max_length=50, blank=False, null=False)
    numero_registro = models.IntegerField(blank=False, null=False, default=0)
    costo_abc = models.CharField(max_length=10, blank=False, null=False, default='A')

    fecha = DateTimeFieldCustome(null=True, blank=True)
    fecha_salida_almacen = DateTimeFieldCustome(null=True, blank=True)
    fecha_recibe_almacen = DateTimeFieldCustome(null=True, blank=True)

    user_perfil_id_fecha = models.IntegerField(blank=False, null=False, default=0)
    user_perfil_id_salida_almacen = models.IntegerField(blank=False, null=False, default=0)
    user_perfil_id_recibe_almacen = models.IntegerField(blank=False, null=False, default=0)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    concepto = models.CharField(max_length=250, blank=False, null=False)
    concepto_salida_almacen = models.CharField(max_length=250, blank=False, null=False)
    concepto_recibe_almacen = models.CharField(max_length=250, blank=False, null=False)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'registros'


class RegistrosDetalles(models.Model):
    registro_detalle_id = models.AutoField(primary_key=True, db_column='registro_detalle_id')
    registro_id = models.ForeignKey(Registros, to_field='registro_id', on_delete=models.PROTECT, db_column='registro_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')

    insumo_id = models.ForeignKey(Insumos, to_field='insumo_id', on_delete=models.PROTECT, db_column='insumo_id')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    fecha_elaboracion = DateTimeFieldCustome(null=True, blank=True)
    fecha_vencimiento = DateTimeFieldCustome(null=True, blank=True)
    lote = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'registros_detalles'


class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True, db_column='stock_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    insumo_id = models.ForeignKey(Insumos, to_field='insumo_id', on_delete=models.PROTECT, db_column='insumo_id')
    fecha_elaboracion = DateTimeFieldCustome(null=True, blank=True)
    fecha_vencimiento = DateTimeFieldCustome(null=True, blank=True)
    lote = models.CharField(max_length=50, null=False, blank=False)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'stock'


class PlanPagos(models.Model):
    plan_pago_id = models.AutoField(primary_key=True, db_column='plan_pago_id')
    registro_id = models.IntegerField(blank=False, null=False, default=0)
    venta_id = models.IntegerField(blank=False, null=False, default=0)
    preventa_id = models.IntegerField(blank=False, null=False, default=0)
    cliente_id = models.IntegerField(blank=False, null=False, default=0)
    punto_id = models.IntegerField(blank=False, null=False, default=0)

    fecha = DateTimeFieldCustome(null=True, blank=True)
    concepto = models.CharField(max_length=250, blank=False, null=False)
    numero_cuotas = models.IntegerField(blank=False, null=False, default=1)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cuota_inicial = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    mensual_dias = models.CharField(max_length=20, blank=False, null=False)
    dia_mensual = models.IntegerField(blank=False, null=False, default=1)
    tiempo_dias = models.IntegerField(blank=False, null=False, default=1)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'plan_pagos'


class PlanPagosDetalles(models.Model):
    plan_pago_detalle_id = models.AutoField(primary_key=True, db_column='plan_pago_detalle_id')
    plan_pago_id = models.ForeignKey(PlanPagos, to_field='plan_pago_id', on_delete=models.PROTECT, db_column='plan_pago_id')
    numero_cuota = models.IntegerField(blank=False, null=False, default=1)
    fecha = DateTimeFieldCustome(null=True, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'plan_pagos_detalles'


class PlanPagosPagos(models.Model):
    plan_pago_pago_id = models.AutoField(primary_key=True, db_column='plan_pago_pago_id')
    plan_pago_id = models.ForeignKey(PlanPagos, to_field='plan_pago_id', on_delete=models.PROTECT, db_column='plan_pago_id')

    numero_cuota = models.IntegerField(blank=False, null=False, default=1)
    fecha = DateTimeFieldCustome(null=True, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_paga = models.IntegerField(blank=False, null=False, default=0)
    cliente_id_paga = models.IntegerField(blank=False, null=False, default=0)
    persona_paga = models.CharField(max_length=250, blank=False, null=False)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'plan_pagos_pagos'
