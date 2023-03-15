var localData = undefined;
function refreshData(ring = true) {
    $.get("/api/tickets/?status=P", function (response) {
        let results = JSON.stringify(response.results);
        if (localData != results) {
            localData = results;

            let data = response.results;
            $("#badgeChamados").text(response.count > 0 ? response.count : "");

            $("#lista-de-chamados").html("");
            $.each(data, (index, reserve) => {
                let row = $("<tr />", { "data-id-chamado": reserve.id });
                let a1 = $("<td />", { class: "text-center px-0 pl-2" });
                let a2 = $("<i />", { class: "fas fa-user-cog text-warning" });
                a1.append(a2);

                var now = new Date();
                let criado_ha_date = new Date(reserve.created);

                let criado_ha = criado_ha_date.toISOString();
                let title = $("<td />", { text: reserve.title });
                let requester = $("<td />", { text: reserve.requester });
                let contact = $("<td />", { text: reserve.contact });
                let e1 = $("<td />", {
                    class:
                        now - criado_ha_date > 1200000
                            ? "font-weight-bold text-danger"
                            : "font-weight-bold",
                });
                let e2 = $("<time />", {
                    text: criado_ha,
                    class: "timeago",
                    dateTime: criado_ha,
                });
                e1.append(e2);

                row.append(a1, title, requester, contact, e1);
                $("#lista-de-chamados").append(row);
            });
            $(".timeago").timeago();

            $("tr[data-id-chamado]").click(function (e) {
                e.preventDefault();
                fillCall(e.currentTarget.dataset.idChamado);
            });

            if (ring) {
                playAudio();
            }
        }
    });
}

var idSelecionado = undefined;
function fillCall(id) {
    idSelecionado = id;

    $("#detalhes").hide();
    $.get(`/api/tickets/${idSelecionado}/`, function (response) {
        fillAttributes(response);
        $("#detalhes").fadeTo("fast", 0).fadeTo("fast", 1).show();
    });
}

function patch(data) {
    $(".loader-global").addClass("load");
    $.ajax({
        url: `/api/tickets/${idSelecionado}/`,
        type: "PATCH",
        data: data,
        success: function (reserve) {
            if (reserve.status != "P") {
                refreshData();
                $("#detalhes").fadeTo("fast", 0).slideUp();
            }
            showMessage("Arquivo atualizado com sucesso", "alert-success");
            $(".loader-global").removeClass("load");
        },
        error: function (err) {
            showMessage(err.responseText, "alert-danger");
            $(".loader-global").removeClass("load");
        },
    });
}

refreshData(false);

setInterval(() => {
    refreshData();
    $("td:last-child:not(.text-danger).font-weight-bold").each(
        (index, element) => {
            var now = new Date();
            var then = new Date(element.lastChild.getAttribute("dateTime"));
            if (now - then > 1200000) {
                element.classList.value = "text-danger font-weight-bold";
                playAudio();
            }
        }
    );
}, 10000);

//--------------- LISTENERS ---------------
$("#confirmCall, #rejectCall").click(function (e) {
    e.preventDefault();
    patch({
        obs: $("#call-obs").val() ? $("#call-obs").val() : "",
        status: $(this).attr("data-status"),
    });
});

$("#obsCall").click(function (e) {
    e.preventDefault();
    patch({
        obs: $("#call-obs").val() ? $("#call-obs").val() : "",
    });
});

$("#detalhes-dismiss").click(() => {
    $("#detalhes").fadeTo("fast", 0).slideUp();
});
