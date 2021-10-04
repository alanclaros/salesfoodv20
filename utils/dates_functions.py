from django.conf import settings
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

months_3digits = {
    'Ene': '01',
    'Feb': '02',
    'Mar': '03',
    'Abr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Ago': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dic': '12'
}

months_2digits = {
    '01': 'Ene',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Abr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Ago',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dic'
}


def get_month_2digits(mes):
    """
    get month format mm
    :param mes: month in 3 digits
    :return: (str) month in 2 digits
    """
    return months_3digits.get(mes, 'error en mes 2 digitos')


def get_month_3digits(mes):
    """
    get month to show 3 digits
    :param mes: month in 2 digits
    :return: (str) month in 3 digits
    """
    return months_2digits.get(mes, 'error en mes 3 digitos')


def get_date_system(time='no'):
    """
    date or datetime system
    :param time: (str) if 'no' just date else datetime
    :return: date or datetime system
    """
    anio = '20' + str(datetime.now().year) if len(str(datetime.now().year)) == 2 else str(datetime.now().year)
    mes = '0' + str(datetime.now().month) if len(str(datetime.now().month)) == 1 else str(datetime.now().month)
    dia = '0' + str(datetime.now().day) if len(str(datetime.now().day)) == 1 else str(datetime.now().day)

    fecha = anio + '-' + mes + '-' + dia

    if time != 'no':
        hora = '0' + str(datetime.now().hour) if len(str(datetime.now().hour)) == 1 else str(datetime.now().hour)
        minutos = '0' + str(datetime.now().minute) if len(str(datetime.now().minute)) == 1 else str(datetime.now().minute)
        segundos = '0' + str(datetime.now().second) if len(str(datetime.now().second)) == 1 else str(datetime.now().second)

        fecha += ' ' + hora + ':' + minutos + ':' + segundos

    return fecha


def get_day_from_date(fecha, formato_ori='dd-MMM-yyyy'):
    """
    get day from datetime
    :param fecha: (date) date or datetime
    :param formato_ori: (str) date format
    :return: (str) day in 2 digits
    """
    dia = ''

    if isinstance(fecha, datetime):
        dia = str(fecha.day)
        if len(dia) == 1:
            dia = '0' + dia

        return dia

    if isinstance(fecha, str):
        if len(formato_ori) == 11 or formato_ori == 'dd-MMM-yyyy':
            # formato por defecto dd-MMM-yyyy
            dia = fecha[0:2]
            return dia

        if len(fecha) == 8 or len(fecha) == 7 or len(fecha) == 6 or formato_ori == 'd.m.yy' or formato_ori == 'd-M-yy':
            divisor = '.'
            if formato_ori == 'd-M-yy':
                divisor = '-'

            pos = fecha.find(divisor)
            if pos > 0:
                dia = fecha[0:pos]
                if len(dia) < 1 or len(dia) > 2:
                    raise ValueError('Error en formato de fecha: ' + fecha + ' (' + formato_ori + ')')

                if len(dia) == 1:
                    dia = '0' + dia

                return dia

            else:
                raise ValueError('Error en formato de fecha: ' + fecha + ' (' + formato_ori + ')')

        if len(fecha) == 10 or formato_ori == 'yyyy-mm-dd':
            dia = fecha[8:10]
            return dia

        if len(fecha) == 19 or formato_ori == 'yyyy-mm-dd HH:ii:ss':
            if len(fecha) != 19:
                raise ValueError('Error en formato de fecha: ' + fecha + ' (' + formato_ori + ')')

            dia = fecha[8:10]
            return dia

    # no cumple ningun parametro
    raise ValueError('Error en formato de fecha: ' + fecha + ' (' + formato_ori + ')')


