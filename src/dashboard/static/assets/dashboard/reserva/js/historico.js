var localData = [];
var next = undefined;
var previous = undefined;
function refreshData(url = undefined) {
    if (!url) {
        let filters = $("[data-filter]").serialize();
        url = `/api/reservas/historico?${filters}`;
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
                        : "fas fa-times-circle text-danger",
            });
            fa.append(a2);

            let fa_calendar = $("<td />", {
                class: "text-center px-0",
                html: v.admin_created
                    ? '<i class="fas fa-key"></i>'
                    : '<i class="far fa-calendar-alt"></i>',
            });

            let classroom = $("<td />", { text: v.classroom.full_name });
            let criado_ha_date = new Date(v.created);
            let criado_ha = criado_ha_date.toLocaleDateString();
            let event = $("<td />", { text: v.event, title: v.event });
            let requester = $("<td />", {
                text: v.requester,
                title: v.requester,
            });
            let e1 = $("<td />", {
                text: criado_ha,
                title: criado_ha,
                class: "font-weight-bold text-center",
            });

            row.append(fa, fa_calendar, classroom, event, requester, e1);
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

var idSelected = undefined;
function fillReserve(id) {
    $("#detalhes").hide();

    var reserve = Object.assign({}, localData.filter((v) => v.id == id)[0]);
    fillAttributes(reserve);

    idSelected = reserve.id;

    let v = $("[data-attribute=status]");
    if (v.text() == "A") {
        v.html('Aceito <i class="fas fa-check-circle text-success"></i>');
    } else {
        v.html('Rejeitado <i class="fas fa-times-circle text-danger"></i>');
    }

    $("#detalhes").fadeTo("fast", 0).fadeTo("fast", 1).show();
}

// ------------------------------------------------------------------- Listeners

$("#filtro, #ordem").change(function (e) {
    e.preventDefault();
    refreshData();
});

$("#load-antigo").click(function (e) {
    e.preventDefault();
    refreshData(next);
});

$("#load-recente").click(function (e) {
    e.preventDefault();
    refreshData(previous);
});

// ------------------------------------------------------------------- Update
function update(data) {
    $.ajax({
        url: `/api/reservas/${idSelected}/`,
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
            $.each(err.responseJSON["details"], (e) => {
                showMessage(e, "alert-danger");
            });
        },
    });
}
$("#confirmReserve, #rejectReserve, #waitReserve").click(function (e) {
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
// -------------------------------------
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
// ------------------------------------------------------------------- Init
refreshData();
