var options = undefined;
function getOptions(callback_function, ...args) {
    if (!baseUrl) {
        console.warn("Can't get options: baseUrl is not defined");
        return;
    }

    $.ajax({
        type: "OPTIONS",
        url: baseUrl,
        success: function (response) {
            options = response;
            getOptionChoices();
            callback_function(...args);
        },
    });
}

var choices = {};
function getOptionChoices() {
    $.each(options.actions.POST, function (index, value) {
        if (value.type == "choice") {
            let values = {};
            $.each(value.choices, function (index, choice) {
                values[choice.value] = choice.display_name;
            });
            choices[index] = values;
        }
    });
}

$.fn.serializeREST = function (
    include_blank = false,
    input_date_format = "DD-MM-YYYY",
    output_date_format = "YYYY-MM-DD"
) {
    let serialized_values = $(this)
        .find("[name]:not([date-field])")
        .serializeArray();

    let serialized_dates = [];
    $(this)
        .find("[name][date-field]")
        .each(function (index) {
            let input_format = $(this).attr("date-input-format");
            let output_format = $(this).attr("date-output-format");

            let value = $(this).val();
            let formated_date = "";
            if (value) {
                formated_date = moment(
                    value,
                    input_format ? input_format : input_date_format
                ).format(output_format ? output_format : output_date_format);
            }
            serialized_dates.push({
                value: formated_date,
                name: $(this).attr("name"),
            });
        });

    serialized_array = serialized_values.concat(serialized_dates);

    let groupedValues = {};
    $.each(serialized_array, function (index, item) {
        if (item.value || include_blank) {
            if (!groupedValues[item.name]) {
                groupedValues[item.name] = [];
            }
            groupedValues[item.name].push(item.value);
        }
    });
    const groupedValuesAsString = {};
    $.each(groupedValues, function (field, values) {
        groupedValuesAsString[field] = values.join(",");
    });

    return groupedValuesAsString;
};

$.fn.fillErrors = function (data, non_field_behavior) {
    $.map(data, (value, key) => {
        $(this).find(`[name=${key}]`).addClass("is-invalid");

        let feedback = $(this).find(`.invalid-feedback[for=${key}]`);
        if (feedback.length) {
            feedback.html("");
            feedback.css("display", "block");
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

$(document).ready(function () {
    $("form [name]").change(function (e) {
        let name = $(this).attr("name");
        $(`form [name=${name}]`).removeClass("is-invalid");
        $(`.invalid-feedback[for=${name}]`).css("display", "none");
    });
});
