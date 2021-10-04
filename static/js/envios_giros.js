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

//ajax, selecciona moneda
function escogeMoneda() {
	//simbolo moneda
	aux_moneda = document.getElementById('tipo_moneda');
	simbolo_moneda = aux_moneda.options[aux_moneda.selectedIndex].text;
	//labels
	lbl_efectivo = document.getElementById('lbl_efectivo');
	lbl_cambio = document.getElementById('lbl_cambio');
	lbl_efectivo.innerHTML = simbolo_moneda;
	lbl_cambio.innerHTML = simbolo_moneda;

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	url_main = document.getElementById('url_main').value;
	ruta_imagen = document.getElementById('ruta_imagen2').value;

	moneda = Trim(document.getElementById('tipo_moneda').value);

	reinicarDivisa();

	if (moneda == '0') {
		$("#tabla_efectivo_divisa").fadeOut();

		$("#div_monto").html('<i>Monto</i><br>');
		$("#div_comision").html('<i>Comision</i><br>');
		$("#div_total").html('<i>Total</i><br>');
		$("#div_moneda_divisa").html('<i>Moneda</i>');
	}
	else {
		$("#tabla_efectivo_divisa").fadeIn();
		datos_monto = {
			'operation_x': 'select_moneda',
			'operation2': 'monto',
			'tipo_moneda': moneda,
			'csrfmiddlewaretoken': token,
		}
		datos_comision = {
			'operation_x': 'select_moneda',
			'operation2': 'comision',
			'tipo_moneda': moneda,
			'csrfmiddlewaretoken': token,
		}
		datos_total = {
			'operation_x': 'select_moneda',
			'operation2': 'total',
			'tipo_moneda': moneda,
			'csrfmiddlewaretoken': token,
		}
		datos_moneda_divisa = {
			'operation_x': 'select_moneda',
			'operation2': 'moneda_divisa',
			'tipo_moneda': moneda,
			'csrfmiddlewaretoken': token,
		}

		imagen = '<img src="' + ruta_imagen + '">';
		//alert(imagen);

		$("#div_monto").html(imagen);
		$("#div_comision").html(imagen);
		$("#div_total").html(imagen);
		$("#div_moneda_divisa").html(imagen);

		$("#div_monto").load(url_main, datos_monto, function () {
			//termina de cargar la ventana
		});
		$("#div_comision").load(url_main, datos_comision, function () {
			//termina de cargar la ventana
		});
		$("#div_total").load(url_main, datos_total, function () {
			//termina de cargar la ventana
		});
		$("#div_moneda_divisa").load(url_main, datos_moneda_divisa, function () {
			//termina de cargar la ventana
		});
	}
}

//calculo de la comision
function calcularComision() {
	lista_comisiones = document.getElementById('lista_comision').value;
	if (lista_comisiones.length == 0) {
		alert('no existen comisiones configuradas');
		return false;
	}

	lista_div = lista_comisiones.split(';;');
	menor = Array();
	mayor = Array();
	fijo = Array();
	porcentaje = Array();

	for (i = 0; i < lista_div.length; i++) {
		div2 = lista_div[i].split('|');

		/*menor[i] = parseFloat(div2[0]);
		mayor[i] = parseFloat(div2[1]);
		fijo[i] = parseFloat(div2[2]);
		porcentaje[i] = parseFloat(div2[3]);*/

		menor[i] = div2[0];
		mayor[i] = div2[1];
		fijo[i] = div2[2];
		porcentaje[i] = div2[3];

	}
	cant_comision = i;

	monto = Trim(document.getElementById('monto').value);

	comision = document.getElementById('comision');
	total = document.getElementById('total');

	//tipo de comision
	chk_fijo = document.getElementById('chk_c_monto');
	tipo_comision = '';
	if (chk_fijo.checked) {
		tipo_comision = 'fijo';
	}
	else {
		tipo_comision = 'porcentaje';
	}

	comision_poner = '';
	total_poner = 0;

	if (monto == '') {
		comision.value = '';
		total.value = '';
		return false;
	}

	//recuperamos la comision
	monto_valor = parseFloat(monto);
	for (i = 0; i < cant_comision; i++) {
		if (monto_valor >= parseFloat(menor[i])) {
			if (tipo_comision == 'fijo') {
				comision_poner = fijo[i];
				total_poner = redondeo((monto_valor + parseFloat(fijo[i])), 2);
			}
			else {
				comision_poner = porcentaje[i];
				p_porcentaje = (parseFloat(porcentaje[i]) / 100) * monto_valor;

				total_poner = redondeo((monto_valor + p_porcentaje), 2);
			}
		}
	}

	//colocamos la comision
	comision.value = comision_poner;
	total.value = total_poner;

	//totoal efectivo
	efectivo = document.getElementById('efectivo');
	cambio_efectivo = document.getElementById('cambio_efectivo');
	efectivo.value = total.value;
	cambio_efectivo.value = '0';

	reinicarDivisa();
}

