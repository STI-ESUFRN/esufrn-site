
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

// $("[required]:visible").each(function (index, elem) {
// 	$("label[for=" + $(this).attr('id') + "]").append("<b data-field_required>*</b>");
// });

function formata_data() {
    $('[data-toggle="datepicker"]').datepicker({
        format: 'dd-mm-yyyy',
        months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        daysMin: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']
    });
}

formata_data();
var _id_data = 1;
$("#add-data").click(function (e) {
    e.preventDefault();
    $("#add-data-box").append(`
    <div class="input-group mb-1" id="remove_data_${_id_data}">
        <input class="form-control rounded-0" name="date" data-mask="00-00-0000" data-toggle="datepicker" required="" autocomplete="off" maxlength="10">
        <div class="input-group-append">
        <button class="btn btn-outline-danger rounded-0" type="button" onclick="remove_data(${_id_data})" title="Remover">X</button>
        </div>
    </div>
    `);
    _id_data += 1;
    formata_data();
});

function remove_data(id) {
    $("#remove_data_" + id).remove();
}

$("#classroom").change(function () {
    resetDate();
    getCalendar();

    $("#sala-selec").text($(this).find("option:selected").text());
    $("#sala-disp").prop("disabled", false);

    selected = $("#classroom option:selected");

    type = selected.attr("data-type");
    term = $("#form-reserva [name=confirm]");
    if (type == "lab") {
        term.parent().prop("hidden", false);
        term.prop('required', true);
    } else {
        term.parent().prop("hidden", true);
        term.prop('required', false);
    }

    justification_required = selected.attr("data-justification_required");
    cause = $("#form-reserva [name=cause]");
    if (justification_required !== undefined) {
        cause.parent().prop("hidden", false);
        cause.prop('required', true);
    } else {
        cause.parent().prop("hidden", true);
        cause.prop('required', false);
    }
});


// Formatação do datepicker no form
$('[data-toggle="datepicker"]').datepicker({
    format: 'dd-mm-yyyy',
    months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    daysMin: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']
});


// Nome dos meses
var mesNome = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

var dataAtual = new Date();
var mesAtual = dataAtual.getMonth() + 1;
var anoAtual = dataAtual.getFullYear();

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


function getCalendar() {
    $("#nome-mes").text(`${mesNome[mesAtual - 1]} / ${anoAtual}`);
    let sala = $("#classroom option:selected").val();

    $.ajax({
        type: "GET",
        url: `/api/calendario?year=${anoAtual}&month=${mesAtual}&classroom=${sala}`,
        dataType: "json",
        success: function (response) {
            calendario.updateCalendar(response, anoAtual, mesAtual);
        }
    });
};

function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}
function isPhone(phone) {
    var regex = /(\([0-9]{2}\)\s+[0-9]{1}\s+[0-9]{4}\-[0-9]{4})/;
    return regex.test(phone);
}
function isDate(date) {
    var regex = /([0-9]{2}\-+[0-9]{2}\-+[0-9]{4})/;
    return regex.test(date);
}
$.fn.tag = function () {
    return this[0].outerHTML.replace(this.html(), "");
};
function validate(input, condition) {
    if (input) {
        if (condition) {
            input.removeClass("is-invalid");
            return false;
        } else {
            input.addClass("is-invalid");
            return true;
        }
    } else {
        return true;
    }
};

$("#form-reserva input").change(function () {
    $(this).removeClass("is-invalid");
});

function formReset() {
    $('#form-reserva').trigger("reset");
    $("#sala-disp").prop("disabled", true);
    resetDate();
}

// Envia formulário de reserva
$("#enviar-reserva").click(function (e) {
    e.preventDefault();

    $("#form-reserva input").removeClass("is-invalid");

    error = false;

    form_classroom = $("#form-reserva [name=classroom]");
    error += validate(form_classroom, form_classroom.val());

    selected = form_classroom.find(":selected");
    class_type = selected.attr("data-type");
    justification_required = selected.attr("data-justification_required") === undefined ? false : true;

    form_confirm = $("#form-reserva [name=confirm]");
    error += validate(form_confirm, (class_type == "lab" && form_confirm.is(":checked")) || class_type != "lab");

    $("#form-reserva [name=date]").map(function () {
        error += validate($(this), $(this).val() && isDate($(this).val()));
    });

    form_event = $("#form-reserva [name=event]");
    error += validate(form_event, form_event.val());

    form_requester = $("#form-reserva [name=requester]");
    error += validate(form_requester, form_requester.val());

    form_email = $("#form-reserva [name=email]");
    error += validate(form_email, form_email.val() && isEmail(form_email.val()));

    form_phone = $("#form-reserva [name=phone]");
    error += validate(form_phone, form_phone.val() && isPhone(form_phone.val()));

    form_cause = $("#form-reserva [name=cause]");
    error += validate(form_cause, (form_cause.val() && justification_required) || !justification_required);

    form_shift = $("#form-reserva [name=shift]");
    error += validate(form_shift, form_shift.filter(":checked").val());

    if (!error) {
        serialized_data = $("#form-reserva [name!=date]").serialize();
        serialized_data += "&date=" + $("#form-reserva [name=date]").map(function () {
            return $(this).val();
        }).get().join(',');

        $.ajax({
            type: "POST",
            url: `/api/admin/reservas`,
            dataType: "json",
            data: serialized_data,
            success: function (response) {
                if (response.status == "success") {
                    showMessage(response.message, "alert-success");
                    formReset();
                } else {
                    showMessage(response.message, "alert-danger");
                }
            }
        });
    } else {
        showMessage("Corrija os erros", "alert-warning");
    }
});
