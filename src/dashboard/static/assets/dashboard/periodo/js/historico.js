
calendario = new ReservationCalendar({
    weekName: ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
    dayName: "Dia",
    varNames: {
        date: "date",
        event: "event",
        status: {
            name: "status",
            confirmed: "A",
            refused: "R",
            waiting: "E"
        },
        shift: "shift"
    }
});

const mesNome = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
const dias = ["None", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"];
const turnos = {
    "M": "Manhã",
    "T": "Tarde",
    "N": "Noite"
};

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
        url: `/api/calendario?year=${anoAtual}&month=${mesAtual}&classroom=${sala}`,
        dataType: "json",
        success: function (response) {
            calendario.updateCalendar(response, anoAtual, mesAtual);
        }
    });
};


var currentPeriod = undefined;
var actualPage = 1;
function updateList(pagina = 1) {
    disableControls();

    $("#lista-de-chamados").html("");

    $(".loader-global").addClass("load");

    actualPage = pagina;

    filters = $("[data-filter]").serialize();
    $.ajax({
        type: "GET",
        url: "/api/admin/periodos",
        data: `${filters}&page=${pagina}`,
        success: function (response) {
            $.each(response.data, (index, value) => {
                let row = $("<tr />", { 'data-id-periodo': value.id });

                let status_fa = $('<td />', { class: 'text-center px-0 pl-2', html: `<i class="${value.status == "A" ? "fa fa-check-circle text-success" : value.status == "R" ? "fa fa-times-circle text-danger" : "fa fa-solid fa-clock text-warning"}">` });
                let calendar_fa = $("<td />", { class: "text-center", html: `<i class="fas fa-calendar" aria-hidden="true"></i>` });
                let classname = $("<td />", { text: value.classname });
                let classroom = $("<td />", { text: value.classroom.classroom_name });


                let shift = $("<td />", {
                    text: $.makeArray(value.shift).map((value, index) => {
                        return turnos[value];
                    }).join(', ')
                });
                let requester = $("<td />", { text: value.requester });

                let date_begin_date = moment(value.date_begin).format("DD-MM-YYYY");
                let date_begin = $("<td />", { class: "text-center", text: date_begin_date });
                let date_end_date = moment(value.date_end).format("DD-MM-YYYY");
                let date_end = $("<td />", { class: "text-center", text: date_end_date });

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
                $("#lista-de-chamados").append(row);
            });

            $("tr[data-id-periodo]").click(function (e) {
                e.preventDefault();
                currentPeriod = e.currentTarget.dataset.idPeriodo;
                showDetails();
            });

            let hasMore = response.paginator.current < response.paginator.total;
            actualPage == 1 ? $("#load-recente").attr("disabled", true) : $("#load-recente").attr("disabled", false);
            hasMore ? $("#load-antigo").attr("disabled", false) : $("#load-antigo").attr("disabled", true);

            $(".loader-global").removeClass("load");
            $("#period-list").fadeIn("fast");
        }
    });
}


function showDetails() {
    $("#period-details").animate({ opacity: 0 }, "fast", function () {
        updateDetails();
    });
}

function updateDetails() {
    $("#editButton").attr("href", `/dashboard/periodo/editar/${currentPeriod}`);
    $.ajax({
        type: "GET",
        url: `/api/admin/periodos/${currentPeriod}`,
        success: function (response) {
            fillAttributes(response);

            $("#weekdays").text($.makeArray(response.weekdays).map((value, index) => {
                return dias[value];
            }).join(', '));
            $("#shift").text($.makeArray(response.shift).map((value, index) => {
                return turnos[value];
            }).join(', '));

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
                $("#sala-selec").text(response.classroom.classroom_name);
                getCalendar();
            }

            $.ajax({
                url: `/api/admin/periodos/${response.id}/dias`,
                type: "GET",
                success: function (response) {
                    $("#perioddays").html('');

                    let activedays = 0;
                    let cancelleddays = 0;
                    let totaldays = response.length;
                    $.each(response, (index, value) => {
                        let row = $("<tr />");
                        let day = $("<td />", { text: moment(value.date).format("DD/MM/YYYY"), style: "vertical-align: middle;" });
                        let shift = $("<td />", { text: value.shift_name });
                        let statusLabel = $("<td />", { text: value.active ? "Ativo" : "Cancelado", style: "vertical-align: middle;" });

                        let action = $("<button />", {
                            html: value.active ? '<i class="fas fa-pause" aria-hidden="true"></i>' : '<i class="fas fa-play" aria-hidden="true"></i>',
                            class: `btn btn-sm ${value.active ? "btn-outline-danger" : "btn-outline-primary"}`,
                            'data-day-id': value.id,
                            'data-day-active': value.active
                        });
                        let td = $("<td />", { class: "text-center" });
                        td.append(action);
                        row.append(day, shift, statusLabel, td);
                        $("#perioddays").append(row);

                        value.active ? activedays++ : cancelleddays++;
                    });
                    $("#totaldays").text(totaldays);
                    $("#activedays").text(`${activedays}(${(activedays / totaldays * 100.).toFixed(2)}%)`);
                    $("#cancelleddays").text(`${cancelleddays} (${(cancelleddays / totaldays * 100.).toFixed(2)}%)`);

                    $("[data-day-id]").click(function () {
                        updateDay($(this));
                    });
                }
            });

            $("#period-details").animate({ opacity: 1 }, "fast").show();
        }
    });
}

function updateDay(elem) {
    $.ajax({
        type: "PUT",
        url: `/api/admin/periodos/${currentPeriod}/dias/${elem.attr("data-day-id")}`,
        data: {
            status: elem.attr("data-day-active") == "true" ? "false" : "true"
        },
        success: function (response) {
            if (response.status == "success") {
                updateDetails();
                getCalendar();
                showMessage(response.message, "alert-success");
            } else {
                showMessage(response.message, "alert-danger");
            }
        }
    });
};


function update(data) {
    $.ajax({
        url: "/api/admin/periodos/" + currentPeriod,
        type: 'PUT',
        data: data,
        success: function (response) {
            $(".loader-global").removeClass("load");
            if (response.status == "success") {
                updateList(actualPage);
                showMessage(response.message, "alert-success");
            } else {
                showMessage(response.message, "alert-danger");
            }
        },
        error: function (err) {
            $(".loader-global").removeClass("load");
            showMessage(err.responseJSON.message, "alert-danger");
        }
    });
}

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
        obs: $("#reserve-obs").val() ? $("#reserve-obs").val() : ""
    });
});

$("[data-filter]").change(function () {
    updateList();
});



$("#deletePeriod").click(function () {
    $.ajax({
        type: "DELETE",
        url: `/api/admin/periodos/${currentPeriod}`,
        success: function (response) {
            if (response.status == "success") {
                updateList(actualPage);
                showMessage(response.message, "alert-success");
            } else {
                showMessage(response.message, "alert-danger");
            }
        }
    });
});

function disableControls() {
    $("#load-antigo").attr('disabled', true);
    $("#load-recente").attr('disabled', true);
}
$("#load-antigo").click(function (e) {
    e.preventDefault();
    updateList(actualPage + 1);
});

$("#load-recente").click(function (e) {
    e.preventDefault();
    updateList(actualPage - 1);
});


updateList();

$("#limpa-filtro").click(function () {
    $.each($("[data-filter]"), function () {
        $(this).val('');
    });
    updateList();
});
