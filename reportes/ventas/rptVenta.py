from app.settings import PRODUCTOS_LBL_LOTE
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import pagesizes
# from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

from datetime import datetime
from django.apps import apps

from reportlab.pdfbase.pdfmetrics import stringWidth

# imagen
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from configuraciones.models import Puntos
from permisos.models import UsersPerfiles
from ventas.models import Ventas, VentasDetalles
from inventarios.models import PlanPagos, PlanPagosDetalles
from django.contrib.auth.models import User

# settings
from django.conf import settings

# utils
from utils.dates_functions import get_date_show
from utils.permissions import get_sucursal_settings, report_date

from reportlab.platypus import PageBreak

import os
import copy

# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
# pagesize = pagesizes.landscape(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_REGISTRO = ''
RPT_ALMACEN = 'almacen'
RPT_FECHA = 'fecha'
RPT_CLIENTE = 'cliente'
RPT_ANULADO = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datosReporte['titulo'] = 'Venta, ' + DATO_REGISTRO
    datosReporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datosReporte['logo'] = dir_img

    # para horizontal
    # posicionY = 207
    # cabecera(canvas, posY=posicionY, **datosReporte)

    # vertical
    cabecera(canvas=canvas, **datosReporte)

    # cabecera
    posY = 244
    altoTxt = 6
    posX = 40

    # iniciando el objecto de texto en las coordenadas iniciales
    texto = canvas.beginText()
    texto.setFont("Helvetica", 10)
    texto.setFillColorRGB(0, 0, 0)

    # almacen
    canvas.drawRightString(posX*mm, posY*mm, 'Almacen: ')
    texto.setTextOrigin((posX-4)*mm, posY*mm)
    texto.textOut(RPT_ALMACEN)

    # fecha
    posY = posY - altoTxt
    canvas.drawRightString((posX-1)*mm, posY*mm, 'Fecha: ')
    texto.setTextOrigin((posX-4)*mm, posY*mm)
    texto.textOut(RPT_FECHA)

    # concepto
    posY = posY - altoTxt
    canvas.drawRightString(posX*mm, posY*mm, 'Cliente: ')
    texto.setTextOrigin((posX-4)*mm, posY*mm)
    texto.textOut(RPT_CLIENTE)

    # anulado
    if RPT_ANULADO != '':
        posY = posY - altoTxt
        canvas.drawRightString(posX*mm, posY*mm, 'Anulado: ')
        texto.setTextOrigin((posX-4)*mm, posY*mm)
        texto.textOut(RPT_ANULADO)

    # dibujamos los objetos texto
    canvas.drawText(texto)

    # pie de pagina
    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))

    canvas.restoreState()


