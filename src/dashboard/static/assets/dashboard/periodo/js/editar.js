function changeClassroom() {
    resetDate();
    getCalendar();

    $("#sala-selec").text($("#classroom").find("option:selected").text());
    $("#sala-disp").prop("disabled", false);

    selected = $("#classroom option:selected");
}

$("#classroom").change(function () {
    changeClassroom();
});

$("#enviar-reserva").click(function (e) {
    e.preventDefault();

    var serialized_data = $("#form-reserva").serializeREST();
    let id = $("[name=id]").val();
    $.ajax({
        type: "PATCH",
        url: `/api/periods/${id}/`,
        data: serialized_data,
        success: function (response) {
            console.log(response);
            showMessage("Período atualizado com sucesso.", "alert-success");
        },
        error: function (response) {
            $("#form-reserva").fillErrors(response.responseJSON, (message) =>
                showMessage(message, "alert-danger")
            );
        },
    });
});

$(document).ready(function () {
    changeClassroom();
});
