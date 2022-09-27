
var localData = [];
function updateDash(data = []) {
	localData = data[0];
	$("#lista-de-chamados").html("");
	$.each(data[0], function (i, v) {
		let row = $('<tr />', { "data-id-chamado": v.id });
		let fa = $('<td />', { "class": 'text-center px-0' });
		let a2 = $('<i />', { "class": v.status == "A" ? 'fas fa-check-circle text-success' : 'fas fa-times-circle text-danger' });
		fa.append(a2);

		let fa_calendar = $('<td />', { class: "text-center px-0", html: v.admin_created ? '<i class="fas fa-key"></i>' : '<i class="far fa-calendar-alt"></i>' });

		let classroom = $('<td />', { text: v.classroom.classroom_name });
		let criado_ha_date = new Date(v.created_at);
		let criado_ha = criado_ha_date.toLocaleDateString();
		let event = $('<td />', { text: v.event, title: v.event });
		let requester = $('<td />', { text: v.requester, title: v.requester });
		let e1 = $('<td />', { text: criado_ha, title: criado_ha, class: "font-weight-bold text-center" });

		row.append(fa, fa_calendar, classroom, event, requester, e1);
		$("#lista-de-chamados").append(row);
	});
	$(".timeago").timeago();

	$("tr[data-id-chamado]").click(function (e) {
		e.preventDefault();
		fillReserve(e.currentTarget.dataset.idChamado);
	});
}

var actualPage = 0;
function refreshData(pagina = 1) {
	actualPage = pagina
	actualPage == 1 ? $("#load-recente").attr("disabled", true) : $("#load-recente").attr("disabled", false)

	filters = $("[data-filter]").serialize();

	$.ajax({
		url: "/api/admin/reservas",
		type: "GET",
		data: `${filters}&page=${pagina}`,
		success: function (data) {
			data[1]['have_more'] ? $("#load-antigo").attr("disabled", false) : $("#load-antigo").attr("disabled", true)
			updateDash(data);
		}
	});
}

var idSelected = undefined;
function fillReserve(id) {
	$("#detalhes").hide();

	var reserve = Object.assign({}, localData.filter((v) => v.id == id)[0]);
	fillAttributes(reserve);

	idSelected = reserve.id;

	let v = $('[data-attribute=status]');
	if (v.text() == 'A') {
		v.html('Aceito <i class="fas fa-check-circle text-success"></i>');
	} else {
		v.html('Rejeitado <i class="fas fa-times-circle text-danger"></i>');
	}

	$("#detalhes").fadeTo("fast", 0).fadeTo("fast", 1).show();
}


// ------------------------------------------------------------------- Listeners

$("#filtro, #ordem").change(function (e) {
	e.preventDefault();
	refreshData("1");
});

$("#load-antigo").click(function (e) {
	e.preventDefault();
	refreshData(String(parseInt(actualPage) + 1));
});

$("#load-recente").click(function (e) {
	e.preventDefault();
	refreshData(String(parseInt(actualPage) - 1));
});


// ------------------------------------------------------------------- Update
function update(data) {
	$.ajax({
		url: "/api/admin/reservas/" + idSelected,
		type: 'PUT',
		data: data,
		success: function (response) {
			$(".loader-global").removeClass("load");
			if (response.status == "success") {
				refreshData();
				$("#detalhes").fadeTo("fast", 0).slideUp();
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
		obs: $("[data-attribute=obs]").val() ? $("[data-attribute=obs]").val() : "",
		status: $(this).attr("data-status"),
		msg: $("#reserve-email").val()
	});
});
// -------------------------------------
$("#obsReserve").click(function (e) {
	e.preventDefault();
	update({
		obs: $("[data-attribute=obs]").val() ? $("[data-attribute=obs]").val() : ""
	});
});

$("[data-filter]").change(function () {
	refreshData();
});

$("#detalhes-dismiss").click(function () {
	$("#detalhes").fadeTo("fast", 0).slideUp();
});
// ------------------------------------------------------------------- Init
refreshData();
