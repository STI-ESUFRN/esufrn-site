var dataAtual = new Date();
var mesAtual = dataAtual.getMonth() + 1;
var anoAtual = dataAtual.getFullYear();

var mesNome = [
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
        success: function (response) {
            calendario.updateCalendar(response, anoAtual, mesAtual);
        },
    });
}

$(document).ready(function () {
    $("#escolheMes").html(`
        <div class="row justify-content-around my-4">
            <div class="col my-auto text-center">
                <button onclick='prevMonth()' class="btn btn-dark"><i class="fas fa-chevron-left" aria-hidden="true"></i></button>
            </div>
            <div class="col my-auto text-center">
                <h5 id="nome-mes" class="m-0">${
                    mesNome[mesAtual - 1]
                } / ${anoAtual}</h5>
            </div>
            <div class="col my-auto text-center">
                <button onclick='nextMonth()' class="btn btn-dark"><i class="fas fa-chevron-right" aria-hidden="true"></i></button>
            </div>
        </div>
    `);

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
});
