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

async function mandarFormularioProducto(operation, operation2, formulario, add_button, button_cancel) {
	if (verifyForm()) {
		//document.forms[formulario].elements[add_button].disabled = true;
		//document.forms[formulario].elements[button_cancel].disabled = true;

		//document.forms[formulario].submit();
		token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
		module_x = document.forms['form_operation'].elements['module_x'].value;

		var fd = new FormData();
		fd.set('csrfmiddlewaretoken', String(token_operation));
		fd.set('module_x', String(module_x));
		fd.set('operation_x', String(operation));
		fd.set('id', String(document.forms['form_operation'].elements['id'].value));
		fd.set(operation2, 'acc');

		fd.set('linea', String(document.getElementById('linea').value));
		fd.set('producto', String(document.getElementById('producto').value));
		fd.set('codigo', String(document.getElementById('codigo').value));
		fd.set('stock_minimo', String(document.getElementById('stock_minimo').value));
		fd.set('activo', String(document.getElementById('activo').checked ? 1 : 0));
		fd.set('unidad', String(document.getElementById('unidad').value));
		fd.set('codigo_barras', String(document.getElementById('codigo_barras').value));

		//alert('antes refresco');
		//refrescos
		/*check_refresco = document.getElementById('check_refresco').checked ? 1 : 0;
		fd.set('check_refresco', check_refresco);

		refrescos_ids = document.getElementById('refrescos_ids').value;
		div_ref = refrescos_ids.split('|');
		for (ir = 0; ir < div_ref.length; ir++) {
			nombre1 = 'check_refresco_' + div_ref[ir];
			aux_ref = document.getElementById(nombre1).checked ? 1 : 0;
			fd.set('chk_ref_' + div_ref[ir], aux_ref);
		}

		for (ie = 0; ie < div_ref.length; ie++) {
			nombre2 = 'refresco_precio_' + div_ref[ie];
			val_aux = Trim(document.getElementById(nombre2).value);
			if (val_aux == '') {
				val_aux = '0';
			}
			fd.set('p_ref_' + div_ref[ie], val_aux);
		}*/

		check_refresco = document.getElementById('check_refresco').checked ? 1 : 0;
		fd.set('checkrefresco', String(check_refresco));
		try {
			refrescos_ids = document.getElementById('refrescos_ids').value;
			div_ref = refrescos_ids.split('|');
			for (var ia = 0; ia < div_ref.length; ia++) {
				nombre1 = 'check_refresco_' + div_ref[ia];
				aux_ref = document.getElementById(nombre1).checked ? 1 : 0;
				if (aux_ref == 1) {
					fd.set('ref' + div_ref[ia], String('nnn' + aux_ref));
					nombre2 = 'refresco_precio_' + div_ref[ia];
					val_aux = Trim(document.getElementById(nombre2).value);
					fd.set('refpre' + div_ref[ia], String('nnn' + val_aux));
				}
			}
		}
		catch (e) {
			alert('error refresco');
		}

		/*fd.set('ref1', '1');
		fd.set('ref2', '1');
		fd.set('ref3', '1');
		fd.set('ref4', '1');
		fd.set('ref5', '1');
		fd.set('ref6', '1');
		fd.set('refpre1', '1');
		fd.set('refpre2', '1');
		fd.set('refpre3', '1');
		fd.set('refpre4', '1');
		fd.set('refpre5', '1');
		fd.set('refpre6', '1');*/


		//alert('antes papa');
		//papas
		check_papa = document.getElementById('check_papa').checked ? 1 : 0;
		fd.set('checkpapa', String(check_papa));

		try {
			papas_ids = document.getElementById('papas_ids').value;
			div_papa = papas_ids.split('|');
			for (var ia = 0; ia < div_papa.length; ia++) {
				nombre1 = 'check_papa_' + div_papa[ia];
				aux_ref = document.getElementById(nombre1).checked ? 1 : 0;

				if (aux_ref == 1) {
					fd.set('pap' + div_papa[ia], String('nnn' + aux_ref));
					nombre2 = 'papa_precio_' + div_papa[ia];
					val_aux = Trim(document.getElementById(nombre2).value);
					fd.set('pappre' + div_papa[ia], String('nnn' + val_aux));
				}
				//fd.set('precio_papa_' + div_papa[ir], document.getElementById('papa_precio_' + div_papa[ir]).value);
			}
		}
		catch (e) {
			alert('error papa');
		}

		//alert('despues papa');
		//descripcion
		fd.set('descripcion1', Trim(String(document.getElementById('descripcion1').value)));
		fd.set('descripcion2', Trim(String(document.getElementById('descripcion2').value)));
		fd.set('descripcion3', Trim(String(document.getElementById('descripcion3').value)));
		fd.set('descripcion4', Trim(String(document.getElementById('descripcion4').value)));
		fd.set('descripcion5', Trim(String(document.getElementById('descripcion5').value)));
		fd.set('descripcion6', Trim(String(document.getElementById('descripcion6').value)));
		fd.set('descripcion7', Trim(String(document.getElementById('descripcion7').value)));
		fd.set('descripcion8', Trim(String(document.getElementById('descripcion8').value)));
		fd.set('descripcion9', Trim(String(document.getElementById('descripcion9').value)));
		fd.set('descripcion10', Trim(String(document.getElementById('descripcion10').value)));

		//costos
		fd.set('costo_a', Trim(String(document.getElementById('costo_a').value)));
		fd.set('costo_b', Trim(String(document.getElementById('costo_b').value)));
		fd.set('costo_c', Trim(String(document.getElementById('costo_c').value)));

		//precios
		fd.set('precio_a', Trim(String(document.getElementById('precio_a').value)));
		fd.set('precio_b', Trim(String(document.getElementById('precio_b').value)));
		fd.set('precio_c', Trim(String(document.getElementById('precio_c').value)));

		//precios factura
		fd.set('precio_a_factura', Trim(String(document.getElementById('precio_a_factura').value)));
		fd.set('precio_b_factura', Trim(String(document.getElementById('precio_b_factura').value)));
		fd.set('precio_c_factura', Trim(String(document.getElementById('precio_c_factura').value)));

		//precios consignacion
		fd.set('precio_a_consignacion', Trim(String(document.getElementById('precio_a_consignacion').value)));
		fd.set('precio_b_consignacion', Trim(String(document.getElementById('precio_b_consignacion').value)));
		fd.set('precio_c_consignacion', Trim(String(document.getElementById('precio_c_consignacion').value)));

		//precios pp
		fd.set('precio_a_pp', Trim(String(document.getElementById('precio_a_pp').value)));
		fd.set('precio_b_pp', Trim(String(document.getElementById('precio_b_pp').value)));
		fd.set('precio_c_pp', Trim(String(document.getElementById('precio_c_pp').value)));

		/*//mandamos
		// Display the key/value pairs
		for (var pair of fd.entries()) {
			console.log(pair[0] + ', ' + pair[1]);
		}
		//div_modulo.html(imagen_modulo);

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
					console.log(errorThrown);
					console.log(qXHR);
					console.log(textStatus);
				},
			});
			alert(result);
		}
		catch (e) {
			console.error(e);
		}*/

		var oReq = new XMLHttpRequest();
		oReq.open("POST", "/", true);
		oReq.onload = function (oEvent) {
			if (oReq.status == 200) {
				console.log('updated..');
			} else {
				console.log('error');
			}
		};

		oReq.send(fd);


		//alert('enviado');
	}
}

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

