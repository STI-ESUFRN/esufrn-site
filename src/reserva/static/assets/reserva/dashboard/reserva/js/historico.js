var localData = [];
var next = undefined;
var previous = undefined;
var idSelected = undefined;
var baseUrl = "/api/reserves";

function refreshData(url = undefined) {
    if (!url) {
        let filters = $("[data-filter]").serialize();
        url = `${baseUrl}/historico?${filters}`;
    }

    $("#load-antigo,#load-recente").attr("disabled", true);
    $.get(url, (response) => {
        localData = response["results"];
        $("#lista-de-chamados").html("");
        $.each(localData, function (i, v) {
            let row = $("<tr />", { "data-id-chamado": v.id });
            let fa = $("<td />", { class: "text-center px-0" });
            let a2 = $("<i />", {
                class:
                    v.status == "A"
                        ? "fas fa-check-circle text-success"
                        : v.status == "R"
                        ? "fas fa-times-circle text-danger"
                        : "fas fa-solid fa-circle-minus text-secondary",
            });
            fa.append(a2);

            let fa_calendar = $("<td />", {
                class: "text-center px-0",
                html: v.admin_created
                    ? '<i class="fas fa-key"></i>'
                    : '<i class="fas fa-calendar-alt"></i>',
            });
            let classroom = $("<td />", { text: v.classroom.full_name });
            let event = $("<td />", { text: v.event, title: v.event });
            let requester = $("<td />", {
                text: v.requester,
                title: v.requester,
            });
            let date = $("<td />", {
                text: moment(v.date).format("DD/MM/YYYY"),
                class: "font-weight-bold text-center",
            });

            row.append(fa, fa_calendar, classroom, event, requester, date);
            $("#lista-de-chamados").append(row);
        });
        $(".timeago").timeago();

        $("tr[data-id-chamado]").click(function (e) {
            e.preventDefault();
            fillReserve(e.currentTarget.dataset.idChamado);
        });

        next = response.next;
        updateButton(next, "#load-antigo");

        previous = response.previous;
        updateButton(previous, "#load-recente");
    });
}

function updateButton(data, button) {
    if (data) {
        $(button).attr("disabled", false);
    } else {
        $(button).attr("disabled", true);
    }
}

function fillReserve(id) {
    $("#detalhes").hide();

    var reserve = Object.assign({}, localData.filter((v) => v.id == id)[0]);
    fillAttributes(reserve);

    idSelected = reserve.id;

    let v = $("[data-attribute=status]");
    if (reserve.status == "A") {
        v.html('Aceito <i class="fas fa-check-circle text-success"></i>');
    } else if (reserve.status == "R") {
        v.html('Rejeitado <i class="fas fa-times-circle text-danger"></i>');
    } else {
        v.html(
            'Cancelado <i class="fas fa-solid fa-circle-stop text-secondary"></i>'
        );
    }

    $("#detalhes").fadeTo("fast", 0).fadeTo("fast", 1).show();
}

function update(data) {
    $.ajax({
        url: `${baseUrl}/${idSelected}/`,
        type: "PATCH",
        data: data,
        success: function (response) {
            $(".loader-global").removeClass("load");
            refreshData();
            $("#detalhes").fadeTo("fast", 0).slideUp();
            showMessage("Alterado com sucesso.", "alert-success");
        },
        error: function (err) {
            $(".loader-global").removeClass("load");
            fillErrors(err.responseJSON, (e) => showMessage(e, "alert-danger"));
        },
    });
}

$(document).ready(function () {
    $("#load-antigo").click(function (e) {
        e.preventDefault();
        refreshData(next);
    });

    $("#load-recente").click(function (e) {
        e.preventDefault();
        refreshData(previous);
    });

    $("[data-submit=reserve]").click(function (e) {
        e.preventDefault();
        $(".loader-global").addClass("load");
        update({
            obs: $("[data-attribute=obs]").val()
                ? $("[data-attribute=obs]").val()
                : "",
            status: $(this).attr("data-status"),
            msg: $("#reserve-email").val(),
        });
    });

    $("#obsReserve").click(function (e) {
        e.preventDefault();
        update({
            obs: $("[data-attribute=obs]").val()
                ? $("[data-attribute=obs]").val()
                : "",
        });
    });

    $("[data-filter]").change(function () {
        refreshData();
    });

    $("#detalhes-dismiss").click(function () {
        $("#detalhes").fadeTo("fast", 0).slideUp();
    });

    getOptions(refreshData);
});
