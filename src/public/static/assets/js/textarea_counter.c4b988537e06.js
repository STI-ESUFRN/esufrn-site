function countChar(elem) {
    limit = elem.prop('maxlength');
    current = elem.val().length;
    counter = $(elem.attr('data-counter'));
    remain = Math.abs(current - limit);
    counter.text(remain);

    counter.removeClass("text-danger text-warning");
    if (remain < 32) {
        counter.addClass("text-danger");
    } else if (remain < 64) {
        counter.addClass("text-warning");
    }
}
$('.textarea-counter').each(function (index, elem) {
    countChar($(elem));
})
$('.textarea-counter').keyup(function () {
    countChar($(this));
});