//selecionamos el insumo
function seleccionarInsumo(insumo_id) {
	insumo_nombre = Trim(document.getElementById('insumo_nombre_' + insumo_id).value);
	cantidad_insumo = Trim(document.getElementById('insumo_cantidad_' + insumo_id).value);
	if (cantidad_insumo == '') {
		alert('debe llenar la cantidad');
		return false;
	}

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_insumo = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'insumo',
		'insumo_id': insumo_id,
		'insumo': insumo_nombre,
		'cantidad': cantidad_insumo,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_insumos").html(imagen);
	$("#lista_insumos").load(url_main, datos_insumo, function () {
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

//minimizar busqueda insumos
function minimizarBusquedaInsumo() {
	$("#div_busqueda_insumos").html('<i>resultado busqueda</i>');
}

//busqueda de insumos
function buscarComponente() {

	componente = Trim(document.getElementById('co_componente').value);
	codigo = Trim(document.getElementById('co_codigo').value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	operation_mandar = document.forms['form_operation'].elements['operation_x'].value;
	pid = document.forms['form_operation'].elements['id'].value;

	datos_busqueda = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'buscar_componente',
		'componente': componente,
		'codigo': codigo,
		'operation_mandar': operation_mandar,
		'pid': pid,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#div_busqueda_componentes").html(imagen);
	$("#div_busqueda_componentes").load(url_main, datos_busqueda, function () {
		//termina de cargar ajax
	});
}

//selecionamos el componente
function seleccionarComponente(componente_id) {
	componente_nombre = Trim(document.getElementById('componente_nombre_' + componente_id).value);
	cantidad_componente = Trim(document.getElementById('componente_cantidad_' + componente_id).value);
	if (cantidad_componente == '') {
		alert('debe llenar la cantidad');
		return false;
	}

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_insumo = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'componente',
		'componente_id': componente_id,
		'componente': componente_nombre,
		'cantidad': cantidad_componente,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_componentes").html(imagen);
	$("#lista_componentes").load(url_main, datos_insumo, function () {
		//termina de cargar ajax
	});
}

//quitamos el insumo
function quitarComponente(componente_id) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_quitar = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'quitar_componente',
		'componente_id': componente_id,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_componentes").html(imagen);
	$("#lista_componentes").load(url_main, datos_quitar, function () {
		//termina de cargar ajax
	});
}

//minimizar busqueda insumos
function minimizarBusquedaComponente() {
	$("#div_busqueda_componentes").html('<i>resultado busqueda</i>');
}

//busqueda de insumos
function buscarExtra() {

	extra = Trim(document.getElementById('ex_extra').value);
	codigo = Trim(document.getElementById('ex_codigo').value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	operation_mandar = document.forms['form_operation'].elements['operation_x'].value;
	pid = document.forms['form_operation'].elements['id'].value;

	datos_busqueda = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'buscar_extra',
		'extra': extra,
		'codigo': codigo,
		'operation_mandar': operation_mandar,
		'pid': pid,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#div_busqueda_extras").html(imagen);
	$("#div_busqueda_extras").load(url_main, datos_busqueda, function () {
		//termina de cargar ajax
	});
}

//selecionamos el componente
function seleccionarExtra(extra_id) {
	extra_nombre = Trim(document.getElementById('extra_nombre_' + extra_id).value);
	extra_precio = Trim(document.getElementById('extra_precio_' + extra_id).value);
	if (Trim(extra_precio) == '') {
		alert('Debe llenar el precio');
		return false;
	}

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_insumo = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'extra',
		'extra_id': extra_id,
		'extra': extra_nombre,
		'extra_precio': extra_precio,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_extras").html(imagen);
	$("#lista_extras").load(url_main, datos_insumo, function () {
		//termina de cargar ajax
	});
}

//quitamos el insumo
function quitarExtra(extra_id) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_quitar = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'quitar_extra',
		'extra_id': extra_id,
		'csrfmiddlewaretoken': token,
	}

	imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
	$("#lista_extras").html(imagen);
	$("#lista_extras").load(url_main, datos_quitar, function () {
		//termina de cargar ajax
	});
}

//minimizar busqueda insumos
function minimizarBusquedaExtra() {
	$("#div_busqueda_extras").html('<i>resultado busqueda</i>');
}

//mostramos refrescos
function listaRefresco() {
	div_ref = $('#div_lista_refrescos');
	check_ref = document.getElementById('check_refresco');

	if (check_ref.checked) {
		div_ref.fadeIn('slow');
	}
	else {
		div_ref.fadeOut('slow');
	}
}

//mostramos papas
function listaPapa() {
	div_papa = $('#div_lista_papas');
	check_papa = document.getElementById('check_papa');

	if (check_papa.checked) {
		div_papa.fadeIn('slow');
	}
	else {
		div_papa.fadeOut('slow');
	}
}

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

//minimizar busqueda productos relacionados
function minimizarBusquedaRelacionado() {
	$("#div_busqueda_relacionados").html('<i>resultado busqueda</i>');
}

//selecionamos el producto relacionado
function seleccionarProductoRelacionado(producto_id) {
	producto_nombre = Trim(document.getElementById('productor_nombre_' + producto_id).value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_producto = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
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

//quitamos el producto del combo
function quitarProductoRelacionado(producto_relacionado_id) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	url_main = document.getElementById('url_main').value;

	datos_quitar = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
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