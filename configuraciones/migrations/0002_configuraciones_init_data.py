# Generated by Django 3.1.1 on 2020-09-07 21:18

from django.db import migrations
from django.contrib.auth.models import User
from configuraciones.models import Configuraciones, Paises, Ciudades, Zonas, Sucursales, Puntos, Cajas, TiposMonedas, Monedas, Almacenes, Proveedores, Lineas, PuntosAlmacenes
from status.models import Status
from permisos.models import UsersPerfiles


def load_data(apps, schema_editor):
    # configuraciones
    configuraciones_add = Configuraciones.objects.create(configuracion_id=1, cant_per_page=30, cant_products_home=10, vender_fracciones='si')
    configuraciones_add.save()

    # paises
    paises_add = Paises.objects.create(pais_id=1, pais='Bolivia')
    paises_add.save()

    # datos
    user_admin = User.objects.get(pk=1)
    user_perfil = UsersPerfiles.objects.get(user_id=user_admin)
    bolivia = Paises.objects.get(pk=1)
    status_activo = Status.objects.get(pk=1)

    # ciudades
    ciudad_add = Ciudades.objects.create(pais_id=bolivia, user_perfil_id=user_perfil, status_id=status_activo, ciudad='Cochabamba', codigo='CBA', created_at='now', updated_at='now')
    ciudad_add.save()

    # ciudad cbba
    cochabamba = Ciudades.objects.get(pk=1)

    # zonas
    zona_add = Zonas.objects.create(ciudad_id=cochabamba, user_perfil_id=user_perfil, status_id=status_activo, zona='Zona Central', codigo='centro', created_at='now', updated_at='now')
    zona_add.save()

    # zona cbba
    zona_cbba = Zonas.objects.get(pk=1)

    # SUCURSALES
    sucursal_add = Sucursales.objects.create(ciudad_id=cochabamba, zona_id=zona_cbba, user_perfil_id=user_perfil, status_id=status_activo, sucursal='Sucursal Central', codigo='SC-CBA', email='acc.claros@gmail.com',
                                             empresa='Hamburguesas - Delicia', direccion='Av. Santa Cruz # 4566', ciudad='Cochabamba - Bolivia', telefonos='4578996 - 78441552', actividad='Servicio de Comida de Rapida', datos_mapa='', ubicacion_mapa='', created_at='now', updated_at='now')
    sucursal_add.save()

    # sucursal central
    sucursal_central = Sucursales.objects.get(pk=1)

    # puntos
    punto_add = Puntos.objects.create(sucursal_id=sucursal_central, user_perfil_id=user_perfil, status_id=status_activo, punto='Punto 1',
                                      codigo='P1', impresora_reportes='impresora reportes', created_at='now', updated_at='now')
    punto_add.save()
    punto2_add = Puntos.objects.create(sucursal_id=sucursal_central, user_perfil_id=user_perfil, status_id=status_activo, punto='Punto 2',
                                       codigo='P2', impresora_reportes='impresora reportes', created_at='now', updated_at='now')
    punto2_add.save()

    # tipos monedas
    tipo_moneda_add = TiposMonedas.objects.create(tipo_moneda_id=1, status_id=status_activo, tipo_moneda='Bolivianos', codigo='Bs.')
    tipo_moneda_add.save()

    # monedas
    tipo_bs = TiposMonedas.objects.get(pk=1)
    # bs
    moneda = Monedas.objects.create(moneda_id=1, tipo_moneda_id=tipo_bs, monto=0.10, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=2, tipo_moneda_id=tipo_bs, monto=0.20, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=3, tipo_moneda_id=tipo_bs, monto=0.50, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=4, tipo_moneda_id=tipo_bs, monto=1.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=5, tipo_moneda_id=tipo_bs, monto=2.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=6, tipo_moneda_id=tipo_bs, monto=5.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=7, tipo_moneda_id=tipo_bs, monto=10.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=8, tipo_moneda_id=tipo_bs, monto=20.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=9, tipo_moneda_id=tipo_bs, monto=50.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=10, tipo_moneda_id=tipo_bs, monto=100.00, status_id=status_activo)
    moneda.save()
    moneda = Monedas.objects.create(moneda_id=11, tipo_moneda_id=tipo_bs, monto=200.00, status_id=status_activo)
    moneda.save()

    # cajas
    punto1 = Puntos.objects.get(pk=1)
    punto2 = Puntos.objects.get(pk=2)
    caja_Bs = Cajas.objects.create(punto_id=punto1, tipo_moneda_id=tipo_bs, user_perfil_id=user_perfil, status_id=status_activo, caja='Caja1-P1-Bs', codigo='C1-P1-Bs', created_at='now', updated_at='now')
    caja_Bs.save()
    caja2_Bs = Cajas.objects.create(punto_id=punto2, tipo_moneda_id=tipo_bs, user_perfil_id=user_perfil, status_id=status_activo, caja='Caja2-P2-Bs', codigo='C2-P2-Bs', created_at='now', updated_at='now')
    caja2_Bs.save()

    # almacenes
    almacen_add = Almacenes.objects.create(almacen='Almacen Central', codigo='AC', sucursal_id=sucursal_central, status_id=status_activo, created_at='now', updated_at='now')
    almacen_add.save()
    # dato
    almacen_central = Almacenes.objects.get(pk=1)

    # proveedores
    proveedores_add = Proveedores.objects.create(proveedor='Proveedor', codigo='Prv', email='contact@proveedor.com', direccion='Av. Costanera # 2345',
                                                 telefonos='4512223', nit='4456582016', status_id=status_activo, created_at='now', updated_at='now')
    proveedores_add.save()
    # dato
    proveedor1 = Proveedores.objects.get(pk=1)

    # lineas
    linea_add = Lineas.objects.create(linea='Hamburguesas', codigo='HAM', linea_principal=1, linea_superior_id=0, descripcion='Hamburguesas en general',
                                      imagen='', imagen_thumb='', proveedor_id=proveedor1, status_id=status_activo, created_at='now', updated_at='now')
    linea_add.save()

    # puntos almacenes
    puntos_almacenes_add = PuntosAlmacenes.objects.create(punto_id=punto1, almacen_id=almacen_central, status_id=status_activo, created_at='now', updated_at='now')
    puntos_almacenes_add.save()


