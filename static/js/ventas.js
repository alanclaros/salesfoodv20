/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

//variables indica si es de preventa o no
from_preventa = 'no';
from_preventa_id = '0';

//control especifico del modulo
function controlModulo() {

    return true;
}

function confirmarAnularVenta() {

    motivo_an = Trim(document.getElementById('motivo_anula').value);
    if (motivo_an == '') {
        alert('Debe llenar el motivo');
        return false;
    }

    if (confirm('Esta seguro de querer anular esta venta?')) {
        token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

        document.forms['formulario'].elements['add_button'].disabled = true;
        document.forms['formulario'].elements['button_cancel'].disabled = true;

        datos_operation = {
            'module_x': document.forms['form_operation'].elements['module_x'].value,
            'csrfmiddlewaretoken': token_operation,
            'operation_x': 'anular',
            'anular_x': 'acc',
        }
        datos_operation['id'] = document.forms['form_operation'].elements['id'].value;
        datos_operation['motivo_anula'] = motivo_an;

        div_modulo.html(imagen_modulo);
        div_modulo.load('/', datos_operation, function () {
            //termina de cargar la ventana
        });
    }
}

async function sendSearchVenta() {
    var fd = new FormData(document.forms['search']);

    div_modulo.html(imagen_modulo);

    let result;

    try {
        result = await $.ajax({
            url: '/',
            method: 'POST',
            type: 'POST',
            cache: false,
            data: fd,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response != 0) {
                    div_modulo.html(response);
                } else {
                    alert('error al realizar la operacion, intentelo de nuevo');
                }
            },
            error: function (qXHR, textStatus, errorThrown) {
                console.log(errorThrown); console.log(qXHR); console.log(textStatus);
            },
        });
        //alert(result);
    }
    catch (e) {
        console.error(e);
    }
}

function mostrarPPVenta() {
    tipo_venta = document.getElementById('tipo_venta').value;
    fila_pp = $('#fila_pp');
    if (tipo_venta == 'PLANPAGO') {
        fila_pp.fadeIn('slow');
    }
    else {
        fila_pp.fadeOut('slow');
    }
}

function tipoPPVenta() {
    tipo_pp = document.getElementById('radio1_pp');
    dias = document.getElementById('dias');
    if (tipo_pp.checked) {
        dias.value = '';
        dias.readOnly = true;
    }
    else {
        dias.value = '';
        dias.readOnly = false;
    }
}

function cancelarVenta() {
    div_datos = $('#div_listap');
    div_ventas_dia = $('#div_ventas_dia');

    div_datos.fadeOut('slow');
    div_ventas_dia.fadeIn('slow');

    //mostramos el boton de nueva venta
    btn_cancelar = $('#btn_cancelar_venta');
    btn_nuevo = $('#btn_nueva_venta');

    btn_cancelar.fadeOut('slow');
    btn_nuevo.fadeIn('slow');
}

function nuevaVenta() {
    ad_operacion_mod = document.getElementById('tipo_operacion');
    ad_m_id_mod = document.getElementById('m_venta_id');
    ad_operacion_mod.value = 'add';
    ad_m_id_mod.value = '';

    //almacen
    almacen = document.getElementById('almacen');
    tipo_venta = document.getElementById('tipo_venta');
    costo_abc = document.getElementById('costo_abc');

    //marcamos como que no se cargo de preventa
    from_preventa = 'no';
    from_preventa_id = '0';

    //verificamos almacen
    if (almacen.value == '0') {
        alert('Debe seleccionar un almacen');
        almacen.focus();
        return false;
    }

    //tipo de venta
    if (tipo_venta.value == '0') {
        alert('Debe seleccionar un tipo de venta');
        tipo_venta.focus();
        return false;
    }

    //costo abc
    if (costo_abc.value == '0') {
        alert('Debe seleccionar un tipo de costo');
        costo_abc.focus();
        return false;
    }

    //si el tipo de venta estaba en plan pago cambiamos a contado
    if (tipo_venta.value == 'PLANPAGO') {
        tipo_venta.value = 'CONTADO';
        fila_pp = $('#fila_pp');
        fila_pp.fadeOut('slow');
    }

    //reiniciamos el cliente al defecto
    mostrarDatosClienteVenta('SIN NOMBRE', '', '0', '', '');

    //lugar y mesa
    n_lugar = document.getElementById('lugar');
    n_mesa = document.getElementById('mesa');
    n_observacion = document.getElementById('observacion');
    n_lugar.selectedIndex = 0;
    n_mesa.value = '';
    n_observacion.value = '';

    div_datos = $('#div_listap');
    div_ventas_dia = $('#div_ventas_dia');
    //si selecciono los datos necesarios
    if (almacen.value != '0' && tipo_venta.value != '0' && costo_abc.value != '0') {

        div_datos.fadeIn('slow');
        div_ventas_dia.fadeOut('slow');
        //reiniciamos la seleccion
        for (i = 1; i <= 50; i++) {
            producto = document.getElementById('producto_' + i);
            tb2 = document.getElementById('tb2_' + i);
            s_id = i;

            try {
                cantidad = document.getElementById('cantidad_' + s_id);
                cantidad.value = '';

                //costo
                costo = document.getElementById('costo_' + s_id);
                costo.value = '';

                //total
                total = document.getElementById('total_' + s_id);
                total.value = '';
            }
            catch (e) { }


            producto.value = "0";
            tb2.value = "";

            //ocultamos las filas
            if (i > 1) {
                fila = document.getElementById('fila_' + i);
                fila.style.display = 'none';
            }
        }//end for
        obj_total = document.getElementById('total_pedido');
        obj_total.value = '';

        obj_desc = document.getElementById('porcentaje_descuento');
        obj_porcentaje_desc = document.getElementById('descuento');
        obj_t_venta = document.getElementById('total_venta');
        obj_desc.value = '';
        obj_porcentaje_desc.value = '';
        obj_t_venta.value = '';

        //mostramos el boton de cancelar venta
        btn_cancelar = $('#btn_cancelar_venta');
        btn_nuevo = $('#btn_nueva_venta');

        btn_cancelar.fadeIn('slow');
        btn_nuevo.fadeOut('slow');

        return true;
    }
    else {
        div_datos.fadeOut('slow');
        return false;
    }
}


