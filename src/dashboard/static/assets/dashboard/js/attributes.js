
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
        $.map($(this).attr("data-attribute").split('.'), (value, index) => {
            attr = attr[value];
            return attr;
        });

        if (attr != null) {
            format = $(this).attr("date-format");
            if (format) {
                attr = moment(attr).format(format);
            }
            setText($(this), attr);
        } else {
            setText($(this), '');
        }
    });
}
