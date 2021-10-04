
function mostrarImagenInsumo(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchInsumo() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormInsumo(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'insumoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Insumos!', 'Esta seguro de querer adicionar este insumo?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Insumos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'insumoWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'insumoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Insumos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Insumos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'insumoWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'insumoDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Insumos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function insumoSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function insumoWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function insumoDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}