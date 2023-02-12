

$("#form-contato").submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: `/api/contato/`,
        data: $("#form-contato").serialize(),
        success: function (response) {
            $("#form-contato .status-message").text(`${response.message}`);
            response.status == 'success' ? $('#form-contato').trigger("reset") : '';
        },
    });
});
