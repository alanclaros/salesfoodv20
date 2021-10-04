
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
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormSucursal(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'sucursalSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Sucursales!', 'Esta seguro de querer adicionar esta sucursal?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Sucursales!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'sucursalWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'sucursalSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Sucursales!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Sucursales!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'sucursalWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'sucursalDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Sucursales!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function sucursalSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function sucursalWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function sucursalDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}