//acc, buscar cliente
function buscarClienteVenta() {
    obj_ci_nit = document.getElementById('b_ci_nit');
    obj_apellidos = document.getElementById('b_apellidos');
    obj_nombres = document.getElementById('b_nombres');

    ci_nit_txt = Trim(obj_ci_nit.value);
    apellidos_txt = Trim(obj_apellidos.value);
    nombres_txt = Trim(obj_nombres.value);
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    url_main = document.getElementById('url_main').value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'buscar_cliente',
        'ci_nit': ci_nit_txt,
        'apellidos': apellidos_txt,
        'nombres': nombres_txt,
        'csrfmiddlewaretoken': token,
    }

    //$("#div_buscar_cliente2").fadeIn('slow');

    $("#div_clientes").html(imagen);
    $("#div_clientes").load(url_main, datos, function () {
        //termina de cargar la ventana
    });
}

//acc, selecccionar cliente
function seleccionarClienteVenta(cliente_id) {
    obj_ci_nit = document.getElementById('ci_nit_' + cliente_id);
    obj_apellidos = document.getElementById('apellidos_' + cliente_id);
    obj_nombres = document.getElementById('nombres_' + cliente_id);
    obj_telefonos = document.getElementById('telefonos_' + cliente_id);
    obj_direccion = document.getElementById('direccion_' + cliente_id);

    mostrarDatosClienteVenta(obj_apellidos.value, obj_nombres.value, obj_ci_nit.value, obj_telefonos.value, obj_direccion.value);

    div_clientes = document.getElementById('div_clientes');
    div_clientes.innerHTML = '';
}

//acc, mostramos datos del cliente cuando se selecciona o crea
function mostrarDatosClienteVenta(apellidos, nombres, nit, telefonos, direccion) {
    cliente_detalle = document.getElementById('cliente_detalle');
    poner = '<b>Cliente : </b>' + apellidos + ' ' + nombres + ', <b>CI/NIT: </b>' + nit + '<br>';
    poner += '<b>Fonos : </b>' + telefonos + '<br>';
    poner += '<b>Direccion : </b>' + direccion + '<br>';
    cliente_detalle.innerHTML = poner;

    obj_ci_nit = document.getElementById('ci_nit');
    obj_apellidos = document.getElementById('apellidos');
    obj_nombres = document.getElementById('nombres');
    obj_telefonos = document.getElementById('telefonos');
    obj_direccion = document.getElementById('direccion');

    obj_ci_nit.value = nit;
    obj_apellidos.value = apellidos;
    obj_nombres.value = nombres;
    obj_telefonos.value = telefonos;
    obj_direccion.value = direccion;
}

//acc, miniminar busqueda cliente
function minimizarClienteVenta() {
    // div_nuevo = $('#div_nuevo_cliente');
    // div_buscar_cliente1 = $('#div_buscar_cliente1');
    // div_buscar_cliente2 = $('#div_buscar_cliente2');

    // div_nuevo.fadeOut('slow');
    // div_buscar_cliente1.fadeOut('slow');
    // div_buscar_cliente2.fadeOut('slow');

    $("#div_clientes").html('<i>resultado busqueda</i>');
}

//acc, miniminar nuevo cliente
function minimizarNuevoClienteVenta() {
    $("#div_nuevo_cliente").html('');
}

//acc, nuevo cliente
function nuevoClienteVenta() {
    div_nuevo = $('#div_nuevo_cliente');

    //recuperamos stock del producto
    url_main = document.getElementById('url_main').value;
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'nuevo_cliente',
        'csrfmiddlewaretoken': token,
    }

    div_nuevo.html(imagen);
    div_nuevo.load(url_main, datos, function () {
        //termina de cargar la ventana
    });
    minimizarClienteVenta();
}

//acc, guardamos al nuevo cliente
function guardarNuevoClienteVenta() {
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    url_main = document.getElementById('url_main').value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    ci_nit = Trim(document.getElementById('n_ci_nit').value);
    apellidos = Trim(document.getElementById('n_apellidos').value);
    nombres = Trim(document.getElementById('n_nombres').value);
    telefonos = Trim(document.getElementById('n_telefonos').value);
    direccion = Trim(document.getElementById('n_direccion').value);

    if (ci_nit == '') {
        alert('debe llenar el CI/NIT');
        return false;
    }

    if (apellidos == '') {
        alert('debe llenar los apellidos');
        return false;
    }

    if (nombres == '') {
        alert('debe llenar los nombres');
        return false;
    }

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'guardar_nc',
        'ci_nit': ci_nit,
        'apellidos': apellidos,
        'nombres': nombres,
        'telefonos': telefonos,
        'direccion': direccion,
        'csrfmiddlewaretoken': token,
    }

    $("#div_nuevo_cliente").html(imagen);
    $("#div_nuevo_cliente").load(url_main, datos, function () {
        //termina de cargar la ventana
        cargarNuevoClienteVenta();
    });
}

//acc, cargamos cuando se adiciona el nuevo cliente
function cargarNuevoClienteVenta() {
    //resultado de la operacion
    try {
        res = document.getElementById('r_operation').value;
        if (res == '1') {
            ci_nit_valor = document.getElementById('r_ci_nit').value;
            apellidos_valor = document.getElementById('r_apellidos').value;
            nombres_valor = document.getElementById('r_nombres').value;
            telefonos_valor = document.getElementById('r_telefonos').value;
            direccion_valor = document.getElementById('r_direccion').value;

            mostrarDatosClienteVenta(apellidos_valor, nombres_valor, ci_nit_valor, telefonos_valor, direccion_valor);
        }
    }
    catch (e) {
        //
        alert('error');
        console.log(e);
    }

}


