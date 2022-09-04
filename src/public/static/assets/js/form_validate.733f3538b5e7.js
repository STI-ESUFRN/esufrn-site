String.prototype.isEmail = function () {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(this);
};
String.prototype.isPhone = function () {
    var regex = /(\([0-9]{2}\)\s+[0-9]{1}\s+[0-9]{4}\-[0-9]{4})/;
    return regex.test(this);
};
String.prototype.isDate = function () {
    var regex = /([0-9]{2}\-+[0-9]{2}\-+[0-9]{4})/;
    return regex.test(this);
};

function validate(input, condition) {
    if (input) {
        if (condition) {
            input.removeClass("is-invalid");
            return false;
        } else {
            input.addClass("is-invalid");
            return true;
        }
    } else {
        return true;
    }
};