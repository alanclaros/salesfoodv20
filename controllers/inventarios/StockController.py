from status.models import Status
from permisos.models import UsersPerfiles
from productos.models import Insumos, Productos, ProductosInsumos
from inventarios.models import Stock
from configuraciones.models import Puntos, PuntosAlmacenes, Almacenes

from controllers.DefaultValues import DefaultValues

from django.db import transaction


class StockController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)

        self.table_name = 'registros'
        self.table_id = 'registro_id'

    def update_stock(self, user_perfil, almacen, producto, cantidad, fecha_elaboracion=None, fecha_vencimiento=None, lote=''):
        """actualizamos el stock"""
        try:
            with transaction.atomic():
                # productos normales
                stock_filter = Stock.objects.filter(almacen_id=almacen, insumo_id=producto, fecha_elaboracion=fecha_elaboracion, fecha_vencimiento=fecha_vencimiento, lote=lote.upper())
                stock = stock_filter.first()
                if not stock:
                    # creamos el registro
                    stock = Stock.objects.create(almacen_id=almacen, insumo_id=producto, fecha_elaboracion=fecha_elaboracion,
                                                 fecha_vencimiento=fecha_vencimiento, lote=lote.upper(), user_perfil_id=user_perfil, status_id=self.status_activo)

                cantidad_update = stock.cantidad + cantidad
                stock.cantidad = cantidad_update
                stock.save()

            return True

        except Exception as ex:
            print('Error update stock: ' + str(ex))
            self.error_operation = 'Error al actualizar stock, ' + str(ex)
            return False

    def stock_producto(self, producto_id, user_perfil, almacen_id):
        """devuelve el stock del producto"""
        try:
            almacen = Almacenes.objects.get(pk=almacen_id)
            #producto = Productos.objects.get(pk=producto_id)
            producto = Insumos.objects.get(pk=producto_id)

            filtros = {}
            filtros['almacen_id'] = almacen
            filtros['cantidad__gt'] = 0
            filtros['insumo_id'] = producto
            stock_almacen = Stock.objects.filter(**filtros).order_by('fecha_vencimiento', 'fecha_elaboracion', 'lote')

            return stock_almacen

        except Exception as ex:
            self.error_operation = 'Error al recuperar stock, ' + str(ex)
            raise ValueError('Error al recuperar stock del producto, ' + str(ex))

    def stock_producto_insumo(self, producto_id, almacen_id):
        """devuelve el stock del producto con sus insumos"""
        try:
            producto = Productos.objects.get(pk=producto_id)

            productos_insumos = ProductosInsumos.objects.filter(producto_id=producto)
            lista_insumos = []
            for pro_ins in productos_insumos:
                dato_insumo = {}
                dato_insumo['insumo_id'] = pro_ins.insumo_id.insumo_id
                dato_insumo['insumo'] = pro_ins.insumo_id.insumo

                datos_stock = self.stock_producto(pro_ins.insumo_id.insumo_id, None, almacen_id)
                actual = 0
                for dato_aux in datos_stock:
                    actual = actual + int(dato_aux.cantidad)

                dato_insumo['cantidad'] = actual
                lista_insumos.append(dato_insumo)

            return lista_insumos

        except Exception as ex:
            self.error_operation = 'Error al recuperar stock, ' + str(ex)
            raise ValueError('Error al recuperar stock del producto, ' + str(ex))
