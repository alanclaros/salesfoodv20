/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: acc.claros@gmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

/** para ocultar los mensajes despues de 3 segundos */
/*setTimeout(function () {
	try {
		$('#message').fadeOut('slow');
	}
	catch (e) {

	}
}, 5000);*/

// function hideMessage(div_message) {
// 	try {
// 		$('#' + div_message).stop(true).fadeOut('slow');
// 	}
// 	catch (e) {

// 	}
// }

function module_pagination(page) {
	token_pagination = document.forms['form_page'].elements['csrfmiddlewaretoken'].value;

	datos_pagination = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'csrfmiddlewaretoken': token_pagination,
	}
	name_var_page = document.forms['form_page'].elements['name_var_page'].value;

	datos_pagination[name_var_page] = page;

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_pagination, function () {
		//termina de cargar la ventana
	});
}

cont_hide = 0;
function hideNotifications() {
	for (im = 0; im <= 20; im++) {
		try {
			if (im == 0) {
				existe_message = document.getElementById('message');
				//alert(existe_message);
			}
			else {
				existe_message = document.getElementById('message' + im);
				//alert(existe_message);
			}

			if (existe_message != null) {
				if (cont_hide == 0) {
					cont_hide = 1;
				}
				else {
					cont_hide = 0;
					if (im == 0) {
						//$('#message').fadeOut('slow');
						$('#message').stop(true);
						//setTimeout(hideMessage('message'), 5000);
						$('#message').fadeOut(5000);
						//console.log('empezando el hide message 0');
					}
					else {
						$('#message' + im).stop(true);
						$('#message' + im).fadeOut(5000);
						//setTimeout(hideMessage('message' + im), 5000);
						//console.log('empezando el hide message ' + im);
					}
				}
			}
		}
		catch (e) {

		}
	}
}

setInterval('hideNotifications()', 3000);

//notificaciones
setInterval('checkNotifications()', 45000); //45 segundos

try {
	url_empresa = document.getElementById('url_empresa').value;
}
catch (e) {
	url_empresa = '';
}

//settings
ruta_imagen_modulo = url_empresa + '/static/img/pass/modulo_load7.gif';
imagen_modulo = '<br><br><br><img src="' + ruta_imagen_modulo + '">';

//block content
div_modulo = $("#div_block_content");

function checkNotifications() {
	//$('#div_notifications').fadeIn('slow');
	//$('#div_notifications').fadeOut('slow');
	try {
		autenticado = document.forms['form_notificaciones'].elements['autenticado'].value;
	}
	catch (e) {
		autenticado = 'no';
	}

	if (autenticado == 'si') {
		try {
			imagen = '<img src="' + url_empresa + '/static/img/pass/loading2.gif">';
			url_main = url_empresa + '/notificacionespagina/';
			token = document.forms['form_notificaciones'].elements['csrfmiddlewaretoken'].value;
			datos = {
				'check': 'ok',
				'csrfmiddlewaretoken': token,
			}

			//verificamos
			$('#div_notifications').fadeIn('slow');
			//$("#div_notifications").html(imagen);
			$("#div_notifications").load(url_main, datos, function () {
				//termina de cargar la ventana
				resultadoNotificacion();
			});
		}
		catch (e) {
			//error
		}
	}
}

//resultado de la notificacion
function resultadoNotificacion() {
	return true;
}

function openModule(module_id) {
	//alert(module_id);

	module_aux = document.getElementById('module_ref_1000');
	module_aux.className = 'nav-link back_menu';

	//desmarcamos todos los posibles
	for (mi = 1; mi <= 50; mi++) {
		try {
			module_aux = document.getElementById('module_ref_' + mi);
			module_aux.className = 'nav-link back_menu';
		}
		catch (e) {

		}
	}

	module_ref = document.getElementById('module_ref_' + module_id);
	module_ref.className = 'nav-link back_menu_item_select active';

	token_module = document.forms['form_notificaciones'].elements['csrfmiddlewaretoken'].value;

	datos_modulo = {
		'module_x': module_id,
		'csrfmiddlewaretoken': token_module,
	}

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_modulo, function () {
		//termina de cargar la ventana
	});

	div_body_class = document.getElementById('div_body').className;
	pos = div_body_class.indexOf('open');
	if (pos > -1) {
		btn_show_menu = document.getElementById('btn_show_menu');
		btn_show_menu.click();
	}

}

//send order forms
function sendOrder(order, type, field_order, field_type) {
	token_search = document.forms['form_order'].elements['csrfmiddlewaretoken'].value;

	datos_search = {
		'csrfmiddlewaretoken': token_search,

		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'module_x2': document.forms['form_operation'].elements['module_x2'].value,
		'module_x3': document.forms['form_operation'].elements['module_x3'].value,

		'operation_x': document.forms['form_operation'].elements['operation_x'].value,
		'operation_x2': document.forms['form_operation'].elements['operation_x2'].value,
		'operation_x3': document.forms['form_operation'].elements['operation_x3'].value,

		'id': document.forms['form_operation'].elements['id'].value,
		'id2': document.forms['form_operation'].elements['id2'].value,
		'id3': document.forms['form_operation'].elements['id3'].value,
	}
	datos_search[field_order] = order;
	datos_search[field_type] = type;

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_search, function () {
		//termina de cargar la ventana
	});
}

