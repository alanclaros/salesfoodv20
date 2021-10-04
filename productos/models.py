from django.db import models
from django.conf import settings
from django.db.models.base import Model

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome
from configuraciones.models import Lineas, Puntos
from permisos.models import UsersPerfiles


class Productos(models.Model):
    producto_id = models.AutoField(primary_key=True, db_column='producto_id')
    linea_id = models.ForeignKey(Lineas, to_field='linea_id', on_delete=models.PROTECT, db_column='linea_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    producto = models.CharField(max_length=250, unique=True, blank=False, null=False)
    codigo = models.CharField(max_length=50, blank=False, null=False)
    codigo_barras = models.CharField(max_length=50, blank=False, null=False)
    stock_minimo = models.IntegerField(blank=False, null=False, default=0)
    unidad = models.CharField(max_length=20, blank=False, null=False, default='')

    descripcion1 = models.CharField(max_length=250, blank=False, null=False)
    descripcion2 = models.CharField(max_length=250, blank=False, null=False)
    descripcion3 = models.CharField(max_length=250, blank=False, null=False)
    descripcion4 = models.CharField(max_length=250, blank=False, null=False)
    descripcion5 = models.CharField(max_length=250, blank=False, null=False)
    descripcion6 = models.CharField(max_length=250, blank=False, null=False)
    descripcion7 = models.CharField(max_length=250, blank=False, null=False)
    descripcion8 = models.CharField(max_length=250, blank=False, null=False)
    descripcion9 = models.CharField(max_length=250, blank=False, null=False)
    descripcion10 = models.CharField(max_length=250, blank=False, null=False)

    # costos en movimientos de almacen
    costo_a = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_b = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo_c = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    # precios de venta
    precio_a = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_b = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_c = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    # precios de venta con factura
    precio_a_factura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_b_factura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_c_factura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    # precio de venta en consignacion
    precio_a_consignacion = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_b_consignacion = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_c_consignacion = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    # precio venta en plan de pago
    precio_a_pp = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_b_pp = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_c_pp = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    user_id_anula = models.IntegerField(blank=True, null=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos'


class Insumos(models.Model):
    insumo_id = models.AutoField(primary_key=True, db_column='insumo_id')
    insumo = models.CharField(max_length=150, null=False, blank=False, default='')
    codigo = models.CharField(max_length=50, null=False, blank=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    posicion = models.IntegerField(null=False, blank=False, default=1)
    precio = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'insumos'


class Componentes(models.Model):
    componente_id = models.AutoField(primary_key=True, db_column='componente_id')
    componente = models.CharField(max_length=150, null=False, blank=False, default='')
    codigo = models.CharField(max_length=50, null=False, blank=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    posicion = models.IntegerField(null=False, blank=False, default=1)
    precio = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    es_aderezo = models.BooleanField(blank=False, null=False, default=False)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'componentes'


class RefrescosGrupo(models.Model):
    refresco_grupo_id = models.AutoField(primary_key=True, db_column='refresco_grupo_id')
    insumo_id = models.IntegerField(blank=False, null=False, default=0)
    componente_id = models.IntegerField(blank=False, null=False, default=0)
    posicion = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'refrescos_grupo'


class PapasGrupo(models.Model):
    papa_grupo_id = models.AutoField(primary_key=True, db_column='papa_grupo_id')
    insumo_id = models.IntegerField(blank=False, null=False, default=0)
    componente_id = models.IntegerField(blank=False, null=False, default=0)
    posicion = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'papas_grupo'


class ProductosInsumos(models.Model):
    producto_insumo_id = models.AutoField(primary_key=True, db_column='producto_insumo_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    insumo_id = models.ForeignKey(Insumos, to_field='insumo_id', on_delete=models.PROTECT, db_column='insumo_id')
    cantidad = models.IntegerField(blank=False, null=False, default=1)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_insumos'


class ProductosComponentes(models.Model):
    producto_componente_id = models.AutoField(primary_key=True, db_column='producto_componente_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    componente_id = models.ForeignKey(Componentes, to_field='componente_id', on_delete=models.PROTECT, db_column='componente_id')
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    posicion = models.IntegerField(blank=False, null=False, default=1)
    defecto = models.BooleanField(blank=False, null=False, default=False)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_componentes'


class ProductosExtras(models.Model):
    producto_extra_id = models.AutoField(primary_key=True, db_column='producto_extra_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    componente_id = models.ForeignKey(Componentes, to_field='componente_id', on_delete=models.PROTECT, db_column='componente_id')
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    precio = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    posicion = models.IntegerField(blank=False, null=False, default=1)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_extras'


class ProductosRefrescos(models.Model):
    producto_refresco_id = models.AutoField(primary_key=True, db_column='producto_refresco_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    insumo_id = models.IntegerField(blank=False, null=False, default=0)
    componente_id = models.IntegerField(blank=False, null=False, default=0)
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    precio = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    posicion = models.IntegerField(blank=False, null=False, default=1)
    defecto = models.BooleanField(blank=False, null=False, default=False)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_refrescos'


class ProductosPapas(models.Model):
    producto_papa_id = models.AutoField(primary_key=True, db_column='producto_papa_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    insumo_id = models.IntegerField(blank=False, null=False, default=0)
    componente_id = models.IntegerField(blank=False, null=False, default=0)
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    precio = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    posicion = models.IntegerField(blank=False, null=False, default=1)
    defecto = models.BooleanField(blank=False, null=False, default=False)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_papas'


class ProductosImagenes(models.Model):
    producto_imagen_id = models.AutoField(primary_key=True, db_column='producto_imagen_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    posicion = models.IntegerField(null=False, blank=False, default=1)

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_imagenes'


class ProductosRelacionados(models.Model):
    producto_relacionado_id = models.AutoField(primary_key=True, db_column='producto_relacionado_id')
    producto_id = models.ForeignKey(Productos, verbose_name='prod1r', related_name='primer_prodr', on_delete=models.PROTECT, db_column='producto_id', to_field='producto_id')
    producto_relacion_id = models.ForeignKey(Productos, verbose_name='prod2r', related_name='segundo_prodr', on_delete=models.PROTECT, db_column='producto_relacion_id', to_field='producto_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'productos_relacionados'


class PuntosPrecios(models.Model):
    producto_punto_precio_id = models.AutoField(primary_key=True, db_column='producto_punto_precio_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    aumento_precio_a = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    aumento_precio_b = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    aumento_precio_c = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    aumento_precio_a_factura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    aumento_precio_b_factura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    aumento_precio_c_factura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    aumento_precio_a_consignacion = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    aumento_precio_b_consignacion = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    aumento_precio_c_consignacion = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    aumento_precio_a_pp = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    aumento_precio_b_pp = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    aumento_precio_c_pp = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'puntos_precios'