//acc, seleccion del producto
function seleccionPVenta(numero_registro, producto, id) {
    //asignamos el id del producto
    obj_aux = document.getElementById("producto_" + numero_registro);
    obj_aux.value = id;

    //recuperamos stock del producto
    url_main = document.getElementById('url_main').value;
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    almacen = document.getElementById('almacen').value;
    tipo_venta = document.getElementById('tipo_venta').value;
    costo_abc = document.getElementById('costo_abc').value;

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'stock_producto',
        'numero_registro': numero_registro,
        'id': id,
        'almacen': almacen,
        'tipo_venta': tipo_venta,
        'costo_abc': costo_abc,
        'csrfmiddlewaretoken': token,
    }

    imagen = '<img src="' + ruta_imagen + '">';
    fila = $("#div_fila_" + numero_registro);

    fila.html(imagen);
    fila.load(url_main, datos, function () {
        //termina de cargar la ventana
        datosCostoVenta(id, numero_registro);
    });

    //alert(numero);alert(id);
    numero = parseInt(numero_registro);
    numero_int = numero + 1;
    if (numero_int <= 50) {
        numero_str = numero_int.toString();
        nombre_actual = "fila_" + numero_str;
        //alert(nombre_actual);
        objeto_actual = document.getElementById(nombre_actual);
        objeto_actual.style.display = "block";
        objeto_actual.style.display = "";
    }
}

//acc, datos del costo del producto
function datosCostoVenta(producto_id, numero_registro) {
    tipo_venta = document.getElementById('tipo_venta').value;
    costo_abc = document.getElementById('costo_abc').value;
    if (tipo_venta != '0' && costo_abc != '0') {
        costo = '0';
        //contado
        if (tipo_venta == 'CONTADO') {
            if (costo_abc == 'A') {
                costo = precio_a[producto_id];
            }
            if (costo_abc == 'B') {
                costo = precio_b[producto_id];
            }
            if (costo_abc == 'C') {
                costo = precio_c[producto_id];
            }
        }

        //FACTURA
        if (tipo_venta == 'FACTURA') {
            if (costo_abc == 'A') {
                costo = precio_a_factura[producto_id];
            }
            if (costo_abc == 'B') {
                costo = precio_b_factura[producto_id];
            }
            if (costo_abc == 'C') {
                costo = precio_c_factura[producto_id];
            }
        }

        //CONSIGNACION
        if (tipo_venta == 'CONSIGNACION') {
            if (costo_abc == 'A') {
                costo = precio_a_consignacion[producto_id];
            }
            if (costo_abc == 'B') {
                costo = precio_b_consignacion[producto_id];
            }
            if (costo_abc == 'C') {
                costo = precio_c_consignacion[producto_id];
            }
        }

        //planpago
        if (tipo_venta == 'PLANPAGO') {
            if (costo_abc == 'A') {
                costo = precio_a_pp[producto_id];
            }
            if (costo_abc == 'B') {
                costo = precio_b_pp[producto_id];
            }
            if (costo_abc == 'C') {
                costo = precio_c_pp[producto_id];
            }
        }

        //costo
        costo_obj = document.getElementById('costo_' + numero_registro);
        costo_obj.value = costo;

        //costo aux
        costo_aux_obj = document.getElementById('costo_aux_' + numero_registro);
        costo_aux_obj.value = costo;
    }
}

//acc
function validarFilaVenta(fila) {
    tb2 = document.getElementById("tb2_" + fila.toString());
    producto = document.getElementById("producto_" + fila.toString());

    tb2_val = Trim(tb2.value);
    pro_val = Trim(producto.value);

    //no selecciono ningun producto
    if (tb2_val == '') {
        producto.value = '0';
    }
    else {
        //escribio un producto, verificamos si selecciono
        if (pro_val == '0') {
            /*alert('Debe Seleccionar un Producto');
            tb2.value = '';
            tb2.focus();*/
        }
    }
}

//acc, modal componentes
function componentesProducto(numero_registro) {
    $('#modal-componentes-' + numero_registro).modal('show');
    loadComponentes(numero_registro);

    //extras
    loadExtras(numero_registro);
    //refrescos
    loadRefrescos(numero_registro);
    //papas
    loadPapas(numero_registro);

    ajustarPrecioExtras(numero_registro);

    totalPedidoVenta();
}

//acc, modal extras
function extrasProducto(numero_registro) {
    $('#modal-extras-' + numero_registro).modal('show');
    loadExtras(numero_registro);
    ajustarPrecioExtras(numero_registro);
    totalPedidoVenta();
}

//acc, carga de componentes
function loadComponentes(numero_registro) {
    componentes_ids = document.getElementById('componentes_ids_' + numero_registro).value;
    if (Trim(componentes_ids) != '') {
        div_co = Trim(componentes_ids).split('|');
        for (ic = 0; ic < div_co.length; ic++) {
            aux_c = document.forms['formulario'].elements['componente_' + numero_registro + '_' + div_co[ic]].value;
            aux_c2 = document.getElementById('aux_componente_' + numero_registro + '_' + div_co[ic]);
            if (aux_c == '1') {
                aux_c2.checked = true;
            }
            else {
                aux_c2.checked = false;
            }
        }
    }
}

//acc, carga de extras
function loadExtras(numero_registro) {
    extras_ids = document.getElementById('extras_ids_' + numero_registro).value;
    if (Trim(extras_ids) != '') {
        div_ex = Trim(extras_ids).split('|');
        for (ie = 0; ie < div_ex.length; ie++) {
            aux_c = document.forms['formulario'].elements['extra_' + numero_registro + '_' + div_ex[ie]].value;
            aux_c2 = document.getElementById('aux_extra_' + numero_registro + '_' + div_ex[ie]);
            if (aux_c == '1') {
                aux_c2.checked = true;
            }
            else {
                aux_c2.checked = false;
            }
        }
    }
}

//acc, carga de refrescos
function loadRefrescos(numero_registro) {
    refrescos_ids = document.getElementById('refrescos_ids_' + numero_registro).value;
    if (Trim(refrescos_ids) != '') {
        div_re = Trim(refrescos_ids).split('|');
        for (ie = 0; ie < div_re.length; ie++) {
            aux_c = document.forms['formulario'].elements['refresco_' + numero_registro + '_' + div_re[ie]].value;
            aux_c2 = document.getElementById('aux_refresco_' + numero_registro + '_' + div_re[ie]);
            if (aux_c == '1') {
                aux_c2.checked = true;
            }
            else {
                aux_c2.checked = false;
            }
        }
    }
}

