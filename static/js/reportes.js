/************************************************************************************/
/************************************************************************************/
/****************Desarrollador, Programador: Alan Claros Camacho ********************/
/****************E-mail: alan_Claros13@hotmail.com **********************************/
/************************************************************************************/
/************************************************************************************/

//acc, control especifico del modulo
function arqueoCaja() {
	caja = document.getElementById('caja').value;
	fecha = document.getElementById('fecha').value;

	document.forms['form_print'].elements['operation_x2'].value = 'print';
	document.forms['form_print'].elements['id'].value = caja;
	document.forms['form_print'].elements['fecha'].value = fecha;

	document.forms['form_print'].submit();
}

//stock productos
function stockProductos(operation) {
	almacen = document.getElementById('almacen').value;

	document.forms['form_print'].elements['operation_x2'].value = operation;
	document.forms['form_print'].elements['almacen'].value = almacen;

	document.forms['form_print'].submit();
}

//plan pagos
function planPagos(operation) {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	punto = document.getElementById('punto').value;
	tipo = document.getElementById('tipo').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = operation;
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['punto'].value = punto;
	document.forms['form_print'].elements['tipo'].value = tipo;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//ventas
function ventas(operation) {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	punto = document.getElementById('punto').value;
	tipo = document.getElementById('tipo').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = operation;
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['punto'].value = punto;
	document.forms['form_print'].elements['tipo'].value = tipo;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//preventas
function preventas(operation) {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	punto = document.getElementById('punto').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	aux_n = document.getElementById('inventario');
	if (aux_n.checked) {
		inventario = 'si';
	}
	else {
		inventario = 'no';
	}

	aux_n = document.getElementById('venta');
	if (aux_n.checked) {
		venta = 'si';
	}
	else {
		venta = 'no';
	}

	document.forms['form_print'].elements['operation_x'].value = operation;
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['punto'].value = punto;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;
	document.forms['form_print'].elements['inventario'].value = inventario;
	document.forms['form_print'].elements['venta'].value = venta;

	document.forms['form_print'].submit();
}

//ingresos de productos
function ingresoProductos(operation) {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	almacen = document.getElementById('almacen').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = operation;
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['almacen'].value = almacen;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//pedido de productos
function pedidoProductos(operation) {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	almacen = document.getElementById('almacen').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = operation;
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['almacen'].value = almacen;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//movimiento de productos
function movimientoProductos(operation) {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	almacen = document.getElementById('almacen').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = operation;
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['almacen'].value = almacen;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//salida de productos
function salidaProductos(operation) {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	almacen = document.getElementById('almacen').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = operation;
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['almacen'].value = almacen;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//acc, ingresos a caja
function ingresosCaja() {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = 'print';
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//acc, ingresos a caja excel
function ingresosCajaExcel() {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_excel'].elements['operation_x2'].value = 'print_excel';
	document.forms['form_excel'].elements['ciudad'].value = ciudad;
	document.forms['form_excel'].elements['sucursal'].value = sucursal;
	document.forms['form_excel'].elements['caja'].value = caja;
	document.forms['form_excel'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_excel'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_excel'].elements['anulados'].value = anulados;

	document.forms['form_excel'].submit();
}

//egresos de caja
function egresosCaja() {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = 'print';
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//egresos de caja excel
function egresosCajaExcel() {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_excel'].elements['operation_x2'].value = 'print_excel';
	document.forms['form_excel'].elements['ciudad'].value = ciudad;
	document.forms['form_excel'].elements['sucursal'].value = sucursal;
	document.forms['form_excel'].elements['caja'].value = caja;
	document.forms['form_excel'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_excel'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_excel'].elements['anulados'].value = anulados;

	document.forms['form_excel'].submit();
}

//movimientos de caja
function movimientosCaja() {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = 'print';
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//movimientos de caja excel
function movimientosCajaExcel() {
	ciudad = document.getElementById('ciudad').value;
	sucursal = document.getElementById('sucursal').value;
	caja = document.getElementById('caja').value;
	fecha_ini = document.getElementById('fecha_ini').value;
	fecha_fin = document.getElementById('fecha_fin').value;

	aux_n = document.getElementById('anulados');
	if (aux_n.checked) {
		anulados = 'si';
	}
	else {
		anulados = 'no';
	}

	document.forms['form_print'].elements['operation_x2'].value = 'print_excel';
	document.forms['form_print'].elements['ciudad'].value = ciudad;
	document.forms['form_print'].elements['sucursal'].value = sucursal;
	document.forms['form_print'].elements['caja'].value = caja;
	document.forms['form_print'].elements['fecha_ini'].value = fecha_ini;
	document.forms['form_print'].elements['fecha_fin'].value = fecha_fin;
	document.forms['form_print'].elements['anulados'].value = anulados;

	document.forms['form_print'].submit();
}

//carga de solo sucursales
function cargarSoloSucursales() {
	ciudad = document.getElementById('ciudad').value;
	url_main = document.getElementById('url_main').value;

	if (ciudad == '0') {
		$("#" + 'div_sucursal').html('<select name="sucursal" id="sucursal" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
	}
	else {
		//cargamos sucursales
		imagen = '<img src="/static/img/pass/loading2.gif">';
		//url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'ciudad': ciudad,
			'operation_x': 'buscar_solo_sucursal',
			'csrfmiddlewaretoken': token,
		}
		$("#" + 'div_sucursal').html(imagen);
		$("#" + 'div_sucursal').load(url_main, datos, function () {
			//termina de cargar la ventana
			//resultadoBusqedaCI();
		});
	}
}

//sucursales por ciudad, y despues caja
function cargarSucursalesCiudad() {
	ciudad = document.getElementById('ciudad').value;
	url_main = document.getElementById('url_main').value;

	if (ciudad == '0') {
		$("#" + 'div_sucursal').html('<select name="sucursal" id="sucursal" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
		$("#" + 'div_caja').html('<select name="caja" id="caja" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
	}
	else {
		$("#" + 'div_caja').html('<select name="caja" id="caja" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
		//cargamos sucursales
		imagen = '<img src="/static/img/pass/loading2.gif">';
		//url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'ciudad': ciudad,
			'operation_x': 'buscar_sucursal',
			'csrfmiddlewaretoken': token,
		}
		$("#" + 'div_sucursal').html(imagen);
		$("#" + 'div_sucursal').load(url_main, datos, function () {
			//termina de cargar la ventana
			//resultadoBusqedaCI();
		});
	}
}

//sucursales por ciudad, y despues almacen
function cargarSucursalesAlmacen() {
	ciudad = document.getElementById('ciudad').value;
	url_main = document.getElementById('url_main').value;

	if (ciudad == '0') {
		$("#" + 'div_sucursal').html('<select name="sucursal" id="sucursal" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
		$("#" + 'div_almacen').html('<select name="almacen" id="almacen" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
	}
	else {
		$("#" + 'div_almacen').html('<select name="almacen" id="almacen" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
		//cargamos sucursales
		imagen = '<img src="/static/img/pass/loading2.gif">';
		//url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'ciudad': ciudad,
			'operation_x': 'buscar_sucursal_almacen',
			'csrfmiddlewaretoken': token,
		}
		$("#" + 'div_sucursal').html(imagen);
		$("#" + 'div_sucursal').load(url_main, datos, function () {
			//termina de cargar la ventana
			//resultadoBusqedaCI();
		});
	}
}

//sucursales por ciudad, y despues punto
function cargarSucursalesCiudadPunto() {
	ciudad = document.getElementById('ciudad').value;
	url_main = document.getElementById('url_main').value;

	if (ciudad == '0') {
		$("#" + 'div_sucursal').html('<select name="sucursal" id="sucursal" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
		$("#" + 'div_punto').html('<select name="punto" id="punto" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
	}
	else {
		$("#" + 'div_punto').html('<select name="punto" id="punto" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
		//cargamos sucursales
		imagen = '<img src="/static/img/pass/loading2.gif">';
		//url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'ciudad': ciudad,
			'operation_x': 'buscar_sucursal_punto',
			'csrfmiddlewaretoken': token,
		}
		$("#" + 'div_sucursal').html(imagen);
		$("#" + 'div_sucursal').load(url_main, datos, function () {
			//termina de cargar la ventana
			//resultadoBusqedaCI();
		});
	}
}

//cajas por sucursal
function cargarCajasSucursal() {
	sucursal = document.getElementById('sucursal').value;
	url_main = document.getElementById('url_main').value;

	if (sucursal == '0') {
		$("#" + 'div_caja').html('<select name="caja" id="caja" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
	}
	else {
		//cargamos sucursales
		imagen = '<img src="/static/img/pass/loading2.gif">';
		//url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'sucursal': sucursal,
			'operation_x': 'buscar_caja',
			'csrfmiddlewaretoken': token,
		}
		$("#" + 'div_caja').html(imagen);
		$("#" + 'div_caja').load(url_main, datos, function () {
			//termina de cargar la ventana
			//resultadoBusqedaCI();
		});
	}
}

//puntos por sucursal
function cargarPuntosSucursal() {
	sucursal = document.getElementById('sucursal').value;
	url_main = document.getElementById('url_main').value;

	if (sucursal == '0') {
		$("#" + 'div_punto').html('<select name="punto" id="punto" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
	}
	else {
		//cargamos sucursales
		imagen = '<img src="/static/img/pass/loading2.gif">';
		//url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'sucursal': sucursal,
			'operation_x': 'buscar_punto',
			'csrfmiddlewaretoken': token,
		}
		$("#" + 'div_punto').html(imagen);
		$("#" + 'div_punto').load(url_main, datos, function () {
			//termina de cargar la ventana
			//resultadoBusqedaCI();
		});
	}
}

//almacenes por sucursal
function cargarAlmacenesSucursal() {
	sucursal = document.getElementById('sucursal').value;
	url_main = document.getElementById('url_main').value;

	if (sucursal == '0') {
		$("#" + 'div_almacen').html('<select name="almacen" id="almacen" class="form-control input w-90 h-35"><option value="0">(TODOS)</option></select>');
	}
	else {
		//cargamos sucursales
		imagen = '<img src="/static/img/pass/loading2.gif">';
		//url_main = '/enviardinero/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'module_x': document.forms['form_operation'].elements['module_x'].value,
			'sucursal': sucursal,
			'operation_x': 'buscar_almacen',
			'csrfmiddlewaretoken': token,
		}
		$("#" + 'div_almacen').html(imagen);
		$("#" + 'div_almacen').load(url_main, datos, function () {
			//termina de cargar la ventana
			//resultadoBusqedaCI();
		});
	}
}