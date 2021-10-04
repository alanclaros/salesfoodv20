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

async function sendSearchSA() {
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

async function mandarFormularioSA(formulario, add_button, cancel_button) {

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

async function confirmarAnularSA() {

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


function seleccionAlmacenSA() {
	//almacen
	almacen = document.getElementById('almacen');
	div_datos = $('#div_listap');
	if (almacen.value == '0') {
		div_datos.fadeOut('slow');
	}
	else {
		div_datos.fadeIn('slow');
		//reiniciamos la seleccion
		for (i = 1; i <= 50; i++) {
			producto = document.getElementById('producto_' + i);
			tb2 = document.getElementById('tb2_' + i);

			//stocks
			if (producto.value != '0' && producto.value != '') {
				try {
					nombre = 'stock_ids_' + producto.value;
					stock_ids = document.getElementById(nombre).value;

					if (stock_ids != '') {
						division = stock_ids.split(',');
						for (j = 0; j < division.length; j++) {
							s_id = division[j];

							cantidad = document.getElementById('cantidad_' + s_id);
							cantidad.value = '';

							//fecha vencimiento
							f_venc = document.getElementById('f_venc_' + s_id);
							f_venc.value = '';

							//lote
							lote = document.getElementById('lote_' + s_id);
							lote.value = '';

							//actual
							lote = document.getElementById('actual_' + s_id);
							lote.value = '';
						}
					}
				}
				catch (e) {

				}
			}

			producto.value = "0";
			tb2.value = "";

			//ocultamos las filas
			if (i > 1) {
				fila = document.getElementById('fila_' + i);
				fila.style.display = 'none';
			}
		}
	}
}

function controlarStockSA(stock_id) {
	actual = parseFloat(document.getElementById('actual_' + stock_id).value);
	cantidad = document.getElementById('cantidad_' + stock_id);
	valor_cantidad = parseFloat(Trim(cantidad.value));
	if (valor_cantidad > actual) {
		cantidad.value = '';
		alert('la cantidad no puede ser mayor a ' + actual);
	}
}

function seleccionPSA(numero_registro, producto, id) {
	//alert(numero_registro);alert(producto);alert(id);

	//verificamos que no repita productos
	for (i = 1; i <= 50; i++) {
		aux_p = document.getElementById('producto_' + i);
		if (parseInt(numero_registro) != i && aux_p.value == id) {
			alert('ya selecciono este producto');
			tb2 = document.getElementById('tb2_' + numero_registro);
			tb2.focus();
			tb2.value = '';
			return false;
		}
	}

	//asignamos el id del producto
	obj_aux = document.getElementById("producto_" + numero_registro);
	obj_aux.value = id;

	//recuperamos stock del producto
	url_main = document.getElementById('url_main').value;
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	ruta_imagen = url_empresa + '/static/img/pass/loading.gif';
	almacen = document.getElementById('almacen').value;

	datos = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'stock_producto',
		'id': id,
		'almacen': almacen,
		'csrfmiddlewaretoken': token
	}

	imagen = '<img src="' + ruta_imagen + '">';
	fila = $("#div_fila_" + numero_registro);

	fila.html(imagen);
	fila.load(url_main, datos, function () {
		//termina de cargar la ventana
	});

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

function validarFilaSA(fila) {
	tb2 = document.getElementById("tb2_" + fila.toString());
	producto = document.getElementById("producto_" + fila.toString());

	tb2_val = Trim(tb2.value);
	pro_val = Trim(producto.value);

	//no selecciono ningun producto
	if (tb2_val == '') {
		producto.value = '0';
	}
	else {
		//escribio un producto, verificamos si selecciono
		if (pro_val == '0') {
			//alert('Debe Seleccionar un Producto');
			tb2.value = '';
			tb2.focus();
		}
	}
}
