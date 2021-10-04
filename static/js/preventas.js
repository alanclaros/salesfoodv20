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

function mostrarPP() {
    tipo_venta = document.getElementById('tipo_venta').value;
    fila_pp = $('#fila_pp');
    if (tipo_venta == 'PLANPAGO') {
        fila_pp.fadeIn('slow');
    }
    else {
        fila_pp.fadeOut('slow');
    }
}

function tipoPP() {
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

    //marcamos la operacion
    operacion = document.getElementById('tipo_operacion');
    m_id = document.getElementById('m_venta_id');
    operacion.value = 'add';
    m_id.value = '';

    //reiniciamos el cliente al defecto
    mostrarDatosCliente('SIN NOMBRE', '', '0', '');

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
                            actual = document.getElementById('actual_' + s_id);
                            actual.value = '';

                            //costo
                            costo = document.getElementById('costo_' + s_id);
                            costo.value = '';

                            //total
                            total = document.getElementById('total_' + s_id);
                            total.value = '';
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
    }
    else {
        div_datos.fadeOut('slow');
    }
}

function controlarStock(stock_id) {
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
function seleccionP(numero_registro, producto, id) {
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
    tipo_venta = document.getElementById('tipo_venta').value;
    costo_abc = document.getElementById('costo_abc').value;

    datos = {
        'operation_x': 'stock_producto',
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
        datosCosto(id);
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
function datosCosto(producto_id) {
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

        //stock ids
        stock_ids = document.getElementById('stock_ids_' + producto_id).value;
        if (Trim(stock_ids) != '') {
            division = stock_ids.split(',');
            for (m = 0; m < division.length; m++) {
                costo_obj = document.getElementById('costo_' + division[m]);
                costo_obj.value = costo;
            }
        }

    }
}

function validarFila(fila) {
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
function aumentarCosto(nombre) {
    costo = document.getElementById(nombre);
    aux = Trim(costo.value);
    if (aux != '') {
        valor = parseFloat(aux);
        valor = valor + 0.1;
        costo.value = redondeo(valor, 2);
    }
}

//disminuimos el costo en 0.1
function disminuirCosto(nombre) {
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
function aumentarCostoTodo() {
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
function disminuirCostoTodo() {
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
function totalPedido() {
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

function calcularPorcentajeDescuento() {
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

//guardamos la venta
function guardarVenta() {
    //verificamos modificacion de preventa
    mod_preventa = 'no';
    try {
        mod_preventa = document.getElementById('modificar_preventa').value;
    }
    catch (e) {
        mod_preventa = 'no';
    }

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

    //datos del cliente
    apellidos = Trim(document.getElementById('apellidos').value);
    nombres = Trim(document.getElementById('nombres').value);
    ci_nit = Trim(document.getElementById('ci_nit').value);
    telefonos = Trim(document.getElementById('telefonos').value);

    //caja
    //caja = Trim(document.getElementById('caja').value);

    div_datos = $('#div_listap');
    div_ventas_dia = $('#div_ventas_dia');

    //recuperamos stock del producto
    url_main = document.getElementById('url_main').value;
    url_add = document.getElementById('url_add').value;
    //alert(url_add);
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    //verificamos si es adicion o modificacion
    add_mod = document.getElementById('tipo_operacion').value;
    m_p_id = document.getElementById('m_venta_id').value;

    p_porcentaje_descuento = Trim(document.getElementById('porcentaje_descuento').value);
    p_descuento = Trim(document.getElementById('descuento').value);

    datos = {
        'add_x': 'add_x',
        'almacen': almacen.value,
        //'caja': caja,
        'tipo_operacion': add_mod,
        'mod_preventa': mod_preventa,
        'm_id': m_p_id,
        'tipo_venta': tipo_venta.value,
        'costo_abc': costo_abc.value,
        'csrfmiddlewaretoken': token,
        'numero_cuotas': numero_cuotas,
        'tipo_pp': tipo_pp,
        'fecha_fija': fecha_fija,
        'dias': dias,
        'apellidos': apellidos,
        'nombres': nombres,
        'ci_nit': ci_nit,
        'telefonos': telefonos,
        'porcentaje_descuento': p_porcentaje_descuento,
        'descuento': p_descuento,
    }

    //reiniciamos la seleccion
    cant_productos = 0;
    for (i = 1; i <= 50; i++) {
        aux_producto = 'producto_' + i;
        aux_tb2 = 'tb2_' + i;
        producto = document.getElementById(aux_producto);
        tb2 = document.getElementById(aux_tb2);

        //stocks
        if (producto.value != '0' && producto.value != '') {
            try {
                nombre = 'stock_ids_' + producto.value;
                stock_ids = document.getElementById(nombre).value;

                if (stock_ids != '') {
                    division = stock_ids.split(',');
                    for (j = 0; j < division.length; j++) {
                        s_id = division[j];

                        //cantidad
                        cantidad = document.getElementById('cantidad_' + s_id);
                        //fecha vencimiento
                        f_venc = document.getElementById('f_venc_' + s_id);
                        //fecha elaboracion
                        f_elab = document.getElementById('f_elab_' + s_id);
                        //lote
                        lote = document.getElementById('lote_' + s_id);
                        //actual
                        actual = document.getElementById('actual_' + s_id);
                        //costo
                        costo = document.getElementById('costo_' + s_id);
                        //total
                        total = document.getElementById('total_' + s_id);

                        if (cantidad.value != '' && costo.value != '' && total.value != '') {
                            datos[aux_producto] = producto.value;
                            datos[aux_tb2] = tb2.value;
                            datos[nombre] = stock_ids;
                            datos['cantidad_' + s_id] = cantidad.value;
                            datos['actual_' + s_id] = actual.value;
                            datos['f_elab_' + s_id] = f_elab.value;
                            datos['f_venc_' + s_id] = f_venc.value;
                            datos['lote_' + s_id] = lote.value;
                            datos['costo_' + s_id] = costo.value;
                            datos['total_' + s_id] = total.value;
                            cant_productos++;
                        }

                        /*cantidad.value = '';
                        f_venc.value = '';
                        lote.value = '';
                        actual.value = '';
                        costo.value = '';
                        total.value = '';*/
                    }
                }
            }
            catch (e) {

            }
        }

        if (cant_productos == 0) {
            alert('debe seleccionar al menos 1 producto');
            return false;
        }

        /*producto.value = "0";
        tb2.value = "";

        //ocultamos las filas
        if (i > 1) {
            fila = document.getElementById('fila_' + i);
            fila.style.display = 'none';
        }*/
    }//end for
    /*obj_total = document.getElementById('total_pedido');
    obj_total.value = '';*/
    div_datos.fadeOut('slow');
    div_ventas_dia.fadeIn();
    div_ventas_dia.html(imagen);
    //alert(url_add);
    div_ventas_dia.load(url_add, datos, function () {
        //termina de cargar la ventana
        setTimeout(function () {
            $('#message').fadeOut('slow');
        }, 3000);
    });
    //mostramos el boton de nueva venta
    btn_cancelar = $('#btn_cancelar_venta');
    btn_nuevo = $('#btn_nueva_venta');

    btn_cancelar.fadeOut('slow');
    btn_nuevo.fadeIn('slow');
}

//nuevo cliente
function nuevoCliente() {
    div_nuevo = $('#div_nuevo_cliente');
    div_nuevo.fadeIn('slow');
    div_buscar_cliente1 = $('#div_buscar_cliente1');
    div_buscar_cliente2 = $('#div_buscar_cliente2');

    //recuperamos stock del producto
    url_main = document.getElementById('url_main').value;
    url_add = document.getElementById('url_add').value;
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    datos = {
        'operation_x': 'nuevo_cliente',
        'csrfmiddlewaretoken': token,
    }

    div_nuevo.html(imagen);
    div_nuevo.load(url_main, datos, function () {
        //termina de cargar la ventana
    });

    div_buscar_cliente1.fadeOut();
    div_buscar_cliente2.fadeOut();
}

//miniminar nuevo cliente
function minimizarCliente() {
    div_nuevo = $('#div_nuevo_cliente');
    div_buscar_cliente1 = $('#div_buscar_cliente1');
    div_buscar_cliente2 = $('#div_buscar_cliente2');

    div_nuevo.fadeOut('slow');
    div_buscar_cliente1.fadeOut('slow');
    div_buscar_cliente2.fadeOut('slow');
}

//mostrar opciones de busqueda de cliente
function mostrarBuscarCliente() {
    div_buscar_cliente1 = $('#div_buscar_cliente1');
    div_nuevo = $('#div_nuevo_cliente');

    div_nuevo.fadeOut('slow');
    div_buscar_cliente1.fadeIn('slow');
}

//buscar cliente
function buscarCliente() {
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
        'operation_x': 'buscar_cliente',
        'ci_nit': ci_nit_txt,
        'apellidos': apellidos_txt,
        'nombres': nombres_txt,
        'csrfmiddlewaretoken': token,
    }

    $("#div_buscar_cliente2").fadeIn('slow');

    $("#div_clientes").html(imagen);
    $("#div_clientes").load(url_main, datos, function () {
        //termina de cargar la ventana
    });
}

//selecccionar cliente
function seleccionarCliente(cliente_id) {
    obj_ci_nit = document.getElementById('ci_nit_' + cliente_id);
    obj_apellidos = document.getElementById('apellidos_' + cliente_id);
    obj_nombres = document.getElementById('nombres_' + cliente_id);
    obj_telefonos = document.getElementById('telefonos_' + cliente_id);

    mostrarDatosCliente(obj_apellidos.value, obj_nombres.value, obj_ci_nit.value, obj_telefonos.value);

    div_clientes = document.getElementById('div_clientes');
    div_clientes.innerHTML = '';
}

//mostramos datos del cliente cuando se selecciona o crea
function mostrarDatosCliente(apellidos, nombres, nit, telefonos) {
    cliente_detalle = document.getElementById('cliente_detalle');
    poner = '<b>' + apellidos + ' ' + nombres + '</b>, CI/NIT: <b>' + nit + '</b>';
    cliente_detalle.innerHTML = poner;

    obj_ci_nit = document.getElementById('ci_nit');
    obj_apellidos = document.getElementById('apellidos');
    obj_nombres = document.getElementById('nombres');
    obj_telefonos = document.getElementById('telefonos');

    obj_ci_nit.value = nit;
    obj_apellidos.value = apellidos;
    obj_nombres.value = nombres;
    obj_telefonos.value = telefonos;
}

//guardamos al nuevo cliente
function guardarNuevoCliente() {
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    url_main = document.getElementById('url_main').value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    ci_nit = Trim(document.getElementById('n_ci_nit').value);
    apellidos = Trim(document.getElementById('n_apellidos').value);
    nombres = Trim(document.getElementById('n_nombres').value);
    telefonos = Trim(document.getElementById('n_telefonos').value);

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
        'operation_x': 'guardar_nc',
        'ci_nit': ci_nit,
        'apellidos': apellidos,
        'nombres': nombres,
        'telefonos': telefonos,
        'csrfmiddlewaretoken': token,
    }

    $("#div_nuevo_cliente").html(imagen);
    $("#div_nuevo_cliente").load(url_main, datos, function () {
        //termina de cargar la ventana
        cargarNuevoCliente();
    });
}

//cargamos cuando se adiciona el nuevo cliente
function cargarNuevoCliente() {
    //resultado de la operacion
    try {
        res = document.getElementById('r_operation').value;
        if (res == '1') {
            ci_nit_valor = document.getElementById('r_ci_nit').value;
            apellidos_valor = document.getElementById('r_apellidos').value;
            nombres_valor = document.getElementById('r_nombres').value;
            telefonos_valor = document.getElementById('r_telefonos').value;

            mostrarDatosCliente(apellidos_valor, nombres_valor, ci_nit_valor, telefonos_valor);
        }
    }
    catch (e) {
        //
        alert('error');
    }

}

//next id
function loadID(id) {
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    url_main = document.getElementById('url_main').value;
    url_add = document.getElementById('url_add').value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    datos = {
        'operation_x': 'load_id_x',
        'load_id': id,
        'csrfmiddlewaretoken': token,
    }

    div_ventas_dia = $('#div_ventas_dia');
    div_ventas_dia.html(imagen);
    div_ventas_dia.load(url_add, datos, function () {
        //termina de cargar la ventana
    });
}

//anulamos la venta
function anularVenta(venta_id) {
    id_anular = document.getElementById('id_null');
    id_anular.value = venta_id;

    fila_anular = $('#linea_anular');
    fila_anular.fadeIn('slow');
}

//confirmar anular general
function confirmarAnularGeneral() {
    if (verifyForm()) {
        if (confirm('Esta seguro de querer anular este elemento?')) {
            document.forms['formulario'].elements['add_button'].disabled = true;
            document.forms['formulario'].elements['button_cancel'].disabled = true;
            document.forms['formulario'].submit();
        }
    }
}

//confirmar anular
function confirmarAnular() {
    motivo = document.getElementById('motivo');
    if (Trim(motivo.value) == '') {
        alert('debe llenar el motivo');
        motivo.focus();
        return false;
    }

    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    id_anular = document.getElementById('id_null').value;

    url_main = document.getElementById('url_main').value;
    url_add = document.getElementById('url_add').value;
    ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
    imagen = '<img src="' + ruta_imagen + '">';

    datos = {
        'operation_x': 'anular_x',
        'venta_id': id_anular,
        'motivo_anula': Trim(motivo.value),
        'csrfmiddlewaretoken': token,
    }

    div_ventas_dia = $('#div_ventas_dia');
    div_ventas_dia.html(imagen);
    div_ventas_dia.load(url_add, datos, function () {
        //termina de cargar la ventana
    });
}

//cancelar la anulacion
function cancelarAnular() {
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

//modificacion de venta
function modificarVenta(venta_id) {
    nuevaVenta();
    producto_id = '';
    producto_nombre = '';
    lista_cantidad = '';
    lista_costo = '';
    lista_total = '';
    lista_fecha_elab = '';
    lista_fecha_venc = '';
    lista_lote = '';

    //marcamos la operacion
    operacion_mod = document.getElementById('tipo_operacion');
    m_id_mod = document.getElementById('m_venta_id');
    operacion_mod.value = 'modify';
    m_id_mod.value = venta_id;

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
    almacen.value = almacen_id;
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

    for (i = 1; i <= 50; i++) {
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

//seleccion del producto modificacion
function seleccionPModificar(numero_registro, producto, id, lista_cantidad, lista_costo, lista_total, lista_fecha_elab, lista_fecha_venc, lista_lote) {

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
        'operation_x': 'stock_producto',
        'id': id,
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
        datosCosto(id);
        datosModificar(numero_registro, id, lista_cantidad, lista_costo, lista_total, lista_fecha_elab, lista_fecha_venc, lista_lote);
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

//cargamos datos de modificacion
function datosModificar(fila, producto_id, lista_cantidad, lista_costo, lista_total, lista_fecha_elab, lista_fecha_venc, lista_lote) {
    m_stock_ids = document.getElementById('stock_ids_' + producto_id).value;
    //alert(m_stock_ids);
    m_lista_cantidad = lista_cantidad.split('|');
    m_lista_costo = lista_costo.split('|');
    m_lista_total = lista_total.split('|');
    m_lista_fecha_elab = lista_fecha_elab.split('|');
    m_lista_fecha_venc = lista_fecha_venc.split('|');
    m_lista_lote = lista_lote.split('|');

    if (m_stock_ids != '') {
        division = m_stock_ids.split(',');
        for (j = 0; j < division.length; j++) {
            s_id = division[j];

            //fecha vencimiento
            f_venc = document.getElementById('f_venc_' + s_id).value;
            //fecha elaboracion
            f_elab = document.getElementById('f_elab_' + s_id).value;
            //lote
            lote = document.getElementById('lote_' + s_id).value;

            for (k = 0; k < m_lista_cantidad.length; k++) {
                if (m_lista_fecha_elab[k] == f_elab && m_lista_fecha_venc[k] == f_venc && m_lista_lote[k] == lote) {
                    //cantidad
                    cantidad = document.getElementById('cantidad_' + s_id);
                    cantidad.value = m_lista_cantidad[k];

                    //costo
                    costo = document.getElementById('costo_' + s_id);
                    costo.value = m_lista_costo[k];

                    //total
                    total = document.getElementById('total_' + s_id);
                    total.value = m_lista_total[k];
                }
            } // fin for k

        }//fin for j
        try {
            totalPedido();
        }
        catch (e) {

        }
    }
}

//pedido de inventario
function pedidoInventario() {
    almancen_pedido = document.getElementById('almacen_pedido').value;
    document.form_operation.operation_x.value = 'pedido_almacen';
    document.form_operation.id.value = almancen_pedido;
    document.form_operation.submit();
}

//pedido de inventario
function pedidoInventario2() {
    almancen_pedido2 = document.getElementById('almacen_pedido2').value;
    document.form_operation.operation_x.value = 'pedido_almacen';
    document.form_operation.id.value = almancen_pedido2;
    document.form_operation.submit();
}

//verificamos los pedidos de preventa
function marcarPedido(numero) {
    //verificamos productos del pedido segun fecha elab, fecha venc, lote
    aux_p = document.getElementById('cant_productos_pedido');
    cant_pro_ped = parseInt(aux_p.value);

    try {
        for (i = 1; i <= 100; i++) {
            a_f_elab = document.getElementById('pedido_' + numero + '_fecha_elab_' + i).value;
            a_f_venc = document.getElementById('pedido_' + numero + '_fecha_venc_' + i).value;
            a_lote = document.getElementById('pedido_' + numero + '_lote_' + i).value;
            a_cant = document.getElementById('pedido_' + numero + '_cantidad_' + i).value;
            a_p_id = document.getElementById('pedido_' + numero + '_producto_id_' + i).value;

            chk_pedido = document.getElementById('pedido_' + numero);

            //disminuimos en el total
            for (j = 1; j <= cant_pro_ped; j++) {
                p_producto_id = document.getElementById('producto_pedido_' + j).value;
                //alert(p_producto_id);
                p_f_elab = document.getElementById('producto_fecha_elab_' + j).value;
                p_f_venc = document.getElementById('producto_fecha_venc_' + j).value;
                p_lote = document.getElementById('producto_lote_' + j).value;
                p_cant = document.getElementById('producto_pedido_cant_' + j);
                p_cantidad = parseInt(p_cant.value);

                if (a_p_id == p_producto_id && a_f_elab == p_f_elab && a_f_venc == p_f_venc && a_lote == p_lote) {
                    if (chk_pedido.checked) {
                        nueva_cantidad = parseInt(a_cant) + p_cantidad;
                    }
                    else {
                        nueva_cantidad = p_cantidad - parseInt(a_cant);
                    }
                    cant_poner = nueva_cantidad + '';
                    p_cant.value = cant_poner;
                }
            }
        }
    }
    catch (e) {
        //alert(e);
    }
}

//cancelamos el pedido
function cancelarPedido() {
    document.formulario.add_button.disabled = true;
    document.formulario.button_cancel.disabled = true;
    document.form_cancel.submit();
    return true;
}

//guardamos el pedido
function guardarPedido() {
    document.formulario.add_button.disabled = true;
    document.formulario.button_cancel.disabled = true;
    document.formulario.submit();
    return true;
}

//en caso de cambiar el tipo de venta y de costo, actualizamos datos del costo
function verificarCostos() {
    for (i = 1; i <= 50; i++) {
        producto = document.getElementById('producto_' + i);
        tb2 = document.getElementById('tb2_' + i);

        //stocks
        if (producto.value != '0' && producto.value != '') {
            try {
                datosCosto(producto.value);
            }
            catch (e) {
                alert('error ' + e.toString());
            }
        }
    }
    totalPedido();
}