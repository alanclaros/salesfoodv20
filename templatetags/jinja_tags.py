from datetime import datetime
from django import template
from django.conf import settings
from django.apps import apps
from django.template.defaultfilters import stringfilter

from utils.dates_functions import get_date_show

from utils.dates_functions import get_month_2digits, get_month_3digits

from controllers.SystemController import SystemController

from datetime import datetime, timedelta, date

# from permisos.models import UsersPerfiles, UsersModulos
# from configuraciones.models import Puntos

register = template.Library()
system_controller = SystemController()


@register.filter('get_item')
def get_item(dictionary, key):
    #print('key...', key, '---')
    return dictionary.get(key)


@register.filter('get_objeto_user_modulo')
def get_objeto_user_modulo(key, lista_user_modulo):
    # print(key)
    # print(lista_user_modulo)
    for user_modulo in lista_user_modulo:  # lista de objectos
        # print(user_modulo.modulo_id.modulo_id)
        if key == user_modulo.modulo_id.modulo_id:  # atributos del objecto
            # print(user_modulo)
            return user_modulo.__dict__


@register.filter('back_class')
def back_class(index):
    """combinacion de color de filas"""
    if int(index) % 2 == 0:
        return '1'
    else:
        return '2'


@register.filter('back_class_color')
def back_class_color(index, estado):
    """combinacion de color de filas segun estado"""
    estado_int = int(estado)

    if estado_int == settings.STATUS_ANULADO:
        return 'anulado'

    if estado_int == settings.STATUS_INACTIVO:
        return 'inhabil'

    if estado_int == settings.STATUS_CONTADO:
        return 'cobrado'

    if estado_int == settings.STATUS_FACTURA:
        return 'cobrado'

    if estado_int == settings.STATUS_CONSIGNACION:
        return 'cobrado'

    if estado_int == settings.STATUS_PLAN_PAGO:
        return 'cobrado'

    if estado_int == settings.STATUS_MOVIMIENTO_CAJA_RECIBE:
        return 'cobrado'

    if estado_int == settings.STATUS_PREVENTA:
        return 'pedido'

    if int(index) % 2 == 0:
        return '1'
    else:
        return '2'


@register.filter('fecha_mostrar')
def fecha_mostrar(fecha, formato):
    if fecha:
        # dividimos
        # anio = '20' + str(fecha.year) if len(str(fecha.year)) == 2 else str(fecha.year)
        # mes = '0' + str(fecha.month) if len(str(fecha.month)) == 1 else str(fecha.month)
        # dia = '0' + str(fecha.day) if len(str(fecha.day)) == 1 else str(fecha.day)
        # hora = '0' + str(fecha.hour) if len(str(fecha.hour)) == 1 else str(fecha.hour)
        # minutos = '0' + str(fecha.minute) if len(str(fecha.minute)) == 1 else str(fecha.minute)
        # segundos = '0' + str(fecha.second) if len(str(fecha.second)) == 1 else str(fecha.second)
        #
        # if formato == 'dd-MMM-yyyy':
        #     return dia + '-' + get_month_3digits(mes) + '-' + anio
        #
        # if formato == 'dd-MMM-yyyy HH:ii':
        #     return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos
        #
        # if formato == 'dd-MMM-yyyy HH:ii:ss':
        #     return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos + ':' + segundos
        #
        # if formato == 'd-M-yy':
        #     return dia + '.' + mes + '.' + anio[2:4]
        #
        # return 'error formato'

        # print('formato: ', formato)
        return get_date_show(fecha, formato=formato)

    else:
        return '/N'


# get cantidad apertura detalle, cajas operacioens detalles
@register.filter('get_cantidad_apertura')
def get_cantidad_apertura(moneda_id, cajas_operaciones_detalles):
    for detalle in cajas_operaciones_detalles:
        #print('moneda_id:', moneda_id, ' detalle:', detalle.moneda_id.moneda_id)
        if moneda_id == detalle.moneda_id.moneda_id:
            return detalle.cantidad_apertura

    return ''


# verificamos si la fecha es de hoy
@register.filter('is_today')
def is_today(fecha):
    retorno = 'n'
    anio = datetime.now().year
    mes = datetime.now().month
    dia = datetime.now().day

    if type(fecha) == datetime:
        f_anio = fecha.year
        f_mes = fecha.month
        f_dia = fecha.day

        if f_anio == anio and f_mes == mes and f_dia == dia:
            retorno = 'y'

    return retorno

# get cantidad cierre detalle, cajas operacioens detalles


@register.filter('get_cantidad_cierre')
def get_cantidad_cierre(moneda_id, cajas_operaciones_detalles):
    for detalle in cajas_operaciones_detalles:
        #print('moneda_id:', moneda_id, ' detalle:', detalle.moneda_id.moneda_id)
        if moneda_id == detalle.moneda_id.moneda_id:
            return detalle.cantidad_cierre

    return ''


# caja get
@register.filter('get_caja')
def get_caja(Cajas_lista, caja_id):
    for caja in Cajas_lista:
        if caja.caja_id == caja_id:
            return caja.codigo

    return ''


# caja punto
@register.filter('get_punto')
def get_punto(Puntos_lista, punto_id):
    for punto in Puntos_lista:
        if punto.punto_id == punto_id:
            return punto.punto

    return ''


# putno del usuario
@register.filter('get_punto_user')
def get_punto_user(user):
    # cuando no tenemos el modulo de permisos
    # return 'Punto jinjatags'

    if system_controller.model_exits('UsersPerfiles'):
        UP = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)
        punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=UP.punto_id)

        return punto.punto

    else:
        return ''


# permiso para el grupo
@register.filter('lista_modulos')
def lista_modulos(user):
    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)

    if system_controller.model_exits('UsersModulos'):
        modulos_usuario = apps.get_model('permisos', 'UsersModulos').objects.filter(user_perfil_id=user_perfil)
    else:
        modulos_usuario = []

    return modulos_usuario


# permisos del usuario
@register.filter('permisos_modulo')
def permisos_modulo(modulos_usuario, modulos):
    lista = str(modulos)
    div = lista.split(',')

    permiso = 'no'
    for mod in div:
        for mu in modulos_usuario:
            if int(mod) == int(mu.modulo_id.modulo_id):
                if mu.enabled:
                    permiso = 'si'

    # cuando no tenemos el modulo de permisos
    #permiso= 'si'

    # print(permiso)
    return permiso


# devolviendo el objeto usuario perfil del usuario
@register.filter('get_status_user')
def get_status_user(usuarios_perfiles, usuario):
    retorno = 0
    for usuario_perfil in usuarios_perfiles:
        if usuario_perfil.user_id == usuario:
            retorno = usuario_perfil.status_id.status_id

    return retorno


# verificando si el almacen esta registrado en puntos almacenes
@register.filter('verificar_punto_almacen')
def verificar_punto_almacen(almacen, lista_punto_almacen):
    retorno = 'no'
    for punto_almacen in lista_punto_almacen:
        if punto_almacen.almacen_id == almacen:
            retorno = 'si'

    return retorno


@register.filter('get_sub_url_empresa')
def get_sub_url_empresa(empresa):
    retorno = ''
    if settings.CURRENT_HOST == '127.0.0.1':
        retorno = ''
    else:
        if settings.SUB_URL_EMPRESA == 'ventas_renekris':
            retorno = ''
        else:
            retorno = '/' + settings.SUB_URL_EMPRESA

    if empresa:
        return retorno
    else:
        return ''


@register.filter('get_forloop_menos1')
def get_forloop_menos1(forloop_number):
    retorno = int(forloop_number) - 1

    return retorno
