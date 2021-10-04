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
from configuraciones.models import Puntos, Almacenes
from inventarios.models import Registros
from permisos.models import UsersPerfiles

from inventarios.models import PlanPagos, PlanPagosDetalles, PlanPagosPagos
from clientes.models import Clientes
from django.contrib.auth.models import User
from status.models import Status

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, report_date
from utils.dates_functions import get_date_show

import os


# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
# pagesize = pagesizes.landscape(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_REGISTRO = ''
RPT_VENTA = 'venta'
RPT_VENTA_TITULO = 'titulo'
RPT_TOTAL = 'total'
RPT_FECHA = 'fecha'
RPT_CLIENTE = 'cliente'
RPT_ANULADO = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    datos_reporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datos_reporte['titulo'] = 'Pagos Plan de Pagos, ' + DATO_REGISTRO
    datos_reporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datos_reporte['logo'] = dir_img

    # para horizontal
    # posicionY = 207
    # cabecera(canvas, posY=posicionY, **datosReporte)

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

    # venta
    canvas.drawRightString(posX*mm, posY*mm, RPT_VENTA_TITULO + ': ')
    texto.setTextOrigin((posX-4)*mm, posY*mm)
    texto.textOut(RPT_VENTA)

    # fecha
    posY = posY - altoTxt
    canvas.drawRightString((posX-1)*mm, posY*mm, 'Fecha: ')
    texto.setTextOrigin((posX-4)*mm, posY*mm)
    texto.textOut(RPT_FECHA)
    # TOTAL
    canvas.drawRightString((posX-1+50)*mm, posY*mm, 'Total: ')
    texto.setTextOrigin((posX-4+50)*mm, posY*mm)
    texto.textOut(RPT_TOTAL)

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


def rptPlanPagoCuota(buffer_pdf, usuario, plan_pago_pago_id, crear_pdf='si'):

    # datos sucursal
    user_perfil = UsersPerfiles.objects.get(user_id=usuario)
    # permisos = get_permisos_usuario(usuario, settings.MOD_REPORTES)
    punto = Puntos.objects.get(pk=user_perfil.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    # cuota
    plan_pago_pago = PlanPagosPagos.objects.get(pk=plan_pago_pago_id)
    plan_pago_id = plan_pago_pago.plan_pago_id.plan_pago_id

    # PLAN DE PAGOS
    plan_pago = PlanPagos.objects.select_related('user_perfil_id').get(pk=plan_pago_id)

    # verificamos si esta anulado
    dato_anulado = ''
    if plan_pago_pago.status_id.status_id == settings.STATUS_ANULADO:
        usuario_perfil = UsersPerfiles.objects.get(pk=plan_pago_pago.user_perfil_id_anula)
        motivo_anula = plan_pago_pago.motivo_anula
        dato_anulado = usuario_perfil.user_id.username + ', ' + motivo_anula

    global DATO_REGISTRO, RPT_VENTA, RPT_VENTA_TITULO, RPT_FECHA, RPT_CLIENTE, RPT_ANULADO, RPT_TOTAL

    DATO_REGISTRO = str(plan_pago.plan_pago_id)
    RPT_TOTAL = str(plan_pago.monto_total) + ' Bs.'
    if plan_pago.registro_id != 0:
        RPT_VENTA_TITULO = 'Pedido'
        RPT_VENTA = str(plan_pago.registro_id)
        # recuperamos el almacen
        registro = Registros.objects.get(pk=plan_pago.registro_id)
        almacen2 = Almacenes.objects.get(pk=registro.almacen2_id)
        RPT_CLIENTE = almacen2.almacen

    if plan_pago.preventa_id != 0:
        RPT_VENTA_TITULO = 'Preventa'
        RPT_VENTA = str(plan_pago.preventa_id)
        # cliente
        cliente = Clientes.objects.get(pk=plan_pago.cliente_id)
        RPT_CLIENTE = cliente.apellidos + ' ' + cliente.nombres + ', CI/NIT: ' + cliente.ci_nit

    if plan_pago.venta_id != 0:
        RPT_VENTA_TITULO = 'Venta'
        RPT_VENTA = str(plan_pago.venta_id)
        # cliente
        cliente = Clientes.objects.get(pk=plan_pago.cliente_id)
        RPT_CLIENTE = cliente.apellidos + ' ' + cliente.nombres + ', CI/NIT: ' + cliente.ci_nit

    RPT_FECHA = get_date_show(fecha=plan_pago.fecha, formato='dd-MMM-yyyy HH:ii')
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

    #data.append(['Producto', 'F.Elab.', 'F.Venc.', 'Lote', 'Cant', 'Costo', 'Total'])
    data.append(['Cuota', 'Fecha', 'Detalle', 'Monto', 'Saldo'])
    filas = 0
    total = 0

    # cargamos los registros
    cuota = str(plan_pago_pago.numero_cuota)
    fecha_plan = get_date_show(fecha=plan_pago_pago.fecha, formato='dd-MMM-yyyy')
    monto = str(round(plan_pago_pago.monto, 2))
    saldo = str(round(plan_pago_pago.saldo, 2))
    observacion = Paragraph(plan_pago_pago.persona_paga, style_tabla_datos)

    datos_tabla = []
    datos_tabla = [cuota, fecha_plan, observacion, monto, saldo]
    data.append(datos_tabla)
    filas += 1
    total += plan_pago_pago.monto

    # aniadimos la tabla
    # datos_tabla = ['', '', 'Total: ', str(round(total, 2))]
    # data.append(datos_tabla)

    tabla_datos = Table(data, colWidths=[12*mm, 25*mm, 90*mm, 20*mm, 20*mm], repeatRows=1)
    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (4, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                     # ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                                     ('ALIGN', (3, 0), (4, filas+1), 'RIGHT'),
                                     ('ALIGN', (1, filas+1), (4, filas+1), 'RIGHT'),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (4, 0), 9),
                                     ('FONTSIZE', (0, 1), (4, filas+1), 8),
                                     ('FONTNAME', (0, 0), (4, 0), 'Helvetica'),
                                     ('FONTNAME', (0, 1), (4, filas), 'Helvetica'),
                                     ('FONTNAME', (0, filas+1), (4, filas+1), 'Helvetica-Bold'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
    # aniadimos la tabla
    # Story.append(Paragraph(titulo_ciudad, style_punto))
    Story.append(tabla_datos)
    # Story.append(Spacer(100*mm, 5*mm))

    # guardamos si se debe, caso contrario ya llenara los datos
    if crear_pdf == 'si':
        # creamos
        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