//acc, carga de papas
function loadPapas(numero_registro) {
    papas_ids = document.getElementById('papas_ids_' + numero_registro).value;
    if (Trim(papas_ids) != '') {
        div_re = Trim(papas_ids).split('|');
        for (ie = 0; ie < div_re.length; ie++) {
            aux_c = document.forms['formulario'].elements['papa_' + numero_registro + '_' + div_re[ie]].value;
            aux_c2 = document.getElementById('aux_papa_' + numero_registro + '_' + div_re[ie]);
            if (aux_c == '1') {
                aux_c2.checked = true;
            }
            else {
                aux_c2.checked = false;
            }
        }
    }
}

//acc, ajustar precio extras
function ajustarPrecioExtras(numero_registro) {
    extras_ids = document.getElementById('extras_ids_' + numero_registro).value;
    precio_extra = 0;
    if (Trim(extras_ids) != '') {
        div_ex = Trim(extras_ids).split('|');
        for (ie = 0; ie < div_ex.length; ie++) {
            aux_c = document.forms['formulario'].elements['extra_' + numero_registro + '_' + div_ex[ie]].value;

            if (aux_c == '1') {
                precio_add = parseFloat(document.forms['formulario'].elements['extra_precio_' + numero_registro + '_' + div_ex[ie]].value);
                precio_extra += precio_add;
            }
        }
    }

    //refrescos
    refrescos_ids = document.getElementById('refrescos_ids_' + numero_registro).value;
    if (Trim(refrescos_ids) != '') {
        div_re = Trim(refrescos_ids).split('|');
        for (ie = 0; ie < div_re.length; ie++) {
            aux_c = document.forms['formulario'].elements['refresco_' + numero_registro + '_' + div_re[ie]].value;

            if (aux_c == '1') {
                precio_add = parseFloat(document.forms['formulario'].elements['refresco_precio_' + numero_registro + '_' + div_re[ie]].value);
                precio_extra += precio_add;
            }
        }
    }

    //papas
    papas_ids = document.getElementById('papas_ids_' + numero_registro).value;
    if (Trim(papas_ids) != '') {
        div_re = Trim(papas_ids).split('|');
        for (ie = 0; ie < div_re.length; ie++) {
            aux_c = document.forms['formulario'].elements['papa_' + numero_registro + '_' + div_re[ie]].value;

            if (aux_c == '1') {
                precio_add = parseFloat(document.forms['formulario'].elements['papa_precio_' + numero_registro + '_' + div_re[ie]].value);
                precio_extra += precio_add;
            }
        }
    }

    costo_obj = document.getElementById('costo_' + numero_registro);
    costo_aux = parseFloat(document.getElementById('costo_aux_' + numero_registro).value);

    costo_obj.value = redondeo(costo_aux + precio_extra, 2);
}

//acc, marcar componente
function marcarComponente(check_c, componente) {
    componente_form = document.forms['formulario'].elements[componente];
    if (check_c.checked) {
        componente_form.value = '1';
    }
    else {
        componente_form.value = '0';
    }
}

//acc, marcar extra
function marcarExtra(check_c, extra, numero_registro) {
    extra_form = document.forms['formulario'].elements[extra];
    if (check_c.checked) {
        extra_form.value = '1';
    }
    else {
        extra_form.value = '0';
    }
    ajustarPrecioExtras(numero_registro);
    totalPedidoVenta();
}

//acc, marcar refresco
function marcarRefresco(check_c, extra, numero_registro) {

    //desmarcamos todo
    a_refrescos_ids = Trim(document.getElementById('refrescos_ids_' + numero_registro).value);
    if (a_refrescos_ids != '') {
        a_div = a_refrescos_ids.split('|');
        for (ai = 0; ai < a_div.length; ai++) {
            a_re = document.forms['formulario'].elements['refresco_' + numero_registro + '_' + a_div[ai]];
            a_aux = document.getElementById('aux_refresco_' + numero_registro + '_' + a_div[ai]);

            a_re.value = '0';
            a_aux.checked = false;
        }
    }

    //siempre marcado el seleccionado
    check_c.checked = true;
    extra_form = document.forms['formulario'].elements[extra];
    extra_form.value = '1';

    ajustarPrecioExtras(numero_registro);
    totalPedidoVenta();
}

//acc, marcar papa
function marcarPapa(check_c, extra, numero_registro) {

    //desmarcamos todo
    a_papas_ids = Trim(document.getElementById('papas_ids_' + numero_registro).value);
    if (a_papas_ids != '') {
        a_div = a_papas_ids.split('|');
        for (ai = 0; ai < a_div.length; ai++) {
            a_re = document.forms['formulario'].elements['papa_' + numero_registro + '_' + a_div[ai]];
            a_aux = document.getElementById('aux_papa_' + numero_registro + '_' + a_div[ai]);

            a_re.value = '0';
            a_aux.checked = false;
        }
    }

    check_c.checked = true;
    extra_form = document.forms['formulario'].elements[extra];
    extra_form.value = '1';

    ajustarPrecioExtras(numero_registro);
    totalPedidoVenta();
}

//acc, total por producto
function totalPedidoVenta() {
    total_pedido = 0;
    for (i = 1; i <= 50; i++) {
        p_id = document.getElementById('producto_' + i).value;
        if (p_id != '0') {
            cantidad = Trim(document.getElementById('cantidad_' + i).value);
            costo = Trim(document.getElementById('costo_' + i).value);
            if (cantidad != '' && costo != '') {
                cantidad_valor = parseFloat(cantidad);
                costo_valor = parseFloat(costo);
                total = cantidad_valor * costo_valor;
                total_pedido += total;
                obj_total = document.getElementById('total_' + i);
                obj_total.value = redondeo(total, 2);
            }
        }
    }
    obj_total_pedido = document.getElementById('total_pedido');
    obj_total_pedido.value = redondeo(total_pedido, 2);

    //descuento
    descuento = Trim(document.getElementById('descuento').value);
    total_venta = document.getElementById('total_venta');
    if (descuento != '') {
        val_descuento = parseFloat(descuento);
        total_venta.value = redondeo((total_pedido - val_descuento), 2);
    }
    else {
        total_venta.value = redondeo(total_pedido, 2);
    }
}


