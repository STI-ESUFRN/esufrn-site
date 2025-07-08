var current_index = undefined;
var next = undefined;
var previous = undefined;

function fillItem() {
    $("#details").hide();
    $(".loader-global").addClass("load");
    let url = `/api/laboratory/ti/permanents/${current_index}/`;
    $.get(url, (response) => {
        fillAttributes(response);

        $("#editMaterial").attr("href", `${window.location.pathname}${current_index}/`);

        $(".loader-global").removeClass("load");
        $("#details").fadeTo("fast", 0).fadeTo("fast", 1).show();
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
    let number = $("<td />", {
        text: data.number,
    });
    let status = $("<td />", {
        text: data.status_display,
    });
    let brand = $("<td />", {
        text: data.brand,
    });

    row.append(icon, name, number, brand, status);
    row.click(function (e) {
        e.preventDefault();
        current_index = e.currentTarget.dataset.idItem;
        fillItem();
    });

    return row;
}

function getMaterials(url = undefined) {
    $(".loader-global").addClass("load");

    if (!url) {
        let filters = $("[data-filter]").serialize();
        url = `/api/laboratory/ti/permanents/?${filters}`;
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

function getCategories() {
    $.ajax({
        url: "/api/laboratory/ti/categories/",
        type: "GET",
        success: function (response) {
            $("#category").html("");
            $("#category-filter").html("");
            response.forEach((value) => {
                let opt = `<option value=${value.id}>${value.name}</option>`;
                $("#category").append(opt);
                $("#category-filter").append(opt);
            });
        },
        error: function (response) {
            $("#form-item").fillErrors(response.responseJSON, (message) =>
                showMessage(message, "alert-danger")
            );
        },
    });
}

function getStatuses() {
    $.ajax({
        url: "/api/laboratory/ti/permanents/",
        type: "OPTIONS",
        success: function (response) {
            $.map(response.actions.POST.status.choices, (value, index) => {
                let opt = `<option value=${value.value}>${value.display_name}</option>`;
                $("#status").append(opt);
                $("#status-filter").append(opt);
            });
        },
    });
}

function getWarehouses(callback = undefined) {
    $.get(`/api/laboratory/ti/warehouses/`, function (response) {
        response.forEach((element) => {
            let opt = `<option value=${element.id}>${element.name}</option>`;
            $("#warehouse").append(opt);
            $("[name=warehouse_ti][data-filter]").append(opt);
        });

        if (callback) {
            callback();
        }
    });
}

$(document).ready(function () {
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
        getMaterials(previous);
    });

    $("#load-next").click(function (e) {
        e.preventDefault();
        getMaterials(next);
    });

    $("#delete-material").click(function (e) {
        e.preventDefault();
        $.ajax({
            url: `/api/laboratory/ti/permanents/${current_index}/`,
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
            url: `/api/laboratory/ti/permanents/${current_index}/`,
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

    $("#form-item [name]").change(function () {
        $(this).removeClass("is-invalid");
    });

    $("#create-material").click(function (e) {
        e.preventDefault();

        let serialized_data = $("#form-item").serializeREST();
        $.ajax({
            type: "POST",
            url: "/api/laboratory/ti/permanents/",
            dataType: "json",
            data: serialized_data,
            success: function (response) {
                showMessage(
                    "Material cadastrado com sucesso.",
                    "alert-success"
                );
                getMaterials();
                $("#add-material").modal("hide");
                $("#form-item").trigger("reset");
            },
            error(response) {
                console.error(response);
                $("#form-item").fillErrors(response.responseJSON, (message) =>
                    showMessage(message, "text-danger")
                );
            },
        });
    });

    $("#add-category").click(function (e) {
        e.preventDefault();
    });

    $("#new-category-modal").on("hidden.bs.modal", function (e) {
        $("#add-material").modal("show");
    });
    $("#new-category-modal").on("show.bs.modal", function (e) {
        $("#add-material").modal("hide");
    });

    $("#create-category").click(function (e) {
        e.preventDefault();

        serialized_data = $("#form-category").serializeREST();
        $.ajax({
            url: "/api/laboratory/ti/categories/",
            type: "POST",
            data: serialized_data,
            success: function (response) {
                getCategories();
                $("#new-category-modal").modal("hide");
                $("#form-category").trigger("reset");
            },
            error: function (response) {
                console.error(response);
                $("#form-category").fillErrors(
                    response.responseJSON,
                    (message) => showNonFieldErrorMessage(message, "errors")
                );
            },
        });
    });

    $("#del-category").click(function (e) {
        e.preventDefault();
        $("#form-errors").html("");
        $.ajax({
            url: `/api/laboratory/ti/categories/${$("#category").val()}/`,
            type: "DELETE",
            success: function (response) {
                getCategories();
            },
            error: function (response) {
                showMessage();
                $("#form-item").fillErrors(response.responseJSON, (message) =>
                    showMessage(message, "alert-danger")
                );
            },
        });
    });

    getWarehouses(() => {
        getMaterials();
        getStatuses();
        getCategories();
    });
});
