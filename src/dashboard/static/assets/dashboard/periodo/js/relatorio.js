
$("[data-filter]").change(function () {
    filters = $("[data-filter]").serialize();
    window.location.replace(window.location.href.replace(/[\?#].*|$/, `?${filters}`));
});

function backTop() {
    $('html, body').animate({ scrollTop: '0px' }, 300);
};
