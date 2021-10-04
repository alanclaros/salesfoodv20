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


//enviando formuario
//guardando el formulario
function mandarPregiro(formulario, add_button, button_cancel) {

	document.forms[formulario].elements[add_button].disabled = true;
	document.forms[formulario].elements[button_cancel].disabled = true;

	document.forms[formulario].submit();
}

function confirmarAnular() {
	motivo_anula = Trim(document.getElementById('motivo_anula').value);
	if (motivo_anula == '') {
		alert('debe llenar el motivo');
		return false;
	}
	if (confirm('Esta seguro de querer anular este pregiro?')) {
		document.forms['formulario'].elements['add_button'].disabled = true;
		document.forms['formulario'].elements['button_cancel'].disabled = true;
		document.forms['formulario'].submit();
		return true;
	}
	//return true;
}