//en caso de que cambie el monto de la comision
function cambiarMontoComision() {
	monto = Trim(document.getElementById('monto').value);
	comision = Trim(document.getElementById('comision').value);
	total = document.getElementById('total');

	//tipo de comision
	chk_fijo = document.getElementById('chk_c_monto');
	tipo_comision = '';
	if (chk_fijo.checked) {
		tipo_comision = 'fijo';
	}
	else {
		tipo_comision = 'porcentaje';
	}

	//calculamos
	if (monto != '' && comision != '') {
		if (tipo_comision == 'fijo') {
			total_poner = parseFloat(comision) + parseFloat(monto);
			total.value = redondeo(total_poner, 2);
		}
		else {
			p_porcentaje = (parseFloat(comision) / 100) * parseFloat(monto);
			total_poner = parseFloat(monto) + p_porcentaje;
			total.value = redondeo(total_poner, 2);
		}
		//totoal efectivo
		efectivo = document.getElementById('efectivo');
		cambio_efectivo = document.getElementById('cambio_efectivo');
		efectivo.value = total.value;
		cambio_efectivo.value = '0';
	}
	else {
		total.value = '';
		//totoal efectivo
		efectivo = document.getElementById('efectivo');
		cambio_efectivo = document.getElementById('cambio_efectivo');
		efectivo.value = '';
		cambio_efectivo.value = '';
	}

	reinicarDivisa();
}

//vuelto del efectivo
function cambioEfectivo() {
	obj_efectivo = document.getElementById('efectivo');
	obj_cambio_efectivo = document.getElementById('cambio_efectivo');
	obj_total = document.getElementById('total');

	efectivo_txt = TrimDerecha(TrimIzquierda(obj_efectivo.value));
	total_txt = TrimDerecha(TrimIzquierda(obj_total.value));

	if (efectivo_txt != '' && total_txt != '') {
		res_cambio = parseFloat(efectivo_txt) - parseFloat(total_txt);
		poner = redondeo(res_cambio, 2);
		obj_cambio_efectivo.value = poner;
	}

	if (efectivo_txt == '') {
		obj_cambio_efectivo.value = '';
	}

	//reinicamos divisas
	reinicarDivisa();
}

//en caso de que requiera cambio de divisa
function verificarCambioDivisa() {
	//verificamos efectivo y cambio
	efectivo = Trim(document.getElementById('efectivo').value);
	vuelto = Trim(document.getElementById('cambio_efectivo').value);

	divisa_monto = document.getElementById('divisa_monto');
	divisa_total = document.getElementById('divisa_total');

	//labels
	lbl_divisa_monto = document.getElementById('lbl_divisa_monto');
	lbl_divisa_total = document.getElementById('lbl_divisa_total');
	label_dcv = document.getElementById('lbl_divisa_cv');

	//moneda seleccionanda
	divisa_moneda = document.getElementById('divisa_moneda').value;
	if (divisa_moneda == '0') {
		divisa_monto.value = '';
		divisa_total.value = '';

		lbl_divisa_monto.innerHTML = '.';
		lbl_divisa_total.innerHTML = '.';
		label_dcv.innerHTML = 'Compra/Venta';
		return false;
	}

	//label con la moneda
	aux_moneda = document.getElementById('divisa_moneda');
	simbolo_moneda = aux_moneda.options[aux_moneda.selectedIndex].text;
	lbl_divisa_monto.innerHTML = simbolo_moneda;
	lbl_divisa_total.innerHTML = simbolo_moneda;

	//efectivo y vuelto
	if (efectivo == '' || vuelto == '') {
		alert('debe llenar el efectivo y tener un vuelto');
		divisa_monto.value = '';
		divisa_total.value = '';
		aux_moneda.value = '0';
		return false;
	}

	efectivo_val = parseFloat(efectivo);
	vuelto_val = parseFloat(vuelto);

	if (vuelto_val == 0) {
		alert('debe tener un vuelto para hacer el cambio de divisas');
		divisa_monto.value = '';
		divisa_total.value = '';
		aux_moneda.value = '0';
		return false;
	}

	//compra o venta
	if (vuelto_val < 0) {
		//venta
		label_dcv.innerHTML = 'Venta';
	}
	else {
		//venta
		label_dcv.innerHTML = 'Compra';
	}

	divisa_monto.readOnly = false;
	//segun la moneda y el vuelto verificamos si es compra y venta
	lista_divisas = document.getElementById('lista_divisas').value;
	lista_div = lista_divisas.split(';;');


	//compra o venta
	for (i = 0; i < lista_div.length; i++) {
		div2 = lista_div[i].split('|');
		if (divisa_moneda == div2[0]) {
			if (vuelto_val < 0) {
				divisa_monto.value = div2[2];
				p_total = Math.abs(vuelto_val) * parseFloat(div2[2]);
				divisa_total.value = redondeo(p_total, 2);
			}
			else {
				divisa_monto.value = div2[1];
				p_total = vuelto_val * parseFloat(div2[1]);
				divisa_total.value = redondeo(p_total, 2);
			}
		}
	}

}

