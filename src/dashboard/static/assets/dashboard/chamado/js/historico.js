
var next = undefined;
var previous = undefined;
function refreshData(url = undefined) {
	if (!url) {
		let filters = $("[data-filter]").serialize();
		url = `/api/admin/chamados/?options=hist&${filters}`;
	}

	$("#load-antigo,#load-recente").attr("disabled", true);
	$.get(url, (response) => {
		$("#lista-de-chamados").html("");

		$.each(response.results, function (i, v) {
			let row = $('<tr />', { "data-id-chamado": v.id });
			let fas = $('<td />', { "class": 'text-center px-0 pl-2' });
			let fa_check = $('<i />', { "class": v.status == "R" ? 'fas fa-check-circle text-success' : 'fas fa-times-circle text-danger' });
			fas.append(fa_check);

			let criado_ha_date = new Date(v.created);
			let criado_ha = criado_ha_date.toLocaleDateString();
			let fa_cog = $('<td />', { class: "text-center", html: '<i class="fas fa-user-cog"></i>' });
			let title = $('<td />', { text: v.title, title: v.title });
			let requester = $('<td />', { text: v.requester, title: v.requester });
			let date = $('<td />', { text: criado_ha, title: criado_ha, class: "font-weight-bold text-center" });

			row.append(fas, fa_cog, title, requester, date);
			$("#lista-de-chamados").append(row);
		});
		$(".timeago").timeago();

		$("tr[data-id-chamado]").click(function (e) {
			e.preventDefault();
			fillCall(e.currentTarget.dataset.idChamado);
		});

		next = response.next;
		updateButton(next, "#load-antigo");

		previous = response.previous;
		updateButton(previous, "#load-recente");
	});
}

function updateButton(data, button) {
	if (data) {
		$(button).attr("disabled", false);
	} else {
		$(button).attr("disabled", true);
	}
}

var idSelecionado = undefined;
function fillCall(id) {
	$("#detalhes").hide();

	idSelecionado = id;
	$.get(`/api/admin/chamados/${id}/`, (response) => {
		fillAttributes(response);

		let status = $('[data-attribute=status]');
		if (status.text() == 'R') {
			status.html('Resolvido <i class="fas fa-check-circle text-success"></i>');
		} else {
			status.html('Não resolvido <i class="fas fa-times-circle text-danger"></i>');
		}

		$("#detalhes").fadeTo("fast", 0).fadeTo("fast", 1).show();
	});
}

function patch(data) {
	$(".loader-global").addClass("load");
	$.ajax({
		url: `/api/admin/chamados/${idSelecionado}/`,
		type: 'PATCH',
		data: data,
		success: function (response) {
			refreshData();
			if (response.status == "P") {
				$("#detalhes").fadeTo("fast", 0).slideUp();
			}
			showMessage("Arquivo atualizado com sucesso", "alert-success");
			$(".loader-global").removeClass("load");
		},
		error: function (err) {
			showMessage(err.responseText, "alert-danger");
			$(".loader-global").removeClass("load");
		}
	});
}

refreshData();


//--------------- LISTENERS ---------------
$("#confirmCall, #rejectCall, #waitCall").click(function (e) {
	e.preventDefault();
	patch({
		obs: $("#call-obs").val() ? $("#call-obs").val() : "",
		status: $(this).attr("data-status")
	});
});

$("#obsCall").click(function (e) {
	e.preventDefault();
	patch({
		obs: $("#call-obs").val() ? $("#call-obs").val() : "",
	});
});

$("[data-filter]").change(function (e) {
	e.preventDefault();
	refreshData();
});

$("#load-antigo").click(function (e) {
	e.preventDefault();
	refreshData(next);
});

$("#load-recente").click(function (e) {
	e.preventDefault();
	refreshData(previous);
});

$("#detalhes-dismiss").click(function () {
	$("#detalhes").fadeTo("fast", 0).slideUp();
});
