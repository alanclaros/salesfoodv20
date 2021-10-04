from django.conf import settings
from django.apps import apps

from controllers.DefaultValues import DefaultValues
# from configuraciones.models import Configuraciones
# from status.models import Status

from utils.validators import validate_number_int, validate_string


class ConfiguracionesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Configuraciones'
        self.modelo_id = 'configuracion_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_CONFIGURACIONES_SISTEMA

        # variables de session
        self.modulo_session = "configuraciones"

        # paginas session
        self.variable_page = "ss_page"
        self.variable_page_defecto = "1"

        # control del formulario
        self.control_form = "txt|1|S|cant_per_page|"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        retorno = modelo.objects.get(pk=1)

        return retorno

    def add(self, request):
        """aniadimos"""
        pass

    def modify(self, request):
        """modificamos"""
        try:
            cant_per_page = validate_number_int('cantidad_pagina', request.POST['cant_per_page'])
            cant_products_home = validate_number_int('cantidad_home', request.POST['cant_products_home'], len_zero='yes')
            vender_fracciones = validate_string('vender_fracciones', request.POST['vender_fracciones'], remove_specials='yes')

            configuracion = apps.get_model('configuraciones', 'Configuraciones').objects.get(pk=1)
            configuracion.cant_per_page = cant_per_page
            configuracion.cant_products_home = cant_products_home
            configuracion.vender_fracciones = vender_fracciones
            configuracion.save()
            return True

        except Exception as ex:
            self.error_operation = "Error al actualizar los datos, " + str(ex)
            return False
