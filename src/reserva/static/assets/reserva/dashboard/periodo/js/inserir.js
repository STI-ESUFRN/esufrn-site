$("#classroom").change(function () {
    resetDate();
    getCalendar();

    $("#sala-selec").text($(this).find("option:selected").text());
    $("#sala-disp").prop("disabled", false);

    selected = $("#classroom option:selected");
});

$("#enviar-reserva").click(function (e) {
    e.preventDefault();

    $("#enviar-reserva").attr("disabled", true);
    var serialized_data = $("#form-reserva").serializeREST();
    $.ajax({
        type: "POST",
        url: "/api/periods/",
        data: serialized_data,
        success: function (response) {
            $("#form-reserva").trigger("reset");
            showMessage("Período inserido com sucesso", "alert-success");
            $("#enviar-reserva").attr("disabled", false);
        },
        error: function (response) {
            console.error(response);
            $("#form-reserva").fillErrors(response.responseJSON, (message) =>
                showMessage(message, "alert-danger")
            );
            $("#enviar-reserva").attr("disabled", false);
        },
    });
});