//boton de adicion
function sendOperation(operation = '', operation2 = '', operation3 = '', id = '', id2 = '', id3 = '') {
	token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

	datos_operation = {
		'csrfmiddlewaretoken': token_operation,

		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'module_x2': document.forms['form_operation'].elements['module_x2'].value,
		'module_x3': document.forms['form_operation'].elements['module_x3'].value,

		'operation_x': operation,
		'operation_x2': operation2,
		'operation_x3': operation3,

		'id': id,
		'id2': id2,
		'id3': id3,
	}

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_operation, function () {
		//termina de cargar la ventana
	});
}

function backWindow() {
	token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

	datos_operation = {
		'csrfmiddlewaretoken': token_operation,

		'module_x': document.forms['form_operation'].elements['module_x'].value,
	}

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_operation, function () {
		//termina de cargar la ventana
	});
}

function backWindow2() {
	token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

	datos_operation = {
		'csrfmiddlewaretoken': token_operation,

		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'module_x2': document.forms['form_operation'].elements['module_x2'].value,

		'operation_x': document.forms['form_operation'].elements['operation_x'].value,

		'id': document.forms['form_operation'].elements['id'].value,
	}

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_operation, function () {
		//termina de cargar la ventana
	});
}

function backWindow3() {
	token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

	datos_operation = {
		'csrfmiddlewaretoken': token_operation,

		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'module_x2': document.forms['form_operation'].elements['module_x2'].value,
		'module_x3': document.forms['form_operation'].elements['module_x3'].value,

		'operation_x': document.forms['form_operation'].elements['operation_x'].value,
		'operation_x2': document.forms['form_operation'].elements['operation_x2'].value,

		'id': document.forms['form_operation'].elements['id'].value,
		'id2': document.forms['form_operation'].elements['id2'].value,
	}

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_operation, function () {
		//termina de cargar la ventana
	});
}

//cambiando el valor del checkbox
function cambiarCheck(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}
	if (campo.checked) {
		campo.value = '1';
	}
	else {
		campo.value = '0';
	}
}

function validarNumero(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}
	//alert(campo);
	var tam = campo.value.length;
	var valor = "";
	var letra = "";
	var nuevo_valor = "";
	for (i = 0; i < tam; i++) {
		valor = campo.value.substring(i, (i + 1));
		letra = valor.toUpperCase();
		if (letra == "1" || letra == "2" || letra == "3" || letra == "4" || letra == "5" || letra == "6" || letra == "7" || letra == "8" || letra == "9" || letra == "0") {
			nuevo_valor = nuevo_valor + letra;
		}
	}
	campo.value = nuevo_valor;
}

function validarNumeroPunto(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}

	var tam = campo.value.length;
	var valor = "";
	var letra = "";
	var nuevo_valor = "";
	for (i = 0; i < tam; i++) {
		valor = campo.value.substring(i, (i + 1));
		letra = valor.toUpperCase();
		if (letra == "1" || letra == "2" || letra == "3" || letra == "4" || letra == "5" || letra == "6" || letra == "7" || letra == "8" || letra == "9" || letra == "0" || letra == ".") {
			nuevo_valor = nuevo_valor + letra;
		}
	}
	campo.value = nuevo_valor;
}

function validarNumeroPuntoNegativo(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}

	var tam = campo.value.length;
	var valor = "";
	var letra = "";
	var nuevo_valor = "";
	for (i = 0; i < tam; i++) {
		valor = campo.value.substring(i, (i + 1));
		letra = valor.toUpperCase();
		if (letra == "1" || letra == "2" || letra == "3" || letra == "4" || letra == "5" || letra == "6" || letra == "7" || letra == "8" || letra == "9" || letra == "0" || letra == "." || letra == '-') {
			nuevo_valor = nuevo_valor + letra;
		}
	}
	campo.value = nuevo_valor;
}

function verifyForm() {
	//variables a controlar
	controlForm = TrimDerecha(TrimIzquierda(document.forms["formulario"].elements["control_form"].value));
	tam = controlForm.length;

	if (tam > 0) {
		var division = controlForm.split(";");
		tamC = division.length;

		for (i = 0; i < tamC; i++) {
			auxS = division[i];
			divisionC = auxS.split("|");
			tipoDato = divisionC[0];
			tamDato = parseInt(divisionC[1]);
			controlarDato = divisionC[2];
			nombreCampo = divisionC[3];

			campoForm = document.getElementById(nombreCampo);
			valor = TrimDerecha(TrimIzquierda(campoForm.value));
			tamValor = valor.length;

			if (tipoDato == "txt" && controlarDato == "S") {
				if (tamValor == 0) {
					txtValid(nombreCampo);
					alert('Debe llenar este campo');
					campoForm.focus();
					return false;
				}
				if (tamValor < tamDato) {
					alert('Este campo debe tener al menos ' + tamDato + ' letras');
					campoForm.focus();
					return false;
				}
			}

			if (tipoDato == "cbo" && controlarDato == "S") {
				if (valor == tamDato) {
					alert('Debe seleccionar un valor');
					campoForm.focus();
					return false;
				}
			}
		} //fin for
	} // fin if tam>0

	module_x = parseInt(document.forms['form_operation'].elements['module_x'].value);
	if (module_x == 9) {
		return controlModuloUsuario();
	}

	return controlModulo();
}

