from django.db import models
from django.conf import settings

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome, DateFieldCustome
from configuraciones.models import Puntos, Almacenes, Cajas, Sucursales
from clientes.models import Clientes
from productos.models import Insumos, Productos, Componentes
from permisos.models import UsersPerfiles


class Lugares(models.Model):
    lugar_id = models.IntegerField(primary_key=True, db_column='lugar_id')
    lugar = models.CharField(max_length=50, db_column='lugar')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    class Meta:
        db_table = 'lugares'


class Ventas(models.Model):
    venta_id = models.AutoField(primary_key=True, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    caja_id = models.ForeignKey(Cajas, to_field='caja_id', on_delete=models.PROTECT, db_column='caja_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    cliente_id = models.ForeignKey(Clientes, to_field='cliente_id', on_delete=models.PROTECT, db_column='cliente_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    lugar_id = models.ForeignKey(Lugares, to_field='lugar_id', on_delete=models.PROTECT, db_column='lugar_id')

    apellidos = models.CharField(max_length=150, blank=False, null=False)
    nombres = models.CharField(max_length=150, blank=False, null=False)
    ci_nit = models.CharField(max_length=150, blank=False, null=False)
    telefonos = models.CharField(max_length=150, blank=False, null=False)

    direccion = models.CharField(max_length=250, blank=False, null=False, default='')
    mesa = models.CharField(max_length=50, blank=False, null=False, default='')
    observacion = models.TextField(null=False, blank=False, default='')

    tipo_venta = models.CharField(max_length=50, blank=False, null=False)
    numero_venta = models.IntegerField(blank=False, null=False, default=0)
    costo_abc = models.CharField(max_length=10, blank=False, null=False, default='A')

    fecha = DateTimeFieldCustome(null=True, blank=True)
    user_perfil_id_fecha = models.IntegerField(blank=False, null=False, default=0)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    concepto = models.CharField(max_length=250, blank=False, null=False)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'ventas'


class VentasDetalles(models.Model):
    venta_detalle_id = models.AutoField(primary_key=True, db_column='venta_detalle_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')

    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    fecha_elaboracion = DateTimeFieldCustome(null=True, blank=True)
    fecha_vencimiento = DateTimeFieldCustome(null=True, blank=True)
    lote = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'ventas_detalles'


class VentasDetallesInsumos(models.Model):
    venta_detalle_insumo_id = models.AutoField(primary_key=True, db_column='venta_insumo_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    venta_detalle_id = models.ForeignKey(VentasDetalles, to_field='venta_detalle_id', on_delete=models.PROTECT, db_column='venta_detalle_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')

    insumo_id = models.ForeignKey(Insumos, to_field='insumo_id', on_delete=models.PROTECT, db_column='insumo_id')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'ventas_detalles_insumos'


class VentasDetallesComponentes(models.Model):
    venta_detalle_componente_id = models.AutoField(primary_key=True, db_column='venta_componente_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    venta_detalle_id = models.ForeignKey(VentasDetalles, to_field='venta_detalle_id', on_delete=models.PROTECT, db_column='venta_detalle_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')

    componente_id = models.ForeignKey(Componentes, to_field='componente_id', on_delete=models.PROTECT, db_column='componente_id')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'ventas_detalles_componentes'


class VentasDetallesExtras(models.Model):
    venta_detalle_extra_id = models.AutoField(primary_key=True, db_column='venta_detalle_extra_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    venta_detalle_id = models.ForeignKey(VentasDetalles, to_field='venta_detalle_id', on_delete=models.PROTECT, db_column='venta_detalle_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')

    componente_id = models.ForeignKey(Componentes, to_field='componente_id', on_delete=models.PROTECT, db_column='componente_id')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'ventas_detalles_extras'


class VentasDetallesRefrescos(models.Model):
    venta_detalle_refresco_id = models.AutoField(primary_key=True, db_column='venta_detalle_refresco_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    venta_detalle_id = models.ForeignKey(VentasDetalles, to_field='venta_detalle_id', on_delete=models.PROTECT, db_column='venta_detalle_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')

    insumo_id = models.IntegerField(blank=False, null=False, default=0)
    componente_id = models.IntegerField(blank=False, null=False, default=0)

    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'ventas_detalles_refrescos'


class VentasDetallesPapas(models.Model):
    venta_detalle_papa_id = models.AutoField(primary_key=True, db_column='venta_detalle_papa_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    venta_detalle_id = models.ForeignKey(VentasDetalles, to_field='venta_detalle_id', on_delete=models.PROTECT, db_column='venta_detalle_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')

    insumo_id = models.IntegerField(blank=False, null=False, default=0)
    componente_id = models.IntegerField(blank=False, null=False, default=0)

    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'ventas_detalles_papas'


class Dosificaciones(models.Model):
    dosificacion_id = models.AutoField(primary_key=True, db_column='dosificacion_id')
    sucursal_id = models.ForeignKey(Sucursales, to_field='sucursal_id', on_delete=models.PROTECT, db_column='sucursal_id')
    dosificacion = models.CharField(max_length=250, null=False, blank=False)
    fecha_inicio = DateFieldCustome(null=True, blank=True)
    fecha_fin = DateFieldCustome(null=True, blank=True)
    numero_autorizacion = models.CharField(max_length=250, blank=False, null=False)
    llave = models.CharField(max_length=250, blank=False, null=False)
    numero_actual = models.IntegerField(blank=False, null=False)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'dosificaciones'


class Facturas(models.Model):
    factura_id = models.AutoField(primary_key=True, db_column='factura_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    dosificacion_id = models.ForeignKey(Dosificaciones, to_field='dosificacion_id', on_delete=models.PROTECT, db_column='dosificacion_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    caja_id = models.ForeignKey(Cajas, to_field='caja_id', on_delete=models.PROTECT, db_column='caja_id')
    cliente_id = models.ForeignKey(Clientes, to_field='cliente_id', on_delete=models.PROTECT, db_column='cliente_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    apellidos = models.CharField(max_length=150, blank=False, null=False)
    nombres = models.CharField(max_length=150, blank=False, null=False)
    ci_nit = models.CharField(max_length=150, blank=False, null=False)
    telefonos = models.CharField(max_length=150, blank=False, null=False)
    nit = models.CharField(max_length=150, blank=False, null=False)
    factura_a = models.CharField(max_length=250, blank=False, null=False)
    numero_factura = models.IntegerField(blank=False, null=False)

    numero_autorizacion = models.CharField(max_length=250, blank=False, null=False)
    llave = models.CharField(max_length=250, blank=False, null=False)
    codigo_control = models.CharField(max_length=250, blank=False, null=False)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    fecha = DateTimeFieldCustome(null=True, blank=True)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'facturas'
        unique_together = ('dosificacion_id', 'numero_factura',)
