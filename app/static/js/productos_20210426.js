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

function sendSearchProducto() {
	token_search = document.forms['search'].elements['csrfmiddlewaretoken'].value;

	datos_search = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'csrfmiddlewaretoken': token_search,
		'search_button_x': 'acc',
	}
	datos_search['search_linea'] = document.getElementById('search_linea').value;
	datos_search['search_producto'] = document.getElementById('search_producto').value;
	datos_search['search_codigo'] = document.getElementById('search_codigo').value;

	div_modulo.html(imagen_modulo);
	div_modulo.load('/', datos_search, function () {
		//termina de cargar la ventana
	});
}

function mandarFormularioProducto(operation, operation2, formulario, add_button, button_cancel) {
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

		var files = $('#imagen1')[0].files[0];
		fd.append('imagen1', files);

		fd.append('insumo', document.getElementById('insumo').value);
		fd.append('codigo', document.getElementById('codigo').value);
		fd.append('precio', document.getElementById('precio').value);
		fd.append('posicion', document.getElementById('posicion').value);
		fd.append('activo', document.getElementById('activo').checked ? 1 : 0);

		div_modulo.html(imagen_modulo);

		$.ajax({
			url: '/',
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

//mostramos datos si es combo
/*function mostrarCombo() {
	es_combo = document.getElementById('combo');

	if (es_combo.checked) {
		$("#div_combo").fadeIn('slow');
		$("#div_combo_busqueda").fadeIn('slow');
	}
	else {
		$("#div_combo").fadeOut('slow');
		$("#div_combo_busqueda").fadeOut('slow');
	}
}*/

//crea descripcion del producto
function crearDescripcion() {
	descr1 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion1').value));
	descr2 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion2').value));
	descr3 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion3').value));
	descr4 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion4').value));
	descr5 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion5').value));
	descr6 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion6').value));
	descr7 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion7').value));
	descr8 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion8').value));
	descr9 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion9').value));
	descr10 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion10').value));

	texto1 = verificarTexto(descr1);
	texto2 = verificarTexto(descr2);
	texto3 = verificarTexto(descr3);
	texto4 = verificarTexto(descr4);
	texto5 = verificarTexto(descr5);
	texto6 = verificarTexto(descr6);
	texto7 = verificarTexto(descr7);
	texto8 = verificarTexto(descr8);
	texto9 = verificarTexto(descr9);
	texto10 = verificarTexto(descr10);

	texto_mostrar = texto1 + texto2 + texto3 + texto4 + texto5 + texto6 + texto7 + texto8 + texto9 + texto10;
	descripcion = $("#datos_descripcion");
	descripcion.html(texto_mostrar);
}

//arma texto de la descripcion del producto con negrita y cursiva
function verificarTexto(descripcion) {
	if (descripcion == '') {
		return '';
	}
	else {
		return descripcion + '<br>';
	}
}

//colocando el precio por defecto a los demas productos
function setPrecioA() {
	precio_a = Trim(document.getElementById('precio_a').value);

	precio_a_factura = document.getElementById('precio_a_factura');
	precio_a_consignacion = document.getElementById('precio_a_consignacion');
	precio_a_pp = document.getElementById('precio_a_pp');

	if (precio_a != '') {
		precio_a_factura.value = precio_a;
		precio_a_consignacion.value = precio_a;
		precio_a_pp.value = precio_a;
	}
}

function setPrecioB() {
	precio_b = Trim(document.getElementById('precio_b').value);

	precio_b_factura = document.getElementById('precio_b_factura');
	precio_b_consignacion = document.getElementById('precio_b_consignacion');
	precio_b_pp = document.getElementById('precio_b_pp');

	if (precio_b != '') {
		precio_b_factura.value = precio_b;
		precio_b_consignacion.value = precio_b;
		precio_b_pp.value = precio_b;
	}
}

function setPrecioC() {
	precio_c = Trim(document.getElementById('precio_c').value);

	precio_c_factura = document.getElementById('precio_c_factura');
	precio_c_consignacion = document.getElementById('precio_c_consignacion');
	precio_c_pp = document.getElementById('precio_c_pp');

	if (precio_c != '') {
		precio_c_factura.value = precio_c;
		precio_c_consignacion.value = precio_c;
		precio_c_pp.value = precio_c;
	}
}

//busqueda de productos
/*function buscarProductos() {

	linea = Trim(document.getElementById('b_linea').value);
	producto = Trim(document.getElementById('b_producto').value);
	codigo = Trim(document.getElementById('b_codigo').value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	operation_mandar = document.getElementById('operation_x').value;
	pid = document.getElementById('pid').value;

	datos_busqueda = {
		'operation_x': 'buscar_producto',
		'linea': linea,
		'producto': producto,
		'codigo': codigo,
		'operation_mandar': operation_mandar,
		'pid': pid,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#div_busqueda_productos").html(imagen);
	$("#div_busqueda_productos").load(url_main, datos_busqueda, function () {
		//termina de cargar ajax
	});
}*/

//busqueda de productos relacionados
function buscarProductosRelacionados() {

	linea = Trim(document.getElementById('br_linea').value);
	producto = Trim(document.getElementById('br_producto').value);
	codigo = Trim(document.getElementById('br_codigo').value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	operation_mandar = document.forms['form_operation'].elements['operation_x'].value;
	pid = document.forms['form_operation'].elements['id'].value;

	datos_busqueda = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'buscar_producto_relacionado',
		'linea': linea,
		'producto': producto,
		'codigo': codigo,
		'operation_mandar': operation_mandar,
		'pid': pid,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#div_busqueda_relacionados").html(imagen);
	$("#div_busqueda_relacionados").load(url_main, datos_busqueda, function () {
		//termina de cargar ajax
	});
}

//busqueda de insumos
function buscarInsumo() {

	insumo = Trim(document.getElementById('in_insumo').value);
	codigo = Trim(document.getElementById('in_codigo').value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	operation_mandar = document.forms['form_operation'].elements['operation_x'].value;
	pid = document.forms['form_operation'].elements['id'].value;

	datos_busqueda = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'buscar_insumo',
		'insumo': insumo,
		'codigo': codigo,
		'operation_mandar': operation_mandar,
		'pid': pid,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#div_busqueda_insumos").html(imagen);
	$("#div_busqueda_insumos").load(url_main, datos_busqueda, function () {
		//termina de cargar ajax
	});
}

//minimizar busqueda productos
/*function minimizarBusqueda() {
	$("#div_busqueda_productos").html('<i>resultado busqueda</i>');
}*/

//minimizar busqueda productos relacionados
function minimizarBusquedaRelacionado() {
	$("#div_busqueda_relacionados").html('<i>resultado busqueda</i>');
}

//selecionamos el producto para el combo
/*function seleccionarProducto(producto_id) {
	cantidad = Trim(document.getElementById('cantidad_' + producto_id).value);
	producto_nombre = Trim(document.getElementById('producto_nombre_' + producto_id).value);

	if (cantidad == '') {
		alert('debe llenar la cantidad del producto para el combo');
		return false;
	}

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_producto = {
		'operation_x': 'producto_combo',
		'producto_id': producto_id,
		'cantidad': cantidad,
		'producto': producto_nombre,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_productos_combo").html(imagen);
	$("#lista_productos_combo").load(url_main, datos_producto, function () {
		//termina de cargar ajax
	});
}*/

//selecionamos el producto relacionado
function seleccionarProductoRelacionado(producto_id) {
	producto_nombre = Trim(document.getElementById('productor_nombre_' + producto_id).value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_producto = {
		'operation_x': 'producto_relacionado',
		'producto_id': producto_id,
		'producto': producto_nombre,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_productos_relacionados").html(imagen);
	$("#lista_productos_relacionados").load(url_main, datos_producto, function () {
		//termina de cargar ajax
	});
}

//selecionamos el insumo
function seleccionarInsumo(insumo_id) {
	insumo_nombre = Trim(document.getElementById('insumo_nombre_' + insumo_id).value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_insumo = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'insumo',
		'insumo_id': insumo_id,
		'insumo': insumo_nombre,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_insumos").html(imagen);
	$("#lista_insumos").load(url_main, datos_insumo, function () {
		//termina de cargar ajax
	});
}

//quitamos el producto del combo
/*function quitarProductoCombo(producto_combo_id) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_quitar = {
		'operation_x': 'quitar_producto_combo',
		'producto_combo_id': producto_combo_id,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_productos_combo").html(imagen);
	$("#lista_productos_combo").load(url_main, datos_quitar, function () {
		//termina de cargar ajax
	});
}*/

//quitamos el producto del combo
function quitarProductoRelacionado(producto_relacionado_id) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_quitar = {
		'operation_x': 'quitar_producto_relacionado',
		'producto_relacionado_id': producto_relacionado_id,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_productos_relacionados").html(imagen);
	$("#lista_productos_relacionados").load(url_main, datos_quitar, function () {
		//termina de cargar ajax
	});
}

//quitamos el insumo
function quitarInsumo(insumo_id) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_quitar = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'quitar_insumo',
		'insumo_id': insumo_id,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_insumos").html(imagen);
	$("#lista_insumos").load(url_main, datos_quitar, function () {
		//termina de cargar ajax
	});
}

//cargamos imagen con ajax
function cargarImagen() {
	posicion = document.getElementById('posn_1');
	posicion_valor = Trim(posicion.value);

	valor_imagen = Trim(document.getElementById('imagen1').value);
	if (valor_imagen == '') {
		alert('debe seleccionar una imagen');
		return false;
	}

	if (posicion_valor == '') {
		alert('Debe llenar la posicion');
		posicion.focus();
		return false;
	}

	//boton de la imagen
	boton_imagen = document.getElementById('btn_imagen');
	boton_imagen.disabled = true;

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	url_main = document.getElementById('url_main').value;
	pid = document.getElementById('pid').value;
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	var fd = new FormData();
	//alert(fd);
	var files = $('#imagen1')[0].files[0];
	//alert(files);
	fd.append('imagen1', files);
	//alert(fd);
	fd.append('operation_x', 'add_imagen');
	fd.append('csrfmiddlewaretoken', token);
	fd.append('pid', pid);
	fd.append('posicion', posicion_valor);

	$.ajax({
		url: url_main,
		type: 'post',
		data: fd,
		contentType: false,
		processData: false,
		success: function (response) {
			if (response != 0) {

				datos_imagen = {
					'operation_x': 'lista_imagenes',
					'pid': pid,
					'csrfmiddlewaretoken': token,
				}

				$("#div_lista_imagenes").html(imagen);
				$("#div_lista_imagenes").load(url_main, datos_imagen, function () {
					//termina de cargar ajax
					boton_imagen.disabled = false;
				});
				//alert('cargado');
			} else {
				alert('no se pudo cargar la imagen, intentelo de nuevo');
				boton_imagen.disabled = false;
			}
		},
	});


	/*datos_imagen = {
		'operation_x': 'add_imagen',
		'data': fd,
		'pid': pid,
		'csrfmiddlewaretoken': token,
	}

	$("#div_lista_imagenes").html(imagen);
	$("#div_lista_imagenes").load(url_main, datos_imagen, function () {
		//termina de cargar ajax
	});*/
}

//mostramos la imagen
function mostrarImagen(pid) {
	document.form_img.id.value = pid;
	document.form_img.submit();
}

//eliminar imagen
function eliminarImagen(pid) {
	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	url_main = document.getElementById('url_main').value;

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	datos_imagen = {
		'operation_x': 'eliminar_imagen',
		'id': pid,
		'csrfmiddlewaretoken': token,
	}

	$("#div_lista_imagenes").html(imagen);
	$("#div_lista_imagenes").load(url_main, datos_imagen, function () {
		//termina de cargar ajax
		//boton_imagen.disabled = false;
	});

}