//acc, modificacion de venta
function modificarVenta(venta_id) {
    nuevaVenta();
    producto_id = '';
    producto_nombre = '';
    lista_cantidad = '';
    lista_costo = '';
    lista_total = '';

    //marcamos la operacion
    operacion_mod = document.getElementById('tipo_operacion');
    m_id_mod = document.getElementById('m_venta_id');
    operacion_mod.value = 'modify';
    m_id_mod.value = venta_id;

    //almacen, tipo de venta y costo
    almacen_id = $('#m_almacen_id').val();
    tipo_preventa_id = $('#m_tipo_venta').val();
    costo_abc_id = $('#m_costo_abc').val();
    cliente_id = $('#m_cliente_id').val();
    apellidos = $('#m_apellidos').val();
    nombres = $('#m_nombres').val();
    ci_nit = $('#m_ci_nit').val();
    telefonos = $('#m_telefonos').val();
    direccion = $('#m_direccion').val();
    mesa = $('#m_mesa').val();
    observacion = $('#m_observacion').val();
    lugar_id = $('#m_lugar_id').val();

    //mesa y observacion
    am_mesa = document.getElementById('mesa');
    am_observacion = document.getElementById('observacion');
    am_mesa.value = mesa;
    am_observacion.value = observacion;

    almacen = document.getElementById('almacen');
    tipo_preventa = document.getElementById('tipo_venta');
    costo_abc = document.getElementById('costo_abc');
    lugar = document.getElementById('lugar');

    //descuento
    pp_porcentaje_descuento = $('#m_porcentaje_descuento').val();
    pp_descuento = $('#m_descuento').val();
    pp_obj_porcentaje_descuento = document.getElementById('porcentaje_descuento');
    pp_obj_descuento = document.getElementById('descuento');

    pp_obj_porcentaje_descuento.value = pp_porcentaje_descuento;
    pp_obj_descuento.value = pp_descuento;

    //datos
    almacen.value = almacen_id;
    tipo_preventa.value = tipo_preventa_id;
    costo_abc.value = costo_abc_id;
    lugar.value = lugar_id;
    mostrarDatosClienteVenta(apellidos, nombres, ci_nit, telefonos, direccion);

    //caso de plan de pagos
    if (tipo_preventa_id == 'PLANPAGO') {
        mostrarPPVenta();
        m_numero_cuotas = document.getElementById('m_numero_cuotas').value;
        m_mensual_dias = document.getElementById('m_mensual_dias').value;
        m_tiempo_dias = document.getElementById('m_tiempo_dias').value;
        m_fecha_fija = document.getElementById('m_fecha_fija').value;

        numero_cuotas = document.getElementById('numero_cuotas');
        numero_cuotas.value = m_numero_cuotas;
        radio1 = document.getElementById('radio1_pp');
        radio2 = document.getElementById('radio2_pp');
        fecha_fija = document.getElementById('fecha_fija');
        dias = document.getElementById('dias');

        if (m_mensual_dias == 'tipo_fecha') {
            radio1.checked = true;
            radio2.checked = false;
            fecha_fija.value = m_fecha_fija;
            dias.value = '';
        }
        else {
            radio1.checked = false;
            radio2.checked = true;
            fecha_fija.value = m_fecha_fija;
            dias.value = m_tiempo_dias;
        }
    }

    div_datos = $('#div_listap');
    div_datos.fadeIn('slow');

    for (i = 1; i <= 50; i++) {
        try {
            producto_id = document.getElementById('m_producto_id_' + i).innerHTML;
            producto_nombre = document.getElementById('m_producto_' + i).innerHTML;
            cantidad = document.getElementById('m_cantidad_' + i).innerHTML;
            costo = document.getElementById('m_costo_' + i).innerHTML;
            total = document.getElementById('m_total_' + i).innerHTML;

            //mostramos el producto
            div_fila = document.getElementById('fila_' + i);
            div_fila.style.display = '';
            p_id = document.getElementById('producto_' + i);
            p_tb2 = document.getElementById('tb2_' + i);

            p_id.value = producto_id;
            p_tb2.value = producto_nombre;

            //carga del stock
            seleccionPModificar(i, producto_nombre, producto_id);
        }
        catch (e) {

        }
    }//end for
}

//acc, seleccion del producto modificacion
function seleccionPModificar(numero_registro, producto, id) {

    //asignamos el id del producto
    obj_aux = document.getElementById("producto_" + numero_registro);
    obj_aux.value = id;

    //recuperamos stock del producto
    url_main = document.getElementById('url_main').value;
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    almacen = document.getElementById('almacen').value;
    tipo_venta = document.getElementById('tipo_venta').value;
    costo_abc = document.getElementById('costo_abc').value;

    datos_mod = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'stock_producto',
        'id': id,
        'numero_registro': numero_registro,
        'almacen': almacen,
        'tipo_venta': tipo_venta,
        'costo_abc': costo_abc,
        'csrfmiddlewaretoken': token,
    }

    imagen = '<img src="' + ruta_imagen + '">';
    fila = $("#div_fila_" + numero_registro);

    fila.html(imagen);
    fila.load(url_main, datos_mod, function () {
        //termina de cargar la ventana
        datosCostoVenta(id, numero_registro);
        datosModificar(numero_registro, id);
    });

    //alert(numero);alert(id);
    numero = parseInt(numero_registro);
    numero_int = numero + 1;
    if (numero_int <= 50) {
        numero_str = numero_int.toString();
        nombre_actual = "fila_" + numero_str;
        //alert(nombre_actual);
        objeto_actual = document.getElementById(nombre_actual);
        objeto_actual.style.display = "block";
        objeto_actual.style.display = "";
    }
}

