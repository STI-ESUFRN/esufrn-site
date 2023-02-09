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

var dataAtual = new Date();
var mesAtual = dataAtual.getMonth() + 1;
var anoAtual = dataAtual.getFullYear();

function resetDate() {
    mesAtual = dataAtual.getMonth() + 1;
    anoAtual = dataAtual.getFullYear();
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

function getCalendar() {
    $("#nome-mes").text(`${mesNome[mesAtual - 1]} / ${anoAtual}`);
    let sala = $("#classroom option:selected").val();

    $.ajax({
        type: "GET",
        url: `/api/calendar/?date__year=${anoAtual}&date__month=${mesAtual}&classroom=${sala}`,
        dataType: "json",
        success: function (response) {
            calendario.updateCalendar(response, anoAtual, mesAtual);
        },
    });
}

$(document).ready(function () {
    $("#classroom").change(function () {
        resetDate();
        getCalendar();

        $("#sala-selec").text($(this).find("option:selected").text());
        $("#sala-disp").prop("disabled", false);

        let selected = $("#classroom option:selected");

        let type = selected.attr("data-type");
        let term = $("#form-reserva [name=confirm]");
        if (type == "lab") {
            term.parent().prop("hidden", false);
            term.prop("required", true);
        } else {
            term.parent().prop("hidden", true);
            term.prop("required", false);
        }

        let justification_required = selected.attr(
            "data-justification_required"
        );
        let cause = $("#form-reserva [name=cause]");
        if (justification_required !== undefined) {
            cause.parent().prop("hidden", false);
            cause.prop("required", true);
        } else {
            cause.parent().prop("hidden", true);
            cause.prop("required", false);
        }
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

    $("#form-reserva [name]").change(function () {
        $(this).removeClass("is-invalid");
    });

    $("#enviar-reserva").click(function (e) {
        e.preventDefault();

        $("#status-message").html("");
        $("#form-reserva [name]").removeClass("is-invalid");

        serialized_data = $("#form-reserva").serializeREST();
        $.ajax({
            type: "POST",
            url: `/api/reserves/cadastrar/`,
            dataType: "json",
            data: serialized_data,
            success: function (response) {
                $("#status-message").html(`
                    <div class="rounded-0 alert alert-success alert-dismissible fade show" role="alert">
                        <strong>Reserva solicitada com sucesso</strong>
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true"><i class="fas fa-times" aria-hidden="true"></i></span>
                        </button>
                    </div>
                `);
                $("#form-reserva").trigger("reset");
                $("#sala-disp").prop("disabled", true);
                resetDate();
            },
            error: function (response) {
                $("#form-reserva").fillErrors(
                    response.responseJSON,
                    "status-message",
                    function (message) {
                        $("#status-message").append(`
                            <div class="rounded-0 alert alert-warning alert-dismissible fade show" role="alert">
                                <strong>${message}</strong>
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true"><i class="fas fa-times" aria-hidden="true"></i></span>
                                </button>
                            </div>
                        `);
                    }
                );
            },
        });
    });
});
