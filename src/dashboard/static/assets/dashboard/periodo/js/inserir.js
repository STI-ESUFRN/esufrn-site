$("#classroom").change(function () {
	resetDate();
	getCalendar();

	$("#sala-selec").text($(this).find("option:selected").text());
	$("#sala-disp").prop("disabled", false);

	selected = $("#classroom option:selected");
});

$("#enviar-reserva").click(function (e) {
	e.preventDefault();

	let error = validate_form();

	if (!error) {
		var serialized_data = $("#form-reserva [name!=week][name!=shift]").serialize();
		serialized_data += "&week=" + $("#form-reserva [name=week]:checked").map(function () {
			return $(this).val();
		}).get().join(',');
		serialized_data += "&shift=" + $("#form-reserva [name=shift]:checked").map(function () {
			return $(this).val();
		}).get().join(',');

		$.ajax({
			type: "POST",
			url: '/api/admin/periodos',
			data: serialized_data,
			success: function (response) {
				if (response.status == "success") {
					$('#form-reserva').trigger("reset");
					showMessage(response.message, "alert-success");
				} else {
					showMessage(response.message, "alert-danger");
				}
			},
			error: function (response) {
				showMessage(response.responseJSON.message, "alert-danger");
			}

		});
	} else {
		showMessage("Corrija os erros", "alert-warning");
	}
});