//en caso de que requiera cambio de divisa al recoger
function verificarCambioDivisaRecogo() {
	//verificamos efectivo y cambio
	efectivo = Trim(document.getElementById('efectivo').value);
	vuelto = Trim(document.getElementById('cambio_efectivo').value);

	divisa_monto = document.getElementById('divisa_monto');
	divisa_total = document.getElementById('divisa_total');

	//labels
	lbl_divisa_monto = document.getElementById('lbl_divisa_monto');
	lbl_divisa_total = document.getElementById('lbl_divisa_total');
	label_dcv = document.getElementById('lbl_divisa_cv');

	//moneda seleccionanda
	divisa_moneda = document.getElementById('divisa_moneda').value;
	if (divisa_moneda == '0') {
		divisa_monto.value = '';
		divisa_total.value = '';

		lbl_divisa_monto.innerHTML = '.';
		lbl_divisa_total.innerHTML = '.';
		label_dcv.innerHTML = 'Compra/Venta';
		return false;
	}

	//label con la moneda
	aux_moneda = document.getElementById('divisa_moneda');
	simbolo_moneda = aux_moneda.options[aux_moneda.selectedIndex].text;
	lbl_divisa_monto.innerHTML = simbolo_moneda;
	lbl_divisa_total.innerHTML = simbolo_moneda;

	//efectivo y vuelto
	if (efectivo == '' || vuelto == '') {
		alert('debe llenar el efectivo y tener un vuelto');
		divisa_monto.value = '';
		divisa_total.value = '';
		aux_moneda.value = '0';
		return false;
	}

	efectivo_val = parseFloat(efectivo);
	vuelto_val = parseFloat(vuelto);

	if (vuelto_val == 0) {
		alert('debe tener un vuelto para hacer el cambio de divisas');
		divisa_monto.value = '';
		divisa_total.value = '';
		aux_moneda.value = '0';
		return false;
	}

	//compra o venta
	if (vuelto_val < 0) {
		//compra
		label_dcv.innerHTML = 'compra';
	}
	else {
		//venta
		label_dcv.innerHTML = 'venta';
	}

	divisa_monto.readOnly = false;
	//segun la moneda y el vuelto verificamos si es compra y venta
	lista_divisas = document.getElementById('lista_divisas').value;
	lista_div = lista_divisas.split(';;');


	//compra o venta
	for (i = 0; i < lista_div.length; i++) {
		div2 = lista_div[i].split('|');
		if (divisa_moneda == div2[0]) {
			if (vuelto_val < 0) {
				divisa_monto.value = div2[1];
				p_total = Math.abs(vuelto_val) * parseFloat(div2[1]);
				divisa_total.value = redondeo(p_total, 2);
			}
			else {
				divisa_monto.value = div2[2];
				p_total = vuelto_val * parseFloat(div2[2]);
				divisa_total.value = redondeo(p_total, 2);
			}
		}
	}

}

//en caso de hacer cambiar el tipo de cambio
function hacerCambioDivisa() {
	//verificamos que haya seleccionado la moneda
	divisa_monto = document.getElementById('divisa_monto');
	divisa_total = document.getElementById('divisa_total');

	try {
		divisa_moneda = document.getElementById('divisa_moneda');
		if (divisa_moneda.value == '0') {
			alert('debe seleccionar la moneda del tipo de cambio');
			divisa_monto.value = '';
			divisa_total.value = '';
			return false;
		}

		//recalculamos
		vuelto = parseFloat(Trim(document.getElementById('cambio_efectivo').value));
		p_monto = parseFloat(Trim(divisa_monto.value));
		total_poner = Math.abs(vuelto) * p_monto;
		divisa_total.value = redondeo(total_poner, 2);
	}
	catch (e) {
		divisa_monto.value = '';
		divisa_total.value = '';
	}
}

