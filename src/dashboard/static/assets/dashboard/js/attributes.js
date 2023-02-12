function setText(e, val) {
    if (e.is("textarea")) {
        e.val(val);
    } else {
        e.text(val);
    }
}

function fillAttributes(object) {
    $(`[data-attribute]`).each(function () {
        let attr = object;
        let path = $(this).attr("data-attribute").split(".");
        $.each(path, function (index, key) {
            attr = attr[key];
            if (choices[key]) {
                if ($.isArray(attr)) {
                    attr = $.map(attr, function (value) {
                        return choices[key][value];
                    }).join(", ");
                } else {
                    attr = choices[key][attr];
                }
            }
        });

        if (attr != null) {
            format = $(this).attr("date-format");
            if (format) {
                attr = moment(attr).format(format);
            }
            setText($(this), attr);
        } else {
            setText($(this), "");
        }
    });
}
