var pathArray = window.location.pathname.split("/");
var id = pathArray[pathArray.length - 1] || pathArray[pathArray.length - 2];

$('[data-toggle="datepicker"]').datepicker({
    format: "dd-mm-yyyy",
    months: [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ],
    daysMin: ["D", "S", "T", "Q", "Q", "S", "S"],
});
$("#deletePeriod").click(function (e) {
    $.ajax({
        type: "DELETE",
        url: `/api/laboratory/consumables/${id}/`,
        success: function (response) {
            window.location.replace("/dashboard");
        },
        error: function (response) {
            showMessage(
                "Ocorreu um erro durante a exclusão do material.",
                "alert-danger"
            );
        },
    });
});

function atualizarQuantidade(serialized_data) {
    $.ajax({
        type: "POST",
        url: `/api/laboratory/consumables/${id}/add/`,
        dataType: "json",
        data: serialized_data,
        success: function (response) {
            showMessage("Material atualizado com sucesso.", "alert-success");
            $("#atualizar-quantidade [name]").removeClass("is-invalid");
            $("#atualizar-quantidade").trigger("reset");
            fillMaterial();
        },
        error(response) {
            $.map(response.responseJSON, (value, label) => {
                $(`#atualizar-quantidade [name=${label}]`).addClass(
                    "is-invalid"
                );
                let feedback = $(
                    `#atualizar-quantidade .invalid-feedback[for=${label}]`
                );
                feedback.html("");
                value.forEach((message) => {
                    error = $("<p />", {
                        html: message,
                    });
                    feedback.append(error);
                });
            });
        },
    });
}

function serialize(form) {
    let serialized_array = form.serializeArray();
    let serialized_data = {};
    for (key in serialized_array) {
        serialized_data[serialized_array[key]["name"]] =
            serialized_array[key]["value"];
    }

    return serialized_data;
}

$("#adicionar").click(function (e) {
    e.preventDefault();

    let serialized_data = serialize($("#atualizar-quantidade"));
    atualizarQuantidade(serialized_data);
});
$("#remover").click(function (e) {
    e.preventDefault();

    let serialized_data = serialize($("#atualizar-quantidade"));
    serialized_data.quantity = serialized_data.quantity * -1;
    atualizarQuantidade(serialized_data);
});

$("#atualizar-instancia").click(function (e) {
    e.preventDefault();
    let serialized_data = $("#form-item").serializeREST();

    $.ajax({
        type: "PATCH",
        url: `/api/laboratory/consumables/${id}/`,
        dataType: "json",
        data: serialized_data,
        success: function (response) {
            showMessage("Material atualizado com sucesso.", "alert-success");
            $("#form-item [name]").removeClass("is-invalid");
            fillMaterial();
        },
        error(response) {
            $.map(response.responseJSON, (value, label) => {
                $(`#form-item [name=${label}]`).addClass("is-invalid");
                let feedback = $(`.invalid-feedback[for=${label}]`);
                feedback.html("");
                value.forEach((message) => {
                    error = $("<p />", {
                        html: message,
                    });
                    feedback.append(error);
                });
            });
        },
    });
});

function fillMaterial() {
    $.get(`/api/laboratory/consumables/${id}/`, (response) => {
        fillAttributes(response);
        $.get(`/api/laboratory/consumables/${id}/history/`, (history) => {
            $("#history").html("");
            history.forEach((entry) => {
                let created = moment(entry.created);
                let action =
                    entry.diff > 0
                        ? '<span class="text-success">adicionou</span>'
                        : '<span class="text-danger">removeu</span>';
                let unit = `${response.measure_unit}${
                    Math.abs(entry.diff) != 1 ? "s" : ""
                }`;

                $("#history").append(`
                    Em ${created.format("DD/MM/YYYY")} 
                    às ${created.format("HH:MM")}, <b>${entry.user.username}</b>
                    <strong>
                        ${action}
                    </strong>
                    ${Math.abs(entry.diff)} ${unit}
                    deste material no inventário
                    (anterior: ${entry.prev_quantity}).
                    <br />
                `);
            });
        });
    });
}

$(document).ready(function () {
    fillMaterial();
});