def get_date_to_db(fecha, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo=''):
    """
    return date in string format to send to database field
    :param fecha: (object) datetime or string, datetime
    :param formato_ori: (str) original format from fecha
    :param formato: (str) format to convert
    :param tiempo: (str) set time in fecha ex: 23:59:59, default 00:00:00
    :return: (str) date or date time, format: yyyy-mm-dd or yyyy-mm-dd HH:ii:ss
    """

    #print('tipo: ', type(fecha))
    dia = '00'
    mes = '00'
    anio = '0000'
    # hora = '00'
    # minuto = '00'
    # segundo = '00'
    hora = '0' + str(datetime.now().hour) if len(str(datetime.now().hour)) == 1 else str(datetime.now().hour)
    minuto = '0' + str(datetime.now().minute) if len(str(datetime.now().minute)) == 1 else str(datetime.now().minute)
    segundo = '0' + str(datetime.now().second) if len(str(datetime.now().second)) == 1 else str(datetime.now().second)

    if isinstance(fecha, date):
        #print('is date....', fecha)
        anio = '20' + str(fecha.year) if len(str(fecha.year)) == 2 else str(fecha.year)
        mes = '0' + str(fecha.month) if len(str(fecha.month)) == 1 else str(fecha.month)
        dia = '0' + str(fecha.day) if len(str(fecha.day)) == 1 else str(fecha.day)

        fecha_a = str(fecha)  # yyyy-mm-dd HH:ii:ss
        if len(fecha_a) > 11:
            hora = '0' + str(fecha.hour) if len(str(fecha.hour)) == 1 else str(fecha.hour)
            minuto = '0' + str(fecha.minute) if len(str(fecha.minute)) == 1 else str(fecha.minute)
            segundo = '0' + str(fecha.second) if len(str(fecha.second)) == 1 else str(fecha.second)

        # ponemos en formato
        if formato == 'yyyy-mm-dd':
            return anio + '-' + mes + '-' + dia

        if formato == 'yyyy-mm-dd HH:ii:ss':
            if tiempo == '':
                return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + segundo
            else:
                return anio + '-' + mes + '-' + dia + ' ' + tiempo

    if isinstance(fecha, datetime):
        #print('fecha..: ', fecha)
        anio = '20' + str(fecha.year) if len(str(fecha.year)) == 2 else str(fecha.year)
        mes = '0' + str(fecha.month) if len(str(fecha.month)) == 1 else str(fecha.month)
        dia = '0' + str(fecha.day) if len(str(fecha.day)) == 1 else str(fecha.day)
        hora = '0' + str(fecha.hour) if len(str(fecha.hour)) == 1 else str(fecha.hour)
        minuto = '0' + str(fecha.minute) if len(str(fecha.minute)) == 1 else str(fecha.minute)
        segundo = '0' + str(fecha.second) if len(str(fecha.second)) == 1 else str(fecha.second)

        # ponemos en formato
        if formato == 'yyyy-mm-dd':
            return anio + '-' + mes + '-' + dia

        if formato == 'yyyy-mm-dd HH:ii:ss':
            if tiempo == '':
                return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + segundo
            else:
                return anio + '-' + mes + '-' + dia + ' ' + tiempo

    if isinstance(fecha, str):

        if len(fecha) == 8 or len(fecha) == 7 or len(fecha) == 6 or formato_ori == 'd.m.yy' or formato_ori == 'd-M-yy':
            divisor = '.'
            if formato_ori == 'd-M-yy':
                divisor = '-'

            pos = fecha.find(divisor)
            pos2 = fecha.find(divisor, pos + 1)

            dia = ''
            mes = ''
            anio = ''

            if pos > 0:
                dia = fecha[0:pos]
                if len(dia) < 1 or len(dia) > 2:
                    raise ValueError('Error en formato de fecha: ' + fecha + ' (' + formato_ori + ')')

                if len(dia) == 1:
                    dia = '0' + dia
            else:
                raise ValueError('Error en formato de fecha: ' + fecha + ' (' + formato_ori + ')')

            if pos2 > 0:
                mes = fecha[pos + 1: pos2]
                if len(mes) < 1 or len(mes) > 2:
                    raise ValueError('Error en formato de fecha: ' + fecha + ' (' + formato_ori + ')')

                if len(mes) == 1:
                    mes = '0' + mes
            else:
                raise ValueError('Error en formato de fecha: ' + fecha + ' (' + formato_ori + ')')

            anio = fecha[pos2 + 1: len(fecha)]

            if formato == 'yyyy-mm-dd':
                return anio + '-' + mes + '-' + dia

            if formato == 'yyyy-mm-dd HH:ii:ss':
                if tiempo == '':
                    return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + segundo
                else:
                    return anio + '-' + mes + '-' + dia + ' ' + tiempo

        if len(fecha) == 10 or formato_ori == 'yyyy-mm-dd' or formato_ori == 'dd/MM/yyyy':

            if formato_ori == 'dd/MM/yyyy':
                anio = fecha[6:10]
                mes = fecha[3:5]
                dia = fecha[0:2]
            else:
                # por defecto yyyy-mm-dd
                anio = fecha[0:4]
                mes = fecha[5:7]
                dia = fecha[8:10]

            if formato == 'yyyy-mm-dd':
                return anio + '-' + mes + '-' + dia

            if formato == 'yyyy-mm-dd HH:ii:ss':
                if tiempo == '':
                    return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + segundo
                else:
                    return anio + '-' + mes + '-' + dia + ' ' + tiempo

        if len(fecha) == 11 or formato_ori == 'dd-MMM-yyyy':
            dia = fecha[0:2]
            mes = get_month_2digits(fecha[3:6])
            anio = fecha[7:11]

            if formato == 'yyyy-mm-dd':
                return anio + '-' + mes + '-' + dia

            if formato == 'yyyy-mm-dd HH:ii:ss':
                if tiempo == '':
                    # return anio + '-' + mes + '-' + dia + ' 00:00:00'
                    return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + segundo
                else:
                    return anio + '-' + mes + '-' + dia + ' ' + tiempo

        if len(fecha) == 17 or formato_ori == 'dd-MMM-yyyy HH:ii':
            dia = fecha[0:2]
            mes = get_month_2digits(fecha[3:6])
            anio = fecha[7:11]
            hora = fecha[12:14]
            minuto = fecha[15:17]

            if formato == 'yyyy-mm-dd':
                return anio + '-' + mes + '-' + dia

            if formato == 'yyyy-mm-dd HH:ii:ss':
                if tiempo == '':
                    return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':00'
                else:
                    return anio + '-' + mes + '-' + dia + ' ' + tiempo

        if len(fecha) == 19 or formato_ori == 'yyyy-mm-dd HH:ii:ss':
            anio = fecha[0:4]
            mes = fecha[5:7]
            dia = fecha[8:10]
            hora = fecha[11:13]
            minuto = fecha[14:16]
            segundo = fecha[17:19]

            if formato == 'yyyy-mm-dd':
                return anio + '-' + mes + '-' + dia

            if formato == 'yyyy-mm-dd HH:ii:ss':
                if tiempo == '':
                    return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + segundo
                else:
                    return anio + '-' + mes + '-' + dia + ' ' + tiempo

        if len(fecha) == 20 or formato_ori == 'dd-MMM-yyyy HH:ii:ss':
            dia = fecha[0:2]
            mes = get_month_2digits(fecha[3:6])
            anio = fecha[7:11]
            hora = fecha[12:14]
            minuto = fecha[15:17]
            segundo = fecha[18:20]

            if formato == 'yyyy-mm-dd':
                return anio + '-' + mes + '-' + dia

            if formato == 'yyyy-mm-dd HH:ii:ss':
                if tiempo == '':
                    return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + segundo
                else:
                    return anio + '-' + mes + '-' + dia + ' ' + tiempo

    # por defecto error si no cumple ninguna condicion
    raise ValueError('Error en formato de fecha ' + fecha + ' (' + formato_ori + ')')


