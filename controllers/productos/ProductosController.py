from decimal import Decimal
from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from productos.models import Insumos, Componentes, PapasGrupo, Productos, ProductosComponentes, ProductosExtras, ProductosInsumos, ProductosPapas, ProductosRefrescos, ProductosRelacionados, ProductosImagenes, PuntosPrecios, RefrescosGrupo
from permisos.models import UsersPerfiles
from configuraciones.models import Puntos, Lineas
from status.models import Status

from django.db import transaction

import random
import os.path as path

# conexion directa a la base de datos
from django.db import connection

from utils.validators import validate_string, validate_number_int, validate_number_decimal

from controllers.SystemController import SystemController


class ProductosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Productos'
        self.modelo_id = 'producto_id'
        self.modelo_app = 'productos'
        self.modulo_id = settings.MOD_PRODUCTOS

        # variables de session
        self.modulo_session = "productos"
        self.columnas.append('linea_id__linea')
        self.columnas.append('producto')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_linea')
        self.variables_filtros.append('search_producto')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_linea'] = ''
        self.variables_filtros_defecto['search_producto'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'ventas': 'VentasDetalles'}

        # control del formulario
        self.control_form = "txt|2|S|producto|Producto;"
        self.control_form += "txt|2|S|codigo|Codigo;"
        self.control_form += "txt|1|S|unidad|Unidad;"
        self.control_form += "txt|1|S|stock_minimo|Stock Minimo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]
        # linea
        if self.variables_filtros_values['search_linea'].strip() != "":
            self.filtros_modulo['linea_id__linea__icontains'] = self.variables_filtros_values['search_linea'].strip()
        # producto
        if self.variables_filtros_values['search_producto'].strip() != "":
            self.filtros_modulo['producto__icontains'] = self.variables_filtros_values['search_producto'].strip()
        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

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
        retorno = modelo.objects.select_related('linea_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]
        # for key, value in retorno.__dict__.items():
        #     print('key:', key, ' value:', value)

        return retorno

    def is_in_db(self, id, linea, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['producto__iexact'] = nuevo_valor

        # restriccion de productos en general con nombre unico
        # filtros['linea_id'] = linea
        #print('is in db: ', id)

        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        #print('cantidad...: ', cantidad)
        # si no existe
        if cantidad > 0:
            return True

        return False

    def is_codigo_barras_db(self, id, codigo_barras):
        """verificando el codigo de barras"""

        # ahora sin control de codigo de barras
        # modelo = apps.get_model(self.modelo_app, self.modelo_name)
        # filtros = {}
        # filtros['status_id_id__in'] = [self.activo, self.inactivo]
        # filtros['codigo_barras__iexact'] = codigo_barras
        #
        # if id:
        #     cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        # else:
        #     cantidad = modelo.objects.filter(**filtros).count()
        #
        # # si no existe
        # if cantidad > 0:
        #     return True

        return False

    def save(self, request, type='add'):
        """aniadimos un nuevo producto"""
        try:
            linea_id = validate_number_int('linea', request.POST['linea'])
            producto_txt = validate_string('producto', request.POST['producto'], remove_specials='yes')
            codigo_barras = validate_string('codigo barras', request.POST['codigo_barras'], remove_specials='yes', len_zero='yes')
            codigo = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            unidad = validate_string('unidad', request.POST['unidad'], remove_specials='yes')
            stock_minimo = validate_number_int('stock minimo', request.POST['stock_minimo'])
            activo = 1 if 'activo' in request.POST.keys() else 0

            descripcion1 = validate_string('descripcion 1', request.POST['descripcion1'], remove_specials='yes', len_zero='yes')
            descripcion2 = validate_string('descripcion 2', request.POST['descripcion2'], remove_specials='yes', len_zero='yes')
            descripcion3 = validate_string('descripcion 3', request.POST['descripcion3'], remove_specials='yes', len_zero='yes')
            descripcion4 = validate_string('descripcion 4', request.POST['descripcion4'], remove_specials='yes', len_zero='yes')
            descripcion5 = validate_string('descripcion 5', request.POST['descripcion5'], remove_specials='yes', len_zero='yes')
            descripcion6 = validate_string('descripcion 6', request.POST['descripcion6'], remove_specials='yes', len_zero='yes')
            descripcion7 = validate_string('descripcion 7', request.POST['descripcion7'], remove_specials='yes', len_zero='yes')
            descripcion8 = validate_string('descripcion 8', request.POST['descripcion8'], remove_specials='yes', len_zero='yes')
            descripcion9 = validate_string('descripcion 9', request.POST['descripcion9'], remove_specials='yes', len_zero='yes')
            descripcion10 = validate_string('descripcion 10', request.POST['descripcion10'], remove_specials='yes', len_zero='yes')

            costo_a = validate_number_decimal('costo A', request.POST['costo_a'], len_zero='yes')
            costo_b = validate_number_decimal('costo B', request.POST['costo_b'], len_zero='yes')
            costo_c = validate_number_decimal('costo C', request.POST['costo_c'], len_zero='yes')

            precio_a = validate_number_decimal('precio A', request.POST['precio_a'])
            precio_b = validate_number_decimal('precio B', request.POST['precio_b'], len_zero='yes')
            precio_c = validate_number_decimal('precio C', request.POST['precio_c'], len_zero='yes')

            precio_a_factura = validate_number_decimal('precio A factura', request.POST['precio_a_factura'])
            precio_b_factura = validate_number_decimal('precio B factura', request.POST['precio_b_factura'], len_zero='yes')
            precio_c_factura = validate_number_decimal('precio C factura', request.POST['precio_c_factura'], len_zero='yes')

            precio_a_consignacion = validate_number_decimal('precio A consignacion', request.POST['precio_a_consignacion'])
            precio_b_consignacion = validate_number_decimal('precio B consignacion', request.POST['precio_b_consignacion'], len_zero='yes')
            precio_c_consignacion = validate_number_decimal('precio C consignacion', request.POST['precio_c_consignacion'], len_zero='yes')

            precio_a_pp = validate_number_decimal('precio A plan pago', request.POST['precio_a_pp'])
            precio_b_pp = validate_number_decimal('precio B plan pago', request.POST['precio_b_pp'], len_zero='yes')
            precio_c_pp = validate_number_decimal('precio C plan pago', request.POST['precio_c_pp'], len_zero='yes')

            check_refresco = 1 if 'check_refresco' in request.POST.keys() else 0
            check_papa = 1 if 'check_papa' in request.POST.keys() else 0

            id = validate_number_int('id', request.POST['id'], len_zero='yes')
            #print('producto id...', id)

            if not self.is_in_db(id, linea_id, producto_txt):

                # verificamos el codigo de barras
                if self.is_codigo_barras_db(id, codigo_barras):
                    self.error_operation = 'Ya existe este codigo de barras'
                    return False

                # activo
                if activo == 1:
                    status_producto = self.status_activo
                else:
                    status_producto = self.status_inactivo

                # punto
                usuario = request.user
                user_perfil = UsersPerfiles.objects.get(user_id=usuario)
                linea = Lineas.objects.get(pk=linea_id)

                datos = {}
                datos['id'] = id
                datos['producto'] = producto_txt
                datos['codigo'] = codigo
                datos['codigo_barras'] = codigo_barras
                datos['linea_id'] = linea
                datos['unidad'] = unidad
                datos['stock_minimo'] = stock_minimo

                datos['descripcion1'] = descripcion1
                datos['descripcion2'] = descripcion2
                datos['descripcion3'] = descripcion3
                datos['descripcion4'] = descripcion4
                datos['descripcion5'] = descripcion5
                datos['descripcion6'] = descripcion6
                datos['descripcion7'] = descripcion7
                datos['descripcion8'] = descripcion8
                datos['descripcion9'] = descripcion9
                datos['descripcion10'] = descripcion10

                datos['costo_a'] = costo_a
                datos['costo_b'] = costo_b
                datos['costo_c'] = costo_c

                datos['precio_a'] = precio_a
                datos['precio_b'] = precio_b
                datos['precio_c'] = precio_c

                datos['precio_a_factura'] = precio_a_factura
                datos['precio_b_factura'] = precio_b_factura
                datos['precio_c_factura'] = precio_c_factura

                datos['precio_a_consignacion'] = precio_a_consignacion
                datos['precio_b_consignacion'] = precio_b_consignacion
                datos['precio_c_consignacion'] = precio_c_consignacion

                datos['precio_a_pp'] = precio_a_pp
                datos['precio_b_pp'] = precio_b_pp
                datos['precio_c_pp'] = precio_c_pp

                datos['created_at'] = 'now'
                datos['updated_at'] = 'now'
                datos['user_perfil_id'] = user_perfil
                datos['status_id'] = status_producto
                #datos['punto_id'] = punto

                # check refresco
                datos['check_refresco'] = check_refresco
                datos['check_papa'] = check_papa

                lista_para_refresco = []
                if check_refresco == 1:
                    lista_de_refresco = self.lista_refrescos()

                    for refresco_aux in lista_de_refresco:
                        nombre1 = 'check_refresco_' + str(refresco_aux['refresco_grupo_id'])
                        nombre2 = 'refresco_precio_'+str(refresco_aux['refresco_grupo_id'])
                        nombre3 = 'check_refresco_def_'+str(refresco_aux['refresco_grupo_id'])
                        nombre4 = 'refresco_pos_'+str(refresco_aux['refresco_grupo_id'])

                        if nombre1 in request.POST.keys():
                            aux_pr = request.POST[nombre2]

                            precio_refresco = 0 if aux_pr == '' else Decimal(aux_pr)

                            if nombre3 in request.POST.keys():
                                defecto_refresco = int(request.POST[nombre3])
                            else:
                                defecto_refresco = 0

                            pos_refresco = 0 if request.POST[nombre4].strip() == '' else int(request.POST[nombre4].strip())

                            dato_ref = {}
                            dato_ref['refresco_grupo_id'] = refresco_aux['refresco_grupo_id']
                            dato_ref['precio'] = precio_refresco
                            dato_ref['defecto'] = defecto_refresco
                            dato_ref['posicion'] = pos_refresco

                            lista_para_refresco.append(dato_ref)

                #print('lista refresco: ', lista_para_refresco)
                datos['lista_refresco'] = lista_para_refresco

                # papas
                lista_para_papa = []
                if check_papa == 1:
                    lista_de_papa = self.lista_papas()
                    for papa_aux in lista_de_papa:
                        if 'check_papa_' + str(papa_aux['papa_grupo_id']) in request.POST.keys():

                            aux_papa = request.POST['papa_precio_'+str(papa_aux['papa_grupo_id'])]
                            precio_papa = 0 if aux_papa == '' else Decimal(aux_papa)

                            if 'check_papa_def_'+str(papa_aux['papa_grupo_id']) in request.POST.keys():
                                defecto_papa = int(request.POST['check_papa_def_'+str(papa_aux['papa_grupo_id'])])
                            else:
                                defecto_papa = 0

                            pos_papa = 0 if request.POST['papa_pos_'+str(papa_aux['papa_grupo_id'])].strip() == '' else int(request.POST['papa_pos_'+str(papa_aux['papa_grupo_id'])].strip())

                            dato_papa = {}
                            dato_papa['papa_grupo_id'] = papa_aux['papa_grupo_id']
                            dato_papa['precio'] = precio_papa
                            dato_papa['defecto'] = defecto_papa
                            dato_papa['posicion'] = pos_papa
                            lista_para_papa.append(dato_papa)

                #print('lista papa: ', lista_para_papa)
                datos['lista_papa'] = lista_para_papa

                # datos relacionados
                datos_relacionados = []

                if 'lista_relacionado' in request.session.keys():
                    lista_relacionado = request.session['lista_relacionado']
                    for relacionado in lista_relacionado:
                        dato_producto = {}
                        dato_producto['producto_id'] = relacionado['producto_relacionado_id']
                        datos_relacionados.append(dato_producto)

                #print('datos relacionado:', datos_relacionados)
                datos['datos_relacionados'] = datos_relacionados

                # insumos
                datos_insumos = []
                if 'lista_insumo' in request.session.keys():
                    lista_insumo = request.session['lista_insumo']
                    for insumo in lista_insumo:
                        dato_insumo = {}
                        dato_insumo['insumo_id'] = insumo['insumo_id']
                        dato_insumo['cantidad'] = insumo['cantidad']
                        datos_insumos.append(dato_insumo)

                #print('datos insumos: ', datos_insumos)
                datos['datos_insumos'] = datos_insumos

                # componentes
                datos_componentes = []
                if 'lista_componente' in request.session.keys():
                    lista_componente = request.session['lista_componente']
                    for componente in lista_componente:
                        dato_componente = {}
                        dato_componente['componente_id'] = componente['componente_id']
                        dato_componente['cantidad'] = componente['cantidad']
                        dato_componente['defecto'] = componente['defecto']
                        dato_componente['posicion'] = componente['posicion']
                        datos_componentes.append(dato_componente)

                #print('datos componentes: ', datos_componentes)
                datos['datos_componentes'] = datos_componentes

                # extras
                datos_extras = []
                if 'lista_extra' in request.session.keys():
                    lista_extra = request.session['lista_extra']
                    for extra in lista_extra:
                        dato_extra = {}
                        dato_extra['extra_id'] = extra['extra_id']
                        dato_extra['precio'] = extra['precio']
                        dato_extra['posicion'] = extra['posicion']
                        datos_extras.append(dato_extra)

                #print('datos extras: ', datos_extras)
                datos['datos_extras'] = datos_extras

                if self.save_db(type, **datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            else:
                self.error_operation = "Ya existe este producto: " + producto_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar producto, " + str(ex)
            print('Error: ', str(ex))
            return False

    def save_db(self, type='add', **datos):
        """aniadimos a la base de datos"""
        try:

            if not self.is_in_db(datos['id'], datos['linea_id'].linea_id, datos['producto']):

                if type == 'add':

                    with transaction.atomic():
                        campos_add = {}
                        campos_add['producto'] = datos['producto']
                        campos_add['codigo'] = datos['codigo']
                        campos_add['codigo_barras'] = datos['codigo_barras']
                        campos_add['linea_id'] = datos['linea_id']
                        campos_add['unidad'] = datos['unidad']
                        campos_add['stock_minimo'] = datos['stock_minimo']

                        campos_add['descripcion1'] = datos['descripcion1']
                        campos_add['descripcion2'] = datos['descripcion2']
                        campos_add['descripcion3'] = datos['descripcion3']
                        campos_add['descripcion4'] = datos['descripcion4']
                        campos_add['descripcion5'] = datos['descripcion5']
                        campos_add['descripcion6'] = datos['descripcion6']
                        campos_add['descripcion7'] = datos['descripcion7']
                        campos_add['descripcion8'] = datos['descripcion8']
                        campos_add['descripcion9'] = datos['descripcion9']
                        campos_add['descripcion10'] = datos['descripcion10']

                        campos_add['costo_a'] = datos['costo_a']
                        campos_add['costo_b'] = datos['costo_b']
                        campos_add['costo_c'] = datos['costo_c']

                        campos_add['precio_a'] = datos['precio_a']
                        campos_add['precio_b'] = datos['precio_b']
                        campos_add['precio_c'] = datos['precio_c']

                        campos_add['precio_a_factura'] = datos['precio_a_factura']
                        campos_add['precio_b_factura'] = datos['precio_b_factura']
                        campos_add['precio_c_factura'] = datos['precio_c_factura']

                        campos_add['precio_a_consignacion'] = datos['precio_a_consignacion']
                        campos_add['precio_b_consignacion'] = datos['precio_b_consignacion']
                        campos_add['precio_c_consignacion'] = datos['precio_c_consignacion']

                        campos_add['precio_a_pp'] = datos['precio_a_pp']
                        campos_add['precio_b_pp'] = datos['precio_b_pp']
                        campos_add['precio_c_pp'] = datos['precio_c_pp']

                        campos_add['created_at'] = datos['created_at']
                        campos_add['updated_at'] = datos['updated_at']
                        campos_add['user_perfil_id'] = datos['user_perfil_id']
                        campos_add['status_id'] = datos['status_id']
                        #campos_add['punto_id'] = datos['punto_id']

                        producto_add = Productos.objects.create(**campos_add)
                        producto_add.save()

                        # borramos antes de insertar productos relacionados
                        productos_relacionados_lista = ProductosRelacionados.objects.filter(producto_id=producto_add)
                        productos_relacionados_lista.delete()

                        for producto in datos['datos_relacionados']:
                            producto_relacion = Productos.objects.get(pk=producto['producto_id'])
                            producto_relacionado = ProductosRelacionados.objects.create(producto_id=producto_add, producto_relacion_id=producto_relacion,
                                                                                        status_id=datos['status_id'], created_at='now', updated_at='now')
                            producto_relacionado.save()

                        # insumos
                        productos_insumos = ProductosInsumos.objects.filter(producto_id=producto_add)
                        productos_insumos.delete()
                        for insumo in datos['datos_insumos']:
                            insumo_aux = Insumos.objects.get(pk=int(insumo['insumo_id']))
                            producto_insumo_add = ProductosInsumos.objects.create(producto_id=producto_add, insumo_id=insumo_aux, status_id=self.status_activo, cantidad=int(insumo['cantidad']),
                                                                                  created_at='now', updated_at='now')
                            producto_insumo_add.save()

                        # componentes
                        productos_componentes = ProductosComponentes.objects.filter(producto_id=producto_add)
                        productos_componentes.delete()
                        for componente in datos['datos_componentes']:
                            componente_aux = Componentes.objects.get(pk=int(componente['componente_id']))
                            producto_componente_add = ProductosComponentes.objects.create(producto_id=producto_add, componente_id=componente_aux, status_id=self.status_activo, cantidad=int(componente['cantidad']),
                                                                                          defecto=componente['defecto'], posicion=componente['posicion'], created_at='now', updated_at='now')
                            producto_componente_add.save()

                        # extras
                        productos_extras = ProductosExtras.objects.filter(producto_id=producto_add)
                        productos_extras.delete()
                        for extra in datos['datos_extras']:
                            componente_aux = Componentes.objects.get(pk=int(extra['extra_id']))
                            producto_extra_add = ProductosExtras.objects.create(producto_id=producto_add, componente_id=componente_aux, status_id=self.status_activo, cantidad=1, precio=Decimal(extra['precio']),
                                                                                posicion=extra['posicion'], created_at='now', updated_at='now')
                            producto_extra_add.save()

                        # refrescos
                        productos_refrescos = ProductosRefrescos.objects.filter(producto_id=producto_add)
                        productos_refrescos.delete()
                        if datos['check_refresco'] == 1:
                            for refresco in datos['lista_refresco']:
                                refresco_grupo = RefrescosGrupo.objects.get(pk=int(refresco['refresco_grupo_id']))
                                producto_refresco_add = ProductosRefrescos.objects.create(producto_id=producto_add, status_id=self.status_activo, cantidad=1, precio=Decimal(refresco['precio']),
                                                                                          defecto=refresco['defecto'], posicion=refresco['posicion'], insumo_id=refresco_grupo.insumo_id, componente_id=refresco_grupo.componente_id, created_at='now', updated_at='now')
                                producto_refresco_add.save()

                        # papas
                        productos_papas = ProductosPapas.objects.filter(producto_id=producto_add)
                        productos_papas.delete()
                        if datos['check_papa'] == 1:
                            for papa in datos['lista_papa']:
                                papa_grupo = PapasGrupo.objects.get(pk=int(papa['papa_grupo_id']))
                                producto_papa_add = ProductosPapas.objects.create(producto_id=producto_add, status_id=self.status_activo, cantidad=1, precio=Decimal(papa['precio']),
                                                                                  defecto=papa['defecto'], posicion=papa['posicion'], insumo_id=papa_grupo.insumo_id, componente_id=papa_grupo.componente_id, created_at='now', updated_at='now')
                                producto_papa_add.save()

                        self.error_operation = ''
                        return True

                if type == 'modify':
                    with transaction.atomic():
                        campos_update = {}
                        campos_update['producto'] = datos['producto']
                        campos_update['codigo'] = datos['codigo']
                        campos_update['codigo_barras'] = datos['codigo_barras']
                        campos_update['linea_id'] = datos['linea_id']
                        campos_update['unidad'] = datos['unidad']
                        campos_update['stock_minimo'] = datos['stock_minimo']

                        campos_update['descripcion1'] = datos['descripcion1']
                        campos_update['descripcion2'] = datos['descripcion2']
                        campos_update['descripcion3'] = datos['descripcion3']
                        campos_update['descripcion4'] = datos['descripcion4']
                        campos_update['descripcion5'] = datos['descripcion5']
                        campos_update['descripcion6'] = datos['descripcion6']
                        campos_update['descripcion7'] = datos['descripcion7']
                        campos_update['descripcion8'] = datos['descripcion8']
                        campos_update['descripcion9'] = datos['descripcion9']
                        campos_update['descripcion10'] = datos['descripcion10']

                        campos_update['costo_a'] = datos['costo_a']
                        campos_update['costo_b'] = datos['costo_b']
                        campos_update['costo_c'] = datos['costo_c']

                        campos_update['precio_a'] = datos['precio_a']
                        campos_update['precio_b'] = datos['precio_b']
                        campos_update['precio_c'] = datos['precio_c']

                        campos_update['precio_a_factura'] = datos['precio_a_factura']
                        campos_update['precio_b_factura'] = datos['precio_b_factura']
                        campos_update['precio_c_factura'] = datos['precio_c_factura']

                        campos_update['precio_a_consignacion'] = datos['precio_a_consignacion']
                        campos_update['precio_b_consignacion'] = datos['precio_b_consignacion']
                        campos_update['precio_c_consignacion'] = datos['precio_c_consignacion']

                        campos_update['precio_a_pp'] = datos['precio_a_pp']
                        campos_update['precio_b_pp'] = datos['precio_b_pp']
                        campos_update['precio_c_pp'] = datos['precio_c_pp']

                        campos_update['created_at'] = datos['created_at']
                        campos_update['updated_at'] = datos['updated_at']
                        #campos_update['user_id'] = datos['user_id']
                        campos_update['status_id'] = datos['status_id']

                        producto_update = Productos.objects.filter(pk=datos['id'])
                        producto_update.update(**campos_update)

                        producto_actual = Productos.objects.get(pk=datos['id'])

                        # borramos antes de insertar productos relacionados
                        productos_relacionados_lista = ProductosRelacionados.objects.filter(producto_id=producto_actual)
                        productos_relacionados_lista.delete()

                        for producto in datos['datos_relacionados']:
                            producto_relacion = Productos.objects.get(pk=producto['producto_id'])
                            producto_relacionado = ProductosRelacionados.objects.create(producto_id=producto_actual, producto_relacion_id=producto_relacion,
                                                                                        status_id=datos['status_id'], created_at='now', updated_at='now')
                            producto_relacionado.save()

                        # insumos
                        productos_insumos = ProductosInsumos.objects.filter(producto_id=producto_actual)
                        productos_insumos.delete()
                        for insumo in datos['datos_insumos']:
                            insumo_aux = Insumos.objects.get(pk=int(insumo['insumo_id']))
                            producto_insumo_add = ProductosInsumos.objects.create(producto_id=producto_actual, insumo_id=insumo_aux, status_id=self.status_activo, cantidad=int(insumo['cantidad']),
                                                                                  created_at='now', updated_at='now')
                            producto_insumo_add.save()

                        # componentes
                        productos_componentes = ProductosComponentes.objects.filter(producto_id=producto_actual)
                        productos_componentes.delete()
                        for componente in datos['datos_componentes']:
                            componente_aux = Componentes.objects.get(pk=int(componente['componente_id']))
                            producto_componente_add = ProductosComponentes.objects.create(producto_id=producto_actual, componente_id=componente_aux, status_id=self.status_activo, cantidad=int(componente['cantidad']),
                                                                                          defecto=componente['defecto'], posicion=componente['posicion'], created_at='now', updated_at='now')
                            producto_componente_add.save()

                        # extras
                        productos_extras = ProductosExtras.objects.filter(producto_id=producto_actual)
                        productos_extras.delete()
                        for extra in datos['datos_extras']:
                            componente_aux = Componentes.objects.get(pk=int(extra['extra_id']))
                            producto_extra_add = ProductosExtras.objects.create(producto_id=producto_actual, componente_id=componente_aux, status_id=self.status_activo, cantidad=1, precio=Decimal(extra['precio']),
                                                                                posicion=extra['posicion'], created_at='now', updated_at='now')
                            producto_extra_add.save()

                        # refrescos
                        productos_refrescos = ProductosRefrescos.objects.filter(producto_id=producto_actual)
                        productos_refrescos.delete()
                        if datos['check_refresco'] == 1:
                            for refresco in datos['lista_refresco']:
                                refresco_grupo = RefrescosGrupo.objects.get(pk=int(refresco['refresco_grupo_id']))
                                producto_refresco_add = ProductosRefrescos.objects.create(producto_id=producto_actual, status_id=self.status_activo, cantidad=1, precio=Decimal(refresco['precio']),
                                                                                          defecto=refresco['defecto'], posicion=refresco['posicion'], insumo_id=refresco_grupo.insumo_id, componente_id=refresco_grupo.componente_id, created_at='now', updated_at='now')
                                producto_refresco_add.save()

                        # papas
                        productos_papas = ProductosPapas.objects.filter(producto_id=producto_actual)
                        productos_papas.delete()
                        if datos['check_papa'] == 1:
                            for papa in datos['lista_papa']:
                                papa_grupo = PapasGrupo.objects.get(pk=int(papa['papa_grupo_id']))
                                producto_papa_add = ProductosPapas.objects.create(producto_id=producto_actual, status_id=self.status_activo, cantidad=1, precio=Decimal(papa['precio']),
                                                                                  defecto=papa['defecto'], posicion=papa['posicion'], insumo_id=papa_grupo.insumo_id, componente_id=papa_grupo.componente_id, created_at='now', updated_at='now')
                                producto_papa_add.save()

                        self.error_operation = ''
                        return True

                self.error_operation = 'operation no valid db'
                return False
            else:
                self.error_operation = "Ya existe este producto: " + datos['producto']
                return False

        except Exception as ex:
            self.error_operation = 'error de argumentos,' + str(ex)
            print('ERROR productos add, ' + str(ex))
            return False

    # def modify(self, request, id):
    #     """modificamos el producto"""
    #     try:
    #         linea_id = validate_number_int('linea', request.POST['linea'])
    #         producto_txt = validate_string('producto', request.POST['producto'], remove_specials='yes')
    #         codigo_barras = validate_string('codigo barras', request.POST['codigo_barras'], remove_specials='yes', len_zero='yes')
    #         codigo = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
    #         unidad = validate_string('unidad', request.POST['unidad'], remove_specials='yes')
    #         stock_minimo = validate_number_int('stock minimo', request.POST['stock_minimo'])
    #         activo = 1 if 'activo' in request.POST.keys() else 0

    #         descripcion1 = validate_string('descripcion 1', request.POST['descripcion1'], remove_specials='yes', len_zero='yes')
    #         descripcion2 = validate_string('descripcion 2', request.POST['descripcion2'], remove_specials='yes', len_zero='yes')
    #         descripcion3 = validate_string('descripcion 3', request.POST['descripcion3'], remove_specials='yes', len_zero='yes')
    #         descripcion4 = validate_string('descripcion 4', request.POST['descripcion4'], remove_specials='yes', len_zero='yes')
    #         descripcion5 = validate_string('descripcion 5', request.POST['descripcion5'], remove_specials='yes', len_zero='yes')
    #         descripcion6 = validate_string('descripcion 6', request.POST['descripcion6'], remove_specials='yes', len_zero='yes')
    #         descripcion7 = validate_string('descripcion 7', request.POST['descripcion7'], remove_specials='yes', len_zero='yes')
    #         descripcion8 = validate_string('descripcion 8', request.POST['descripcion8'], remove_specials='yes', len_zero='yes')
    #         descripcion9 = validate_string('descripcion 9', request.POST['descripcion9'], remove_specials='yes', len_zero='yes')
    #         descripcion10 = validate_string('descripcion 10', request.POST['descripcion10'], remove_specials='yes', len_zero='yes')

    #         costo_a = validate_number_decimal('costo A', request.POST['costo_a'], len_zero='yes')
    #         costo_b = validate_number_decimal('costo B', request.POST['costo_b'], len_zero='yes')
    #         costo_c = validate_number_decimal('costo C', request.POST['costo_c'], len_zero='yes')

    #         precio_a = validate_number_decimal('precio A', request.POST['precio_a'])
    #         precio_b = validate_number_decimal('precio B', request.POST['precio_b'], len_zero='yes')
    #         precio_c = validate_number_decimal('precio C', request.POST['precio_c'], len_zero='yes')

    #         precio_a_factura = validate_number_decimal('precio A factura', request.POST['precio_a_factura'])
    #         precio_b_factura = validate_number_decimal('precio B factura', request.POST['precio_b_factura'], len_zero='yes')
    #         precio_c_factura = validate_number_decimal('precio C factura', request.POST['precio_c_factura'], len_zero='yes')

    #         precio_a_consignacion = validate_number_decimal('precio A consignacion', request.POST['precio_a_consignacion'])
    #         precio_b_consignacion = validate_number_decimal('precio B consignacion', request.POST['precio_b_consignacion'], len_zero='yes')
    #         precio_c_consignacion = validate_number_decimal('precio C consignacion', request.POST['precio_c_consignacion'], len_zero='yes')

    #         precio_a_pp = validate_number_decimal('precio A plan pago', request.POST['precio_a_pp'])
    #         precio_b_pp = validate_number_decimal('precio B plan pago', request.POST['precio_b_pp'], len_zero='yes')
    #         precio_c_pp = validate_number_decimal('precio C plan pago', request.POST['precio_c_pp'], len_zero='yes')

    #         check_refresco = 1 if 'check_refresco' in request.POST.keys() else 0
    #         check_papa = 1 if 'check_papa' in request.POST.keys() else 0

    #         if not self.is_in_db(id, linea_id, producto_txt):
    #             # verificamos el codigo de barras
    #             if self.is_codigo_barras_db(None, codigo_barras):
    #                 self.error_operation = 'Ya existe este codigo de barras'
    #                 return False

    #             # activo
    #             if activo == 1:
    #                 status_producto = self.status_activo
    #             else:
    #                 status_producto = self.status_inactivo

    #             # punto
    #             usuario = request.user
    #             # UsuarioPerfil = UsersPerfiles.objects.get(user_id=usuario)
    #             # punto = Puntos.objects.get(pk=UsuarioPerfil.punto_id)
    #             linea = Lineas.objects.get(pk=linea_id)

    #             datos = {}
    #             datos['producto'] = producto_txt
    #             datos['codigo'] = codigo
    #             datos['codigo_barras'] = codigo_barras
    #             datos['linea_id'] = linea
    #             datos['unidad'] = unidad
    #             datos['stock_minimo'] = stock_minimo

    #             datos['descripcion1'] = descripcion1
    #             datos['descripcion2'] = descripcion2
    #             datos['descripcion3'] = descripcion3
    #             datos['descripcion4'] = descripcion4
    #             datos['descripcion5'] = descripcion5
    #             datos['descripcion6'] = descripcion6
    #             datos['descripcion7'] = descripcion7
    #             datos['descripcion8'] = descripcion8
    #             datos['descripcion9'] = descripcion9
    #             datos['descripcion10'] = descripcion10

    #             datos['costo_a'] = costo_a
    #             datos['costo_b'] = costo_b
    #             datos['costo_c'] = costo_c

    #             datos['precio_a'] = precio_a
    #             datos['precio_b'] = precio_b
    #             datos['precio_c'] = precio_c

    #             datos['precio_a_factura'] = precio_a_factura
    #             datos['precio_b_factura'] = precio_b_factura
    #             datos['precio_c_factura'] = precio_c_factura

    #             datos['precio_a_consignacion'] = precio_a_consignacion
    #             datos['precio_b_consignacion'] = precio_b_consignacion
    #             datos['precio_c_consignacion'] = precio_c_consignacion

    #             datos['precio_a_pp'] = precio_a_pp
    #             datos['precio_b_pp'] = precio_b_pp
    #             datos['precio_c_pp'] = precio_c_pp

    #             datos['created_at'] = 'now'
    #             datos['updated_at'] = 'now'
    #             datos['user_id'] = usuario
    #             datos['status_id'] = status_producto
    #             #datos['punto_id'] = punto

    #             # check refresco
    #             datos['check_refresco'] = check_refresco
    #             datos['check_papa'] = check_papa

    #             lista_para_refresco = []
    #             if check_refresco == 1:
    #                 lista_de_refresco = self.lista_refrescos()

    #                 for refresco_aux in lista_de_refresco:
    #                     nombre1 = 'check_refresco_' + str(refresco_aux['refresco_grupo_id'])
    #                     nombre2 = 'refresco_precio_'+str(refresco_aux['refresco_grupo_id'])
    #                     nombre3 = 'check_refresco_def_'+str(refresco_aux['refresco_grupo_id'])
    #                     nombre4 = 'refresco_pos_'+str(refresco_aux['refresco_grupo_id'])

    #                     if nombre1 in request.POST.keys():
    #                         aux_pr = request.POST[nombre2]

    #                         precio_refresco = 0 if aux_pr == '' else Decimal(aux_pr)

    #                         if nombre3 in request.POST.keys():
    #                             defecto_refresco = int(request.POST[nombre3])
    #                         else:
    #                             defecto_refresco = 0

    #                         pos_refresco = 0 if request.POST[nombre4].strip() == '' else int(request.POST[nombre4].strip())

    #                         dato_ref = {}
    #                         dato_ref['refresco_grupo_id'] = refresco_aux['refresco_grupo_id']
    #                         dato_ref['precio'] = precio_refresco
    #                         dato_ref['defecto'] = defecto_refresco
    #                         dato_ref['posicion'] = pos_refresco

    #                         lista_para_refresco.append(dato_ref)

    #             #print('lista refresco: ', lista_para_refresco)
    #             datos['lista_refresco'] = lista_para_refresco

    #             # papas
    #             lista_para_papa = []
    #             if check_papa == 1:
    #                 lista_de_papa = self.lista_papas()
    #                 for papa_aux in lista_de_papa:
    #                     if 'check_papa_' + str(papa_aux['papa_grupo_id']) in request.POST.keys():

    #                         aux_papa = request.POST['papa_precio_'+str(papa_aux['papa_grupo_id'])]
    #                         precio_papa = 0 if aux_papa == '' else Decimal(aux_papa)

    #                         if 'check_papa_def_'+str(papa_aux['papa_grupo_id']) in request.POST.keys():
    #                             defecto_papa = int(request.POST['check_papa_def_'+str(papa_aux['papa_grupo_id'])])
    #                         else:
    #                             defecto_papa = 0

    #                         pos_papa = 0 if request.POST['papa_pos_'+str(papa_aux['papa_grupo_id'])].strip() == '' else int(request.POST['papa_pos_'+str(papa_aux['papa_grupo_id'])].strip())

    #                         dato_papa = {}
    #                         dato_papa['papa_grupo_id'] = papa_aux['papa_grupo_id']
    #                         dato_papa['precio'] = precio_papa
    #                         dato_papa['defecto'] = defecto_papa
    #                         dato_papa['posicion'] = pos_papa
    #                         lista_para_papa.append(dato_papa)

    #             #print('lista papa: ', lista_para_papa)
    #             datos['lista_papa'] = lista_para_papa

    #             # datos relacionados
    #             datos_relacionados = []

    #             if 'lista_relacionado' in request.session.keys():
    #                 lista_relacionado = request.session['lista_relacionado']
    #                 for relacionado in lista_relacionado:
    #                     dato_producto = {}
    #                     dato_producto['producto_id'] = relacionado['producto_relacionado_id']
    #                     datos_relacionados.append(dato_producto)

    #             #print('datos relacionado:', datos_relacionados)
    #             datos['datos_relacionados'] = datos_relacionados

    #             # insumos
    #             datos_insumos = []
    #             if 'lista_insumo' in request.session.keys():
    #                 lista_insumo = request.session['lista_insumo']
    #                 for insumo in lista_insumo:
    #                     dato_insumo = {}
    #                     dato_insumo['insumo_id'] = insumo['insumo_id']
    #                     dato_insumo['cantidad'] = insumo['cantidad']
    #                     datos_insumos.append(dato_insumo)

    #             #print('datos insumos: ', datos_insumos)
    #             datos['datos_insumos'] = datos_insumos

    #             # componentes
    #             datos_componentes = []
    #             if 'lista_componente' in request.session.keys():
    #                 lista_componente = request.session['lista_componente']
    #                 for componente in lista_componente:
    #                     dato_componente = {}
    #                     dato_componente['componente_id'] = componente['componente_id']
    #                     dato_componente['cantidad'] = componente['cantidad']
    #                     dato_componente['defecto'] = componente['defecto']
    #                     dato_componente['posicion'] = componente['posicion']
    #                     datos_componentes.append(dato_componente)

    #             #print('datos componentes: ', datos_componentes)
    #             datos['datos_componentes'] = datos_componentes

    #             # extras
    #             datos_extras = []
    #             if 'lista_extra' in request.session.keys():
    #                 lista_extra = request.session['lista_extra']
    #                 for extra in lista_extra:
    #                     dato_extra = {}
    #                     dato_extra['extra_id'] = extra['extra_id']
    #                     dato_extra['precio'] = extra['precio']
    #                     dato_extra['posicion'] = extra['posicion']
    #                     datos_extras.append(dato_extra)

    #             #print('datos extras: ', datos_extras)
    #             datos['datos_extras'] = datos_extras

    #             if self.modify_db(id, **datos):
    #                 self.error_operation = ""
    #                 return True
    #             else:
    #                 return False
    #         else:
    #             self.error_operation = "Ya existe este producto: " + producto_txt
    #             return False

    #     except Exception as ex:
    #         self.error_operation = "Error al actualizar el producto, " + str(ex)
    #         return False

    # def modify_db(self, id, **datos):
    #     """actualizamos a la base de datos"""
    #     try:
    #         if not self.is_in_db(id, datos['linea_id'].linea_id, datos['producto']):
    #             with transaction.atomic():
    #                 campos_update = {}
    #                 campos_update['producto'] = datos['producto']
    #                 campos_update['codigo'] = datos['codigo']
    #                 campos_update['codigo_barras'] = datos['codigo_barras']
    #                 campos_update['linea_id'] = datos['linea_id']
    #                 campos_update['unidad'] = datos['unidad']
    #                 campos_update['stock_minimo'] = datos['stock_minimo']

    #                 campos_update['descripcion1'] = datos['descripcion1']
    #                 campos_update['descripcion2'] = datos['descripcion2']
    #                 campos_update['descripcion3'] = datos['descripcion3']
    #                 campos_update['descripcion4'] = datos['descripcion4']
    #                 campos_update['descripcion5'] = datos['descripcion5']
    #                 campos_update['descripcion6'] = datos['descripcion6']
    #                 campos_update['descripcion7'] = datos['descripcion7']
    #                 campos_update['descripcion8'] = datos['descripcion8']
    #                 campos_update['descripcion9'] = datos['descripcion9']
    #                 campos_update['descripcion10'] = datos['descripcion10']

    #                 campos_update['costo_a'] = datos['costo_a']
    #                 campos_update['costo_b'] = datos['costo_b']
    #                 campos_update['costo_c'] = datos['costo_c']

    #                 campos_update['precio_a'] = datos['precio_a']
    #                 campos_update['precio_b'] = datos['precio_b']
    #                 campos_update['precio_c'] = datos['precio_c']

    #                 campos_update['precio_a_factura'] = datos['precio_a_factura']
    #                 campos_update['precio_b_factura'] = datos['precio_b_factura']
    #                 campos_update['precio_c_factura'] = datos['precio_c_factura']

    #                 campos_update['precio_a_consignacion'] = datos['precio_a_consignacion']
    #                 campos_update['precio_b_consignacion'] = datos['precio_b_consignacion']
    #                 campos_update['precio_c_consignacion'] = datos['precio_c_consignacion']

    #                 campos_update['precio_a_pp'] = datos['precio_a_pp']
    #                 campos_update['precio_b_pp'] = datos['precio_b_pp']
    #                 campos_update['precio_c_pp'] = datos['precio_c_pp']

    #                 campos_update['created_at'] = datos['created_at']
    #                 campos_update['updated_at'] = datos['updated_at']
    #                 campos_update['user_id'] = datos['user_id']
    #                 campos_update['status_id'] = datos['status_id']

    #                 producto_update = Productos.objects.filter(pk=id)
    #                 producto_update.update(**campos_update)

    #                 producto_actual = Productos.objects.get(pk=id)

    #                 # borramos antes de insertar productos relacionados
    #                 productos_relacionados_lista = ProductosRelacionados.objects.filter(producto_id=producto_actual)
    #                 productos_relacionados_lista.delete()

    #                 for producto in datos['datos_relacionados']:
    #                     producto_relacion = Productos.objects.get(pk=producto['producto_id'])
    #                     producto_relacionado = ProductosRelacionados.objects.create(producto_id=producto_actual, producto_relacion_id=producto_relacion,
    #                                                                                 status_id=datos['status_id'], created_at='now', updated_at='now')
    #                     producto_relacionado.save()

    #                 # insumos
    #                 productos_insumos = ProductosInsumos.objects.filter(producto_id=producto_actual)
    #                 productos_insumos.delete()
    #                 for insumo in datos['datos_insumos']:
    #                     insumo_aux = Insumos.objects.get(pk=int(insumo['insumo_id']))
    #                     producto_insumo_add = ProductosInsumos.objects.create(producto_id=producto_actual, insumo_id=insumo_aux, status_id=self.status_activo, cantidad=int(insumo['cantidad']),
    #                                                                           created_at='now', updated_at='now')
    #                     producto_insumo_add.save()

    #                 # componentes
    #                 productos_componentes = ProductosComponentes.objects.filter(producto_id=producto_actual)
    #                 productos_componentes.delete()
    #                 for componente in datos['datos_componentes']:
    #                     componente_aux = Componentes.objects.get(pk=int(componente['componente_id']))
    #                     producto_componente_add = ProductosComponentes.objects.create(producto_id=producto_actual, componente_id=componente_aux, status_id=self.status_activo, cantidad=int(componente['cantidad']),
    #                                                                                   defecto=componente['defecto'], posicion=componente['posicion'], created_at='now', updated_at='now')
    #                     producto_componente_add.save()

    #                 # extras
    #                 productos_extras = ProductosExtras.objects.filter(producto_id=producto_actual)
    #                 productos_extras.delete()
    #                 for extra in datos['datos_extras']:
    #                     componente_aux = Componentes.objects.get(pk=int(extra['extra_id']))
    #                     producto_extra_add = ProductosExtras.objects.create(producto_id=producto_actual, componente_id=componente_aux, status_id=self.status_activo, cantidad=1, precio=Decimal(extra['precio']),
    #                                                                         posicion=extra['posicion'], created_at='now', updated_at='now')
    #                     producto_extra_add.save()

    #                 # refrescos
    #                 productos_refrescos = ProductosRefrescos.objects.filter(producto_id=producto_actual)
    #                 productos_refrescos.delete()
    #                 if datos['check_refresco'] == 1:
    #                     for refresco in datos['lista_refresco']:
    #                         refresco_grupo = RefrescosGrupo.objects.get(pk=int(refresco['refresco_grupo_id']))
    #                         producto_refresco_add = ProductosRefrescos.objects.create(producto_id=producto_actual, status_id=self.status_activo, cantidad=1, precio=Decimal(refresco['precio']),
    #                                                                                   defecto=refresco['defecto'], posicion=refresco['posicion'], insumo_id=refresco_grupo.insumo_id, componente_id=refresco_grupo.componente_id, created_at='now', updated_at='now')
    #                         producto_refresco_add.save()

    #                 # papas
    #                 productos_papas = ProductosPapas.objects.filter(producto_id=producto_actual)
    #                 productos_papas.delete()
    #                 if datos['check_papa'] == 1:
    #                     for papa in datos['lista_papa']:
    #                         papa_grupo = PapasGrupo.objects.get(pk=int(papa['papa_grupo_id']))
    #                         producto_papa_add = ProductosPapas.objects.create(producto_id=producto_actual, status_id=self.status_activo, cantidad=1, precio=Decimal(papa['precio']),
    #                                                                           defecto=papa['defecto'], posicion=papa['posicion'], insumo_id=papa_grupo.insumo_id, componente_id=papa_grupo.componente_id, created_at='now', updated_at='now')
    #                         producto_papa_add.save()

    #                 self.error_operation = ''
    #                 return True
    #         else:
    #             self.error_operation = "Ya existe este producto: " + datos['producto']
    #             return False

    #     except Exception as ex:
    #         self.error_operation = 'error de argumentos, ' + str(ex)
    #         print('ERROR productos modify, ' + str(ex))
    #         return False

    def buscar_producto(self, linea='', producto='', codigo='', operation='', pid=''):
        """busqueda de productos"""
        filtros = {}
        filtros['status_id__in'] = [self.activo]
        #filtros['es_combo'] = False

        if linea.strip() != '':
            filtros['linea_id__linea__icontains'] = linea
        if producto.strip() != '':
            filtros['producto__icontains'] = producto
        if codigo.strip() != '':
            filtros['codigo__icontains'] = codigo

        if operation == 'modify':
            productos_lista = Productos.objects.select_related('linea_id').filter(**filtros).exclude(pk=int(pid)).order_by('linea_id__linea', 'producto')[0:30]
        else:
            productos_lista = Productos.objects.select_related('linea_id').filter(**filtros).order_by('linea_id__linea', 'producto')[0:30]

        return productos_lista

    def buscar_insumo(self, insumo='', codigo='', operation='', pid=''):
        """busqueda de productos"""
        filtros = {}
        filtros['status_id__in'] = [self.activo]
        #filtros['es_combo'] = False

        if insumo.strip() != '':
            filtros['insumo__icontains'] = insumo
        if codigo.strip() != '':
            filtros['codigo__icontains'] = codigo

        if operation == 'modify':
            insumos_lista = Insumos.objects.filter(**filtros).exclude(pk=int(pid)).order_by('insumo')[0:30]
        else:
            insumos_lista = Insumos.objects.filter(**filtros).order_by('insumo')[0:30]

        return insumos_lista

    def buscar_componente(self, componente='', codigo='', operation='', pid=''):
        """busqueda de productos"""
        filtros = {}
        filtros['status_id__in'] = [self.activo]
        #filtros['es_combo'] = False

        if componente.strip() != '':
            filtros['componente__icontains'] = componente
        if codigo.strip() != '':
            filtros['codigo__icontains'] = codigo

        if operation == 'modify':
            componentes_lista = Componentes.objects.filter(**filtros).exclude(pk=int(pid)).order_by('componente')[0:30]
        else:
            componentes_lista = Componentes.objects.filter(**filtros).order_by('componente')[0:30]

        return componentes_lista

    def crear_descripcion(self, producto):
        texto_mostrar = ''

        des1 = producto.descripcion1.strip()
        des2 = producto.descripcion2.strip()
        des3 = producto.descripcion3.strip()
        des4 = producto.descripcion4.strip()
        des5 = producto.descripcion5.strip()
        des6 = producto.descripcion6.strip()
        des7 = producto.descripcion7.strip()
        des8 = producto.descripcion8.strip()
        des9 = producto.descripcion9.strip()
        des10 = producto.descripcion10.strip()

        texto1 = self.verificar_texto(des1)
        texto2 = self.verificar_texto(des2)
        texto3 = self.verificar_texto(des3)
        texto4 = self.verificar_texto(des4)
        texto5 = self.verificar_texto(des5)
        texto6 = self.verificar_texto(des6)
        texto7 = self.verificar_texto(des7)
        texto8 = self.verificar_texto(des8)
        texto9 = self.verificar_texto(des9)
        texto10 = self.verificar_texto(des10)

        texto_mostrar = texto1 + texto2 + texto3 + texto4 + texto5 + texto6 + texto7 + texto8 + texto9 + texto10

        return texto_mostrar

    def verificar_texto(self, descripcion):
        if descripcion == '':
            return ''
        else:
            return descripcion + '<br>'

    def save_images(self, request, producto_id):
        """guardamos las posiciones de las imagenes"""
        try:
            producto = Productos.objects.get(pk=producto_id)
            productos_imagenes = ProductosImagenes.objects.filter(producto_id=producto)

            for producto_imagen in productos_imagenes:
                aux = 'posicion_' + str(producto_imagen.producto_imagen_id)
                #print('aux: ', aux)
                if aux in request.POST.keys():
                    valor = 0 if request.POST[aux].strip() == '' else int(request.POST[aux].strip())
                    producto_imagen.posicion = valor
                    producto_imagen.save()

            return True

        except Exception as e:
            print('error guardar posicion imagen: ', str(e))
            self.error_operation = 'Error al guardar posiciones de imagen'
            return False

    def lista_productos(self, linea_id=0, punto_id=0, combos=0):
        """lista de productos por linea seleccionada o todos"""
        try:
            # aumento de precios en los productos segun el punto
            aumento_precio_a = 0
            aumento_precio_b = 0
            aumento_precio_c = 0
            aumento_precio_a_factura = 0
            aumento_precio_b_factura = 0
            aumento_precio_c_factura = 0
            aumento_precio_a_consignacion = 0
            aumento_precio_b_consignacion = 0
            aumento_precio_c_consignacion = 0
            aumento_precio_a_pp = 0
            aumento_precio_b_pp = 0
            aumento_precio_c_pp = 0

            if punto_id != 0:
                # recuperamos si tiene
                punto = Puntos.objects.get(pk=punto_id)
                status_activo = Status.objects.get(pk=self.activo)
                puntos_precios = PuntosPrecios.objects.filter(punto_id=punto, status_id=status_activo)
                if puntos_precios:
                    punto_precio = puntos_precios.first()
                    if punto_precio:
                        # asignamos los precios
                        aumento_precio_a += punto_precio.aumento_precio_a
                        aumento_precio_b += punto_precio.aumento_precio_b
                        aumento_precio_c += punto_precio.aumento_precio_c
                        aumento_precio_a_factura += punto_precio.aumento_precio_a_factura
                        aumento_precio_b_factura += punto_precio.aumento_precio_b_factura
                        aumento_precio_c_factura += punto_precio.aumento_precio_c_factura
                        aumento_precio_a_consignacion += punto_precio.aumento_precio_a_consignacion
                        aumento_precio_b_consignacion += punto_precio.aumento_precio_b_consignacion
                        aumento_precio_c_consignacion += punto_precio.aumento_precio_c_consignacion
                        aumento_precio_a_pp += punto_precio.aumento_precio_a_pp
                        aumento_precio_b_pp += punto_precio.aumento_precio_b_pp
                        aumento_precio_c_pp += punto_precio.aumento_precio_c_pp

            if linea_id == 0:
                sql_add = ''
            else:
                sql_add = f"AND l.linea_id='{linea_id}' "

            if combos == 0:
                sql_add += 'AND p.es_combo=0 '

            msql = f"SELECT l.linea, p.producto, p.codigo, p.costo_a, p.costo_b, p.costo_c, p.precio_a, p.precio_b, p.precio_c, p.precio_a_factura, p.precio_b_factura, p.precio_c_factura, p.precio_a_consignacion, p.precio_b_consignacion, p.precio_c_consignacion, p.precio_a_pp, p.precio_b_pp, p.precio_c_pp, p.producto_id "
            msql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.status_id='{self.activo}' AND p.status_id='{self.activo}' "
            msql += sql_add
            msql += f"ORDER BY l.linea, p.producto "
            #print('msql ', msql)

            datos_productos = []
            with connection.cursor() as cursor:
                cursor.execute(msql)
                rows = cursor.fetchall()
                for row in rows:
                    datos_productos.append({'linea': row[0], 'producto': row[1], 'codigo': row[2], 'costo_a': row[3], 'costo_b': row[4], 'costo_c': row[5],
                                            'precio_a': row[6] + aumento_precio_a, 'precio_b': row[7] + aumento_precio_b, 'precio_c': row[8] + aumento_precio_c,
                                            'precio_a_factura': row[9] + aumento_precio_a_factura, 'precio_b_factura': row[10] + aumento_precio_b_factura, 'precio_c_factura': row[11] + aumento_precio_c_factura,
                                            'precio_a_consignacion': row[12] + aumento_precio_a_consignacion, 'precio_b_consignacion': row[13] + aumento_precio_b_consignacion, 'precio_c_consignacion': row[14] + aumento_precio_c_consignacion,
                                            'precio_a_pp': row[15] + aumento_precio_a_pp, 'precio_b_pp': row[16] + aumento_precio_b_pp, 'precio_c_pp': row[17] + aumento_precio_c_pp, 'producto_id': row[18]})

            # print(datos_arqueo)
            return datos_productos

        except Exception as e:
            print('error lista productos: ', str(e))
            self.error_operation = 'Error al recuperar lista productos'
            return False

    def lista_insumos(self):
        """lista de insumos"""
        try:
            msql = f"SELECT i.insumo_id, i.insumo, i.codigo, i.imagen, i.imagen_thumb, i.posicion, i.precio "
            msql += f"FROM insumos i "
            msql += "WHERE i.status_id='1' "
            msql += f"ORDER BY i.posicion, i.insumo "
            #print('msql ', msql)

            datos_productos = []
            with connection.cursor() as cursor:
                cursor.execute(msql)
                rows = cursor.fetchall()
                for row in rows:
                    datos_productos.append({'producto_id': row[0], 'producto': row[1], 'codigo': row[2], 'imagen': row[3], 'imagen_thumb': row[4], 'posicion': row[5],
                                            'costo_a': row[6], 'costo_b': row[6], 'costo_c': row[6],
                                            'precio_a': row[6], 'precio_b': row[6], 'precio_c': row[6],
                                            'precio_a_factura': row[6], 'precio_b_factura': row[6], 'precio_c_factura': row[6],
                                            'precio_a_consignacion': row[6], 'precio_b_consignacion': row[6], 'precio_c_consignacion': row[6],
                                            'precio_a_pp': row[6], 'precio_b_pp': row[6], 'precio_c_pp': row[6]})

            # print(datos_arqueo)
            return datos_productos

        except Exception as e:
            print('error lista productos: ', str(e))
            self.error_operation = 'Error al recuperar lista productos'
            return False

    def lista_refrescos(self):
        """lista de refrescos para hacer el cambio"""
        try:
            msql = "SELECT rg.insumo_id, rg.componente_id, i.insumo, c.componente, rg.refresco_grupo_id "
            msql += "FROM refrescos_grupo rg LEFT JOIN insumos i ON rg.insumo_id=i.insumo_id "
            msql += "LEFT JOIN componentes c ON rg.componente_id=c.componente_id "
            msql += "ORDER BY rg.posicion "

            datos_refrescos = []
            with connection.cursor() as cursor:
                cursor.execute(msql)
                rows = cursor.fetchall()
                for row in rows:
                    datos_refrescos.append({'insumo_id': row[0], 'componente_id': row[1],
                                            'insumo': row[2], 'componente': row[3], 'refresco_grupo_id': row[4]})

            # print(datos_arqueo)
            return datos_refrescos

        except Exception as e:
            print('error lista refrescos: ', str(e))
            self.error_operation = 'Error al recuperar lista refrescos'
            return False

    def lista_papas(self):
        """lista de papas para hacer el cambio"""
        try:
            msql = "SELECT pg.insumo_id, pg.componente_id, i.insumo, c.componente, pg.papa_grupo_id "
            msql += "FROM papas_grupo pg LEFT JOIN insumos i ON pg.insumo_id=i.insumo_id "
            msql += "LEFT JOIN componentes c ON pg.componente_id=c.componente_id "
            msql += "ORDER BY pg.posicion "

            datos_papas = []
            with connection.cursor() as cursor:
                cursor.execute(msql)
                rows = cursor.fetchall()
                for row in rows:
                    datos_papas.append({'insumo_id': row[0], 'componente_id': row[1], 'insumo': row[2],
                                        'componente': row[3], 'papa_grupo_id': row[4]})

            # print(datos_arqueo)
            return datos_papas

        except Exception as e:
            print('error lista refrescos: ', str(e))
            self.error_operation = 'Error al recuperar lista refrescos'
            return False

    def datos_producto(self, producto_id):
        producto = Productos.objects.get(pk=producto_id)

        lista_componentes = []
        lista_extras = []
        lista_refrescos = []
        lista_papas = []

        componentes_ids = ''
        extras_ids = ''
        productos_refrescos_ids = ''
        productos_papas_ids = ''
        refresco_grupo_ids = ''
        papa_grupo_ids = ''

        productos_componentes = ProductosComponentes.objects.filter(producto_id=producto).order_by('posicion')
        for pc in productos_componentes:
            dato = {}
            dato['componente_id'] = pc.componente_id.componente_id
            dato['componente'] = pc.componente_id.componente
            dato['defecto'] = pc.defecto
            dato['posicion'] = pc.posicion

            lista_componentes.append(dato)
            componentes_ids += str(pc.componente_id.componente_id) + '|'

        if len(componentes_ids) > 0:
            componentes_ids = componentes_ids[0:len(componentes_ids)-1]

        #print('lista componentes: ', lista_componentes)

        # extras
        productos_extras = ProductosExtras.objects.filter(producto_id=producto).order_by('posicion')
        for pe in productos_extras:
            dato = {}
            dato['componente_id'] = pe.componente_id.componente_id
            dato['componente'] = pe.componente_id.componente
            dato['precio'] = pe.precio
            dato['posicion'] = pe.posicion

            lista_extras.append(dato)
            extras_ids += str(pe.componente_id.componente_id) + '|'

        if len(extras_ids) > 0:
            extras_ids = extras_ids[0:len(extras_ids)-1]

        # refrescos
        lista_ref = self.lista_refrescos()

        msql = "SELECT pr.insumo_id, pr.componente_id, i.insumo, c.componente, pr.producto_refresco_id, pr.precio, pr.posicion, pr.defecto "
        msql += "FROM productos_refrescos pr LEFT JOIN insumos i ON pr.insumo_id=i.insumo_id "
        msql += "LEFT JOIN componentes c ON pr.componente_id=c.componente_id "
        msql += f"WHERE pr.producto_id='{producto_id}' "
        msql += "ORDER BY pr.posicion "

        with connection.cursor() as cursor:
            cursor.execute(msql)
            rows = cursor.fetchall()
            for row in rows:
                dato = {}
                dato['insumo_id'] = row[0]
                dato['componente_id'] = row[1]
                dato['insumo'] = row[2]
                dato['componente'] = row[3]
                dato['producto_refresco_id'] = row[4]
                dato['precio'] = row[5]
                dato['posicion'] = row[6]
                dato['defecto'] = row[7]

                ref_gr_id = 0
                for li_re in lista_ref:
                    if li_re['insumo_id'] == row[0] and li_re['componente_id'] == row[1]:
                        ref_gr_id = li_re['refresco_grupo_id']

                # asignamos
                dato['refresco_grupo_id'] = ref_gr_id

                lista_refrescos.append(dato)
                productos_refrescos_ids += str(row[4]) + '|'
                refresco_grupo_ids += str(ref_gr_id) + '|'

        if len(productos_refrescos_ids) > 0:
            productos_refrescos_ids = productos_refrescos_ids[0:len(productos_refrescos_ids)-1]
            refresco_grupo_ids = refresco_grupo_ids[0:len(refresco_grupo_ids)-1]

        # papas
        lista_pap = self.lista_papas()

        msql = "SELECT pp.insumo_id, pp.componente_id, i.insumo, c.componente, pp.producto_papa_id, pp.precio, pp.posicion, pp.defecto "
        msql += "FROM productos_papas pp LEFT JOIN insumos i ON pp.insumo_id=i.insumo_id "
        msql += "LEFT JOIN componentes c ON pp.componente_id=c.componente_id "
        msql += f"WHERE pp.producto_id='{producto_id}' "
        msql += "ORDER BY pp.posicion "

        with connection.cursor() as cursor:
            cursor.execute(msql)
            rows = cursor.fetchall()
            for row in rows:
                dato = {}
                dato['insumo_id'] = row[0]
                dato['componente_id'] = row[1]
                dato['insumo'] = row[2]
                dato['componente'] = row[3]
                dato['producto_papa_id'] = row[4]
                dato['precio'] = row[5]
                dato['posicion'] = row[6]
                dato['defecto'] = row[7]

                ref_gr_id = 0
                for li_pa in lista_pap:
                    if li_pa['insumo_id'] == row[0] and li_pa['componente_id'] == row[1]:
                        ref_gr_id = li_pa['papa_grupo_id']

                # asignamos
                dato['papa_grupo_id'] = ref_gr_id

                lista_papas.append(dato)
                productos_papas_ids += str(row[4]) + '|'
                papa_grupo_ids += str(ref_gr_id) + '|'

        if len(productos_papas_ids) > 0:
            productos_papas_ids = productos_papas_ids[0:len(productos_papas_ids)-1]
            papa_grupo_ids = papa_grupo_ids[0:len(papa_grupo_ids)-1]

        detalle_producto = {}
        detalle_producto['lista_componentes'] = lista_componentes
        detalle_producto['lista_extras'] = lista_extras
        detalle_producto['lista_refrescos'] = lista_refrescos
        detalle_producto['lista_papas'] = lista_papas

        detalle_producto['componentes_ids'] = componentes_ids
        detalle_producto['extras_ids'] = extras_ids
        detalle_producto['productos_refrescos_ids'] = productos_refrescos_ids
        detalle_producto['productos_papas_ids'] = productos_papas_ids
        detalle_producto['refresco_grupo_ids'] = refresco_grupo_ids
        detalle_producto['papa_grupo_ids'] = papa_grupo_ids

        return detalle_producto
