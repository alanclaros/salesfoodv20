
//cambio en opcion de busqueda de planes de pagos
function cambiarTipoPlanP() {
    tipo = document.getElementById('search_tipo_plan_pago').value;
    fila1_ven = $('#fila1_venta');
    fila2_ven = $('#fila2_venta');
    fila1_inv = $('#fila1_inventario');

    if (tipo == 'venta') {
        fila1_ven.fadeIn('slow');
        fila2_ven.fadeIn('slow');
        fila1_inv.fadeOut('slow');
    }
    else {
        fila1_ven.fadeOut('slow');
        fila2_ven.fadeOut('slow');
        fila1_inv.fadeIn('slow');
    }
}

async function sendSearchPlanP() {
    var fd = new FormData(document.forms['search']);

    // for (var pair of fd.entries()) {
    //     console.log(pair[0] + ', ' + pair[1]);
    // }

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

//detalle del plan de pagos
async function detallePPPlanP(plan_pago_id) {
    document.form_operation.operation_x.value = 'detail';
    document.form_operation.id.value = plan_pago_id;
    //document.form_operation.submit();

    var fd = new FormData(document.forms['form_operation']);

    // for (var pair of fd.entries()) {
    //     console.log(pair[0] + ', ' + pair[1]);
    // }

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

//acc, cobro de la cuota
async function cobroCuotaPlanP() {
    monto = document.getElementById('monto');
    monto_valor = Trim(monto.value);

    observacion = document.getElementById('observacion');
    observacion_valor = Trim(observacion.value);

    if (monto_valor == '') {
        alert('Debe llenar el monto');
        monto.focus();
        return false;
    }

    if (observacion_valor == '') {
        alert('Debe llenar la observacion');
        observacion.focus();
        return false;
    }

    saldo = document.getElementById('plan_pago_saldo').value;
    saldo2 = parseFloat(saldo);
    monto2 = parseFloat(monto_valor);

    if (monto2 > saldo2) {
        alert('el saldo es de: ' + saldo + ' bs.');
        monto.focus();
        return false;
    }

    document.formulario.add_button.disabled = true;
    //document.formulario.submit();
    var fd = new FormData(document.forms['formulario']);

    // for (var pair of fd.entries()) {
    //     console.log(pair[0] + ', ' + pair[1]);
    // }

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

    return true;
}

//acc, anulacion de pago
function anularCuotaPlanP(plan_pago_id, cuota_id) {
    fila = $('#fila_anular_' + cuota_id);
    fila.fadeIn('slow');
}

//acc, imprimir cuota
function imprimirCuotaPlanP(cuota_id) {
    document.form_print.operation_x.value = 'imprimir_cuota';
    document.form_print.id.value = cuota_id;

    document.form_print.submit();
}

//acc, confirmacion de anulacion
async function confirmarAnularPlanP(plan_pago_id, cuota_id) {
    motivo = document.getElementById('motivo_anula_' + cuota_id);
    if (Trim(motivo.value) == '') {
        alert('Debe llenar el motivo');
        motivo.focus();
        return false;
    }

    document.form_operation.operation_x.value = 'detail';
    document.form_operation.operation_x2.value = 'anular';
    document.form_operation.id.value = plan_pago_id;
    document.form_operation.id2.value = cuota_id;
    document.form_operation.motivo_anula.value = motivo.value;

    //document.form_operation.submit();

    var fd = new FormData(document.forms['form_operation']);

    // for (var pair of fd.entries()) {
    //     console.log(pair[0] + ', ' + pair[1]);
    // }

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

    return true;
}

//acc, cancelar anulacion
function cancelarAnularPlanP(cuota_id) {
    fila = $('#fila_anular_' + cuota_id);
    fila.fadeOut('slow');
}

//acc, impresion plan de pagos
function imprimirPlanPagosPlanP(plan_pago_id) {
    document.form_print.operation_x.value = 'imprimir_plan_pago';
    document.form_print.id.value = plan_pago_id;

    document.form_print.submit();
}

//acc, impresion pagos del plan de pagos
function imprimirPagosPlanP(plan_pago_id) {
    document.form_print.operation_x.value = 'imprimir_pagos';
    document.form_print.id.value = plan_pago_id;

    document.form_print.submit();
}