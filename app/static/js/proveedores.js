
function sendSearchProveedor() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormProveedor(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'proveedorSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Proveedores!', 'Esta seguro de querer adicionar este proveedor?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Proveedores!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'proveedorWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'proveedorSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Proveedores!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Proveedores!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'proveedorWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'proveedorDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Proveedores!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function proveedorSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function proveedorWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function proveedorDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}