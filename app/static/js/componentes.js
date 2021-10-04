
function mostrarImagenComponente(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchComponente() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormComponente(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'componenteSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Componentes!', 'Esta seguro de querer adicionar este componente?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Componentes!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'componenteWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'componenteSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Componentes!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Componentes!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'componenteWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'componenteDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Componentes!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function componenteSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function componenteWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function componenteDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}