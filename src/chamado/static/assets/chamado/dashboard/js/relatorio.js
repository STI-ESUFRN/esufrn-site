$(document).on('click', '.ver-mais', function(e){
    e.preventDefault();

    const description = $(this).attr('data-description') || '';
    const obs = $(this).attr('data-obs') || '';

    const esc = function(str){
        if(!str) return '---';
        return $('<div/>').text(str).html().replace(/\n/g, '<br/>');
    };

    const html = `
        <div><h5>Descrição</h5><p>${esc(description)}</p></div>
        <div><h5>Observações</h5><p>${esc(obs)}</p></div>
    `;

    // create or reuse modal
    let $modal = $('#verMaisModal');
    if ($modal.length === 0) {
        $modal = $("<div class='modal fade' id='verMaisModal' tabindex='-1' role='dialog' aria-hidden='true'>\
            <div class='modal-dialog modal-lg' role='document'>\
                <div class='modal-content'>\
                    <div class='modal-header'>\
                        <h5 class='modal-title'>Detalhes</h5>\
                        <button type='button' class='close' data-dismiss='modal' aria-label='Fechar'>\
                            <span aria-hidden='true'>&times;</span>\
                        </button>\
                    </div>\
                    <div class='modal-body'></div>\
                </div>\
            </div>\
        </div>");
        $('body').append($modal);
    }

    $modal.find('.modal-body').html(html);
    $modal.modal('show');
});

// Ensure print-only / no-print classes behave via CSS in template; no extra JS needed.
