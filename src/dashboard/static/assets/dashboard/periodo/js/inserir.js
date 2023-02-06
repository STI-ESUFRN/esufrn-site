$("#classroom").change(function () {
    resetDate();
    getCalendar();

    $("#sala-selec").text($(this).find("option:selected").text());
    $("#sala-disp").prop("disabled", false);

    selected = $("#classroom option:selected");
});

$("#enviar-reserva").click(function (e) {
    e.preventDefault();

    var serialized_data = $("#form-reserva").serializeREST();
    $.ajax({
        type: "POST",
        url: "/api/periods/",
        data: serialized_data,
        success: function (response) {
            $("#form-reserva").trigger("reset");
            showMessage("Período inserido com sucesso", "alert-success");
        },
        error: function (response) {
            $("#form-reserva").fillErrors(response.responseJSON, (message) =>
                showMessage(message, "alert-danger")
            );
        },
    });
});
