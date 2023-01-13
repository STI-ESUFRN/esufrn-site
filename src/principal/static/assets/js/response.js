$.fn.serializeREST = function (
    input_date_format = "DD-MM-YYYY",
    output_date_format = "YYYY-MM-DD"
) {
    let serialized_data = {};

    let serialized_array = $(this)
        .find("[name]:not([date-field])")
        .serializeArray();
    for (key in serialized_array) {
        let value = serialized_array[key]["value"];
        if (value) {
            serialized_data[serialized_array[key]["name"]] = value;
        }
    }

    let serialized_dates = $(this).find("[name][date-field]").serializeArray();
    for (key in serialized_dates) {
        let value = serialized_dates[key]["value"];
        if (value) {
            serialized_data[serialized_dates[key]["name"]] = moment(
                value,
                input_date_format
            ).format(output_date_format);
        }
    }
    return serialized_data;
};

$.fn.fillErrors = function (data, non_field_behavior) {
    $.map(data, (value, key) => {
        obj = $(this).find(`[name=${key}]`);
        if (obj.length) {
            obj.addClass("is-invalid");
            let feedback = $(this).find(`.invalid-feedback[for=${key}]`);
            feedback.html("");
            value.forEach((message) => {
                error = $("<p />", {
                    html: message,
                    class: "m-0",
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
