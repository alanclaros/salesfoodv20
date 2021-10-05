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

//guardamos
function mandarFormularioConfiguracion(operation, operation2, formulario, add_button, button_cancel) {
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

		fd.append('cant_per_page', document.getElementById('cant_per_page').value);
		fd.append('cant_products_home', document.getElementById('cant_products_home').value);
		fd.append('vender_fracciones', document.getElementById('vender_fracciones').value);

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

//guardamos
function mandarFormularioConfiguracion() {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');
	resValidation = verifyForm();

	if (resValidation === true) {
		modalFunction.value = 'configuracionesSaveForm();';
		//set data modal
		modalSetParameters('success', 'center', 'Configuraciones!', 'Esta seguro de querer guardar los datos?', 'Cancelar', 'Guardar');
		modalF.modal();
	}
	else {
		//set data modal
		modalSetParameters('warning', 'center', 'Configuraciones!', resValidation, 'Cancelar', 'Volver');

		//function cancel
		modalFunction.value = 'configuracionesWarning(modalF);';
		modalF.modal();
	}
}

function configuracionesSaveForm() {
	modalF = $('#modalForm');
	modalF.modal('toggle');

	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	//document.forms[formulario].submit();
	token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
	module_x = document.forms['form_operation'].elements['module_x'].value;
	operation = document.forms['form_operation'].elements['operation_x'].value;

	var fd = new FormData();
	fd.append('csrfmiddlewaretoken', token_operation);
	fd.append('module_x', module_x);
	fd.append('operation_x', operation);
	fd.append('id', document.forms['form_operation'].elements['id'].value);
	fd.append('cant_per_page', document.getElementById('cant_per_page').value);
	fd.append('cant_products_home', document.getElementById('cant_products_home').value);
	fd.append('vender_fracciones', document.getElementById('vender_fracciones').value);


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

function configuracionesWarning(modalF) {
	//modalF = $('#modalForm');

	modalF.modal('toggle');
}