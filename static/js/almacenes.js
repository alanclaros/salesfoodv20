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

function sendSearchAlmacen() {
	token_search = document.forms['search'].elements['csrfmiddlewaretoken'].value;

	datos_search = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'almacenes',
		'operation_x2': '',
		'id': document.forms['form_operation'].elements['id'].value,
		'csrfmiddlewaretoken': token_search,
		'search_button_x': 'acc',
	}
	datos_search['search_almacen'] = document.getElementById('search_almacen').value;
	datos_search['search_codigo'] = document.getElementById('search_codigo').value;

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_search, function () {
		//termina de cargar la ventana
	});
}

function mandarFormularioAlmacen(operation, operation2, formulario, add_button, button_cancel) {
	if (verifyForm()) {
		document.forms[formulario].elements[add_button].disabled = true;
		document.forms[formulario].elements[button_cancel].disabled = true;

		//document.forms[formulario].submit();
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
		module_x = document.forms['form_operation'].elements['module_x'].value;
		module_x2 = document.forms['form_operation'].elements['module_x2'].value;

		var fd = new FormData();
		fd.append('csrfmiddlewaretoken', token_operation);
		fd.append('module_x', module_x);
		fd.append('module_x2', module_x2);
		fd.append('operation_x', 'almacenes')
		fd.append('operation_x2', operation)
		fd.append(operation2, 'acc');
		fd.append('id', document.forms['form_operation'].elements['id'].value);
		fd.append('id2', document.forms['form_operation'].elements['id2'].value);

		fd.append('almacen', document.getElementById('almacen').value);
		fd.append('codigo', document.getElementById('codigo').value);
		fd.append('activo', document.getElementById('activo').checked ? 1 : 0);

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

function confirmarEliminarAlmacen() {
	if (confirm('Esta seguro de querer eliminar este almacen?')) {
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

		document.forms['formulario'].elements['add_button'].disabled = true;
		document.forms['formulario'].elements['button_cancel'].disabled = true;

		datos_operation = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'module_x2': document.forms['form_operation'].elements['module_x2'].value,
			'csrfmiddlewaretoken': token_operation,
			'operation_x': 'almacenes',
			'operation_x2': 'delete',
			'delete_x': 'acc',
		}
		datos_operation['id'] = document.forms['form_operation'].elements['id'].value;
		datos_operation['id2'] = document.forms['form_operation'].elements['id2'].value;
		datos_operation['almacen'] = document.getElementById('almacen').value;

		div_modulo.html(imagen_modulo);
		div_modulo.load('/', datos_operation, function () {
			//termina de cargar la ventana
		});
	}
}