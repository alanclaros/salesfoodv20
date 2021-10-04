
function sendSearchUsuario() {
	div_modulo = $("#div_block_content");
	sendFormObject('search', div_modulo);
}

function sendFormUsuario(operation, message) {
	//modal function
	modalFunction = document.getElementById('modalFunctionSuccess');
	modalF = $('#modalForm');

	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				resControlModulo = controlModuloUsuario();
				if (resControlModulo === true) {
					modalFunction.value = 'usuarioSaveForm();';
					//set data modal
					modalSetParameters('success', 'center', 'Usuarios!', 'Esta seguro de querer adicionar este Usuario?', 'Cancelar', 'Guardar');
					modalF.modal();
				}
				else {
					//set data modal
					modalSetParameters('warning', 'center', 'Usuarios!', resControlModulo, 'Cancelar', 'Volver');
					//function cancel
					modalFunction.value = 'usuarioWarning();';
					modalF.modal();
				}
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Usuarios!', resValidation, 'Cancelar', 'Volver');
				//function cancel
				modalFunction.value = 'usuarioWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				resControlModulo = controlModuloUsuario();
				if (resControlModulo === true) {
					modalFunction.value = 'usuarioSaveForm();';
					//set data modal
					modalSetParameters('success', 'center', 'Usuarios!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
					modalF.modal();
				}
				else {
					//set data modal
					modalSetParameters('warning', 'center', 'Usuarios!', resControlModulo, 'Cancelar', 'Volver');
					//function cancel
					modalFunction.value = 'usuarioWarning();';
					modalF.modal();
				}
				// modalFunction.value = 'usuarioSaveForm();';
				// //set data modal
				// modalSetParameters('success', 'center', 'Usuarios!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				// modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Usuarios!', resValidation, 'Cancelar', 'Volver');
				//function cancel
				modalFunction.value = 'usuarioWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'usuarioDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Usuarios!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function usuarioSaveForm() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function usuarioWarning() {
	modalF = $('#modalForm');
	modalF.modal('toggle');
}

function usuarioDelete() {
	modalF = $('#modalForm');
	div_modulo = $("#div_block_content");

	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}


//control especifico del modulo
function controlModuloUsuario() {
	metodo = document.getElementById("metodo").value;
	if (metodo == "add") {
		up = document.getElementById("password");
		user_password = TrimDerecha(TrimIzquierda(up.value));
		if (user_password == "") {
			//alert("Debe llenar este campo");
			//up.focus();
			return 'Debe llenar el password';
		}
	}
	if (metodo == "modify") {
		up = document.getElementById("password");
		cambiar = document.getElementById("cambiar").value;
		if (cambiar == "yes") {
			user_password = TrimDerecha(TrimIzquierda(up.value));
			if (user_password == "") {
				// alert("Debe llenar este campo");
				// up.focus();
				// return false;
				return 'Debe Llenar el nuevo password';
			}
		}
	}
	return true;
}

function deshabilitar(valor) {
	if (valor.value == "yes") {
		document.formulario.password.disabled = false;
		document.formulario.password.focus();
	}
	else {
		document.formulario.password.disabled = true;
	}
}