/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

// function objectAjaxBC() {
// 	var xmlhttp = false;
// 	try {
// 		xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
// 	} catch (e) {
// 		try {
// 			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
// 		} catch (E) {
// 			xmlhttp = false;
// 		}
// 	}

// 	if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
// 		xmlhttp = new XMLHttpRequest();
// 	}
// 	return xmlhttp;
// }


//control especifico del modulo
function controlModulo() {

	return true;
}

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
}

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
}

// function buscarCliente(url, img_loading) {
// 	obj_ci_dni = document.getElementById('b_ci_dni');
// 	obj_apellidos = document.getElementById('b_apellidos');
// 	obj_nombres = document.getElementById('b_nombres');
// 	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

// 	ci_dni_txt = TrimDerecha(TrimIzquierda(obj_ci_dni.value));
// 	apellidos_txt = TrimDerecha(TrimIzquierda(obj_apellidos.value));
// 	nombres_txt = TrimDerecha(TrimIzquierda(obj_nombres.value));

// 	p_window = url;
// 	divResult = document.getElementById('div_clientes');
// 	divResult.innerHTML = '<img src="' + img_loading + '">';
// 	ajax = objectAjaxBC();

// 	ajax.open("POST", p_window, true);
// 	ajax.onreadystatechange = function () {
// 		if (ajax.readyState == 4) {
// 			divResult.innerHTML = ajax.responseText;
// 		}
// 	}

// 	ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
// 	ajax.send("&operation_x=buscar_cliente&ci_dni=" + ci_dni_txt + "&apellidos=" + apellidos_txt + "&nombres=" + nombres_txt + '&csrfmiddlewaretoken=' + token);
// 	ajax.done(function () {
// 		alert('abc');
// 	});
// }


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

//minimizar nuevo cliente
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

			ci_dni = document.getElementById('ci_dni');
			apellidos = document.getElementById('apellidos');
			nombres = document.getElementById('nombres');

			ci_dni.value = ci_dni_valor;
			apellidos.value = apellidos_valor;
			nombres.value = nombres_valor;

			cliente_detalle = document.getElementById('cliente_detalle');
			poner = apellidos.value + ' ' + nombres.value + ', CI/DNI: ' + ci_dni.value;
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

	obj2_ci_dni = document.getElementById('ci_dni');
	obj2_apellidos = document.getElementById('apellidos');
	obj2_nombres = document.getElementById('nombres');

	obj2_ci_dni.value = obj_ci_dni.value;
	obj2_apellidos.value = obj_apellidos.value;
	obj2_nombres.value = obj_nombres.value;

	cliente_detalle = document.getElementById('cliente_detalle');
	poner = obj2_apellidos.value + ' ' + obj2_nombres.value + ', CI/DNI: ' + obj2_ci_dni.value;
	cliente_detalle.innerHTML = poner;

	div_clientes = document.getElementById('div_clientes');
	div_clientes.innerHTML = '';
}

//guardando el formulario
function guardarDivisa(formulario, add_button, button_cancel) {

	if (verificarDivisa()) {
		document.forms[formulario].elements[add_button].disabled = true;
		document.forms[formulario].elements[button_cancel].disabled = true;

		document.forms[formulario].submit();
	}
}

function verificarDivisa() {
	divisa = document.getElementById('divisa').value;
	monto = Trim(document.getElementById('monto').value);
	cambio = Trim(document.getElementById('cambio').value);

	if (divisa == '') {
		alert('debe seleccionar la divisa');
		return false;
	}

	if (monto == '') {
		alert('debe llenar el monto');
		return false;
	}

	if (cambio == '') {
		alert('debe llenar el tipo de cambio');
		return false;
	}

	return true;
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