def get_date_show(fecha, formato_ori='yyyy-mm-dd HH:ii:ss', formato='dd-MMM-yyyy'):
    """
    devolvemos fecha en formato propio, desde campo de la DB
    :param fecha: (object) datetime to convert
    :param formato: (str) format to show default: dd-MMM-yyyy
    :param formato_ori: (str) string case, original format in string
    :return: (str) date time to show user
    """

    if isinstance(fecha, datetime):
        #print('instancia datetime')
        anio = '20' + str(fecha.year) if len(str(fecha.year)) == 2 else str(fecha.year)
        mes = '0' + str(fecha.month) if len(str(fecha.month)) == 1 else str(fecha.month)
        dia = '0' + str(fecha.day) if len(str(fecha.day)) == 1 else str(fecha.day)
        hora = '0' + str(fecha.hour) if len(str(fecha.hour)) == 1 else str(fecha.hour)
        minutos = '0' + str(fecha.minute) if len(str(fecha.minute)) == 1 else str(fecha.minute)
        segundos = '0' + str(fecha.second) if len(str(fecha.second)) == 1 else str(fecha.second)

        if formato == 'dd-MMM-yyyy':
            return dia + '-' + get_month_3digits(mes) + '-' + anio

        if formato == 'dd-MMM-yyyy HH:ii':
            return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos

        if formato == 'dd-MMM-yyyy HH:ii:ss':
            return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos + ':' + segundos

        if formato == 'd.m.yy':
            if len(dia) == 2:
                if dia[0:1] == '0':
                    dia = dia[1:2]
            if len(mes) == 2:
                if mes[0:1] == '0':
                    mes = mes[1:2]
            return dia + '.' + mes + '.' + anio[2:4]

        if formato == 'yyyy-mm-dd':
            return anio + '-' + mes + '-' + dia

        if formato == 'yyyy-mm-dd HH:ii:ss':
            return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minutos + ':' + segundos

    if isinstance(fecha, date):
        #print('instancia date')
        anio = '20' + str(fecha.year) if len(str(fecha.year)) == 2 else str(fecha.year)
        mes = '0' + str(fecha.month) if len(str(fecha.month)) == 1 else str(fecha.month)
        dia = '0' + str(fecha.day) if len(str(fecha.day)) == 1 else str(fecha.day)
        hora = '00'
        minutos = '00'
        segundos = '00'

        if formato == 'dd-MMM-yyyy':
            return dia + '-' + get_month_3digits(mes) + '-' + anio

        if formato == 'dd-MMM-yyyy HH:ii':
            return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos

        if formato == 'dd-MMM-yyyy HH:ii:ss':
            return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos + ':' + segundos

        if formato == 'd.m.yy':
            if len(dia) == 2:
                if dia[0:1] == '0':
                    dia = dia[1:2]
            if len(mes) == 2:
                if mes[0:1] == '0':
                    mes = mes[1:2]
            return dia + '.' + mes + '.' + anio[2:4]

        if formato == 'd-M-yy':
            if len(dia) == 2:
                if dia[0:1] == '0':
                    dia = dia[1:2]
            if len(mes) == 2:
                if mes[0:1] == '0':
                    mes = mes[1:2]
            return dia + '-' + mes + '-' + anio[2:4]

        if formato == 'yyyy-mm-dd':
            return anio + '-' + mes + '-' + dia

        if formato == 'yyyy-mm-dd HH:ii:ss':
            return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minutos + ':' + segundos

    if isinstance(fecha, str):
        anio = '2021'
        mes = '01'
        dia = '01'
        # hora = '00'
        # minutos = '00'
        # segundos = '00'
        hora = '0' + str(datetime.now().hour) if len(str(datetime.now().hour)) == 1 else str(datetime.now().hour)
        minutos = '0' + str(datetime.now().minute) if len(str(datetime.now().minute)) == 1 else str(datetime.now().minute)
        segundos = '0' + str(datetime.now().second) if len(str(datetime.now().second)) == 1 else str(datetime.now().second)

        if formato_ori == 'yyyy-mm-dd':
            anio = fecha[0:4]
            mes = fecha[5:7]
            dia = fecha[8:10]

        if formato_ori == 'yyyy-mm-dd HH:ii:ss':
            anio = fecha[0:4]
            mes = fecha[5:7]
            dia = fecha[8:10]
            hora = fecha[11:13]
            minutos = fecha[14:16]
            segundos = fecha[17:19]

        if formato_ori == 'yyyy-mm-dd HH:ii':
            anio = fecha[0:4]
            mes = fecha[5:7]
            dia = fecha[8:10]
            hora = fecha[11:13]
            minutos = fecha[14:16]

        # devolvemos en el formato
        if formato == 'dd-MMM-yyyy':
            return dia + '-' + get_month_3digits(mes) + '-' + anio

        if formato == 'dd-MMM-yyyy HH:ii':
            return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos

        if formato == 'dd-MMM-yyyy HH:ii:ss':
            return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos + ':' + segundos

        if formato == 'd.m.yy':
            if len(dia) == 2:
                if dia[0:1] == '0':
                    dia = dia[1:2]
            if len(mes) == 2:
                if mes[0:1] == '0':
                    mes = mes[1:2]

            return dia + '.' + mes + '.' + anio[2:4]

    raise ValueError('Error en formato de fecha ' + fecha + ' (' + formato + ', ' + formato_ori + ')')