//function reiniciar divisa
function reinicarDivisa() {
	try {
		divisa_moneda = document.getElementById('divisa_moneda');

		//labels
		lbl_divisa_monto = document.getElementById('lbl_divisa_monto');
		lbl_divisa_total = document.getElementById('lbl_divisa_total');
		label_dcv = document.getElementById('lbl_divisa_cv');

		divisa_monto = document.getElementById('divisa_monto');
		divisa_total = document.getElementById('divisa_total');

		divisa_moneda.value = '0';
		lbl_divisa_monto.innerHTML = '.';
		lbl_divisa_total.innerHTML = '.';
		lbl_dcv.innerHTML = 'Compra/Venta';
		divisa_monto.value = '';
		divisa_total.value = '';
		divisa_monto.readOnly = true;
	}
	catch (e) {
		//labels
		lbl_divisa_monto = document.getElementById('lbl_divisa_monto');
		lbl_divisa_total = document.getElementById('lbl_divisa_total');
		lbl_dcv = document.getElementById('lbl_divisa_cv');

		divisa_monto = document.getElementById('divisa_monto');
		divisa_total = document.getElementById('divisa_total');

		lbl_divisa_monto.innerHTML = '.';
		lbl_divisa_total.innerHTML = '.';
		lbl_dcv.innerHTML = 'Compra/Venta';

		divisa_monto.value = '';
		divisa_total.value = '';
		divisa_monto.readOnly = true;
	}
}








/*
function getMoneda1() {
	divisa_id = document.getElementById('divisa').value;

	lista_monedas1 = document.getElementById('divisas_moneda1').value;
	lista_monedas2 = document.getElementById('divisas_moneda2').value;

	etiqueta = document.getElementById('lbl_moneda1');
	etiqueta.innerHTML = '.';

	lbl_total = document.getElementById('lbl_total');
	lbl_total.innerHTML = '.';

	lbl_total2 = document.getElementById('lbl_total2');
	lbl_total2.innerHTML = '.';

	lbl_efectivo = document.getElementById('lbl_efectivo');
	lbl_efectivo.innerHTML = '.';

	lbl_cambio = document.getElementById('lbl_cambio');
	lbl_cambio.innerHTML = '.';

	chk_compra = document.getElementById('chk_compra');
	chk_venta = document.getElementById('chk_venta');

	txt_cambio = document.getElementById('cambio');
	txt_cambio.value = '';
	//efectivo y cambio
	txt_efectivo = document.getElementById('efectivo');
	txt_efectivo.value = '';
	txt_cambio_efectivo = document.getElementById('cambio_efectivo');
	txt_cambio_efectivo.value = '';

	division = lista_monedas1.split(';;');
	division_moneda2 = lista_monedas2.split(';;');

	for (i = 0; i < division.length; i++) {
		div2 = division[i].split('|');
		div_moneda2 = division_moneda2[i].split('|');

		compra_txt = div2[2];
		venta_txt = div2[3];
		compra = parseFloat(div2[2]);
		venta = parseFloat(div2[3]);

		//moneda1
		if (divisa_id == div2[0]) {
			etiqueta.innerHTML = div2[1];

			lbl_total.innerHTML = div_moneda2[1];
			lbl_total2.innerHTML = div_moneda2[1];
			lbl_efectivo.innerHTML = div_moneda2[1];
			lbl_cambio.innerHTML = div_moneda2[1];

			//si es compra
			if (chk_compra.checked) {
				txt_cambio.value = compra_txt;
			}

			//si es venta
			if (chk_venta.checked) {
				txt_cambio.value = venta_txt;
			}
		}
	}// fin for
	calcularTotal();
}

function calcularTotal() {
	obj_monto = document.getElementById('monto');
	obj_cambio = document.getElementById('cambio');
	obj_total = document.getElementById('total');

	//efectivo y cambio
	txt_efectivo = document.getElementById('efectivo');
	txt_efectivo.value = '';
	txt_cambio_efectivo = document.getElementById('cambio_efectivo');
	txt_cambio_efectivo.value = '';

	monto_txt = TrimDerecha(TrimIzquierda(obj_monto.value));
	cambio_txt = TrimDerecha(TrimIzquierda(obj_cambio.value));

	if (monto_txt != '' && cambio_txt != '') {
		try {
			total = parseFloat(monto_txt) * parseFloat(cambio_txt);
			res = redondeo(total, 2);
			obj_total.value = res;

		} catch (error) {
			alert('error');
		}
	}
	else {
		obj_total.value = '';
	}
}*/