def width_string(string, font, size, charspace):
    width = stringWidth(string, font, size)
    width += (len(string) - 1) * charspace
    return width


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptVenta(buffer_pdf, usuario, venta_id):

    # datos sucursal
    user_perfil = UsersPerfiles.objects.get(user_id=usuario)
    # permisos = get_permisos_usuario(usuario, settings.MOD_REPORTES)
    punto = Puntos.objects.get(pk=user_perfil.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    # registros
    venta = Ventas.objects.select_related('almacen_id').select_related('almacen_id__sucursal_id').select_related('user_perfil_id').get(pk=venta_id)
    ventas_detalles = VentasDetalles.objects.select_related('producto_id').select_related('producto_id__linea_id').filter(venta_id=venta).order_by('producto_id__linea_id__linea', 'producto_id__producto')

    # verificamos si esta anulado
    dato_anulado = ''
    if venta.status_id.status_id == settings.STATUS_ANULADO:
        usuario_perfil_anula = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=registro.user_perfil_id_anula)
        motivo_anula = venta.motivo_anula
        dato_anulado = usuario_perfil_anula.user_id.username + ', ' + motivo_anula

    global DATO_REGISTRO, RPT_ALMACEN, RPT_FECHA, RPT_CLIENTE, RPT_ANULADO
    DATO_REGISTRO = str(venta.venta_id)
    RPT_ALMACEN = venta.almacen_id.sucursal_id.sucursal + ' - ' + venta.almacen_id.almacen
    RPT_FECHA = get_date_show(fecha=venta.fecha, formato='dd-MMM-yyyy HH:ii')
    RPT_CLIENTE = venta.apellidos + ' ' + venta.nombres + ', CI/NIT: ' + venta.ci_nit
    RPT_ANULADO = dato_anulado

    styles = getSampleStyleSheet()
    # personalizamos
    style_tabla_datos = ParagraphStyle('tabla_datos',
                                       fontName="Helvetica",
                                       fontSize=8,
                                       parent=styles['Normal'],
                                       alignment=0,
                                       spaceAfter=0)

    # hoja vertical
    doc = SimpleDocTemplate(buffer_pdf, pagesize=letter, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    # hoja horizontal
    # doc = SimpleDocTemplate(buffer_pdf, pagesize=landscape(letter), leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    # armamos
    Story = []
    if RPT_ANULADO == '':
        Story.append(Spacer(100*mm, 43*mm))
    else:
        Story.append(Spacer(100*mm, 48*mm))

    # tabla
    datos_tabla = []
    data = []

    if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
        data.append(['Producto', 'F.Elab.', 'F.Venc.', 'Lote', 'Cant', 'Costo', 'Total'])
    else:
        if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
            data.append(['Producto', 'Cant', 'Costo', 'Total'])
        else:
            if settings.PRODUCTOS_USAR_LOTE:
                data.append(['Producto', settings.PRODUCTOS_LBL_LOTE, 'Cant', 'Costo', 'Total'])

    filas = 0
    total = 0

    # cargamos los registros
    for detalle in ventas_detalles:
        producto = Paragraph(detalle.producto_id.linea_id.linea + '-' + detalle.producto_id.producto, style_tabla_datos)
        # fecha elaboracion
        if detalle.fecha_elaboracion:
            fecha_elaboracion = get_date_show(fecha=detalle.fecha_elaboracion, formato='dd-MMM-yyyy')
        else:
            fecha_elaboracion = ''

        # fecha elaboracion
        if detalle.fecha_vencimiento:
            fecha_vencimiento = get_date_show(fecha=detalle.fecha_vencimiento, formato='dd-MMM-yyyy')
        else:
            fecha_vencimiento = ''

        # lote
        if detalle.lote:
            lote = Paragraph(detalle.lote, style_tabla_datos)
        else:
            lote = ''

        datos_tabla = []

        if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
            datos_tabla = [producto, fecha_elaboracion, fecha_vencimiento, lote, str(detalle.cantidad), str(round(detalle.costo, 2)), str(round(detalle.total, 2))]
        else:
            if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
                datos_tabla = [producto, str(detalle.cantidad), str(round(detalle.costo, 2)), str(round(detalle.total, 2))]
            else:
                if settings.PRODUCTOS_USAR_LOTE:
                    datos_tabla = [producto, detalle.lote, str(detalle.cantidad), str(round(detalle.costo, 2)), str(round(detalle.total, 2))]

        data.append(datos_tabla)
        filas += 1
        total += detalle.total

    subtotal = venta.subtotal
    descuento = venta.descuento
    porcentaje_descuento = venta.porcentaje_descuento
    total = venta.total

    # aniadimos la tabla
    if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
        datos_tabla = ['', '', '', '', '', 'SubT: ', str(round(subtotal, 2))]
        data.append(datos_tabla)
        # descuento
        datos_tabla = ['', '', '', '', str(round(porcentaje_descuento, 2)) + '%', 'Desc: ', str(round(descuento, 2))]
        data.append(datos_tabla)
        # total
        datos_tabla = ['', '', '', '', '', 'Total: ', str(round(total, 2))]
        data.append(datos_tabla)
        filas += 2

    else:
        if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
            datos_tabla = ['', '', 'SubT: ', str(round(subtotal, 2))]
            data.append(datos_tabla)
            # descuento
            datos_tabla = ['', str(round(porcentaje_descuento, 2)) + '%', 'Desc: ',  str(round(descuento, 2))]
            data.append(datos_tabla)
            # total
            datos_tabla = ['', '', 'Total: ', str(round(total, 2))]
            data.append(datos_tabla)
            filas += 2
        else:
            if settings.PRODUCTOS_USAR_LOTE:
                datos_tabla = ['', '', '', 'SubT: ', str(round(subtotal, 2))]
                data.append(datos_tabla)
                # descuento
                datos_tabla = ['', '', str(round(porcentaje_descuento, 2)) + '%', 'Desc: ',  str(round(descuento, 2))]
                data.append(datos_tabla)
                # total
                datos_tabla = ['', '', '', 'Total: ', str(round(total, 2))]
                data.append(datos_tabla)
                filas += 2

    if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
        tabla_datos = Table(data, colWidths=[80*mm, 20*mm, 20*mm, 20*mm, 15*mm, 15*mm, 18*mm], repeatRows=1)
        num_cols = 7 - 1
        align_right_from = 4
    else:
        if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
            tabla_datos = Table(data, colWidths=[140*mm, 15*mm, 15*mm, 18*mm], repeatRows=1)
            num_cols = 4-1
            align_right_from = 1
        else:
            if settings.PRODUCTOS_USAR_LOTE:
                tabla_datos = Table(data, colWidths=[125*mm, 15*mm, 15*mm, 15*mm, 18*mm], repeatRows=1)
                num_cols = 5-1
                align_right_from = 2

    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (num_cols, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                     ('ALIGN', (align_right_from, 0), (num_cols, filas+1), 'RIGHT'),
                                     #('ALIGN', (5, filas+1), (6, filas+1), 'RIGHT'),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (num_cols, 0), 9),
                                     ('FONTSIZE', (0, 1), (num_cols, filas+1), 8),
                                     ('FONTNAME', (0, 0), (num_cols, 0), 'Helvetica'),
                                     ('FONTNAME', (0, 1), (num_cols, filas), 'Helvetica'),
                                     ('FONTNAME', (0, filas+1), (num_cols, filas+1), 'Helvetica-Bold'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
    # aniadimos la tabla
    # Story.append(Paragraph(titulo_ciudad, style_punto))
    Story.append(tabla_datos)
    # Story.append(Spacer(100*mm, 5*mm))

    # verificamos si tiene plan de pagos
    if venta.tipo_venta == 'PLANPAGO':
        Story.append(PageBreak())
        # creamos la tabla
        plan_pago = PlanPagos.objects.get(venta_id=venta.venta_id)
        pp_detalles = PlanPagosDetalles.objects.filter(plan_pago_id=plan_pago).order_by('numero_cuota')

        # tabla
        datos_tabla = []
        data = []

        data.append(['Cuotas :', str(plan_pago.numero_cuotas), 'Monto :', str(plan_pago.monto_total) + ' Bs.'])
        data.append(['Fecha :', get_date_show(fecha=plan_pago.fecha, formato='dd-MMM-yyyy'), '', ''])

        tabla_datos = Table(data, colWidths=[25*mm, 30*mm, 25*mm, 30*mm], repeatRows=1)
        tabla_datos.setStyle(TableStyle([
                                        # ('BACKGROUND', (0, 0), (3, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                        # ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                                        ('ALIGN', (0, 0), (0, 1), 'RIGHT'),
                                        ('ALIGN', (1, 0), (1, 1), 'LEFT'),

                                        ('ALIGN', (2, 0), (2, 1), 'RIGHT'),
                                        ('ALIGN', (3, 0), (3, 1), 'LEFT'),

                                        #('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                        ('FONTSIZE', (0, 0), (-1, -1), 9),

                                        ('FONTNAME', (0, 0), (0, 1), 'Helvetica-Bold'),
                                        ('FONTNAME', (2, 0), (2, 1), 'Helvetica-Bold'),

                                        ('FONTNAME', (1, 0), (1, 1), 'Helvetica'),
                                        ('FONTNAME', (3, 0), (3, 1), 'Helvetica'),

                                        ('LEFTPADDING', (0, 0), (3, 1), 1),
                                        ('RIGHTPADDING', (0, 0), (3, 1), 1),
                                        ('VALIGN', (0, 0), (3, 1), 'TOP'),
                                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
        # aniadimos la tabla
        Story.append(tabla_datos)

        # tabla
        datos_tabla = []
        data = []

        # cabecera
        data.append(['Cuota', 'Fecha', 'Monto', 'Saldo'])
        filas = 0
        total = 0

        # cargamos los registros
        for detalle in pp_detalles:
            datos_tabla = []
            datos_tabla = [str(detalle.numero_cuota), get_date_show(fecha=detalle.fecha, formato='dd-MMM-yyyy'), str(detalle.monto), str(detalle.saldo)]
            data.append(datos_tabla)
            filas += 1
            total += detalle.monto

        # aniadimos la tabla
        datos_tabla = ['', 'Total :', str(round(total, 2)), '']
        data.append(datos_tabla)

        tabla_datos = Table(data, colWidths=[20*mm, 30*mm, 25*mm, 25*mm], repeatRows=1)
        tabla_datos.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (3, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                        ('ALIGN', (0, filas), (1, filas), 'LEFT'),
                                        ('ALIGN', (1, filas+1), (1, filas+1), 'RIGHT'),
                                        ('ALIGN', (2, 0), (3, filas+1), 'RIGHT'),

                                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                        ('FONTSIZE', (0, 0), (-1, -1), 9),

                                        ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
                                        ('FONTNAME', (1, filas+1), (3, filas+1), 'Helvetica-Bold'),

                                        ('FONTNAME', (0, 1), (3, filas), 'Helvetica'),

                                        ('LEFTPADDING', (0, 0), (3, filas+1), 1),
                                        ('RIGHTPADDING', (0, 0), (3, filas+1), 1),
                                        ('VALIGN', (0, 0), (3, filas+1), 'TOP'),
                                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
        # aniadimos la tabla
        Story.append(tabla_datos)

    # creamos
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
