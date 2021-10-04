/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

//control especifico del modulo
function controlModulo() {

    return true;
}

async function sendSearchPA() {
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

async function mandarFormularioPA(formulario, add_button, cancel_button) {

    btn_add = document.forms[formulario].elements[add_button];
    btn_cancel = document.forms[formulario].elements[cancel_button];

    btn_add.disabled = true;
    btn_cancel.disabled = true;

    var fd = new FormData(document.forms[formulario]);

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

async function confirmarAnularPA() {

    motivo = Trim(document.forms['formulario'].elements['motivo_anula'].value);
    if (motivo == '') {
        alert('Debe llenar el motivo');
        return false;
    }

    if (confirm('Esta seguro de anular este registro?')) {
        btn_add = document.forms['formulario'].elements['add_button'];
        btn_cancel = document.forms['formulario'].elements['button_cancel'];

        btn_add.disabled = true;
        btn_cancel.disabled = true;

        var fd = new FormData(document.forms['formulario']);

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
}

function mostrarPPPA() {
    tipo_movimiento = document.getElementById('tipo_movimiento').value;
    fila_pp = $('#fila_pp');
    if (tipo_movimiento == 'PLANPAGO') {
        fila_pp.fadeIn('slow');
    }
    else {
        fila_pp.fadeOut('slow');
    }
}

function tipoPPPA() {
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

function seleccionAlmacenPA() {
    //almacen
    almacen = document.getElementById('almacen');
    almacen2 = document.getElementById('almacen2');
    tipo_movimiento = document.getElementById('tipo_movimiento');
    costo_abc = document.getElementById('costo_abc');

    div_datos = $('#div_listap');
    //si selecciono los datos necesarios
    if (almacen.value != '0' && almacen2.value != '0' && almacen.value != almacen2.value && tipo_movimiento.value != '0' && costo_abc.value != '0') {
        div_datos.fadeIn('slow');
        //reiniciamos la seleccion
        for (i = 1; i <= 50; i++) {
            producto = document.getElementById('producto_' + i);
            tb2 = document.getElementById('tb2_' + i);

            //stocks
            if (producto.value != '0' && producto.value != '') {
                try {
                    nombre = 'stock_ids_' + producto.value;
                    stock_ids = document.getElementById(nombre).value;

                    if (stock_ids != '') {
                        division = stock_ids.split(',');
                        for (j = 0; j < division.length; j++) {
                            s_id = division[j];

                            cantidad = document.getElementById('cantidad_' + s_id);
                            cantidad.value = '';

                            //fecha vencimiento
                            f_venc = document.getElementById('f_venc_' + s_id);
                            f_venc.value = '';

                            //lote
                            lote = document.getElementById('lote_' + s_id);
                            lote.value = '';

                            //actual
                            lote = document.getElementById('actual_' + s_id);
                            lote.value = '';
                        }
                    }
                }
                catch (e) {

                }
            }

            producto.value = "0";
            tb2.value = "";

            //ocultamos las filas
            if (i > 1) {
                fila = document.getElementById('fila_' + i);
                fila.style.display = 'none';
            }
        }
    }
    else {
        div_datos.fadeOut('slow');
    }
}

function controlarStockPA(stock_id) {
    actual = parseFloat(document.getElementById('actual_' + stock_id).value);
    cantidad = document.getElementById('cantidad_' + stock_id);
    if (Trim(cantidad.value) == '') {
        obj_total = document.getElementById('total_' + stock_id);
        obj_total.value = '';
    }
    valor_cantidad = parseFloat(Trim(cantidad.value));
    if (valor_cantidad > actual) {
        cantidad.value = '';
        alert('la cantidad no puede ser mayor a ' + actual);
    }
}

//seleccion del producto
function seleccionPPA(numero_registro, producto, id) {
    //verificamos que no repita productos
    for (i = 1; i <= 50; i++) {
        aux_p = document.getElementById('producto_' + i);
        if (parseInt(numero_registro) != i && aux_p.value == id) {
            alert('ya selecciono este producto');
            tb2 = document.getElementById('tb2_' + numero_registro);
            tb2.focus();
            tb2.value = '';
            return false;
        }
    }

    //asignamos el id del producto
    obj_aux = document.getElementById("producto_" + numero_registro);
    obj_aux.value = id;

    //recuperamos stock del producto
    url_main = document.getElementById('url_main').value;
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    almacen = document.getElementById('almacen').value;
    tipo_movimiento = document.getElementById('tipo_movimiento').value;
    costo_abc = document.getElementById('costo_abc').value;

    datos = {
        'operation_x': 'stock_producto',
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'id': id,
        'almacen': almacen,
        'tipo_movimiento': tipo_movimiento,
        'costo_abc': costo_abc,
        'csrfmiddlewaretoken': token
    }

    imagen = '<img src="' + ruta_imagen + '">';
    fila = $("#div_fila_" + numero_registro);

    fila.html(imagen);
    fila.load(url_main, datos, function () {
        //termina de cargar la ventana
        datosCostoPA(id);
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

//datos del costo del producto
function datosCostoPA(producto_id) {
    tipo_movimiento = document.getElementById('tipo_movimiento').value;
    costo_abc = document.getElementById('costo_abc').value;
    if (tipo_movimiento != '0' && costo_abc != '0') {
        costo = '0';
        //contado
        if (tipo_movimiento == 'CONTADO') {
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
        if (tipo_movimiento == 'FACTURA') {
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
        if (tipo_movimiento == 'CONSIGNACION') {
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
        if (tipo_movimiento == 'PLANPAGO') {
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

        //stock ids
        stock_ids = document.getElementById('stock_ids_' + producto_id).value;
        if (Trim(stock_ids) != '') {
            division = stock_ids.split(',');
            for (i = 0; i < division.length; i++) {
                costo_obj = document.getElementById('costo_' + division[i]);
                costo_obj.value = costo;
            }
        }

    }
}

function validarFilaPA(fila) {
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

//aumentamos el costo en 0.1
function aumentarCostoPA(nombre) {
    costo = document.getElementById(nombre);
    aux = Trim(costo.value);
    if (aux != '') {
        valor = parseFloat(aux);
        valor = valor + 0.1;
        costo.value = redondeo(valor, 2);
    }
}

//disminuimos el costo en 0.1
function disminuirCostoPA(nombre) {
    costo = document.getElementById(nombre);
    aux = Trim(costo.value);
    if (aux != '') {
        valor = parseFloat(aux);
        valor = valor - 0.1;
        if (valor >= 0) {
            costo.value = redondeo(valor, 2);
        }
        else {
            costo.value = '0';
        }
    }
}

//aumentar costo a todos los productos
function aumentarCostoTodoPA() {
    for (i = 1; i <= 50; i++) {
        p_id = document.getElementById('producto_' + i).value;
        if (p_id != '0') {
            stock_ids = document.getElementById('stock_ids_' + p_id).value;
            //alert(stock_ids);
            if (Trim(stock_ids) != '') {
                division = stock_ids.split(',');
                for (j = 0; j < division.length; j++) {
                    obj_costo = document.getElementById('costo_' + division[j]);
                    costo = Trim(obj_costo.value);
                    if (costo != '') {
                        costo_valor = parseFloat(costo) + 0.1;
                        obj_costo.value = redondeo(costo_valor, 2);
                    }
                }
            }
        }
    }
}

//disminuir costo a todos los productos
function disminuirCostoTodoPA() {
    for (i = 1; i <= 50; i++) {
        p_id = document.getElementById('producto_' + i).value;
        if (p_id != '0') {
            stock_ids = document.getElementById('stock_ids_' + p_id).value;
            //alert(stock_ids);
            if (Trim(stock_ids) != '') {
                division = stock_ids.split(',');
                for (j = 0; j < division.length; j++) {
                    obj_costo = document.getElementById('costo_' + division[j]);
                    costo = Trim(obj_costo.value);
                    if (costo != '') {
                        costo_valor = parseFloat(costo) - 0.1;
                        if (costo_valor >= 0) {
                            obj_costo.value = redondeo(costo_valor, 2);
                        }
                        else {
                            obj_costo.value = '0';
                        }
                    }
                }
            }
        }
    }
}

//total por producto
function totalPedidoPA() {
    total_pedido = 0;
    for (i = 1; i <= 50; i++) {
        p_id = document.getElementById('producto_' + i).value;
        if (p_id != '0') {
            stock_ids = document.getElementById('stock_ids_' + p_id).value;
            //alert(stock_ids);
            if (Trim(stock_ids) != '') {
                division = stock_ids.split(',');
                for (j = 0; j < division.length; j++) {
                    cantidad = Trim(document.getElementById('cantidad_' + division[j]).value);
                    costo = Trim(document.getElementById('costo_' + division[j]).value);
                    if (cantidad != '' && costo != '') {
                        cantidad_valor = parseFloat(cantidad);
                        costo_valor = parseFloat(costo);
                        total = cantidad_valor * costo_valor;
                        total_pedido += total;
                        obj_total = document.getElementById('total_' + division[j]);
                        obj_total.value = redondeo(total, 2);
                    }
                }
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

function calcularPorcentajeDescuentoPA() {
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
