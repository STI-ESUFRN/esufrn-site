
$("#chamado-form [name]").change(function () {
    $(this).removeClass("is-invalid");
});

$("#enviar-chamado").click(function (e) {
    e.preventDefault();

    $("#status-message").html("")
    $("#chamado-form input").removeClass("is-invalid");

    error = false;

    form_title = $("#chamado-form [name=title]");
    error += validate(form_title, form_title.val());

    form_description = $("#chamado-form [name=description]");
    error += validate(form_description, form_description.val());

    form_requester = $("#chamado-form [name=requester]");
    error += validate(form_requester, form_requester.val());

    form_course = $("#chamado-form [name=course]");
    error += validate(form_course, form_course.val());

    form_contact = $("#chamado-form [name=contact]");
    error += validate(form_contact, form_contact.val());

    if (!error) {
        $.ajax({
            type: "POST",
            url: "/api/chamados/",
            data: $("#chamado-form").serialize(),
            success: function () {
                $("#status-message").html(`
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        <strong>Chamado cadastrado com sucesso.</strong>
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true"><i class="fas fa-times" aria-hidden="true"></i></span>
                        </button>
                    </div>
                `);
                $('#chamado-form').trigger("reset");
            },
            error: function (err) {
                console.warn(err.responseText);
            }
        });
    } else {
        $("#status-message").html(`
			<div class="rounded-0 alert alert-warning alert-dismissible fade show" role="alert">
				<strong>Corrija os erros</strong>
				<button type="button" class="close" data-dismiss="alert" aria-label="Close">
					<span aria-hidden="true"><i class="fas fa-times" aria-hidden="true"></i></span>
				</button>
			</div>
		`);
    }
});