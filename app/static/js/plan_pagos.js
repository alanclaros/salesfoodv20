
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

function sendSearchPlanP() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

//detalle del plan de pagos
function detallePPPlanP(plan_pago_id) {
    document.form_operation.operation_x.value = 'detail';
    document.form_operation.id.value = plan_pago_id;
    div_modulo = $("#div_block_content");

    sendFormObject('form_operation', div_modulo);
}

function cobrarCuotaWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function cobrarCuotaSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');

    sendFormObject('formulario', div_modulo);
}

//acc, cobro de la cuota
function cobroCuotaPlanP() {
    monto = document.getElementById('monto');
    monto_valor = Trim(monto.value);

    observacion = document.getElementById('observacion');
    observacion_valor = Trim(observacion.value);

    caja = document.getElementById('caja');
    caja_valor = Trim(caja.value);

    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    if (monto_valor == '') {
        //alert('Debe llenar el monto');
        //monto.focus();
        modalSetParameters('warning', 'center', 'Plan Pagos!', 'debe llenar el monto', 'Cancelar', 'Volver');
        modalFunction.value = 'cobrarCuotaWarning();';
        modalF.modal();
        return false;
    }

    if (caja_valor == '' || caja_valor === null) {
        //alert('Debe llenar el monto');
        //monto.focus();
        modalSetParameters('warning', 'center', 'Plan Pagos!', 'debe seleccionar una caja', 'Cancelar', 'Volver');
        modalFunction.value = 'cobrarCuotaWarning();';
        modalF.modal();
        return false;
    }

    if (observacion_valor == '') {
        //alert('Debe llenar la observacion');
        //observacion.focus();
        modalSetParameters('warning', 'center', 'Plan Pagos!', 'debe llenar la observacion', 'Cancelar', 'Volver');
        modalFunction.value = 'cobrarCuotaWarning();';
        modalF.modal();
        return false;
    }

    saldo = document.getElementById('plan_pago_saldo').value;
    saldo2 = parseFloat(saldo);
    monto2 = parseFloat(monto_valor);

    if (monto2 > saldo2) {
        //alert('el saldo es de: ' + saldo + ' bs.');
        //monto.focus();
        modalSetParameters('warning', 'center', 'Plan Pagos!', 'el saldo es de: ' + saldo + ' bs.', 'Cancelar', 'Volver');
        modalFunction.value = 'cobrarCuotaWarning();';
        modalF.modal();

        return false;
    }

    modalSetParameters('success', 'center', 'Plan Pagos!', 'esta seguro de realizar este pago?', 'Cancelar', 'Cobrar');
    modalFunction.value = 'cobrarCuotaSaveForm();';
    modalF.modal();
}

//acc, anulacion de pago
function anularCuotaPlanP(plan_pago_id, cuota_id) {
    fila = $('#fila_anular_' + cuota_id);
    fila.fadeIn('slow');
}

//acc, confirmacion de anulacion
function confirmarAnularPlanP(plan_pago_id, cuota_id) {
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    motivo = document.getElementById('motivo_anula_' + cuota_id);
    if (Trim(motivo.value) == '') {
        //alert('Debe llenar el motivo');
        //motivo.focus();
        modalSetParameters('warning', 'center', 'Plan Pagos!', 'Debe llenar el motivo de anulacion', 'Cancelar', 'Volver');
        //function cancel
        modalFunction.value = 'cobrarCuotaWarning();';
        modalF.modal();
        return false;
    }

    document.form_operation.operation_x.value = 'detail';
    document.form_operation.operation_x2.value = 'anular';
    document.form_operation.id.value = plan_pago_id;
    document.form_operation.id2.value = cuota_id;
    document.form_operation.motivo_anula.value = motivo.value;

    modalSetParameters('danger', 'center', 'Plan Pagos!', 'esta seguro de querer anular este pago?', 'Cancelar', 'Anular');
    //function cancel
    modalFunction.value = 'anularCuotaSaveForm();';
    modalF.modal();

    //div_modulo = $("#div_block_content");
    //sendFormObject('form_operation', div_modulo);
}

function anularCuotaSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');

    sendFormObject('form_operation', div_modulo);
}

//acc, cancelar anulacion
function cancelarAnularPlanP(cuota_id) {
    fila = $('#fila_anular_' + cuota_id);
    fila.fadeOut('slow');
}

//acc, imprimir cuota
function imprimirCuotaPlanP(cuota_id) {
    document.form_print.operation_x.value = 'imprimir_cuota';
    document.form_print.id.value = cuota_id;

    document.form_print.submit();
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