$("#form-chamado input").change(function () {
    $(this).removeClass("is-invalid");
});

$("#enviar-chamado").click(function (e) {
    e.preventDefault();

    $("#form-chamado [name]").removeClass("is-invalid");

    var error = false;

    var form_requester = $("#form-chamado [name=requester]");
    error += validate(form_requester, form_requester.val());

    var form_course = $("#form-chamado [name=course]");
    error += validate(form_course, form_course.val());

    var form_contact = $("#form-chamado [name=contact]");
    error += validate(form_contact, form_contact.val());

    var form_title = $("#form-chamado [name=title]");
    error += validate(form_title, form_title.val());

    var form_description = $("#form-chamado [name=description]");
    error += validate(form_description, form_description.val());

    let data = new FormData($("#form-chamado")[0]);
    data.set(
        "status",
        $("#form-chamado [name=status]").is(":checked") ? true : ""
    );
    if (!error) {
        $.ajax({
            type: "POST",
            url: "/api/tickets/",
            data: data,
            processData: false,
            contentType: false,
            success: function () {
                $("#form-chamado").trigger("reset");
                showMessage("Chamado cadastrado com sucesso", "alert-success");
            },
            error: function (err) {
                showMessage(err.responseText, "alert-danger");
            },
        });
    } else {
        showMessage("Corrija os erros", "alert-warning");
    }
});