//ajax, buscar cliente
$(document).ready(function () {
	$('#btn_buscar_cliente').click(function (evento) {
		//alert('entra...');
		//$("#div_clientes").html('');

		evento.preventDefault();

		obj_ci_dni = document.getElementById('b_ci_dni');
		obj_apellidos = document.getElementById('b_apellidos');
		obj_nombres = document.getElementById('b_nombres');

		ci_dni_txt = TrimDerecha(TrimIzquierda(obj_ci_dni.value));
		apellidos_txt = TrimDerecha(TrimIzquierda(obj_apellidos.value));
		nombres_txt = TrimDerecha(TrimIzquierda(obj_nombres.value));
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

		url_main = document.getElementById('url_main').value;
		ruta_imagen = document.getElementById('ruta_imagen').value;

		datos = {
			'operation_x': 'buscar_cliente',
			'ci_dni': ci_dni_txt,
			'apellidos': apellidos_txt,
			'nombres': nombres_txt,
			'csrfmiddlewaretoken': token
		}

		imagen = '<img src="' + ruta_imagen + '">';
		//alert(imagen);

		$("#div_clientes").html(imagen);
		//$('#div_clientes_loading').show();

		$("#div_clientes").load(url_main, datos, function () {
			//termina de cargar la ventana
			//$('#div_clientes_loading').hide();
			//alert("recibidos los datos por ajax");
		});
	});
});

//minimizar busqueda
function minimizarBusqueda() {
	$("#div_clientes").html('');
}

//$('#div_clientes_loading').hide();

//buscar clientes, loading
// $('#div_clientes_loading')
// 	.hide()  // Hide it initially
// 	.ajaxStart(function () {
// 		$(this).show();
// 	})
// 	.ajaxStop(function () {
// 		$(this).hide();
// 	})
// 	;


//ajax, nuevo cliente
$(document).ready(function () {
	$('#btn_nuevo_cliente').click(function (evento) {
		//ajax default
		evento.preventDefault();

		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

		url_main = document.getElementById('url_main').value;
		ruta_imagen = document.getElementById('ruta_imagen').value;

		datos = {
			'operation_x': 'nuevo_cliente',
			'csrfmiddlewaretoken': token,
		}

		imagen = '<img src="' + ruta_imagen + '">';
		//alert(imagen);

		$("#div_nuevo_cliente").html(imagen);
		$("#div_nuevo_cliente").load(url_main, datos, function () {
			//termina de cargar la ventana
		});
	});
});

//minimizar cliente
function minimizarCliente() {
	$("#div_nuevo_cliente").html('');
}

//ajax, nuevo cliente  guardar
// $(document).ready(function () {
// 	$('#btn_guardar_nc').click(function (evento) {
// 		//ajax default
// 		evento.preventDefault();

// 		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

// 		url_main = document.getElementById('url_main').value;
// 		ruta_imagen = document.getElementById('ruta_imagen').value;

// 		ci_dni = Trim(document.getElementById('n_ci_dni').value);
// 		apellidos = Trim(document.getElementById('n_apellidos').value);
// 		nombres = Trim(document.getElementById('n_nombres').value);

// 		datos = {
// 			'operation_x': 'guardar_nc',
// 			'ci_dni': ci_dni,
// 			'apellidos': apellidos,
// 			'nombres': nombres,
// 			'csrfmiddlewaretoken': token,
// 		}

// 		imagen = '<img src="' + ruta_imagen + '">';
// 		//alert(imagen);

// 		$("#div_nuevo_cliente").html(imagen);
// 		$("#div_nuevo_cliente").load(url_main, datos, function () {
// 			//termina de cargar la ventana
// 			cargarNuevoCliente();
// 		});
// 	});
// });

function guardarNuevoCliente() {
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	url_main = document.getElementById('url_main').value;
	ruta_imagen = document.getElementById('ruta_imagen').value;

	ci_dni = Trim(document.getElementById('n_ci_dni').value);
	apellidos = Trim(document.getElementById('n_apellidos').value);
	nombres = Trim(document.getElementById('n_nombres').value);
	telefonos = Trim(document.getElementById('n_telefonos').value);
	email = Trim(document.getElementById('n_email').value);
	direccion = Trim(document.getElementById('n_direccion').value);

	if (ci_dni == '') {
		alert('debe llenar el CI/DNI');
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
		'ci_dni': ci_dni,
		'apellidos': apellidos,
		'nombres': nombres,
		'telefonos': telefonos,
		'email': email,
		'direccion': direccion,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + ruta_imagen + '">';
	//alert(imagen);

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
			ci_dni_valor = document.getElementById('r_ci_dni').value;
			apellidos_valor = document.getElementById('r_apellidos').value;
			nombres_valor = document.getElementById('r_nombres').value;
			telefonos_valor = document.getElementById('r_telefonos').value;
			email_valor = document.getElementById('r_email').value;

			ci_dni = document.getElementById('ci_dni');
			apellidos = document.getElementById('apellidos');
			nombres = document.getElementById('nombres');
			telefonos = document.getElementById('telefonos');
			email = document.getElementById('email');

			ci_dni.value = ci_dni_valor;
			apellidos.value = apellidos_valor;
			nombres.value = nombres_valor;
			telefonos.value = telefonos_valor;
			email.value = email_valor;

			cliente_detalle = document.getElementById('cliente_detalle');
			poner = apellidos.value + ' ' + nombres.value + ', CI/DNI: ' + ci_dni.value + ', Fonos: ' + telefonos.value;
			cliente_detalle.innerHTML = poner;
		}
	}
	catch (e) {
		//
		alert('error');
	}

}