//acc, cargamos datos de modificacion
function datosModificar(fila, producto_id) {

    //cantidad
    cantidad = document.getElementById('cantidad_' + fila);
    cantidad.value = parseInt(document.getElementById('m_cantidad_' + fila).innerHTML);

    //costo
    costo = document.getElementById('costo_' + fila);
    costo.value = document.getElementById('m_costo_' + fila).innerHTML;

    //total
    total = document.getElementById('total_' + fila);
    total.value = document.getElementById('m_total_' + fila).innerHTML;

    //componentes de la fila
    componentes_ids = document.getElementById('componentes_ids_' + fila).value;
    if (componentes_ids != '') {
        div_com = componentes_ids.split('|');
        for (k = 0; k < div_com.length; k++) {
            mod_componente = document.getElementById('m_componente_' + fila + '_' + div_com[k]).innerHTML;

            aux_com = document.forms['formulario'].elements['componente_' + fila + '_' + div_com[k]];
            aux_com.value = parseInt(mod_componente);
        }
    }

    //refrescos
    refrescos_ids = document.getElementById('refrescos_ids_' + fila).value;
    if (refrescos_ids != '') {
        div_ref = refrescos_ids.split('|');
        for (k = 0; k < div_ref.length; k++) {
            //try {
            mod_ref = document.getElementById('m_refresco_' + fila + '_' + div_ref[k]).innerHTML;

            aux_ref = document.forms['formulario'].elements['refresco_' + fila + '_' + div_ref[k]];
            aux_ref.value = parseInt(mod_ref);
            // }
            // catch (e) { }
        }
    }

    //papas
    papas_ids = document.getElementById('papas_ids_' + fila).value;
    if (papas_ids != '') {
        div_pa = papas_ids.split('|');
        for (k = 0; k < div_pa.length; k++) {
            try {
                mod_pa = document.getElementById('m_papa_' + fila + '_' + div_pa[k]).innerHTML;

                aux_pa = document.forms['formulario'].elements['papa_' + fila + '_' + div_pa[k]];
                aux_pa.value = parseInt(mod_pa);
            }
            catch (e) { }
        }
    }

    //extras
    extras_ids = document.getElementById('extras_ids_' + fila).value;
    if (extras_ids != '') {
        div_ex = extras_ids.split('|');
        for (k = 0; k < div_ex.length; k++) {
            try {
                mod_ex = document.getElementById('m_extra_' + fila + '_' + div_ex[k]).innerHTML;

                aux_ex = document.forms['formulario'].elements['extra_' + fila + '_' + div_ex[k]];
                aux_ex.value = parseInt(mod_ex);
            }
            catch (e) { }
        }
    }

    //total de venta
    try {
        totalPedidoVenta();
    }
    catch (e) {

    }
}

//acc, descuento en venta
function calcularPorcentajeDescuentoVenta() {
    porcentaje_descuento = Trim(document.getElementById('porcentaje_descuento').value);
    total_pedido2 = Trim(document.getElementById('total_pedido').value);

    descuento_obj = document.getElementById('descuento');

    if (total_pedido2 != '' && porcentaje_descuento != '') {
        resta_descuento = (parseFloat(porcentaje_descuento) / 100) * parseFloat(total_pedido2);
        descuento_obj.value = redondeo(resta_descuento, 2);
    }
    else {
        descuento_obj.value = '';
    }
}

//acc, guardamos la venta
async function guardarVenta() {
    //almacen
    almacen = document.getElementById('almacen');
    tipo_venta = document.getElementById('tipo_venta');
    costo_abc = document.getElementById('costo_abc');

    //verificamos almacen
    if (almacen.value == '0') {
        alert('Debe seleccionar un almacen');
        almacen.focus();
        return false;
    }

    //tipo de venta
    numero_cuotas = 0;
    tipo_pp = 'tipo_fecha';
    fecha_fija = document.getElementById('fecha_fija').value;
    dias = 0;

    if (tipo_venta.value == '0') {
        alert('Debe seleccionar un tipo de venta');
        tipo_venta.focus();
        return false;
    }
    else {
        if (tipo_venta.value == 'PLANPAGO') {
            //numero de cuotas
            aux_cuotas = Trim(document.getElementById('numero_cuotas').value);
            if (aux_cuotas == '') {
                alert('debe indicar el numero de cuotas');
                return false;
            }
            numero_cuotas = parseInt(aux_cuotas);

            //tipo de plan de pago
            aux_radio = document.getElementById('radio1_pp');
            if (aux_radio.checked) {
                tipo_pp = 'tipo_fecha';
            }
            else {
                tipo_pp = 'tipo_dias';
                aux_dias = Trim(document.getElementById('dias').value);
                if (aux_dias == '') {
                    alert('debe indicar los dias');
                    return false;
                }
                dias = parseInt(aux_dias);
            }
        }
    }

    //costo abc
    if (costo_abc.value == '0') {
        alert('Debe seleccionar un tipo de costo');
        costo_abc.focus();
        return false;
    }

    //imagen
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';
    //formulario
    var fd = new FormData(document.forms['formulario']);

    // for (var pair of fd.entries()) {
    //     console.log(pair[0] + ', ' + pair[1]);
    // }

    div_datos = $('#div_listap');
    div_ventas_dia = $('#div_ventas_dia');

    div_datos.fadeOut('slow');
    div_ventas_dia.fadeIn();
    div_ventas_dia.html(imagen);

    let result2;
    try {
        result2 = await $.ajax({
            url: '/',
            method: 'POST',
            type: 'POST',
            cache: false,
            data: fd,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response != 0) {
                    div_ventas_dia.html(response);
                } else {
                    alert('error al realizar la operacion, intentelo de nuevo');
                }
            },
            error: function (qXHR, textStatus, errorThrown) {
                console.log(errorThrown); console.log(qXHR); console.log(textStatus);
            },
        });
        //alert(result);
    }
    catch (e) {
        console.error(e);
    }


    // div_ventas_dia.load(url_add, datos, function () {
    //     //termina de cargar la ventana
    //     setTimeout(function () {
    //         $('#message').fadeOut('slow');
    //     }, 3000);
    //     if (from_preventa == 'si') {
    //         loadListaPreventa();
    //     }
    // });

    //mostramos el boton de nueva venta
    btn_cancelar = $('#btn_cancelar_venta');
    btn_nuevo = $('#btn_nueva_venta');

    btn_cancelar.fadeOut('slow');
    btn_nuevo.fadeIn('slow');

    if (parseInt(document.getElementById('pedido_id').value) != 0) {
        btn_cargar_pedido = $('#btn_cargar_pedido');
        btn_cargar_pedido.fadeOut('slow');
        document.getElementById('pedido_id').value = '0';
    }
}

