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


function cargarZonas() {
	ciudad = document.getElementById('ciudad').value;
	if (ciudad == '0') {
		$("#div_zonas").html('');
	}
	else {
		imagen = '<img src="/static/img/pass/loading2.gif">';
		url_main = '/configuraciones/sucursales/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'ciudad': Trim(ciudad),
			'operation_x': 'zonas',
			'csrfmiddlewaretoken': token,
		}

		$("#div_zonas").html(imagen);
		$("#div_zonas").load(url_main, datos, function () {
			//termina de cargar la ventana
			resultadoZona();
		});
	}
}

function resultadoZona() {
	return true;
}


function sendSearchSucursal() {
	token_search = document.forms['search'].elements['csrfmiddlewaretoken'].value;

	datos_search = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'csrfmiddlewaretoken': token_search,
		'search_button_x': 'acc',
	}
	datos_search['search_zona'] = document.getElementById('search_zona').value;
	datos_search['search_sucursal'] = document.getElementById('search_sucursal').value;

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_search, function () {
		//termina de cargar la ventana
	});
}

function mandarFormularioSucursal(operation, operation2, formulario, add_button, button_cancel) {
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

		fd.append('ciudad', document.getElementById('ciudad').value);
		fd.append('zona', document.getElementById('zona').value);
		fd.append('sucursal', document.getElementById('sucursal').value);
		fd.append('codigo', document.getElementById('codigo').value);
		fd.append('activo', document.getElementById('activo').checked ? 1 : 0);
		fd.append('email', document.getElementById('email').value);
		fd.append('empresa', document.getElementById('empresa').value);
		fd.append('direccion', document.getElementById('direccion').value);
		fd.append('ciudad_rp', document.getElementById('ciudad_rp').value);
		fd.append('telefonos', document.getElementById('telefonos').value);
		fd.append('actividad', document.getElementById('actividad').value);
		fd.append('datos_mapa', document.getElementById('datos_mapa').value);
		fd.append('ubicacion_mapa', document.getElementById('ubicacion_mapa').value);

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

function confirmarEliminarSucursal() {
	if (confirm('Esta seguro de querer eliminar esta sucursal?')) {
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

		document.forms['formulario'].elements['add_button'].disabled = true;
		document.forms['formulario'].elements['button_cancel'].disabled = true;

		datos_operation = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'csrfmiddlewaretoken': token_operation,
			'operation_x': 'delete',
			'delete_x': 'acc',
		}
		datos_operation['id'] = document.forms['form_operation'].elements['id'].value;
		datos_operation['sucursal'] = document.getElementById('sucursal').value;

		div_modulo.html(imagen_modulo);
		div_modulo.load('/', datos_operation, function () {
			//termina de cargar la ventana
		});
	}
}