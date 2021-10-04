from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import pagesizes
# from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

from datetime import datetime

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
from pedidos.models import Pedidos, PedidosDetalles
from django.contrib.auth.models import User

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings
from utils.dates_functions import get_date_report, get_date_show

from reportlab.platypus import PageBreak

from controllers.pedidos.PedidosController import PedidosController

import os
import copy

# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
# pagesize = pagesizes.landscape(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_REGISTRO = ''
RPT_TOTAL = 'total'
RPT_FECHA = 'fecha'
RPT_CLIENTE = 'cliente'
RPT_ANULADO = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    datos_reporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datos_reporte['titulo'] = 'Pedido, ' + DATO_REGISTRO
    datos_reporte['fecha_impresion'] = get_date_report()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datos_reporte['logo'] = dir_img

    # para horizontal
    # posicionY = 207
    # cabecera(canvas, posY=posicionY, **datos_reporte)

    # vertical
    cabecera(canvas=canvas, **datos_reporte)

    # cabecera
    posY = 244
    altoTxt = 6
    posX = 40

    # iniciando el objecto de texto en las coordenadas iniciales
    texto = canvas.beginText()
    texto.setFont("Helvetica", 10)
    texto.setFillColorRGB(0, 0, 0)

    # fecha
    canvas.drawRightString(posX*mm, posY*mm, 'Fecha: ')
    texto.setTextOrigin((posX-4)*mm, posY*mm)
    texto.textOut(RPT_FECHA)

    # cliente
    posY = posY - altoTxt
    canvas.drawRightString((posX-1)*mm, posY*mm, 'Cliente: ')
    texto.setTextOrigin((posX-4)*mm, posY*mm)
    texto.textOut(RPT_CLIENTE)

    # total
    posY = posY - altoTxt
    canvas.drawRightString(posX*mm, posY*mm, 'Total: ')
    texto.setTextOrigin((posX-4)*mm, posY*mm)
    texto.textOut(RPT_TOTAL)

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


def rptPedidoCliente(buffer_pdf, usuario, pedido_id):

    # datos sucursal
    UP = UsersPerfiles.objects.get(user_id=usuario)
    # permisos = get_permisos_usuario(usuario, settings.MOD_REPORTES)
    punto = Puntos.objects.get(pk=UP.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    # registros
    pedido_controller= PedidosController()
    datos_pedido= pedido_controller.get_pedido(pedido_id=pedido_id)

    # verificamos si esta anulado
    dato_anulado = ''
    if datos_pedido['status_id_id'] == settings.STATUS_ANULADO:
        usuario_anula = User.objects.get(pk=datos_pedido['user_id_anula'])
        motivo_anula = datos_pedido['motivo_anula']
        dato_anulado = usuario_anula.username + ', ' + motivo_anula

    global DATO_REGISTRO, RPT_TOTAL, RPT_FECHA, RPT_CLIENTE, RPT_ANULADO
    DATO_REGISTRO = str(datos_pedido['pedido_id'])
    RPT_TOTAL = str(datos_pedido['total']) + ' Bs.'
    RPT_FECHA = get_date_show(fecha=datos_pedido['created_at'], formato='dd-MMM-yyyy HH:ii')
    RPT_CLIENTE = datos_pedido['apellidos'] + ' ' + datos_pedido['nombres'] + ', (' + datos_pedido['email'] + ') - ' + datos_pedido['telefonos']
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

    data.append(['Producto', 'Cant', 'Costo', 'Total'])
    filas = 0
    total = 0

    # cargamos los registros
    for detalle in datos_pedido['detalles']:
        producto = Paragraph(detalle['producto'], style_tabla_datos)

        datos_tabla = []
        datos_tabla = [producto, str(detalle['cantidad']), str(round(detalle['costo'],2)), str(round(detalle['total'],2))]
        data.append(datos_tabla)
        filas += 1
        total += detalle['total']

    # aniadimos la tabla
    datos_tabla = ['', '', 'Total: ', str(round(total, 2))]
    data.append(datos_tabla)

    tabla_datos = Table(data, colWidths=[150*mm, 15*mm, 15*mm, 20*mm], repeatRows=1)
    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (3, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                     # ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                                     ('ALIGN', (1, 0), (3, filas+1), 'RIGHT'),
                                     ('ALIGN', (2, filas+1), (3, filas+1), 'RIGHT'),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (3, 0), 9),
                                     ('FONTSIZE', (0, 1), (3, filas+1), 8),
                                     ('FONTNAME', (0, 0), (3, 0), 'Helvetica'),
                                     ('FONTNAME', (0, 1), (3, filas), 'Helvetica'),
                                     ('FONTNAME', (0, filas+1), (3, filas+1), 'Helvetica-Bold'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
    # aniadimos la tabla
    # Story.append(Paragraph(titulo_ciudad, style_punto))
    Story.append(tabla_datos)
    # Story.append(Spacer(100*mm, 5*mm))

    # creamos
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