def add_days_datetime(fecha, formato_ori='yyyy-mm-dd', dias='1', formato='dd-MMM-yyyy'):
    """
    get result add days to datetime
    :param fecha: (object) datetime
    :param formato_ori: (str) string format-> original format
    :param dias: (object) days to add
    :param formato: (str) format to show new date
    :return: (str): datetime with add days
    """

    fecha_formato = get_date_to_db(fecha, formato_ori=formato_ori, formato='yyyy-mm-dd HH:ii:ss')

    anio = fecha_formato[0:4]
    mes = fecha_formato[5:7]
    dia = fecha_formato[8:10]
    hora = fecha_formato[11:13]
    minutos = fecha_formato[14:16]
    segundos = fecha_formato[17:19]

    nueva_fecha = anio + '-' + mes + '-' + dia
    fecha_aux = datetime.strptime(nueva_fecha, "%Y-%m-%d")
    fecha_suma = fecha_aux + timedelta(days=int(dias))
    fecha_suma = fecha_suma + timedelta(hours=int(hora)) + timedelta(minutes=int(minutos)) + timedelta(seconds=int(segundos))

    return get_date_show(fecha_suma, formato_ori='yyyy-mm-dd HH:ii:ss', formato=formato)

    raise ValueError('Error en formato de fecha ' + fecha + ' (' + formato + ', ' + formato_ori + ')')


