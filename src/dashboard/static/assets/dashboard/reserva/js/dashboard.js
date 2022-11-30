
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

const mesNome = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
var mesAtual = undefined;
var anoAtual = undefined;
var salaAtual = undefined;
function getCalendar() {
	$("#nome-mes").text(`${mesNome[mesAtual - 1]} / ${anoAtual}`);

	$.ajax({
		type: "GET",
		url: `/api/calendario/?year=${anoAtual}&month=${mesAtual}&classroom=${salaAtual}`,
		dataType: "json",
		success: function (response) {
			calendario.updateCalendar(response, anoAtual, mesAtual);
		}
	});
};

// ---------------------------------------------------------------------------------------------

var localData = [];
var idSelecionado = undefined;

function updateDash(data = []) {
	localData = data

	$("#lista-de-chamados").html("");
	console.log(data);
	$.each(data, function (i, v) {
		let a = $('<tr />', { "data-id-chamado": v.id });
		let fa = $('<td />', { "class": 'text-center px-0 pl-2' });
		let a2 = $('<i />', { "class": 'far fa-calendar-alt text-warning' });
		fa.append(a2);

		let now = new Date();
		let criado_ha_date = new Date(v.created);
		let criado_ha = criado_ha_date.toISOString();
		let date = $("<td />", { text: moment(v.date).format("DD/MM/YYYY"), class: "text-center" });
		let classroom = $('<td />', { text: v.classroom.full_name });
		let event = $('<td />', { text: v.event });
		let requester = $('<td />', { text: v.requester });
		let elapsed = $('<td />', { class: `text-center font-weight-bold ${(now - criado_ha_date) > 1200000 ? "text-danger" : ""}`, });
		let ago = $('<time />', { text: criado_ha, class: "timeago", dateTime: criado_ha });
		elapsed.append(ago);

		a.append(fa, event, classroom, requester, date, elapsed);
		$("#lista-de-chamados").append(a);

	});
	$(".timeago").timeago();

	$("tr[data-id-chamado]").click(function (e) {
		e.preventDefault();
		fillReserve(e.currentTarget.dataset.idChamado);
	});
}

function refreshData(force = false, ring = true) {
	$.get("/api/reservas", function (data, textStatus, jqXHR) {
		if ((localData.length != data.length) || force) {
			updateDash(data);
			if (ring) {
				playAudio();
			}
			$("#badgeChamados").text(data.length);
		} else {
			var idArray = [];
			$.each(localData, function (i, v) {
				idArray.push(v.id);
			});
			$.each(data, function (i, v) {
				if (!v.id in idArray) {
					updateDash(data);
					playAudio();
					$("#badgeChamados").text(data.length);
					return;
				}
			});
		}
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
		url: `/api/admin/reservas/${idSelecionado}/`,
		type: "PUT",
		data: data,
		success: function (response) {
			$(".loader-global").removeClass("load");
			if (response.status == "success") {
				refreshData(true);
				$("#detalhes").fadeTo("fast", 0).slideUp();
				showMessage(response.message, "alert-success");
			} else {
				showMessage(response.message, "alert-danger");
			}
		},
		error: function (err) {
			$(".loader-global").removeClass("load");
			showMessage(err.responseJSON.message, "alert-" + (response.status == "success" ? "success" : "danger"));
		}
	});
}

$("#detalhes-dismiss").click(function () {
	$("#detalhes").fadeTo("fast", 0).slideUp();
});

$("#confirmReserve, #rejectReserve").click(function (e) {
	e.preventDefault();
	$(".loader-global").addClass("load");
	update({
		status: $(this).attr("data-status"),
		obs: $("#reserve-obs").val() ? $("#reserve-obs").val() : "",
		msg: $("#reserve-email").val()
	});
});

$("#obsReserve").click(function (e) {
	e.preventDefault();
	update({
		obs: $("#reserve-obs").val() ? $("#reserve-obs").val() : ""
	});
});

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

refreshData(false, false);

setInterval(() => {
	refreshData();
	$("td:last-child:not(.text-danger).font-weight-bold").each(function (index, element) {
		var now = new Date()
		var then = new Date(element.lastChild.getAttribute('dateTime'));
		if (now - then > 1200000) {
			element.classList.value = "text-danger font-weight-bold";
			playAudio();
		}
	});
}, 10000);
