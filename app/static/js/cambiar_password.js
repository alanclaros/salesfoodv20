
function cambiarPassword() {
	actual = document.getElementById('actual');
	nuevo = document.getElementById('nuevo');
	nuevo2 = document.getElementById('nuevo2');

	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	if (Trim(actual.value) == '') {
		//alert('debe llenar su password');
		//actual.focus();
		modalSetParameters('warning', 'center', 'Cambiar Password!', 'debe llenar su password actual', 'Cancelar', 'Volver');

		//function cancel
		modalFunction.value = 'cambiarPasswordWarning();';
		modalF.modal();

		return false;
	}

	if (Trim(nuevo.value) == '') {
		//alert('debe llenar su nuevo password');
		//nuevo.focus();
		modalSetParameters('warning', 'center', 'Cambiar Password!', 'debe llenar su nuevo password', 'Cancelar', 'Volver');

		//function cancel
		modalFunction.value = 'cambiarPasswordWarning();';
		modalF.modal();
		return false;
	}

	if (Trim(nuevo2.value) == '') {
		//alert('debe llenar la repeticion de su password');
		//nuevo2.focus();
		modalSetParameters('warning', 'center', 'Cambiar Password!', 'debe llenar la repeticion de su password', 'Cancelar', 'Volver');

		//function cancel
		modalFunction.value = 'cambiarPasswordWarning();';
		modalF.modal();

		return false;
	}

	if (Trim(nuevo.value) != Trim(nuevo2.value)) {
		//alert('La repeticion de password debe coincidir');
		//nuevo2.focus();
		modalSetParameters('warning', 'center', 'Cambiar Password!', 'la repeticion de su nuevo password debe coincidir', 'Cancelar', 'Volver');

		//function cancel
		modalFunction.value = 'cambiarPasswordWarning();';
		modalF.modal();

		return false;
	}

	modalFunction.value = 'cambiarPasswordSaveForm();';
	//set data modal
	modalSetParameters('success', 'center', 'Cambiar Password!', 'Esta seguro de querer cambiar su password?', 'Cancelar', 'Guardar');
	modalF.modal();
}

function cambiarPasswordSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	//document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cambiarPasswordWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}