def add_months_datetime(fecha, formato_ori='dd-MMM_yyyy', meses='1', formato='yyyy-mm-dd'):
    """

    :param fecha: (object) date to add months
    :param formato_ori: (str) fecha original format
    :param meses: (object) months to add date
    :param formato: (str) format to show date
    :return: (str) new datetime with months add
    """

    fecha_formato = get_date_to_db(fecha, formato_ori=formato_ori, formato='yyyy-mm-dd HH:ii:ss')

    anio = fecha_formato[0:4]
    mes = fecha_formato[5:7]
    dia = fecha_formato[8:10]
    hora = fecha_formato[11:13]
    minutos = fecha_formato[14:16]
    segundos = fecha_formato[17:19]

    nueva_fecha = anio + '-' + mes + '-' + dia
    fecha_aux = datetime.strptime(nueva_fecha, "%Y-%m-%d")
    fecha_suma = fecha_aux + relativedelta(months=int(meses))
    fecha_suma = fecha_suma + timedelta(hours=int(hora)) + timedelta(minutes=int(minutos)) + timedelta(seconds=int(segundos))

    return get_date_show(fecha_suma, formato_ori='yyyy-mm-dd HH:ii:ss', formato=formato)

    raise ValueError('Error en formato de fecha ' + fecha + ' (' + formato + ', ' + formato_ori + ')')


# def get_date_report():
#     """
#     date time report impression
#     :return: (str) date time report impression
#     """
#     now = datetime.now()
#     anio = '20' + str(now.year) if len(str(now.year)) == 2 else str(now.year)
#     mes = '0' + str(now.month) if len(str(now.month)) == 1 else str(now.month)
#     dia = '0' + str(now.day) if len(str(now.day)) == 1 else str(now.day)
#     hora = '0' + str(now.hour) if len(str(now.hour)) == 1 else str(now.hour)
#     minutos = '0' + str(now.minute) if len(str(now.minute)) == 1 else str(now.minute)
#     segundos = '0' + str(now.second) if len(str(now.second)) == 1 else str(now.second)

#     # print('mes..', mes)

#     return dia + '-' + get_month_3digits(mes) + '-' + anio + ' ' + hora + ':' + minutos


def get_seconds_date1_sub_date2(fecha1, fecha2, formato1='yyyy-mm-dd HH:ii:ss', formato2='yyyy-mm-dd HH:ii:ss'):
    """
    get seconds date1 sub date2
    :param fecha1: (object) date1
    :param fecha2: (object) date2
    :param formato1: (str) format date1, string case
    :param formato2: (str) format date2, string case
    :return: (int) seconds sub
    """

    # fecha 1
    fecha1_formato = get_date_to_db(fecha1, formato_ori=formato1, formato='yyyy-mm-dd HH:ii:ss')

    anio = fecha1_formato[0:4]
    mes = fecha1_formato[5:7]
    dia = fecha1_formato[8:10]
    hora = fecha1_formato[11:13]
    minutos = fecha1_formato[14:16]
    segundos = fecha1_formato[17:19]

    nueva_fecha = anio + '-' + mes + '-' + dia
    fecha1_aux = datetime.strptime(nueva_fecha, "%Y-%m-%d")
    fecha1_aux = fecha1_aux + timedelta(hours=int(hora)) + timedelta(minutes=int(minutos)) + timedelta(seconds=int(segundos))

    # fecha 2
    fecha2_formato = get_date_to_db(fecha2, formato_ori=formato2, formato='yyyy-mm-dd HH:ii:ss')

    anio = fecha2_formato[0:4]
    mes = fecha2_formato[5:7]
    dia = fecha2_formato[8:10]
    hora = fecha2_formato[11:13]
    minutos = fecha2_formato[14:16]
    segundos = fecha2_formato[17:19]

    nueva_fecha = anio + '-' + mes + '-' + dia
    fecha2_aux = datetime.strptime(nueva_fecha, "%Y-%m-%d")
    fecha2_aux = fecha2_aux + timedelta(hours=int(hora)) + timedelta(minutes=int(minutos)) + timedelta(seconds=int(segundos))

    resta = abs((fecha1_aux - fecha2_aux).seconds)

    return resta
