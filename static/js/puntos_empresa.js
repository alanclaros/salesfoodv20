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


function desplegarZonas(ciudad_id) {
	img_ciudad = document.getElementById('img_' + ciudad_id);
	src = img_ciudad.src;
	pos = src.indexOf('desplegar');

	if (pos > 0) {
		//click en desplegar
		img_ciudad.src = '/static/img/png/contraer.png';
		imagen = '<img src="/static/img/pass/loading2.gif">';
		url_main = '/puntosempresa/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'ciudad': ciudad_id,
			'operation_x': 'zonas',
			'csrfmiddlewaretoken': token,
		}

		div_zonas = "#div_zonas_" + ciudad_id;

		$(div_zonas).fadeIn('slow');
		$(div_zonas).html(imagen);
		$(div_zonas).load(url_main, datos, function () {
			//termina de cargar la ventana
			resultadoZona();
		});
	}
	else {
		//click contraer
		img_ciudad.src = '/static/img/png/desplegar.png';
		div_zonas = "#div_zonas_" + ciudad_id;
		$(div_zonas).html('');
	}
}

function resultadoZona() {
	return true;
}

//sucursales
function desplegarSucursales(zona_id) {
	img_zona = document.getElementById('imgz_' + zona_id);
	src = img_zona.src;
	pos = src.indexOf('desplegar');

	if (pos > 0) {
		//click en desplegar
		img_zona.src = '/static/img/png/contraer.png';
		imagen = '<img src="/static/img/pass/loading2.gif">';
		url_main = '/puntosempresa/';
		token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
		datos = {
			'zona': zona_id,
			'operation_x': 'sucursales',
			'csrfmiddlewaretoken': token,
		}

		div_sucursales = "#div_sucursales_" + zona_id;

		$(div_sucursales).fadeIn('slow');
		$(div_sucursales).html(imagen);
		$(div_sucursales).load(url_main, datos, function () {
			//termina de cargar la ventana
			resultadoSucursal();
		});
	}
	else {
		//click contraer
		img_zona.src = '/static/img/png/desplegar.png';
		div_sucursales = "#div_sucursales_" + zona_id;
		$(div_sucursales).html('');
	}
}

function resultadoSucursal() {
	return true;
}