/*
**seleccion de cliente
*/
function seleccionarCliente(cliente_id) {
	obj_ci_dni = document.getElementById('ci_dni_' + cliente_id);
	obj_apellidos = document.getElementById('apellidos_' + cliente_id);
	obj_nombres = document.getElementById('nombres_' + cliente_id);
	obj_telefonos = document.getElementById('telefonos_' + cliente_id);
	obj_email = document.getElementById('email_' + cliente_id);

	obj2_ci_dni = document.getElementById('ci_dni');
	obj2_apellidos = document.getElementById('apellidos');
	obj2_nombres = document.getElementById('nombres');
	obj2_telefonos = document.getElementById('telefonos');
	obj2_email = document.getElementById('email');

	obj2_ci_dni.value = obj_ci_dni.value;
	obj2_apellidos.value = obj_apellidos.value;
	obj2_nombres.value = obj_nombres.value;
	obj2_telefonos.value = obj_telefonos.value;
	obj2_email.value = obj_email.value;

	cliente_detalle = document.getElementById('cliente_detalle');
	poner = obj2_apellidos.value + ' ' + obj2_nombres.value + ', CI/DNI: ' + obj2_ci_dni.value + ', Fonos: ' + obj2_telefonos.value;
	cliente_detalle.innerHTML = poner;

	div_clientes = document.getElementById('div_clientes');
	div_clientes.innerHTML = '';
}






//destinatario
//destinatario
//ajax, buscar cliente
$(document).ready(function () {
	$('#btn2_buscar_cliente').click(function (evento) {
		evento.preventDefault();

		obj_ci_dni = document.getElementById('b2_ci_dni');
		obj_apellidos = document.getElementById('b2_apellidos');
		obj_nombres = document.getElementById('b2_nombres');

		ci_dni_txt = TrimDerecha(TrimIzquierda(obj_ci_dni.value));
		apellidos_txt = TrimDerecha(TrimIzquierda(obj_apellidos.value));
		nombres_txt = TrimDerecha(TrimIzquierda(obj_nombres.value));
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

		url_main = document.getElementById('url_main').value;
		ruta_imagen = document.getElementById('ruta_imagen').value;

		datos = {
			'operation_x': 'buscar_cliente2',
			'ci_dni': ci_dni_txt,
			'apellidos': apellidos_txt,
			'nombres': nombres_txt,
			'csrfmiddlewaretoken': token
		}

		imagen = '<img src="' + ruta_imagen + '">';

		$("#div2_clientes").html(imagen);

		$("#div2_clientes").load(url_main, datos, function () {
			//termina de cargar la ventana
		});
	});
});

//minimizar busqueda
function minimizarBusqueda2() {
	$("#div2_clientes").html('');
}

//ajax, nuevo cliente
$(document).ready(function () {
	$('#btn2_nuevo_cliente').click(function (evento) {
		//ajax default
		evento.preventDefault();

		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

		url_main = document.getElementById('url_main').value;
		ruta_imagen = document.getElementById('ruta_imagen').value;

		datos = {
			'operation_x': 'nuevo_cliente2',
			'csrfmiddlewaretoken': token,
		}

		imagen = '<img src="' + ruta_imagen + '">';

		$("#div2_nuevo_cliente").html(imagen);
		$("#div2_nuevo_cliente").load(url_main, datos, function () {
			//termina de cargar la ventana
		});
	});
});

//minimizar nuevo cliente
function minimizarCliente2() {
	$("#div2_nuevo_cliente").html('');
}

