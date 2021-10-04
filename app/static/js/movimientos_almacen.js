
function sendSearchMA() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormMA(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'MASaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Movimientos Almacen!', 'Esta seguro de querer adicionar este movimiento de Almacen?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Movimientos Almacen!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'MAWarning();';
                modalF.modal();
            }
            break;

        case ('anular'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'MAAnular();';
                //set data modal
                modalSetParameters('danger', 'center', 'Movimientos Almacen!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Movimientos Almacen!', resValidation, 'Cancelar', 'Volver');
                //function cancel
                modalFunction.value = 'MAWarning();';
                modalF.modal();
            }

            break;

        default:
            break;
    }
}

function MASaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function MAWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function MAAnular() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function seleccionAlmacenMA() {
    //almacen
    almacen = document.getElementById('almacen');
    almacen2 = document.getElementById('almacen2');

    div_datos = $('#div_listap');
    //si selecciono los datos necesarios
    if (almacen.value != '0' && almacen2.value != '0' && almacen.value != almacen2.value) {
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

function controlarStockMA(stock_id) {
    actual = parseFloat(document.getElementById('actual_' + stock_id).value);
    cantidad = document.getElementById('cantidad_' + stock_id);
    valor_cantidad = parseFloat(Trim(cantidad.value));
    if (valor_cantidad > actual) {
        cantidad.value = '';
        alert('la cantidad no puede ser mayor a ' + actual);
    }
}

function seleccionPMA(numero_registro, producto, id) {
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

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'stock_producto',
        'id': id,
        'almacen': almacen,
        'csrfmiddlewaretoken': token
    }

    imagen = '<img src="' + ruta_imagen + '">';
    fila = $("#div_fila_" + numero_registro);

    fila.html(imagen);
    fila.load(url_main, datos, function () {
        //termina de cargar la ventana
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

function validarFilaMA(fila) {
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
            //alert('Debe Seleccionar un Producto');
            tb2.value = '';
            tb2.focus();
        }
    }
}
