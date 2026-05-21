$("#form-chamado input").change(function () {
    $(this).removeClass("is-invalid");
});

$("#sala-select").change(function () {
    const isOther = $(this).val() === "__other__";

    if (isOther) {
        $("#sala-outros-row").removeClass("d-none");
        $("#sala-outros").attr("required", true);
    } else {
        $("#sala-outros-row").addClass("d-none");
        $("#sala-outros").removeAttr("required").val("");
    }
});

// Character counters for description and obs
function updateRemaining(element, counterId) {
    const max = parseInt($(element).attr('maxlength') || 300, 10);
    const len = $(element).val().length;
    $(`#${counterId}`).text(Math.max(0, max - len));
}

$(document).ready(function() {
    // initialize counters
    updateRemaining('#description', 'descRemaining');
    updateRemaining('#obs', 'obsRemaining');

    $('#description').on('input', function() { updateRemaining(this, 'descRemaining'); });
    $('#obs').on('input', function() { updateRemaining(this, 'obsRemaining'); });
});

$("#enviar-chamado").click(function (e) {
    e.preventDefault();

    $("#form-chamado [name]").removeClass("is-invalid");

    var error = false;

    var form_requester = $("#form-chamado [name=requester]");
    error += validate(form_requester, form_requester.val());

    var form_date = $("#form-chamado [name=date]");
    error += validate(form_date, form_date.val());

    var form_sala = $("#form-chamado [name=sala]");
    error += validate(form_sala, form_sala.val());

    if (form_sala.val() === "__other__") {
        var form_sala_outros = $("#form-chamado [name=sala_outros]");
        error += validate(form_sala_outros, form_sala_outros.val());
    }

    var form_equipment = $("#form-chamado [name=equipment]");
    error += validate(form_equipment, form_equipment.val());

    var form_tombamento = $("#form-chamado [name=tombamento]");
    error += validate(form_tombamento, form_tombamento.val());

    var form_description = $("#form-chamado [name=description]");
    error += validate(form_description, form_description.val());

    var form_status = $("#form-chamado [name=status]");
    error += validate(form_status, form_status.val());

    var form_responsible = $("#form-chamado [name=responsible_technician]");
    error += validate(form_responsible, form_responsible.val());

    let data = new FormData($("#form-chamado")[0]);

    if (data.get("sala") === "__other__") {
        data.delete("sala");
    } else {
        data.delete("sala_outros");
    }

    if (!error) {
        $.ajax({
            type: "POST",
            url: "/api/tickets/",
            data: data,
            processData: false,
            contentType: false,
            success: function () {
                $("#form-chamado").trigger("reset");
                showMessage("Chamado cadastrado com sucesso", "alert-success");
            },
            error: function (err) {
                showMessage(err.responseText, "alert-danger");
            },
        });
    } else {
        showMessage("Corrija os erros", "alert-warning");
    }
});
