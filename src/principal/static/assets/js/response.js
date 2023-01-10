$.fn.serializeREST = function (
    input_date_format = "DD-MM-YYYY",
    output_date_format = "YYYY-MM-DD"
) {
    let serialized_data = {};

    let serialized_array = $(this)
        .find("[name]:not([date-field])")
        .serializeArray();
    for (key in serialized_array) {
        serialized_data[serialized_array[key]["name"]] =
            serialized_array[key]["value"];
    }

    let serialized_dates = $(this).find("[name][date-field]").serializeArray();
    for (key in serialized_dates) {
        serialized_data[serialized_dates[key]["name"]] = moment(
            serialized_dates[key]["value"],
            input_date_format
        ).format(output_date_format);
    }
    return serialized_data;
};

$.fn.fillErrors = function (data, non_field_div_id, non_field_behavior) {
    $(`#${non_field_div_id}`).html("");
    $.map(data, (value, key) => {
        obj = $(this).find(`[name=${key}]`);
        if (obj) {
            obj.addClass("is-invalid");
            let feedback = $(this).find(`.invalid-feedback[for=${key}]`);
            feedback.html("");
            value.forEach((message) => {
                error = $("<p />", {
                    html: message,
                });
                feedback.append(error);
            });
        } else {
            value.forEach((message) => {
                non_field_behavior(message);
            });
        }
    });
};
