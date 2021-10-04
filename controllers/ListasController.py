from django.apps import apps
from django.conf import settings


class ListasController(object):
    """
    listas de objetos para los combos
    """

    def __init__(self):
        # propiedades
        self.modelo_name = 'unknow'
        self.modelo_id = 'unknow'
        self.modelo_app = 'unknow'

    def get_lista_zonas(self, user, module=''):
        """
        zonas list according user profile and module
        :param user: (object) user session
        :param module: (object) modulo for list
        :return: (list) zonas list
        """
        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        lista_zonas = apps.get_model('configuraciones', 'Zonas').objects.filter(status_id=status_activo).order_by('zona')

        return lista_zonas

    def get_lista_lugares(self, user, module=''):
        """
        lugares list according user profile and module
        :param user: (object) user session
        :param module: (object) modulo for list
        :return: (list) zonas list
        """
        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        lista_lugares = apps.get_model('ventas', 'Lugares').objects.filter(status_id=status_activo).order_by('lugar')

        return lista_lugares

    def get_lista_almacenes(self, user, sucursal=None, module=''):
        """
        get almacenes list
        :param user: (object) request user
        :param module: (object) module for list
        :return: (list) almacenes list
        """

        # ALMACEN1 devuelve solo el almacen central
        if module == 'almacen1':
            status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
            filtros = {}
            filtros['status_id'] = status_activo
            filtros['almacen_id'] = 1

            lista_almacenes = apps.get_model('configuraciones', 'Almacenes').objects.filter(**filtros).order_by('almacen')

            return lista_almacenes

        # preventas
        if module == settings.MOD_PREVENTAS:
            status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
            filtros = {}
            filtros['status_id'] = status_activo
            filtros['almacen_id'] = 1

            lista_almacenes = apps.get_model('configuraciones', 'Almacenes').objects.filter(**filtros).order_by('almacen')

            return lista_almacenes

        # modulo
        if module == settings.MOD_MOVIMIENTOS_ALMACEN:
            status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
            filtros = {}
            filtros['status_id'] = status_activo

            lista_almacenes = apps.get_model('configuraciones', 'Almacenes').objects.filter(**filtros).order_by('almacen')

            return lista_almacenes

        # valores por defecto
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)

        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        filtros = {}
        filtros['status_id'] = status_activo

        if sucursal:
            filtros['sucursal_id'] = sucursal
        else:
            if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                filtros['sucursal_id'] = sucursal

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                user_punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
                punto_almacen = apps.get_model('configuraciones', 'PuntosAlmacenes').objects.filter(punto_id=user_punto)
                lista_ids = []
                for almacen in punto_almacen:
                    lista_ids.append(almacen.almacen_id.almacen_id)

                filtros['almacen_id__in'] = lista_ids

        lista_almacenes = apps.get_model('configuraciones', 'Almacenes').objects.filter(**filtros).order_by('almacen')

        return lista_almacenes

    def get_lista_sucursales(self, user, module='', *select_relateds):
        """
        get sucursales list
        :param user: (object) request user
        :param module: (object) module for list
        :param *args: (list) list select_related modules
        :return: (list) almacenes list
        """

        #print('select relateds: ', *select_relateds)

        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        filtros = {}
        filtros['status_id'] = status_activo

        lista_sucursales = apps.get_model('configuraciones', 'Sucursales').objects.filter(**filtros).order_by('sucursal')

        return lista_sucursales

    def get_lista_tipos_monedas(self, user, module='', *select_relateds):
        """
        get tipos monedas list
        :param user: (object) request user
        :param module: (object) module for list
        :param *args: (list) list select_related modules
        :return: (list) tipos monedas list
        """

        #print('select relateds: ', *select_relateds)

        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        filtros = {}
        filtros['status_id'] = status_activo

        lista_tipos_monedas = apps.get_model('configuraciones', 'TiposMonedas').objects.filter(**filtros).order_by('codigo')

        return lista_tipos_monedas

    def get_lista_proveedores(self, user, module='', *select_relateds):
        """
        get proveedores list
        :param user: (object) request user
        :param module: (object) module for list
        :param *args: (list) list select_related modules
        :return: (list) proveedores list
        """

        #print('select relateds: ', *select_relateds)

        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        filtros = {}
        filtros['status_id'] = status_activo

        lista_proveedores = apps.get_model('configuraciones', 'Proveedores').objects.filter(**filtros).order_by('proveedor')

        return lista_proveedores

    def get_lista_perfiles(self, user, module='', *select_relateds):
        """
        get perfiles list
        :param user: (object) request user
        :param module: (object) module for list
        :param *args: (list) list select_related modules
        :return: (list) perfiles list
        """

        #print('select relateds: ', *select_relateds)
        lista_perfiles = apps.get_model('permisos', 'Perfiles').objects.order_by('perfil')

        return lista_perfiles

    def get_lista_modulos(self, user, module='', *select_relateds):
        """
        get modulos list
        :param user: (object) request user
        :param module: (object) module for list
        :param *args: (list) list select_related modules
        :return: (list) modulos list
        """

        lista_modulos = apps.get_model('permisos', 'Modulos').objects.filter(enabled=True).order_by('position')

        return lista_modulos

    def get_lista_cajas(self, user, module='', *select_relateds):
        """
        get cajas list
        :param user: (object) request user
        :param module: (object) module for list
        :param *args: (list) list select_related modules
        :return: (list) cajas list
        """

        # verificamos el perfil del usuario
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)
        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        punto_user = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
        filtros = {}

        if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
            # todas las cajas del sistema
            filtros['status_id'] = status_activo

        if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
            filtros['status_id'] = status_activo
            filtros['punto_id__sucursal_id'] = punto_user.sucursal_id

        if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO or module in ['cajas_ingresos', 'cajas_egresos']:
            # para mostrar solo la caja asignada en adicion
            filtros['status_id'] = status_activo
            filtros['caja_id'] = user_perfil.caja_id

        lista_cajas = apps.get_model('configuraciones', 'Cajas').objects.filter(**filtros).order_by('caja')

        return lista_cajas

    def get_lista_puntos(self, user, module='', *select_relateds):
        """
        get cajas list
        :param user: (object) request user
        :param module: (object) module for list
        :param *args: (list) list select_related modules
        :return: (list) cajas list
        """

        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        filtros = {}
        filtros['status_id'] = status_activo
        lista_puntos = apps.get_model('configuraciones', 'Puntos').objects.filter(**filtros).order_by('punto')

        return lista_puntos

    def get_lista_lineas(self, user, module='', *select_relateds):
        """
        get lineas list
        :param user: (object) request user
        :param module: (object) module for list
        :param *args: (list) list select_related modules
        :return: (list) lineas list
        """

        status_activo = apps.get_model('status', 'Status').objects.get(pk=int(settings.STATUS_ACTIVO))
        filtros = {}
        filtros['status_id'] = status_activo
        lista_lineas = apps.get_model('configuraciones', 'Lineas').objects.filter(**filtros).order_by('linea')

        return lista_lineas
