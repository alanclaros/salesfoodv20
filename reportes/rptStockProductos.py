from app.settings import PRODUCTOS_LBL_LOTE
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import pagesizes
#from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

from datetime import datetime

# imagen
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from configuraciones.models import Puntos, Sucursales
from permisos.models import UsersPerfiles

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, report_date
from utils.dates_functions import get_date_system, get_date_show

# clases
from controllers.reportes.ReportesController import ReportesController


import os
import copy

# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_CAJA = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datosReporte['titulo'] = 'Stock de Productos ' + DATO_CAJA
    datosReporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datosReporte['logo'] = dir_img

    cabecera(canvas, **datosReporte)

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptStockProductos(buffer_pdf, usuario, linea_id, almacen_id):
    # pdf
    #pdf = canvas.Canvas(buffer, pagesize=letter)

    # datos sucursal
    user_perfil = UsersPerfiles.objects.get(user_id=usuario)
    #permisos = get_permisos_usuario(usuario, settings.MOD_REPORTES)
    punto = Puntos.objects.get(pk=user_perfil.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    styles = getSampleStyleSheet()
    # personalizamos
    style_almacen = ParagraphStyle('almacen',
                                   fontName="Helvetica-Bold",
                                   fontSize=12,
                                   parent=styles['Normal'],
                                   alignment=1,
                                   spaceAfter=10)

    doc = SimpleDocTemplate(buffer_pdf, pagesize=letter, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    """datos del reporte"""
    reporte_controller = ReportesController()
    datos_reporte = reporte_controller.datos_stock_productos(usuario, linea_id=linea_id, almacen_id=almacen_id)
    # print(datos_reporte)

    Story = []
    Story.append(Spacer(100*mm, 22*mm))

    almacen_actual = ''
    datos_tabla = []
    data = []
    filas = 0
    bande = 0

    for dato in datos_reporte:

        # almacen
        if almacen_actual != dato['almacen']:
            bande += 1
            # primera vuelta, no se cierra tabla
            if bande > 1:
                # cerramos tabla anterior y aniadimos
                if len(data) > 0:
                    #datos_tabla = ['', '', '', 'Totales: ', str(subtotal), str(descuento), str(total) + ' ' + codigo_moneda]
                    # data.append(datos_tabla)

                    # ancho columnas
                    if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
                        tabla_datos = Table(data, colWidths=[50*mm, 60*mm, 22*mm, 22*mm, 22*mm, 16*mm], repeatRows=1)
                        num_cols = 6-1
                        align_right_from = 5
                    else:
                        if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
                            tabla_datos = Table(data, colWidths=[181*mm, 16*mm], repeatRows=1)
                            num_cols = 2-1
                            align_right_from = 1
                        else:
                            if settings.PRODUCTOS_USAR_LOTE:
                                tabla_datos = Table(data, colWidths=[65*mm, 70*mm, 15*mm, 16*mm], repeatRows=1)
                                num_cols = 4-1
                                align_right_from = 3

                    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (num_cols, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                                     ('ALIGN', (align_right_from, 0), (num_cols, filas), 'RIGHT'),
                                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                                     ('FONTSIZE', (0, 0), (num_cols, 0), 10),
                                                     ('FONTSIZE', (0, 1), (-1, -1), 9),
                                                     ('FONTNAME', (0, 0), (num_cols, 0), 'Helvetica'),
                                                     ('FONTNAME', (0, 1), (num_cols, filas), 'Helvetica'),
                                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
                    # aniadimos la tabla
                    Story.append(Paragraph(almacen_actual, style_almacen))
                    Story.append(tabla_datos)
                    Story.append(Spacer(100*mm, 5*mm))

            # creamos tabla para este almacen
            data = []

            if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
                data.append(['Linea', 'Producto', 'F.Elab', 'F.Venc', 'Lote', 'Cant'])
            else:
                if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
                    data.append(['Insumo', 'Cant'])
                else:
                    if settings.PRODUCTOS_USAR_LOTE:
                        data.append(['Linea', 'Producto', settings.PRODUCTOS_LBL_LOTE, 'Cant'])

            filas = 0
            total = 0

        # seguimos llenando de datos la tabla hasta cambiar de caja, sucursal o ciudad
        linea = Paragraph(dato['linea'])
        producto = Paragraph(dato['producto'])

        if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
            datos_tabla = [linea, producto, dato['fecha_elaboracion'], dato['fecha_vencimiento'], dato['lote'], str(dato['cantidad'])]
        else:
            if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
                datos_tabla = [producto, str(dato['cantidad'])]
            else:
                if settings.PRODUCTOS_USAR_LOTE:
                    datos_tabla = [linea, producto, dato['lote'], str(dato['cantidad'])]

        data.append(datos_tabla)
        filas += 1

        # titulo de ciudad, despues que se terminen las tablas
        if almacen_actual != dato['almacen']:
            # Story.append(Paragraph(dato['almacen'], style_almacen))
            almacen_actual = dato['almacen']

    # datos de la ultima tabla
    if len(data) > 0:

        if settings.PRODUCTOS_USAR_FECHAS and settings.PRODUCTOS_USAR_LOTE:
            tabla_datos = Table(data, colWidths=[50*mm, 60*mm, 22*mm, 22*mm, 22*mm, 16*mm], repeatRows=1)
            num_cols = 6-1
            align_right_from = 5
        else:
            if not settings.PRODUCTOS_USAR_FECHAS and not settings.PRODUCTOS_USAR_LOTE:
                tabla_datos = Table(data, colWidths=[181*mm, 16*mm], repeatRows=1)
                num_cols = 2-1
                align_right_from = 1
            else:
                if not settings.PRODUCTOS_USAR_LOTE:
                    tabla_datos = Table(data, colWidths=[65*mm, 70*mm, 15*mm, 16*mm], repeatRows=1)
                    num_cols = 4-1
                    align_right_from = 3

        tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (num_cols, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                         ('ALIGN', (align_right_from, 0), (num_cols, filas), 'RIGHT'),
                                         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                         ('FONTSIZE', (0, 0), (num_cols, 0), 10),
                                         ('FONTSIZE', (0, 1), (-1, -1), 9),
                                         ('FONTNAME', (0, 0), (num_cols, 0), 'Helvetica'),
                                         ('FONTNAME', (0, 1), (num_cols, filas), 'Helvetica'),
                                         ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                         ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                         ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                         ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
        # aniadimos la tabla
        Story.append(Paragraph(almacen_actual, style_almacen))
        Story.append(tabla_datos)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