def delete_data(apps, schema_editor):
    puntos_almacenes_del = apps.get_model('configuraciones', 'PuntosAlmacenes')
    puntos_almacenes_del.objects.all().delete

    lineas_del = apps.get_model('configuraciones', 'Lineas')
    lineas_del.objects.all().delete

    almacenes_del = apps.get_model('configuraciones', 'Almacenes')
    almacenes_del.objects.all().delete

    cajas_del = apps.get_model('configuraciones', 'Cajas')
    cajas_del.objects.all().delete

    monedas_del = apps.get_model('configuraciones', 'Monedas')
    monedas_del.objects.all().delete

    tipos_monedas_del = apps.get_model('configuraciones', 'TiposMonedas')
    tipos_monedas_del.objects.all().delete

    puntos_del = apps.get_model('configuraciones', 'Puntos')
    puntos_del.objects.all().delete

    sucursales_del = apps.get_model('configuraciones', 'Sucursales')
    sucursales_del.objects.all().delete

    zonas_del = apps.get_model('configuraciones', 'Zonas')
    zonas_del.objects.all().delete

    ciudades_del = apps.get_model('configuraciones', 'Ciudades')
    ciudades_del.objects.all().delete

    paises_del = apps.get_model('configuraciones', 'Paises')
    paises_del.objects.all().delete

    configuraciones_del = apps.get_model('configuraciones', 'Configuraciones')
    configuraciones_del.objects.all().delete


class Migration(migrations.Migration):

    dependencies = [
        ('configuraciones', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data, delete_data),
    ]
