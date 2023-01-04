
var dataAtual = new Date();
var mesAtual = dataAtual.getMonth() + 1;
var anoAtual = dataAtual.getFullYear();

var mesNome = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
var mesFullNome = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
function update() {
    var dt = new Date();
    $(".issued_at").text("Emitido em: " + ('0' + dt.getDate()).slice(-2) + "/" + ('0' + (dt.getMonth() + 1)).slice(-2) + "/" + dt.getFullYear() + " às " + ('0' + dt.getHours()).slice(-2) + ":" + ('0' + dt.getMinutes()).slice(-2));
    $(".planilha-data").text(`Reservas do mês de ${mesFullNome[mesAtual - 1]} - ${anoAtual}`);

    $("#nome-mes").text(`${mesNome[mesAtual - 1]} / ${anoAtual}`);

    $(".reservation-calendar").each(function () {
        var self = $(this);
        var id = $(self).attr("data-id");
        var calendario = new ReservationCalendar({
            element: `reservation-calendar-${id}`,
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
        $.ajax({
            type: "GET",
            url: `/api/reservas/calendario/?year=${anoAtual}&month=${mesAtual}&classroom=${id}&status=A`,
            dataType: "json",
            success: function (response) {
                calendario.updateCalendar(response, anoAtual, mesAtual);
            },
            error: function (response) {
                $(self).html(`<h5 class="text-danger"><b>Não foi possível obter informações sobre o calendário (${response.status})</b></h5>`);
            }
        });
    });
};



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

function resetDate() {
    mesAtual = dataAtual.getMonth() + 1;
    anoAtual = dataAtual.getFullYear();
};
function prevMonth() {
    if (mesAtual == 1) {
        anoAtual -= 1;
        mesAtual = 12;
    } else {
        mesAtual -= 1;
    }
    update();
}
function nextMonth() {
    if (mesAtual == 12) {
        anoAtual += 1;
        mesAtual = 1;
    } else {
        mesAtual += 1;
    }
    update();
}
update();

function backTop() {
    $('html, body').animate({ scrollTop: '0px' }, 300);
};
