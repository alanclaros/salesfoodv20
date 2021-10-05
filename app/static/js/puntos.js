
//colocando el precio por defecto a los demas productos
function setPrecioA() {
	precio_a = Trim(document.getElementById('precio_a').value);

	precio_a_factura = document.getElementById('precio_a_factura');
	precio_a_consignacion = document.getElementById('precio_a_consignacion');
	precio_a_pp = document.getElementById('precio_a_pp');

	if (precio_a != '') {
		precio_a_factura.value = precio_a;
		precio_a_consignacion.value = precio_a;
		precio_a_pp.value = precio_a;
	}
}

function setPrecioB() {
	precio_b = Trim(document.getElementById('precio_b').value);

	precio_b_factura = document.getElementById('precio_b_factura');
	precio_b_consignacion = document.getElementById('precio_b_consignacion');
	precio_b_pp = document.getElementById('precio_b_pp');

	if (precio_b != '') {
		precio_b_factura.value = precio_b;
		precio_b_consignacion.value = precio_b;
		precio_b_pp.value = precio_b;
	}
}

function setPrecioC() {
	precio_c = Trim(document.getElementById('precio_c').value);

	precio_c_factura = document.getElementById('precio_c_factura');
	precio_c_consignacion = document.getElementById('precio_c_consignacion');
	precio_c_pp = document.getElementById('precio_c_pp');

	if (precio_c != '') {
		precio_c_factura.value = precio_c;
		precio_c_consignacion.value = precio_c;
		precio_c_pp.value = precio_c;
	}
}

// function sendSearchPunto() {
// 	token_search = document.forms['search'].elements['csrfmiddlewaretoken'].value;

// 	datos_search = {
// 		'module_x': document.forms['form_operation'].elements['module_x'].value,
// 		'csrfmiddlewaretoken': token_search,
// 		'search_button_x': 'acc',
// 	}
// 	datos_search['search_sucursal'] = document.getElementById('search_sucursal').value;
// 	datos_search['search_punto'] = document.getElementById('search_punto').value;

// 	div_modulo.html(imagen_modulo);
// 	div_modulo.load('/', datos_search, function () {
// 		//termina de cargar la ventana
// 	});
// }

// function mandarFormularioPunto(operation, operation2, formulario, add_button, button_cancel) {
// 	if (verifyForm()) {
// 		document.forms[formulario].elements[add_button].disabled = true;
// 		document.forms[formulario].elements[button_cancel].disabled = true;

// 		//document.forms[formulario].submit();
// 		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
// 		module_x = document.forms['form_operation'].elements['module_x'].value;

// 		var fd = new FormData();
// 		fd.append('csrfmiddlewaretoken', token_operation);
// 		fd.append('module_x', module_x);
// 		fd.append('operation_x', operation);
// 		fd.append('id', document.forms['form_operation'].elements['id'].value);

// 		fd.append(operation2, 'acc');

// 		fd.append('sucursal', document.getElementById('sucursal').value);
// 		fd.append('punto', document.getElementById('punto').value);
// 		fd.append('codigo', document.getElementById('codigo').value);
// 		fd.append('activo', document.getElementById('activo').checked ? 1 : 0);

// 		div_modulo.html(imagen_modulo);

// 		$.ajax({
// 			url: '/',
// 			type: 'post',
// 			data: fd,
// 			contentType: false,
// 			processData: false,
// 			success: function (response) {
// 				if (response != 0) {
// 					div_modulo.html(response);
// 				} else {
// 					alert('error al realizar la operacion, intentelo de nuevo');
// 				}
// 			},
// 		});
// 	}
// }

// function confirmarEliminarPunto() {
// 	if (confirm('Esta seguro de querer eliminar este punto?')) {
// 		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

// 		document.forms['formulario'].elements['add_button'].disabled = true;
// 		document.forms['formulario'].elements['button_cancel'].disabled = true;

// 		datos_operation = {
// 			'module_x': document.forms['form_operation'].elements['module_x'].value,
// 			'csrfmiddlewaretoken': token_operation,
// 			'operation_x': 'delete',
// 			'delete_x': 'acc',
// 		}
// 		datos_operation['id'] = document.forms['form_operation'].elements['id'].value;
// 		datos_operation['punto'] = document.getElementById('punto').value;

// 		div_modulo.html(imagen_modulo);
// 		div_modulo.load('/', datos_operation, function () {
// 			//termina de cargar la ventana
// 		});
// 	}
// }


function sendSearchPunto() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormPunto(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'puntoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Puntos!', 'Esta seguro de querer adicionar este punto?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Puntos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'puntoWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'puntoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Puntos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Puntos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'puntoWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'puntoDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Puntos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function puntoSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function puntoWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function puntoDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//guardamos puntos almacenes
function guardarPuntosAlmacenes(formulario, add_button, button_cancel) {
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
		fd.append('operation_x', 'puntos_almacenes')
		fd.append('operation_x2', 'modify_x')

		fd.append('id', document.forms['form_operation'].elements['id'].value);

		//almacenes ids
		almacenes_ids = document.forms['formulario'].elements['almacenes_ids'].value;
		div_almacenes = almacenes_ids.split('|');
		if (almacenes_ids != '') {
			for (ia = 0; ia < div_almacenes.length; ia++) {
				//alert(document.getElementById('almacen_' + div_almacenes[ia]).checked);
				fd.append('almacen_' + div_almacenes[ia], document.getElementById('almacen_' + div_almacenes[ia]).checked ? 1 : 0);
			}
		}

		div_modulo.html(imagen_modulo);

		let para_cargar = url_empresa;
		if (para_cargar != '') {
			para_cargar = url_empresa + '/';
		}
		// div_modulo.load(para_cargar, datos_operation, function () {
		// 	//termina de cargar la ventana
		// });

		$.ajax({
			url: para_cargar,
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


//guardamos puntos precios
function guardarPuntosPrecios(formulario, add_button, button_cancel) {
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
		fd.append('operation_x', 'puntos_precios')
		fd.append('operation_x2', 'modify_x')

		fd.append('id', document.forms['form_operation'].elements['id'].value);

		//precios
		fd.append('precio_a', document.getElementById('precio_a').value);
		fd.append('precio_b', document.getElementById('precio_b').value);
		fd.append('precio_c', document.getElementById('precio_c').value);

		fd.append('precio_a_factura', document.getElementById('precio_a_factura').value);
		fd.append('precio_b_factura', document.getElementById('precio_b_factura').value);
		fd.append('precio_c_factura', document.getElementById('precio_c_factura').value);

		fd.append('precio_a_consignacion', document.getElementById('precio_a_consignacion').value);
		fd.append('precio_b_consignacion', document.getElementById('precio_b_consignacion').value);
		fd.append('precio_c_consignacion', document.getElementById('precio_c_consignacion').value);

		fd.append('precio_a_pp', document.getElementById('precio_a_pp').value);
		fd.append('precio_b_pp', document.getElementById('precio_b_pp').value);
		fd.append('precio_c_pp', document.getElementById('precio_c_pp').value);

		div_modulo.html(imagen_modulo);
		let para_cargar = url_empresa;
		if (para_cargar != '') {
			para_cargar = url_empresa + '/';
		}

		$.ajax({
			url: para_cargar,
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