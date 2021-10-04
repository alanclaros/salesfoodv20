/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/


//control especifico del modulo
function controlModulo() {
	caja1 = document.getElementById('caja1');
	caja1_value = caja1.value;
	caja2 = document.getElementById('caja2');
	caja2_value = caja2.value;

	if (caja1_value == '') {
		alert('debe seleccionar una caja de envio');
		caja1.focus();
		return false;
	}

	if (caja2_value == '0') {
		alert('debe seleccionar una caja de destino');
		caja2.focus();
		return false;
	}

	operation = document.getElementById('operation_x').value;
	if (operation == 'anular' || operation == 'anular_guardar' || operation == 'anular_recepcion_guardar') {
		motivo = document.getElementById('motivo_anula');
		motivo_txt = TrimDerecha(TrimIzquierda(motivo.value));
		if (motivo_txt == '') {
			alert('debe llenar este campo');
			motivo.focus();
			return false;
		}
	}

	return true;
}

function cambiarSaldo() {
	caja1 = document.getElementById('caja1');
	caja1_valor = caja1.value;
	label_saldo = document.getElementById('lbl_saldo');

	lista_saldo = document.getElementById('lista_saldo_origen').value;
	if (lista_saldo.length > 0) {
		division = lista_saldo.split(";;");

		for (i = 0; i < division.length; i++) {
			div2 = division[i].split('|');
			if (caja1_valor == div2[0]) {
				label_saldo.innerHTML = div2[1];
			}
		}
	}
}


function mandarFormularioCajaMovimientoEnvio(operation, operation2, formulario, add_button, button_cancel) {
	if (verifyForm()) {
		document.forms[formulario].elements[add_button].disabled = true;
		document.forms[formulario].elements[button_cancel].disabled = true;

		//document.forms[formulario].submit();
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
		module_x = document.forms['form_operation'].elements['module_x'].value;

		var fd = new FormData();
		fd.append('csrfmiddlewaretoken', token_operation);
		fd.append('module_x', module_x);
		fd.append('operation_x', operation);
		fd.append('id', document.forms['form_operation'].elements['id'].value);

		fd.append(operation2, 'acc');

		fd.append('caja1', document.getElementById('caja1').value);
		fd.append('caja2', document.getElementById('caja2').value);
		fd.append('monto', document.getElementById('monto').value);
		fd.append('concepto', document.getElementById('concepto').value);

		div_modulo.html(imagen_modulo);

		$.ajax({
			url: '/',
			type: 'post',
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
		});
	}
}

function confirmarAnularCajaMovimientoEnvio() {
	if (Trim(document.getElementById('motivo_anula').value) == '') {
		alert('Debe llenar el motivo');
		document.getElementById('motivo_anula').focus();
		return false;
	}

	if (confirm('Esta seguro de querer anular este envio de movimiento?')) {
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

		document.forms['formulario'].elements['add_button'].disabled = true;
		document.forms['formulario'].elements['button_cancel'].disabled = true;

		datos_operation = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'csrfmiddlewaretoken': token_operation,
			'operation_x': 'anular_guardar',
			'anular_guardar': 'acc',
		}
		datos_operation['id'] = document.forms['form_operation'].elements['id'].value;
		datos_operation['concepto'] = document.getElementById('concepto').value;
		datos_operation['motivo_anula'] = document.getElementById('motivo_anula').value;

		div_modulo.html(imagen_modulo);
		div_modulo.load('/', datos_operation, function () {
			//termina de cargar la ventana
		});
	}
}


function mandarFormularioCajaMovimientoRecibe(operation, operation2, formulario, add_button, button_cancel) {
	if (verifyForm()) {
		document.forms[formulario].elements[add_button].disabled = true;
		document.forms[formulario].elements[button_cancel].disabled = true;

		//document.forms[formulario].submit();
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
		module_x = document.forms['form_operation'].elements['module_x'].value;

		var fd = new FormData();
		fd.append('csrfmiddlewaretoken', token_operation);
		fd.append('module_x', module_x);
		fd.append('operation_x', operation);
		fd.append('id', document.forms['form_operation'].elements['id'].value);

		fd.append(operation2, 'acc');

		fd.append('caja1', document.getElementById('caja1').value);
		fd.append('caja2', document.getElementById('caja2').value);
		fd.append('monto', document.getElementById('monto').value);
		fd.append('concepto', document.getElementById('concepto').value);

		div_modulo.html(imagen_modulo);

		$.ajax({
			url: '/',
			type: 'post',
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
		});
	}
}

function confirmarAnularCajaMovimientoRecibe() {
	if (Trim(document.getElementById('motivo_anula').value) == '') {
		alert('Debe llenar el motivo');
		document.getElementById('motivo_anula').focus();
		return false;
	}

	if (confirm('Esta seguro de querer anular esta recepcion de movimiento?')) {
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

		document.forms['formulario'].elements['add_button'].disabled = true;
		document.forms['formulario'].elements['button_cancel'].disabled = true;

		datos_operation = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'csrfmiddlewaretoken': token_operation,
			'operation_x': 'anular_recepcion_guardar',
			'anular_recepcion_guardar': 'acc',
		}
		datos_operation['id'] = document.forms['form_operation'].elements['id'].value;
		datos_operation['concepto'] = document.getElementById('concepto').value;
		datos_operation['motivo_anula'] = document.getElementById('motivo_anula').value;

		div_modulo.html(imagen_modulo);
		div_modulo.load('/', datos_operation, function () {
			//termina de cargar la ventana
		});
	}
}