//acc, load next o previous venta id
function loadIDVenta(id) {
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    url_main = '';
    url_add = '';
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    datos = {
        'module_x': document.forms['formulario'].elements['module_x'].value,
        'operation_x': document.forms['formulario'].elements['operation_x'].value,
        'operation_x2': 'load_id_x',
        'load_id': id,
        'csrfmiddlewaretoken': token,
    }

    div_ventas_dia = $('#div_ventas_dia');
    div_ventas_dia.html(imagen);
    div_ventas_dia.load(url_add, datos, function () {
        //termina de cargar la ventana
    });
}

//acc, anulamos la venta
function anularVenta(venta_id) {
    id_anular = document.getElementById('id_null');
    id_anular.value = venta_id;

    fila_anular = $('#linea_anular');
    fila_anular.fadeIn('slow');
}

//confirmar anular general
function confirmarAnularGeneralVenta() {
    if (verifyForm()) {
        if (confirm('Esta seguro de querer anular este elemento?')) {
            document.forms['formulario'].elements['add_button'].disabled = true;
            document.forms['formulario'].elements['button_cancel'].disabled = true;
            document.forms['formulario'].submit();
        }
    }
}

//acc, cancelar la anulacion
function cancelarAnularVenta() {
    motivo = document.getElementById('motivo');
    motivo.value = '';

    fila_anular = $('#linea_anular');
    fila_anular.fadeOut('slow');
}

//impresion de venta
function imprimirVenta(venta_id) {
    document.form_print.id.value = venta_id;
    document.form_print.operation_x.value = 'print';
    document.form_print.submit();
}

//cargar datos de preventa
function loadPreventaData() {
    preventa_id = document.getElementById('preventa').value;
    if (preventa_id == '0') {
        return;
    }

    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    url_main = document.getElementById('url_main').value;
    url_add = document.getElementById('url_add').value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    datos_v = {
        'operation_x': 'load_preventa_data',
        'preventa_id': preventa_id,
        'csrfmiddlewaretoken': token,
    }

    div_datos = $('#div_datos_venta');
    div_datos.html(imagen);
    div_datos.load(url_add, datos_v, function () {
        //alert('cargado');
        loadPreventa();
    });
}

