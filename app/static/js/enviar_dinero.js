/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

//$('#div_cuenta_bancaria').fadeOut('slow');

//remitente
var tiempo_ini = 0;
var tiempo_fin = 0;
var primera_vez = 0;
var timeDiff = 0;
var seBusco = 0;

//destinatario
var tiempo_ini2 = 0;
var tiempo_fin2 = 0;
var primera_vez2 = 0;
var timeDiff2 = 0;
var seBusco2 = 0;

setInterval('buscarCI()', 1000);
setInterval('buscarCI2()', 1000);

//remitente
function empiezaEscribir() {
	if (primera_vez == 0) {
		primera_vez = 1;
		tiempo_ini = new Date();
		tiempo_fin = new Date();
	}
	else {
		//variable que indicar si mandar el ajax para buscar
		seBusco = 0;

		tiempo = new Date();
		// time difference in ms
		timeDiff = tiempo - tiempo_fin;

		tiempo_fin = tiempo;

		// strip the ms
		timeDiff /= 1000;

		// segundos
		// var seconds = Math.round(timeDiff % 60);
		// ci_origen = Trim(document.getElementById('ci').value);
		// if (ci_origen.length > 5) {
		// 	if (seconds > 1) {
		// 		alert(timeDiff);
		// 		/*setTimeout(function () {
		// 			$('#message').fadeOut('slow');
		// 		}, 3000);*/
		// 	}
		// }
	}
}

//destinatario
function empiezaEscribir2() {
	if (primera_vez2 == 0) {
		primera_vez2 = 1;
		tiempo_ini2 = new Date();
		tiempo_fin2 = new Date();
	}
	else {
		seBusco2 = 0;

		tiempo2 = new Date();
		// time difference in ms
		timeDiff2 = tiempo2 - tiempo_fin2;

		tiempo_fin2 = tiempo2;

		// strip the ms
		timeDiff2 /= 1000;
	}
}

//remitente
function buscarCI() {
	ci_origen = Trim(document.getElementById('ci').value);
	if (ci_origen.length > 5) {
		tiempo = new Date();
		timeDiff = tiempo - tiempo_fin;
		tiempo_fin = tiempo;
		timeDiff /= 1000;

		imagen = '<img src="/static/img/pass/loading2.gif">';
		url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'ci': ci_origen,
			'operation': 'buscar_ci',
			'csrfmiddlewaretoken': token,
		}
		//alert(timeDiff>1.5);
		if (timeDiff > 0.7 && seBusco == 0) {
			seBusco = 1;
			//alert('termino escribir');

			$('#div_tabla_datos').fadeIn('slow');

			$("#img_load").html(imagen);
			$("#img_load").load(url_main, datos, function () {
				//termina de cargar la ventana
				resultadoBusqedaCI();
			});
		}
	}
}

//remitente
function resultadoBusqedaCI() {
	try {
		r_apellidos = document.getElementById('r_apellidos').value;
		r_nombres = document.getElementById('r_nombres').value;
		r_telefonos = document.getElementById('r_telefonos').value;
		r_email = document.getElementById('r_email').value;

		apellidos = document.getElementById('apellidos');
		nombres = document.getElementById('nombres');
		telefonos = document.getElementById('telefonos');
		email = document.getElementById('email');

		apellidos.value = r_apellidos;
		nombres.value = r_nombres;
		telefonos.value = r_telefonos;
		email.value = r_email;
		//alert('busqueda terminada');
	}
	catch (e) {
		alert('error al buscar sus datos');
	}
}


//destinatario
function buscarCI2() {
	ci_origen2 = Trim(document.getElementById('ci2').value);
	if (ci_origen2.length > 5) {
		tiempo2 = new Date();
		timeDiff2 = tiempo2 - tiempo_fin2;
		tiempo_fin2 = tiempo2;
		timeDiff2 /= 1000;

		imagen = '<img src="/static/img/pass/loading2.gif">';
		url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'ci2': ci_origen2,
			'operation': 'buscar_ci2',
			'csrfmiddlewaretoken': token,
		}
		//alert(timeDiff>1.5);
		if (timeDiff2 > 0.7 && seBusco2 == 0) {
			seBusco2 = 1;

			//$('#div_tabla_datos').fadeIn('slow');

			$("#img_load2").html(imagen);
			$("#img_load2").load(url_main, datos, function () {
				//termina de cargar la ventana
				resultadoBusqedaCI2();
			});
		}
	}
}

