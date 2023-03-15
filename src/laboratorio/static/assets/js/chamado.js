$("#chamado-form [name]").change(function () {
    $(this).removeClass("is-invalid");
});

$("#enviar-chamado").click(function (e) {
    e.preventDefault();

    $("#status-message").html("");
    $("#chamado-form input").removeClass("is-invalid");

    $.ajax({
        type: "POST",
        url: "/api/tickets/open/",
        data: $("#chamado-form").serializeREST(),
        success: function () {
            $("#status-message").html(`
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        <strong>Chamado cadastrado com sucesso.</strong>
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true"><i class="fas fa-times" aria-hidden="true"></i></span>
                        </button>
                    </div>
                `);
            $("#chamado-form").trigger("reset");
        },
        error: function (err) {
            console.error(err.responseJSON);
            $("#chamado-form").fillErrors(err.responseJSON);
        },
    });
});
