var current_index = undefined;
var next = undefined;
var previous = undefined;

function fillItem() {
    $("#details").hide();
    $(".loader-global").addClass("load");
    let url = `/api/laboratory/consumables/${current_index}/`;
    $.get(url, (response) => {
        fillAttributes(response);

        $("#material-history").html("");
        $.get(`${url}history/`, (response) => {
            $.each(response, (index, item) => {
                let date = moment(item.created);
                let p = $("<p />", {
                    html: `
                        Em
                        ${date.format("DD/MM/YYYY")}
                        às
                        ${date.format("HH:mm")},
                        <strong>
                            ${item.user.username}
                            ${
                                item.diff > 0
                                    ? '<span class="text-success">adicionou</span>'
                                    : '<span class="text-danger">removeu</span>'
                            }
                        </strong>
                        ${Math.abs(item.diff)}
                        unidade${
                            item.diff != 1 ? "s" : ""
                        } deste material no inventário
                        (anterior: ${item.prev_quantity}).
                        <br/>
                    `,
                });
                $("#material-history").append(p);
            });

            $(".loader-global").removeClass("load");
            $("#details").fadeTo("fast", 0).fadeTo("fast", 1).show();
        });
    });
}

function updateButton(data, button) {
    if (data) {
        $(button).attr("disabled", false);
    } else {
        $(button).attr("disabled", true);
    }
}

function createMaterialRow(data) {
    let row = $("<tr />", {
        "data-id-item": data.id,
    });

    let icon = $("<td />", {
        class: "text-center px-0 pl-2",
        html: `<i class="fas fa-qrcode text-warning"></i>`,
    });
    let name = $("<td />", {
        text: data.name,
    });
    let quantity = $("<td />", {
        text: data.quantity,
        class: data.quantity <= data.alert_below ? "text-danger" : "",
    });
    let expiration = $("<td />", {
        text: moment(data.expiration).format("DD/MM/YYYY"),
    });
    let brand = $("<td />", {
        text: data.brand,
    });

    row.append(icon, name, brand, expiration, quantity);
    row.click(function (e) {
        e.preventDefault();
        current_index = e.currentTarget.dataset.idItem;
        fillItem();
    });

    return row;
}

function getAllMaterials(url = undefined) {
    $(".loader-global").addClass("load");

    if (!url) {
        let filters = $("[data-filter]").serialize();
        url = `/api/laboratory/consumables/dashboard/?${filters}`;
    }

    $.ajax({
        url: url,
        type: "GET",
        success: function (response) {
            $(".loader-global").removeClass("load");

            $("#materials-list").html("");
            $("#material-count").text(response.count);
            if (response.count) {
                $.each(response.results, (index, item) => {
                    let row = createMaterialRow(item);
                    $("#materials-list").append(row);
                });
                $("#materials-collapse").collapse("show");
            } else {
                $("#materials-collapse").collapse("hide");
            }

            next = response.next;
            updateButton(next, "#load-next");

            previous = response.previous;
            updateButton(previous, "#load-previous");
        },
    });
}

function getWarnMaterials() {
    $(".loader-global").addClass("load");

    let filters = $("[data-filter]").serialize();
    $.ajax({
        url: `/api/laboratory/consumables/alert/?${filters}`,
        type: "GET",
        success: function (response) {
            $(".loader-global").removeClass("load");

            let length = response.length;
            $("#critical-materials-list").html("");
            $("#critical-materials-count").text(length);
            if (length) {
                $.each(response, (index, item) => {
                    let row = createMaterialRow(item);
                    $("#critical-materials-list").append(row);
                });
                $("#critical-materials-collapse").collapse("show");
            } else {
                $("#critical-materials-collapse").collapse("hide");
            }
        },
    });
}

function getMaterials() {
    getAllMaterials();
    getWarnMaterials();
}

$(document).ready(function () {
    getMaterials();

    $("#details-dismiss").click(() => {
        $("#details").fadeTo("fast", 0).slideUp();
    });

    $("#filters").submit(function (e) {
        e.preventDefault();
    });

    $("[data-filter]").change(function () {
        getMaterials();
    });

    $("#load-previous").click(function (e) {
        e.preventDefault();
        getAllMaterials(previous);
    });

    $("#load-next").click(function (e) {
        e.preventDefault();
        getAllMaterials(next);
    });

    $("#delete-material").click(function (e) {
        e.preventDefault();
        $.ajax({
            url: `/api/laboratory/consumables/${current_index}/`,
            type: "DELETE",
            success: function (response) {
                showMessage("Material apagado com sucesso.", "alert-success");
                getMaterials();
            },
            error: function (response) {
                showMessage("Algo deu errado", "alert-danger");
            },
        });
    });

    $("#patch-comment").click(function (e) {
        e.preventDefault();
        $.ajax({
            url: `/api/laboratory/consumables/${current_index}/`,
            type: "PATCH",
            data: {
                comments: $("[data-attribute=comments]").val(),
            },
            success: function (response) {
                showMessage("Observação salva com sucesso", "alert-success");
            },
            error: function (response) {
                showMessage("Algo deu errado", "alert-danger");
            },
        });
    });

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

    $("#create-material-form [name]").change(function () {
        $(this).removeClass("is-invalid");
    });

    $("#create-material-form [name=quantity]").on("input", function () {
        $("#create-material-form [name=alert_below]").val(
            Math.trunc($(this).val() * 0.25)
        );
    });

    $("#create-material").click(function (e) {
        e.preventDefault();

        let serialized_data = $("#create-material-form").serializeREST();
        $.ajax({
            type: "POST",
            url: "/api/laboratory/consumables/",
            dataType: "json",
            data: serialized_data,
            success: function (response) {
                showMessage(
                    "Material cadastrado com sucesso.",
                    "alert-success"
                );
                getMaterials();
                $("#add-material").modal("hide");
                $("#create-material-form").trigger("reset");
            },
            error(response) {
                $("#create-material-form").fillErrors(
                    response.responseJSON,
                    (message) => showMessage(message, "text-danger")
                );
            },
        });
    });

    $("#quantity").ke;
});