//destinatario
function resultadoBusqedaCI2() {
	try {
		r_apellidos = document.getElementById('r_apellidos2').value;
		r_nombres = document.getElementById('r_nombres2').value;
		r_telefonos = document.getElementById('r_telefonos2').value;
		r_email = document.getElementById('r_email2').value;

		apellidos = document.getElementById('apellidos2');
		nombres = document.getElementById('nombres2');
		telefonos = document.getElementById('telefonos2');
		email = document.getElementById('email2');

		apellidos.value = r_apellidos;
		nombres.value = r_nombres;
		telefonos.value = r_telefonos;
		email.value = r_email;
		//alert('busqueda terminada');
	}
	catch (e) {
		alert('error al buscar sus datos');
	}
}








//verificamos que seleccione la moneda para el monto
function verificarMoneda() {
	//moneda
	tipo_moneda = document.getElementById('tipo_moneda').value;
	if (tipo_moneda == '0') {
		monto_a = document.getElementById('monto');
		monto_a.value = '';
		alert('Primero debe selecionar una moneda');
		return false;
	}

	//valor del monto
	monto = document.getElementById('monto');
	comision = document.getElementById('comision');
	total = document.getElementById('total');

	if (Trim(monto.value) == '') {
		comision.value = '';
		total.value = '';
		return false;
	}

	lista_monedas = document.getElementById('lista_monedas').value;
	lista_div = lista_monedas.split('||');

	for (i = 0; i < lista_div.length; i++) {
		//dividimos por tipo de moneda
		lista_div2 = lista_div[i].split(':');

		if (lista_div2[0] == tipo_moneda) {
			//moneda correcta
			lista_div3 = lista_div2[1].split(';;');
			//lista de comisiones por rangos
			menor = Array();
			mayor = Array();
			fijo = Array();
			porcentaje = Array();
			tipo_comision = 'fijo';
			comision_poner = '';
			total_poner = '';

			for (j = 0; j < lista_div3.length; j++) {
				div2 = lista_div3[j].split('|');

				menor[j] = div2[0];
				mayor[j] = div2[1];
				fijo[j] = div2[2];
				porcentaje[j] = div2[3];
			}
			cant_comision = j;

			//recuperamos la comision
			monto_valor = parseFloat(Trim(monto.value));
			for (k = 0; k < cant_comision; k++) {
				if (monto_valor >= parseFloat(menor[k])) {
					if (tipo_comision == 'fijo') {
						comision_poner = fijo[k];
						total_poner = redondeo((monto_valor + parseFloat(fijo[k])), 2);
					}
					else {
						comision_poner = porcentaje[k];
						p_porcentaje = (parseFloat(porcentaje[k]) / 100) * monto_valor;

						total_poner = redondeo((monto_valor + p_porcentaje), 2);
					}
				}
			}

			//colocamos la comision
			comision.value = comision_poner;
			total.value = total_poner;
		}
	}
}

//cambiamos el tipo de moneda
function cambiarTipoMoneda() {
	tipo_moneda = document.getElementById('tipo_moneda');
	label_moneda = document.getElementById('label_moneda');
	label_total = document.getElementById('label_total');
	label_comision = document.getElementById('label_comision');

	txt_monto = document.getElementById('monto');
	txt_comision = document.getElementById('comision');
	txt_total = document.getElementById('total');

	if (tipo_moneda.value == '0') {
		label_moneda.innerHTML = '.';
		label_total.innerHTML = '.';
		label_comision.innerHTML = '.';
	}
	else {
		simbolo_moneda = tipo_moneda.options[tipo_moneda.selectedIndex].text;
		label_moneda.innerHTML = simbolo_moneda;
		label_total.innerHTML = simbolo_moneda;
		label_comision.innerHTML = simbolo_moneda;
	}
	txt_monto.value = '';
	txt_comision.value = '';
	txt_total.value = '';
}


