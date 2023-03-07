var baseUrl = "/api/reserves";

var calendario = new ReservationCalendar({
    weekName: [
        "Domingo",
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
        "Sábado",
    ],
    dayName: "Dia",
    varNames: {
        date: "date",
        event: "event",
        status: {
            name: "status",
            confirmed: "A",
            refused: "R",
            waiting: "E",
        },
        shift: "shift",
    },
});

var mesAtual = undefined;
var anoAtual = undefined;
var salaAtual = undefined;

var localData = [];
var idSelecionado = undefined;

const mesNome = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
];

function getCalendar() {
    $("#nome-mes").text(`${mesNome[mesAtual - 1]} / ${anoAtual}`);

    $.ajax({
        type: "GET",
        url: `/api/calendar?date__year=${anoAtual}&date__month=${mesAtual}&classroom=${salaAtual}`,
        dataType: "json",
        success: function (response) {
            calendario.updateCalendar(response, anoAtual, mesAtual);
        },
    });
}
function createRow(data) {
    let row = $("<tr />", { "data-id-chamado": data.id });
    let fa = $("<td />", { class: "text-center px-0 pl-2" });
    let a2 = $("<i />", { class: "far fa-calendar-alt text-warning" });
    fa.append(a2);

    let now = new Date();
    let date = $("<td />", {
        text: moment(data.date).format("DD/MM/YYYY"),
        class: "text-center",
    });
    let classroom = $("<td />", { text: data.classroom.full_name });
    let event = $("<td />", { text: data.event });
    let requester = $("<td />", { text: data.requester });
    let criado_ha_date = new Date(data.created);
    let criado_ha = criado_ha_date.toISOString();
    let elapsed = $("<td />", {
        class: `text-center font-weight-bold ${
            now - criado_ha_date > 1200000 ? "text-danger" : ""
        }`,
    });
    let ago = $("<time />", {
        text: criado_ha,
        class: "timeago",
        dateTime: criado_ha,
    });
    elapsed.append(ago);

    row.append(fa, event, classroom, requester, date, elapsed);
    row.click(function (e) {
        e.preventDefault();
        fillReserve(e.currentTarget.dataset.idChamado);
    });
    return row;
}
function updateDash(data = []) {
    localData = data;

    $("#lista-de-chamados").html("");
    $.each(data, function (i, reserve) {
        let row = createRow(reserve);
        $("#lista-de-chamados").append(row);
    });
    $(".timeago").timeago();
}

function refreshData(force = false, ring = true) {
    $.ajax({
        type: "GET",
        url: "/api/reserves/dashboard/",
        success: function (response) {
            if (
                JSON.stringify(localData) != JSON.stringify(response) ||
                force
            ) {
                updateDash(response);
                if (ring) {
                    playAudio();
                }
                $("#badgeChamados").text(response.length);
            }
        },
    });
}

function fillReserve(id) {
    $("#detalhes").hide();

    var reserve = Object.assign({}, localData.filter((v) => v.id == id)[0]);
    fillAttributes(reserve);

    idSelecionado = reserve.id;

    let date = new Date(reserve.date);
    anoAtual = date.getFullYear();
    mesAtual = date.getMonth() + 1;
    salaAtual = reserve.classroom.id;

    getCalendar();

    $("#detalhes").fadeTo("fast", 0).fadeTo("fast", 1).show();
}

function update(data) {
    $.ajax({
        url: `/api/reserves/${idSelecionado}/`,
        type: "PATCH",
        data: data,
        success: function (response) {
            $(".loader-global").removeClass("load");
            refreshData(true);
            $("#detalhes").fadeTo("fast", 0).slideUp();
            showMessage("Reserva atualizada com sucesso.", "alert-success");
        },
        error: function (err) {
            $(".loader-global").removeClass("load");
            fillErrors(err.responseJSON, (e) => showMessage(e, "alert-danger"));
        },
    });
}

function prevMonth() {
    if (mesAtual == 1) {
        anoAtual -= 1;
        mesAtual = 12;
    } else {
        mesAtual -= 1;
    }
    getCalendar();
}

function nextMonth() {
    if (mesAtual == 12) {
        anoAtual += 1;
        mesAtual = 1;
    } else {
        mesAtual += 1;
    }
    getCalendar();
}

$(document).ready(function () {
    $("#detalhes-dismiss").click(function () {
        $("#detalhes").fadeTo("fast", 0).slideUp();
    });

    $("[data-submit=reserve]").click(function (e) {
        e.preventDefault();
        $(".loader-global").addClass("load");
        update({
            status: $(this).attr("data-status"),
            obs: $("#reserve-obs").val() ? $("#reserve-obs").val() : "",
            msg: $("#reserve-email").val(),
        });
    });

    $("#obsReserve").click(function (e) {
        e.preventDefault();
        update({
            obs: $("#reserve-obs").val() ? $("#reserve-obs").val() : "",
        });
    });

    getOptions(refreshData, false, false);

    setInterval(() => {
        refreshData();
        $("td:last-child:not(.text-danger).font-weight-bold").each(function (
            index,
            element
        ) {
            var now = new Date();
            var then = new Date(element.lastChild.getAttribute("dateTime"));
            if (now - then > 1200000) {
                element.classList.value = "text-danger font-weight-bold";
                playAudio();
            }
        });
    }, 10000);
});
