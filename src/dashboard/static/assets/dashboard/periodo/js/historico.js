var next = undefined;
var previous = undefined;
var currentPeriod = undefined;
var baseUrl = "/api/periods";

calendario = new ReservationCalendar({
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

var mesAtual = undefined;
var anoAtual = undefined;

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

$("#escolheMes").html(`
	<div class="row justify-content-around my-4">
		<div class="col my-auto text-center">
			<button onclick='prevMonth()' class="btn btn-dark"><i class="fas fa-chevron-left" aria-hidden="true"></i></button>
		</div>
		<div class="col my-auto text-center">
			<h5 id="nome-mes" class="m-0">${mesNome[mesAtual - 1]} / ${anoAtual}</h5>
		</div>
		<div class="col my-auto text-center">
			<button onclick='nextMonth()' class="btn btn-dark"><i class="fas fa-chevron-right" aria-hidden="true"></i></button>
		</div>
	</div>
`);

var sala = undefined;
function getCalendar() {
    $("#nome-mes").text(`${mesNome[mesAtual - 1]} / ${anoAtual}`);

    $.ajax({
        type: "GET",
        url: `/api/calendar/?date__year=${anoAtual}&date__month=${mesAtual}&classroom=${sala}`,
        dataType: "json",
        success: function (response) {
            calendario.updateCalendar(response, anoAtual, mesAtual);
        },
    });
}

function updateButton(data, button) {
    if (data) {
        $(button).attr("disabled", false);
    } else {
        $(button).attr("disabled", true);
    }
}

function createRow(data) {
    let row = $("<tr />", { "data-period-id": data.id });

    let status_fa = $("<td />", {
        class: "text-center px-0 pl-2",
        html: `<i class="${
            data.status == "A"
                ? "fa fa-check-circle text-success"
                : data.status == "R"
                ? "fa fa-times-circle text-danger"
                : "fa fa-solid fa-clock text-warning"
        }">`,
    });
    let calendar_fa = $("<td />", {
        class: "text-center",
        html: `<i class="fas fa-calendar" aria-hidden="true"></i>`,
    });
    let classname = $("<td />", { text: data.classname });
    let classroom = $("<td />", {
        text: data.classroom.full_name,
    });

    let shift = $("<td />", {
        text: $.map(data.shift, function (value) {
            return choices.shift[value];
        }).join(", "),
    });
    let requester = $("<td />", { text: data.requester });

    let date_begin = $("<td />", {
        class: "text-center",
        text: moment(data.date_begin).format("DD-MM-YYYY"),
    });
    let date_end = $("<td />", {
        class: "text-center",
        text: moment(data.date_end).format("DD-MM-YYYY"),
    });

    row.append(
        status_fa,
        calendar_fa,
        classname,
        classroom,
        shift,
        requester,
        date_begin,
        date_end
    );

    row.click(function (e) {
        e.preventDefault();
        currentPeriod = e.currentTarget.dataset.periodId;
        showDetails();
    });

    return row;
}

function updateList(url) {
    $(".loader-global").addClass("load");
    if (!url) {
        let filters = $("[data-filter]").serialize();
        url = `${baseUrl}/?${filters}`;
    }

    disableControls();

    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            $("#lista-de-chamados").html("");
            $.each(response.results, (index, value) => {
                let row = createRow(value);
                $("#lista-de-chamados").append(row);
            });

            next = response.next;
            updateButton(next, "#load-next");

            previous = response.previous;
            updateButton(previous, "#load-previous");

            $(".loader-global").removeClass("load");
            $("#period-list").fadeIn("fast");
        },
    });
}

function showDetails() {
    $("#period-details").animate({ opacity: 0 }, "fast", function () {
        updateDetails();
    });
}

function createDayRow(data) {
    let row = $("<tr />");
    let day = $("<td />", {
        text: moment(data.date).format("DD/MM/YYYY"),
        style: "vertical-align: middle;",
    });
    let shift = $("<td />", {
        text: choices.shift[data.shift],
    });
    let statusLabel = $("<td />", {
        text: data.active ? "Ativo" : "Cancelado",
        style: "vertical-align: middle;",
    });

    let action = $("<button />", {
        html: data.active
            ? '<i class="fas fa-pause" aria-hidden="true"></i>'
            : '<i class="fas fa-play" aria-hidden="true"></i>',
        class: `btn btn-sm ${
            data.active ? "btn-outline-danger" : "btn-outline-primary"
        }`,
        "data-day-id": data.id,
        "data-day-active": data.active,
    });
    let td = $("<td />", { class: "text-center" });
    td.append(action);
    row.append(day, shift, statusLabel, td);

    action.click(function (e) {
        let data = e.currentTarget.dataset;
        updateDay(data.dayId, {
            active: data.dayActive == "true" ? false : true,
        });
    });

    return row;
}