function TrimDerecha(str) {
	var resultStr = "";
	var i = 0;

	// Return immediately if an invalid value was passed in
	if (str + "" == "undefined" || str == null)
		return null;

	// Make sure the argument is a string
	str += "";

	if (str.length == 0)
		resultStr = "";
	else {
		// Loop through string starting at the end as long as there
		// are spaces.
		i = str.length - 1;
		while ((i >= 0) && (str.charAt(i) == " "))
			i--;

		// When the loop is done, we're sitting at the last non-space char,
		// so return that char plus all previous chars of the string.
		resultStr = str.substring(0, i + 1);
	}

	return resultStr;
}

function TrimIzquierda(str) {
	var resultStr = "";
	var i = len = 0;

	// Return immediately if an invalid value was passed in
	if (str + "" == "undefined" || str == null)
		return null;

	// Make sure the argument is a string
	str += "";

	if (str.length == 0)
		resultStr = "";
	else {
		// Loop through string starting at the beginning as long as there
		// are spaces.
		//	  	len = str.length - 1;
		len = str.length;

		while ((i <= len) && (str.charAt(i) == " "))
			i++;

		// When the loop is done, we're sitting at the first non-space char,
		// so return that char plus the remaining chars of the string.
		resultStr = str.substring(i, len);
	}

	return resultStr;
}

function Trim(str) {
	resultado = TrimDerecha(TrimIzquierda(str));

	return resultado;
}


/**impresion, dialogo modal */
function closeModalPrint() {
	modal = document.getElementById("printModal");
	modal.style.display = "none";
}

function openModalPrint() {
	modal = document.getElementById("printModal");
	modal.style.display = "block";
}

// Get the modal
var modal = document.getElementById("printModal");

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}

/**labels para cambiar el texto: apellidos a ape:, para version movil */
/*window.addEventListener('resize', cambiarTexto);

var arrayLabels = Array();
var arrayLabelsPeque = Array();
cantLabels = 100;

function cargarLabels() {
	for (k = 0; k <= cantLabels; k++) {
		aux = document.getElementById('label' + k);
		nombre = 'label' + k + '_c';
		hidd = document.getElementById(nombre);
		if (aux != null) {
			arrayLabels[k] = aux.innerHTML;
			arrayLabelsPeque[k] = hidd.value;
		}
	}
}


function cambiarTexto() {
	var width = document.documentElement.clientWidth;
	if (width <= 768) {
		for (i = 0; i <= cantLabels; i++) {
			aux = document.getElementById('label' + i);
			if (aux != null) {
				aux.innerHTML = arrayLabelsPeque[i];
			}
		}
	} else {
		for (i = 0; i <= cantLabels; i++) {
			aux = document.getElementById('label' + i);
			if (aux != null) {
				aux.innerHTML = arrayLabels[i];
			}
		}
	}
}*/

function redondeo(numero, decimales) {
	var flotante = parseFloat(numero);
	var resultado = Math.round(flotante * Math.pow(10, decimales)) / Math.pow(10, decimales);
	resultado2 = resultado;
	var aux_c = "" + resultado;
	if (aux_c.indexOf('.') != -1) {
		//si hay decimales
		var division = aux_c.split(".");
		ta = division[1].length;
		if (ta == 1) {
			resultado2 = resultado + "0";
		}
	}
	else {
		//sin decimales
		resultado2 = resultado + ".00";
	}

	return resultado2;
}

/**valida campos de texto
 * mostrando rojo, si no lleno datos
 */
function txtValid(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}
	clase = campo.className;
	clase = clase.replace('is-invalid', '');
	if (TrimDerecha(TrimIzquierda(campo.value)) == "" || campo.value == "0") {
		clase = clase + ' is-invalid';
	}
	clase = clase.replace('  ', ' ');
	campo.className = clase;
}

//boton up
function cambiarUp(nombre) {
	boton = document.getElementById(nombre);
	//boton.src = '/static/img/pass/r_asc_press.gif';
	boton.src = url_empresa + '/static/img/pass/up1_press.jpg';
}
function volverUp(nombre) {
	boton = document.getElementById(nombre);
	boton.src = url_empresa + '/static/img/pass/up1.jpg';
}

//boton down
function cambiarDown(nombre) {
	boton = document.getElementById(nombre);
	boton.src = url_empresa + '/static/img/pass/down1_press.jpg';
}
function volverDown(nombre) {
	boton = document.getElementById(nombre);
	boton.src = url_empresa + '/static/img/pass/down1.jpg';
}