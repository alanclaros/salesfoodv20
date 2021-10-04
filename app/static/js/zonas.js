
function sendSearchZonas() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormZona(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'zonaSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Zonas!', 'Esta seguro de querer adicionar esta zona?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Zonas!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'zonaWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'zonaSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Zonas!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Zonas!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'zonaWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'zonaDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Zonas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function zonaSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function zonaWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function zonaDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}