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

async function sendSearchIngresoAlmacen() {
	var fd = new FormData(document.forms['search']);

	div_modulo.html(imagen_modulo);

	let result;

	try {
		result = await $.ajax({
			url: '/',
			method: 'POST',
			type: 'POST',
			cache: false,
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
			error: function (qXHR, textStatus, errorThrown) {
				console.log(errorThrown); console.log(qXHR); console.log(textStatus);
			},
		});
		//alert(result);
	}
	catch (e) {
		console.error(e);
	}
}

async function mandarFormularioIA(formulario, add_button, cancel_button) {

	btn_add = document.forms[formulario].elements[add_button];
	btn_cancel = document.forms[formulario].elements[cancel_button];

	btn_add.disabled = true;
	btn_cancel.disabled = true;

	var fd = new FormData(document.forms[formulario]);

	div_modulo.html(imagen_modulo);

	let result;

	try {
		result = await $.ajax({
			url: '/',
			method: 'POST',
			type: 'POST',
			cache: false,
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
			error: function (qXHR, textStatus, errorThrown) {
				console.log(errorThrown); console.log(qXHR); console.log(textStatus);
			},
		});
		//alert(result);
	}
	catch (e) {
		console.error(e);
	}
}

async function confirmarAnularIA() {

	motivo = Trim(document.forms['formulario'].elements['motivo_anula'].value);
	if (motivo == '') {
		alert('Debe llenar el motivo');
		return false;
	}

	if (confirm('Esta seguro de anular este registro?')) {
		btn_add = document.forms['formulario'].elements['add_button'];
		btn_cancel = document.forms['formulario'].elements['button_cancel'];

		btn_add.disabled = true;
		btn_cancel.disabled = true;

		var fd = new FormData(document.forms['formulario']);

		div_modulo.html(imagen_modulo);

		let result;

		try {
			result = await $.ajax({
				url: '/',
				method: 'POST',
				type: 'POST',
				cache: false,
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
				error: function (qXHR, textStatus, errorThrown) {
					console.log(errorThrown); console.log(qXHR); console.log(textStatus);
				},
			});
			//alert(result);
		}
		catch (e) {
			console.error(e);
		}
	}
}

function seleccionAlmacenIA() {
	//almacen
	almacen = document.getElementById('almacen');
	div_datos = $('#div_listap');
	if (almacen.value == '0') {
		div_datos.fadeOut('slow');
	}
	else {
		div_datos.fadeIn('slow');
	}
}

function seleccionPIA(numero_registro, producto, id) {
	//alert(numero_registro); alert(producto); alert(id);
	//asignamos el id del producto
	obj_aux = document.getElementById("producto_" + numero_registro);
	obj_aux.value = id;

	//alert(numero);alert(id);
	numero = parseInt(numero_registro);
	numero_int = numero + 1;
	if (numero_int <= 50) {
		numero_str = numero_int.toString();
		nombre_actual = "fila_" + numero_str;
		//alert(nombre_actual);
		objeto_actual = document.getElementById(nombre_actual);
		objeto_actual.style.display = "block";
		objeto_actual.style.display = "";
	}
}

//calculamos el total
function calcularTotalesIA() {
	limite = 50;

	total_todo = 0;

	for (i = 1; i <= limite; i++) {
		cantidad = document.getElementById("cantidad_" + i.toString());
		costo = document.getElementById("costo_" + i.toString());
		total = document.getElementById("total_" + i.toString());

		//valores
		cantidad_s = Trim(cantidad.value);
		costo_s = Trim(costo.value);

		if (cantidad_s != "" && costo_s != "") {
			total_v = parseFloat(cantidad_s) * parseFloat(costo_s);
			total_v2 = redondeo(total_v, 2);
			total_todo = total_todo + parseFloat(total_v2);
			total.value = total_v2;
		}
	}

	obj_total = document.getElementById('total');
	obj_total.value = redondeo(total_todo, 2);
}


function validarFilaIA(fila) {
	cantidad = document.getElementById("cantidad_" + fila.toString());
	costo = document.getElementById("costo_" + fila.toString());
	total = document.getElementById("total_" + fila.toString());
	tb2 = document.getElementById("tb2_" + fila.toString());
	producto = document.getElementById("producto_" + fila.toString());

	cant_val = Trim(cantidad.value);
	costo_val = Trim(costo.value);
	tb2_val = Trim(tb2.value);
	pro_val = Trim(producto.value);

	//no selecciono ningun producto
	if (tb2_val == '') {
		cantidad.value = '';
		costo.value = '';
		total.value = '';
		producto.value = '0';
	}
	else {
		//escribio un producto, verificamos si selecciono
		if (pro_val == '0') {
			//alert('Debe Seleccionar un Producto');
			cantidad.value = '';
			costo.value = '';
			total.value = '';
		}
	}
}