//registramos el pregiro
function registrarPreGiro() {

	//remitente
	//ciudad origen
	campo = 'ciudad_origen';
	ciudad_origen = document.getElementById(campo);
	if (Trim(ciudad_origen.value) == '0') {
		alert('debe seleccionar la ciudad de origen');
		ciudad_origen.focus();
		return false;
	}

	//ci
	campo = 'ci';
	ci = document.getElementById(campo);
	if (Trim(ci.value) == '') {
		alert('debe llenar su CI');
		ci.focus();
		return false;
	}

	//apellidos
	campo = 'apellidos';
	apellidos = document.getElementById(campo);
	if (Trim(apellidos.value) == '') {
		alert('debe llenar sus apellidos');
		apellidos.focus();
		return false;
	}

	//nombres
	campo = 'nombres';
	nombres = document.getElementById(campo);
	if (Trim(nombres.value) == '') {
		alert('debe llenar su nombre');
		nombres.focus();
		return false;
	}

	//telefonos
	campo = 'telefonos';
	telefonos = document.getElementById(campo);
	if (Trim(telefonos.value) == '') {
		alert('debe llenar sus telefonos');
		telefonos.focus();
		return false;
	}

	//tipo de moneda
	campo = 'tipo_moneda';
	tipo_moneda = document.getElementById(campo);
	if (Trim(tipo_moneda.value) == '0') {
		alert('debe seleccionar la moneda');
		tipo_moneda.focus();
		return false;
	}

	//monto
	campo = 'monto';
	monto = document.getElementById(campo);
	if (Trim(monto.value) == '') {
		alert('debe llenar el monto');
		monto.focus();
		return false;
	}

	//ciudad
	campo = 'ciudad';
	ciudad = document.getElementById(campo);
	if (Trim(ciudad.value) == '0') {
		alert('debe seleccionar la ciudad de destino');
		ciudad.focus();
		return false;
	}

	//apellidos2
	campo = 'apellidos2';
	apellidos2 = document.getElementById(campo);
	if (Trim(apellidos2.value) == '') {
		alert('debe llenar los apellidos del destinatario');
		apellidos2.focus();
		return false;
	}

	//nombres
	campo = 'nombres2';
	nombres2 = document.getElementById(campo);
	if (Trim(nombres2.value) == '') {
		alert('debe llenar el nombre del destinatario');
		nombres2.focus();
		return false;
	}

	//telefonos
	campo = 'telefonos2';
	telefonos2 = document.getElementById(campo);
	if (Trim(telefonos2.value) == '') {
		alert('debe llenar los telefonos del destinatario');
		telefonos2.focus();
		return false;
	}

	//email
	email = document.getElementById('email');
	email2 = document.getElementById('email2');
	ci2 = document.getElementById('ci2');
	tipo_comision = document.getElementById('tipo_comision');
	comision = document.getElementById('comision');
	total = document.getElementById('total');

	// mandamos
	imagen = '<img src="/static/img/pass/loading.gif">';
	url_main = '/enviardinero/';
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	datos = {
		'ci': Trim(ci.value),
		'nombres': Trim(nombres.value),
		'apellidos': Trim(apellidos.value),
		'telefonos': Trim(telefonos.value),
		'email': Trim(email.value),
		'tipo_moneda': Trim(tipo_moneda.value),
		'monto': Trim(monto.value),
		'ciudad': Trim(ciudad.value),
		'ci2': Trim(ci2.value),
		'apellidos2': Trim(apellidos2.value),
		'nombres2': Trim(nombres2.value),
		'telefonos2': Trim(telefonos2.value),
		'email2': Trim(email2.value),
		'ciudad_origen': Trim(ciudad_origen.value),
		'tipo_comision': Trim(tipo_comision.value),
		'comision': Trim(comision.value),
		'total': Trim(total.value),

		'operation': 'add_pregiro',
		'csrfmiddlewaretoken': token,
	}

	$("#div_resultado_pregiro").html(imagen);
	$("#div_resultado_pregiro").load(url_main, datos, function () {
		//termina de cargar la ventana
		resultadoPregiro();
	});

	return true;
}

function resultadoPregiro() {
	r_pregiro = document.getElementById('r_pregiro').value;
	if (r_pregiro == '1') {
		//error
	}
	else {
		reiniciarPregiro();
	}
}

function reiniciarPregiro() {
	//remitente
	//ciudad origen
	campo = 'ciudad_origen';
	ciudad_origen = document.getElementById(campo);
	ciudad_origen.value = '0';

	//ci
	campo = 'ci';
	ci = document.getElementById(campo);
	ci.value = '';

	//apellidos
	campo = 'apellidos';
	apellidos = document.getElementById(campo);
	apellidos.value = '';

	//nombres
	campo = 'nombres';
	nombres = document.getElementById(campo);
	nombres.value = '';

	//telefonos
	campo = 'telefonos';
	telefonos = document.getElementById(campo);
	telefonos.value = '';

	//tipo de moneda
	campo = 'tipo_moneda';
	tipo_moneda = document.getElementById(campo);
	tipo_moneda.value = '0';

	//monto
	campo = 'monto';
	monto = document.getElementById(campo);
	monto.value = '';

	//ciudad
	campo = 'ciudad';
	ciudad = document.getElementById(campo);
	ciudad.value = '0';

	//apellidos2
	campo = 'apellidos2';
	apellidos2 = document.getElementById(campo);
	apellidos2.value = '';

	//nombres
	campo = 'nombres2';
	nombres2 = document.getElementById(campo);
	nombres2.value = '';

	//telefonos
	campo = 'telefonos2';
	telefonos2 = document.getElementById(campo);
	telefonos2.value = '';

	//email
	email = document.getElementById('email');
	email.value = '';
	email2 = document.getElementById('email2');
	email2.value = '';
	ci2 = document.getElementById('ci2');
	ci2.value = '';
	comision = document.getElementById('comision');
	comision.value = '';
	total = document.getElementById('total');
	total.value = '';

	return true;
}