//cargamos la preventa
function loadPreventa() {
    if (!nuevaVenta()) {
        return false;
    }
    producto_id = '';
    producto_nombre = '';
    lista_cantidad = '';
    lista_costo = '';
    lista_total = '';
    lista_fecha_elab = '';
    lista_fecha_venc = '';
    lista_lote = '';

    //marcamos como que no se cargo de preventa
    from_preventa = 'si';
    from_preventa_id = preventa_id;

    //marcamos la operacion
    // operacion_mod = document.getElementById('tipo_operacion');
    // m_id_mod = document.getElementById('m_venta_id');
    // operacion_mod.value = 'load_preventa';
    // m_id_mod.value = venta_id;

    //almacen, tipo de venta y costo
    almacen_id = $('#m_almacen_id').val();
    tipo_preventa_id = $('#m_tipo_preventa').val();
    costo_abc_id = $('#m_costo_abc').val();
    cliente_id = $('#m_cliente_id').val();
    apellidos = $('#m_apellidos').val();
    nombres = $('#m_nombres').val();
    ci_nit = $('#m_ci_nit').val();
    telefonos = $('#m_telefonos').val();

    almacen = document.getElementById('almacen');
    tipo_preventa = document.getElementById('tipo_venta');
    costo_abc = document.getElementById('costo_abc');

    //descuento
    pp_porcentaje_descuento = $('#m_porcentaje_descuento').val();
    pp_descuento = $('#m_descuento').val();
    pp_obj_porcentaje_descuento = document.getElementById('porcentaje_descuento');
    pp_obj_descuento = document.getElementById('descuento');

    pp_obj_porcentaje_descuento.value = pp_porcentaje_descuento;
    pp_obj_descuento.value = pp_descuento;

    //datos
    //almacen.value = almacen_id;
    tipo_preventa.value = tipo_preventa_id;
    costo_abc.value = costo_abc_id;
    mostrarDatosCliente(apellidos, nombres, ci_nit, telefonos);

    //caso de plan de pagos
    if (tipo_preventa_id == 'PLANPAGO') {
        mostrarPP();
        m_numero_cuotas = document.getElementById('m_numero_cuotas').value;
        m_mensual_dias = document.getElementById('m_mensual_dias').value;
        m_tiempo_dias = document.getElementById('m_tiempo_dias').value;
        m_fecha_fija = document.getElementById('m_fecha_fija').value;

        numero_cuotas = document.getElementById('numero_cuotas');
        numero_cuotas.value = m_numero_cuotas;
        radio1 = document.getElementById('radio1_pp');
        radio2 = document.getElementById('radio2_pp');
        fecha_fija = document.getElementById('fecha_fija');
        dias = document.getElementById('dias');

        if (m_mensual_dias == 'tipo_fecha') {
            radio1.checked = true;
            radio2.checked = false;
            fecha_fija.value = m_fecha_fija;
            dias.value = '';
        }
        else {
            radio1.checked = false;
            radio2.checked = true;
            fecha_fija.value = m_fecha_fija;
            dias.value = m_tiempo_dias;
        }
    }

    fila_r = 1;
    div_datos = $('#div_listap');
    div_datos.fadeIn('slow');

    for (i = 1; i <= 500; i++) {
        try {
            if (i == 1) {
                producto_id = document.getElementById('m_producto_id_' + i).innerHTML;
                producto_nombre = document.getElementById('m_producto_' + i).innerHTML;
                cantidad = document.getElementById('m_cantidad_' + i).innerHTML;
                costo = document.getElementById('m_costo_' + i).innerHTML;
                total = document.getElementById('m_total_' + i).innerHTML;
                fecha_elab = document.getElementById('m_fecha_elab_' + i).innerHTML;
                fecha_venc = document.getElementById('m_fecha_venc_' + i).innerHTML;
                lote = document.getElementById('m_lote_' + i).innerHTML;

                lista_cantidad += cantidad + '|';
                lista_costo += costo + '|';
                lista_total += total + '|';
                lista_fecha_elab += fecha_elab + '|';
                lista_fecha_venc += fecha_venc + '|';
                lista_lote += lote + '|';
            }
            else {
                aux_producto_id = document.getElementById('m_producto_id_' + i).innerHTML;
                aux_producto_nombre = document.getElementById('m_producto_' + i).innerHTML;
                //alert(aux_producto_nombre);

                // p_nombre = 'm_producto_id_' + i.toString();
                // objeto = $('#' + p_nombre);
                // alert(objeto);
                // alert(objeto.val());

                cantidad = document.getElementById('m_cantidad_' + i).innerHTML;
                costo = document.getElementById('m_costo_' + i).innerHTML;
                total = document.getElementById('m_total_' + i).innerHTML;
                fecha_elab = document.getElementById('m_fecha_elab_' + i).innerHTML;
                fecha_venc = document.getElementById('m_fecha_venc_' + i).innerHTML;
                lote = document.getElementById('m_lote_' + i).innerHTML;

                if (aux_producto_id == producto_id) {
                    lista_cantidad += cantidad + '|';
                    lista_costo += costo + '|';
                    lista_total += total + '|';
                    lista_fecha_elab += fecha_elab + '|';
                    lista_fecha_venc += fecha_venc + '|';
                    lista_lote += lote + '|';
                }
                else {
                    //mostramos el producto
                    div_fila = document.getElementById('fila_' + fila_r);
                    div_fila.style.display = '';
                    p_id = document.getElementById('producto_' + fila_r);
                    p_tb2 = document.getElementById('tb2_' + fila_r);
                    p_id.value = producto_id;
                    p_tb2.value = producto_nombre;

                    //carga del stock
                    seleccionPModificar(fila_r, producto_nombre, producto_id, lista_cantidad, lista_costo, lista_total, lista_fecha_elab, lista_fecha_venc, lista_lote);

                    fila_r = fila_r + 1;
                    //reiniciamos
                    producto_id = aux_producto_id;
                    producto_nombre = aux_producto_nombre;
                    lista_cantidad = cantidad + '|';
                    lista_costo = costo + '|';
                    lista_total = total + '|';
                    lista_fecha_elab = fecha_elab + '|';
                    lista_fecha_venc = fecha_venc + '|';
                    lista_lote = lote + '|';
                }
            }
        }
        catch (e) {

        }
    }//end for

    //si existe uno mas
    if (lista_cantidad != '') {
        //alert(fila_r);
        div_fila = document.getElementById('fila_' + fila_r);
        div_fila.style.display = '';
        p_id = document.getElementById('producto_' + fila_r);
        p_tb2 = document.getElementById('tb2_' + fila_r);
        p_id.value = producto_id;
        p_tb2.value = producto_nombre;

        //carga del stock
        seleccionPModificar(fila_r, producto_nombre, producto_id, lista_cantidad, lista_costo, lista_total, lista_fecha_elab, lista_fecha_venc, lista_lote);
    }
}

//recargando la lista de preventas
function loadListaPreventa() {

    //recuperamos stock del producto
    url_add = document.getElementById('url_add').value;
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';

    datos_p = {
        'operation_x': 'load_lista_preventa',
        'csrfmiddlewaretoken': token,
    }

    imagen = '<img src="' + ruta_imagen + '">';
    lista_p = $("#div_lista_preventa");

    lista_p.html(imagen);
    lista_p.load(url_add, datos_p, function () {
        //termina de cargar la ventana
    });
}


//acc, en caso de cambiar el tipo de venta y de costo, actualizamos datos del costo
function verificarCostosVenta() {
    for (i = 1; i <= 50; i++) {
        producto = document.getElementById('producto_' + i);
        tb2 = document.getElementById('tb2_' + i);

        //stocks
        if (producto.value != '0' && producto.value != '') {
            try {
                datosCostoVenta(producto.value, i);
            }
            catch (e) {
                alert('error ' + e.toString());
            }
        }
    }
    totalPedidoVenta();
}

//cargamos un pedido
function loadPedidoVenta() {
    nuevaVenta();

    //datos para buscar el cliente
    pe_apellidos = document.getElementById('pe_apellidos').value;
    pe_nombres = document.getElementById('pe_nombres').value;
    pe_detalles = parseInt(document.getElementById('pe_detalles').value);

    bb_apellidos = document.getElementById('b_apellidos');
    bb_nombres = document.getElementById('b_nombres');

    bb_apellidos.value = pe_apellidos;
    bb_nombres.value = pe_nombres;

    for (aa = 1; aa <= pe_detalles; aa++) {
        id_pp = document.getElementById('pe_det_producto_id_' + aa);
        producto_pp = document.getElementById('pe_det_producto_' + aa);
        pp_pr = document.getElementById('tb2_' + aa);
        pp_pr.value = producto_pp.value;

        buscarClienteVenta();

        //cantidad
        pp_cantidad = document.getElementById('pe_det_cantidad_' + aa).value;
        pp_talla = document.getElementById('pe_det_talla_' + aa).value;

        if (typeof id_pp === "object" || id_pp !== null) {
            seleccionPPedidoVenta(aa, '', id_pp.value, pp_cantidad, pp_talla);
        }
    }
}