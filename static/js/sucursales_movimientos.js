/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

//$('#div_cuenta_bancaria').fadeOut('slow');

//control especifico del modulo
function controlModulo() {
	//por efectivo
	caja1 = document.getElementById('caja1');
	caja1_value = caja1.value;
	caja2 = document.getElementById('caja2');
	caja2_value = caja2.value;
	monto = document.getElementById('monto');
	monto_value = Trim(monto.value);
	concepto = document.getElementById('concepto');
	concepto_value = Trim(concepto.value);

	//cuenta bancaria
	cb1 = document.getElementById('cuenta_bancaria1');
	cb1_value = cb1.value;
	cb2 = document.getElementById('cuenta_bancaria2');
	cb2_value = cb2.value;
	monto_cb = document.getElementById('monto_cb');
	monto_cb_value = Trim(monto_cb.value);
	concepto_cb = document.getElementById('concepto_cb');
	concepto_cb_value = Trim(concepto_cb.value);

	//opcion seleccionada
	chk_cb = document.getElementById('chk_cuenta_bancaria');

	if (chk_cb.checked) {
		//metodo cuenta bancaria
		if (cb1_value == '0') {
			alert('debe seleccionar una cuenta bancaria de envio');
			cb1.focus();
			return false;
		}

		if (cb2_value == '0') {
			alert('debe seleccionar una cuenta bancaria de destino');
			cb2.focus();
			return false;
		}

		if (monto_cb_value == '') {
			alert('debe llenar el monto');
			monto_cb.focus();
			return false;
		}

		if (concepto_cb_value == '') {
			alert('debe llenar el concepto');
			concepto_cb.focus();
			return false;
		}
	}
	else {
		//metodo por cajas
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

		if (monto_value == '') {
			alert('debe llenar el monto');
			monto.focus();
			return false;
		}

		if (concepto_value == '') {
			alert('debe llenar el concepto');
			concepto.focus();
			return false;
		}
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

//tipo de operacion: cuenta bancaria o efectivo cajas
function tipoMovimiento() {
	//tipo_mov = document.getElementById('tipo_movimiento').value;
	chk_cb = document.getElementById('chk_cuenta_bancaria');

	div_cuenta_bancaria = document.getElementById('div_cuenta_bancaria');
	div_efectivo = document.getElementById('div_efectivo');

	if (chk_cb.checked) {
		//div_cuenta_bancaria.style.display = 'block';
		//div_efectivo.style.display = 'none';

		$('#div_efectivo').fadeOut('slow');
		$('#div_cuenta_bancaria').fadeIn('slow');
	}
	else {
		//div_cuenta_bancaria.style.display = 'none';
		//div_efectivo.style.display = 'block';

		$('#div_cuenta_bancaria').fadeOut('slow');
		$('#div_efectivo').fadeIn('slow');
	}
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

//label de moneda de la cuenta bancaria
function monedaCB() {
	cuenta_bancaria = document.getElementById('cuenta_bancaria1').value;
	cb_text = document.getElementById('cuenta_bancaria1');
	lbl_cb = document.getElementById('lbl_cb');

	if (cuenta_bancaria == '0') {
		lbl_cb.innerHTML = '.';
	}
	else {
		//alert(cb_text.options[cb_text.selectedIndex].text);
		dato = cb_text.options[cb_text.selectedIndex].text;
		pos = dato.indexOf('(');
		moneda = dato.substring(pos + 1, dato.length - 1);
		lbl_cb.innerHTML = moneda;
	}
}

//confirmacion de la recepcion
function confirmarRecibir(formulario, add_button, button_cancel) {
	if (confirm('Esta seguro de recibir este envio')) {
		mandarFormularioDirecto(formulario, add_button, button_cancel);
	}
}

//function confirmar anular
function confirmarAnularRecibir(formulario, add_button, button_cancel) {
	motivo = document.getElementById('motivo_anula');
	motivo_txt = TrimDerecha(TrimIzquierda(motivo.value));
	if (motivo_txt == '') {
		alert('debe llenar este campo');
		motivo.focus();
		return false;
	}

	if (confirm('Esta seguro de anular esta recepcion de envio')) {
		mandarFormularioDirecto(formulario, add_button, button_cancel);
	}
}