function updateDetails() {
    $("#editButton").attr("href", `/dashboard/periodo/editar/${currentPeriod}`);
    $.ajax({
        type: "GET",
        url: `${baseUrl}/${currentPeriod}/`,
        success: function (response) {
            fillAttributes(response);

            let date = new Date(response.date_begin);
            let _sala = response.classroom.id;
            let _anoAtual = date.getFullYear();
            let _mesAtual = date.getMonth() + 1;
            if (
                _sala != sala ||
                _anoAtual != anoAtual ||
                _mesAtual != mesAtual
            ) {
                sala = _sala;
                anoAtual = _anoAtual;
                mesAtual = _mesAtual;
                $("#sala-selec").text(response.classroom.full_name);
                getCalendar();
            }

            $.ajax({
                url: `${baseUrl}/${response.id}/days/`,
                type: "GET",
                success: function (response) {
                    $("#perioddays").html("");

                    let activedays = 0;
                    let cancelleddays = 0;
                    let totaldays = response.length;
                    $.each(response, (index, value) => {
                        let row = createDayRow(value);
                        $("#perioddays").append(row);

                        value.active ? activedays++ : cancelleddays++;
                    });
                    $("#totaldays").text(totaldays);
                    $("#activedays").text(
                        `${activedays}(${(
                            (activedays / totaldays) *
                            100
                        ).toFixed(2)}%)`
                    );
                    $("#cancelleddays").text(
                        `${cancelleddays} (${(
                            (cancelleddays / totaldays) *
                            100
                        ).toFixed(2)}%)`
                    );
                },
            });

            $("#period-details").animate({ opacity: 1 }, "fast").show();
        },
    });
}

function updateDay(id, data) {
    $.ajax({
        type: "PATCH",
        url: `${baseUrl}/${currentPeriod}/days/${id}/`,
        data: data,
        success: function (response) {
            showMessage("Atualizado com sucesso", "alert-success");
            updateDetails();
            getCalendar();
        },
        error: function (response) {
            showMessage("Ocorreu um erro ao atualizar", "alert-danger");
            console.error(response);
        },
    });
}

function update(data) {
    $.ajax({
        url: `${baseUrl}/${currentPeriod}/`,
        type: "PATCH",
        data: data,
        success: function (response) {
            showMessage("Atualizado com sucesso", "alert-success");
            updateList();
            $(".loader-global").removeClass("load");
        },
        error: function (response) {
            showMessage("Ocorreu um erro.", "alert-danger");
            console.error(response);
            $(".loader-global").removeClass("load");
        },
    });
}

function disableControls() {
    $("#load-previous").attr("disabled", true);
    $("#load-next").attr("disabled", true);
}

$(document).ready(function () {
    $("#confirmReserve, #rejectReserve, #waitReserve").click(function (e) {
        e.preventDefault();
        $(".loader-global").addClass("load");
        update({
            obs: $("#reserve-obs").val() ? $("#reserve-obs").val() : "",
            status: $(this).attr("data-status"),
        });
    });
    $("#obsReserve").click(function (e) {
        e.preventDefault();
        update({
            obs: $("#reserve-obs").val() ? $("#reserve-obs").val() : "",
        });
    });

    $("[data-filter]").change(function () {
        updateList();
    });

    $("#deletePeriod").click(function () {
        $.ajax({
            type: "DELETE",
            url: `${baseUrl}/${currentPeriod}/`,
            success: function (response) {
                showMessage("Deletado com sucesso.", "alert-success");
                updateList();
                $("#period-details").fadeTo("fast", 0).slideUp();
            },
            error: function (response) {
                showMessage("Ocorreu um erro.", "alert-danger");
                console.error(response);
            },
        });
    });

    $("#load-previous").click(function (e) {
        e.preventDefault();
        updateList(previous);
    });

    $("#load-next").click(function (e) {
        e.preventDefault();
        updateList(next);
    });

    $("#limpa-filtro").click(function () {
        $.each($("[data-filter]"), function () {
            $(this).val("");
        });
        updateList();
    });

    getOptions(updateList);
});
