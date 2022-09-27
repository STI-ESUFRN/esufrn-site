
var selected = undefined;

var dataAtual = new Date();
var mesAtual = dataAtual.getMonth() + 1;
var anoAtual = dataAtual.getFullYear();

var mesNome = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

var calendario = new ReservationCalendar({
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

$('[data-toggle="datepicker"]').datepicker({
    format: 'dd-mm-yyyy',
    months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    daysMin: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']
});

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
    let sala = $("#classroom option:selected").val()

    $.ajax({
        type: "GET",
        url: `/api/calendario?year=${anoAtual}&month=${mesAtual}&classroom=${sala}`,
        success: function (response) {
            calendario.updateCalendar(response, anoAtual, mesAtual);
        }
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

$("#form-reserva [name]").change(function () {
    $(this).removeClass("is-invalid");
});

function validate_form() {
    $("#form-reserva [name]").removeClass("is-invalid");

    var error = false;

    let form_classroom = $("#form-reserva [name=classroom]");
    error += validate(form_classroom, form_classroom.val());

    let form_course = $("#form-reserva [name=course]");
    error += validate(form_course, form_course.val());

    let form_date_begin = $("#form-reserva [name=date_begin]");
    error += validate(form_date_begin, form_date_begin.val() && form_date_begin.val().isDate());

    let form_date_end = $("#form-reserva [name=date_end]");
    error += validate(form_date_end, form_date_end.val() && form_date_end.val().isDate());

    let form_classname = $("#form-reserva [name=classname]");
    error += validate(form_classname, form_classname.val());

    let form_requester = $("#form-reserva [name=requester]");
    error += validate(form_requester, form_requester.val());

    let form_period = $("#form-reserva [name=period]");
    error += validate(form_period, form_period.val());

    let form_classcode = $("#form-reserva [name=classcode]");
    error += validate(form_classcode, form_classcode.val());

    let form_class_period = $("#form-reserva [name=class_period]");
    error += validate(form_class_period, form_class_period.val());

    let form_email = $("#form-reserva [name=email]");
    error += validate(form_email, form_email.val() && form_email.val().isEmail());

    let form_phone = $("#form-reserva [name=phone]");
    error += validate(form_phone, form_phone.val() && form_phone.val().isPhone());

    let form_shift = $("#form-reserva [name=shift]");
    error += validate(form_shift, form_shift.filter(":checked").val());

    let form_week = $("#form-reserva [name=week]");
    error += validate(form_week, form_week.filter(":checked").val());

    return error;
}
