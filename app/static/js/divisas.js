/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

//control especifico del modulo
function controlModulo() {
	//moneda1 y moneda2
	moneda1 = document.getElementById("tipo_moneda").value;
	moneda2 = document.getElementById("tipo_moneda2").value;
	if (moneda1 == moneda2) {
		alert("Debe seleccionar una moneda 2 diferente");
		moneda = document.getElementById("tipo_moneda2");
		moneda.focus();
		return false;
	}

	return true;
}