//guardar nuevo destinatario
function guardarNuevoCliente2() {
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	url_main = document.getElementById('url_main').value;
	ruta_imagen = document.getElementById('ruta_imagen').value;

	ci_dni = Trim(document.getElementById('n_ci_dni2').value);
	apellidos = Trim(document.getElementById('n_apellidos2').value);
	nombres = Trim(document.getElementById('n_nombres2').value);
	telefonos = Trim(document.getElementById('n_telefonos2').value);
	email = Trim(document.getElementById('n_email2').value);
	direccion = Trim(document.getElementById('n_direccion2').value);

	if (ci_dni == '') {
		alert('debe llenar el CI/DNI');
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
		'operation_x': 'guardar_nc2',
		'ci_dni': ci_dni,
		'apellidos': apellidos,
		'nombres': nombres,
		'telefonos': telefonos,
		'email': email,
		'direccion': direccion,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + ruta_imagen + '">';
	//alert(imagen);

	$("#div2_nuevo_cliente").html(imagen);
	$("#div2_nuevo_cliente").load(url_main, datos, function () {
		//termina de cargar la ventana
		cargarNuevoCliente2();
	});
}


//cargamos cuando se adiciona el nuevo cliente
function cargarNuevoCliente2() {
	//resultado de la operacion
	try {
		res = document.getElementById('r_operation2').value;
		if (res == '1') {
			ci_dni_valor = document.getElementById('r_ci_dni2').value;
			apellidos_valor = document.getElementById('r_apellidos2').value;
			nombres_valor = document.getElementById('r_nombres2').value;
			telefonos_valor = document.getElementById('r_telefonos2').value;
			email_valor = document.getElementById('r_email2').value;

			ci_dni = document.getElementById('ci_dni2');
			apellidos = document.getElementById('apellidos2');
			nombres = document.getElementById('nombres2');
			telefonos = document.getElementById('telefonos2');
			email = document.getElementById('email2');

			ci_dni.value = ci_dni_valor;
			apellidos.value = apellidos_valor;
			nombres.value = nombres_valor;
			telefonos.value = telefonos_valor;
			email.value = email_valor;

			cliente_detalle = document.getElementById('cliente2_detalle');
			poner = apellidos.value + ' ' + nombres.value + ', CI/DNI: ' + ci_dni.value + ', Fonos: ' + telefonos.value;
			cliente_detalle.innerHTML = poner;
		}
	}
	catch (e) {
		//
		alert('error');
	}

}

//seleccion destinatario
function seleccionarCliente2(cliente_id) {
	obj_ci_dni = document.getElementById('ci_dni2_' + cliente_id);
	obj_apellidos = document.getElementById('apellidos2_' + cliente_id);
	obj_nombres = document.getElementById('nombres2_' + cliente_id);
	obj_telefonos = document.getElementById('telefonos2_' + cliente_id);
	obj_email = document.getElementById('email2_' + cliente_id);

	obj2_ci_dni = document.getElementById('ci_dni2');
	obj2_apellidos = document.getElementById('apellidos2');
	obj2_nombres = document.getElementById('nombres2');
	obj2_telefonos = document.getElementById('telefonos2');
	obj2_email = document.getElementById('email2');

	obj2_ci_dni.value = obj_ci_dni.value;
	obj2_apellidos.value = obj_apellidos.value;
	obj2_nombres.value = obj_nombres.value;
	obj2_telefonos.value = obj_telefonos.value;
	obj2_email.value = obj_email.value;

	cliente_detalle = document.getElementById('cliente2_detalle');
	poner = obj2_apellidos.value + ' ' + obj2_nombres.value + ', CI/DNI: ' + obj2_ci_dni.value + ', Fonos: ' + obj2_telefonos.value;
	cliente_detalle.innerHTML = poner;

	div_clientes = document.getElementById('div2_clientes');
	div_clientes.innerHTML = '';
}

//asignamos el destinatario sin carnet
function asignarDestinatarioSinCI() {
	ci_dni = document.getElementById('b2_ci_dni');
	apellidos = document.getElementById('b2_apellidos');
	nombres = document.getElementById('b2_nombres');
	telefonos = document.getElementById('b2_telefonos');
	//email = document.getElementById('b2_email');

	ci_dni_valor = Trim(ci_dni.value);
	apellidos_valor = Trim(apellidos.value);
	nombres_valor = Trim(nombres.value);
	telefonos_valor = Trim(telefonos.value);
	//email_valor = Trim(email.value);

	if (ci_dni_valor != '') {
		alert('si el destinatario tiene carnet debe agregarlo al sistema');
		ci_dni.value = '';
		ci_dni.focus();
		return false;
	}

	if (apellidos_valor == '') {
		alert('debe llenar los apellidos');
		apellidos.focus();
		return false;
	}

	if (nombres_valor == '') {
		alert('debe llenar los nombres');
		nombres.focus();
		return false;
	}

	if (telefonos_valor == '') {
		alert('debe llenar los telefonos');
		telefonos.focus();
		return false;
	}

	//asignamos
	ci_dni_p = document.getElementById('ci_dni2');
	apellidos_p = document.getElementById('apellidos2');
	nombres_p = document.getElementById('nombres2');
	telefonos_p = document.getElementById('telefonos2');
	//email_p = document.getElementById('email2');

	ci_dni_p.value = '';
	apellidos_p.value = apellidos_valor;
	nombres_p.value = nombres_valor;
	telefonos_p.value = telefonos_valor;
	//email_p.value = email_valor;

	cliente_detalle = document.getElementById('cliente2_detalle');
	poner = apellidos_valor + ' ' + nombres_valor + ', CI/DNI: , Fonos: ' + telefonos_valor;
	cliente_detalle.innerHTML = poner;

	//alert('asignado');
}










//enviando formuario
//guardando el formulario
function guardarGiro(formulario, add_button, button_cancel) {

	if (verificarGiro()) {
		document.forms[formulario].elements[add_button].disabled = true;
		document.forms[formulario].elements[button_cancel].disabled = true;

		document.forms[formulario].submit();
	}
}

function verificarGiro() {
	//campos
	campo = 'tipo_moneda'
	objeto = document.getElementById(campo);
	if (Trim(objeto.value) == '0') {
		alert('Debe seleccionar la moneda');
		objeto.focus();
		return false;
	}

	campo = 'monto'
	objeto = document.getElementById(campo);
	if (Trim(objeto.value) == '') {
		alert('Debe llenar el monto');
		objeto.focus();
		return false;
	}

	campo = 'comision'
	objeto = document.getElementById(campo);
	if (Trim(objeto.value) == '0' || Trim(objeto.value) == '') {
		alert('Debe llenar la comision');
		objeto.focus();
		return false;
	}

	campo = 'total'
	objeto = document.getElementById(campo);
	if (Trim(objeto.value) == '0') {
		alert('Debe tener un total');
		objeto.focus();
		return false;
	}

	campo = 'divisa_moneda'
	try {
		objeto = document.getElementById(campo);
		if (Trim(objeto.value) != '0') {
			//verificamos que llene el cambio y total
			divisa_monto = document.getElementById('divisa_monto');
			divisa_total = document.getElementById('divisa_total');

			if (Trim(divisa_monto.value) == '') {
				alert('el cambio de divisa debe tener un valor');
				divisa_monto.focus();
				return false;
			}
			if (Trim(divisa_total.value) == '') {
				alert('el cambio de divisa debe tener un total');
				divisa_total.focus();
				return false;
			}
		}
	}
	catch (e) {
		//no hacemos nada
	}

	//cliente
	campo = 'ci_dni'
	objeto = document.getElementById(campo);
	if (Trim(objeto.value) == '0' || Trim(objeto.value) == '') {
		alert('Debe seleccionar un cliente valido');
		return false;
	}

	//apellidos nombres
	campo = 'apellidos'
	campo2 = 'nombres'
	objeto = document.getElementById(campo);
	objeto2 = document.getElementById(campo2);
	if (Trim(objeto.value) == '' || Trim(objeto2.value) == '') {
		alert('Debe seleccionar un cliente valido');
		return false;
	}

	//destinatario apellidos nombres
	campo = 'apellidos2'
	campo2 = 'nombres2'
	objeto = document.getElementById(campo);
	objeto2 = document.getElementById(campo2);
	if (Trim(objeto.value) == '' || Trim(objeto2.value) == '') {
		alert('Debe seleccionar un destinatario valido');
		return false;
	}

	//ciudad destino
	campo = 'ciudad_destino'
	objeto = document.getElementById(campo);
	if (Trim(objeto.value) == '0' || Trim(objeto.value) == '') {
		alert('Debe seleccionar una ciudad de destino');
		return false;
	}

	if (confirm('esta seguro de guardar el giro')) {
		return true;
	}
	else {
		return false;
	}
}

function confirmarAnular() {
	motivo_anula = Trim(document.getElementById('motivo_anula').value);
	if (motivo_anula == '') {
		alert('debe llenar el motivo');
		return false;
	}
	if (confirm('Esta seguro de querer anular este elemento?')) {
		document.forms['formulario'].elements['add_button'].disabled = true;
		document.forms['formulario'].elements['button_cancel'].disabled = true;
		document.forms['formulario'].submit();
		return true;
	}
	//return true;
}




//guardando el formulario
function guardarGiroRecogo(formulario, add_button, button_cancel) {

	if (verificarGiroRecogo()) {
		document.forms[formulario].elements[add_button].disabled = true;
		document.forms[formulario].elements[button_cancel].disabled = true;

		document.forms[formulario].submit();
	}
}

function verificarGiroRecogo() {

	campo = 'divisa_moneda'
	try {
		objeto = document.getElementById(campo);
		if (Trim(objeto.value) != '0') {
			//verificamos que llene el cambio y total
			divisa_monto = document.getElementById('divisa_monto');
			divisa_total = document.getElementById('divisa_total');

			if (Trim(divisa_monto.value) == '') {
				alert('el cambio de divisa debe tener un valor');
				divisa_monto.focus();
				return false;
			}
			if (Trim(divisa_total.value) == '') {
				alert('el cambio de divisa debe tener un total');
				divisa_total.focus();
				return false;
			}
		}
	}
	catch (e) {
		//no hacemos nada
	}

	if (confirm('esta seguro de cobrar el giro')) {
		return true;
	}
	else {
		return false;
	}
}
