
function showAlerts() {
    if (!sessionStorage.getItem('alerts')) {
        sessionStorage.setItem('alerts', '[]');
    }
    let alerts = JSON.parse(sessionStorage.getItem('alerts'));
    $.each($(".notification-modal"), function () {
        let id = $(this).attr('data-alert-id');
        if (alerts && alerts.includes(id)) {
            $(this).remove();
        } else {
            $(this).on('hidden.bs.modal', function (e) {
                let showed = JSON.parse(sessionStorage.getItem('alerts'));
                showed.push(id);
                sessionStorage.setItem('alerts', JSON.stringify(showed));

                $(this).remove();
                $(".notification-modal").first().modal('show');
            });
        }
    });
    $(".notification-modal").first().modal('show');
}

$(document).ready(function ($) {
    $('.slide-owl').owlCarousel({
        items: 1,
        loop: true,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        dots: true,
    });

    $('.portais-owl').owlCarousel({
        loop: true,
        autoplay: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: false,
        nav: false,
        dots: false,
        responsive: {
            0: {
                items: 1, nav: false, loop: true,
            },
            600: {
                items: 2, nav: false, loop: true,
            },
            1000: {
                items: 3, nav: false, loop: true,
            },
            1200: {
                items: 4, nav: false, loop: true,
            }
        },
    });

    $('.depoimentos-owl').owlCarousel({
        items: 2,
        center: true,
        loop: true,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            700: {
                items: 2
            }
        },
        dots: false,
    });

    showAlerts();
});

$("#newsletter-form").submit(function (e) {
    e.preventDefault();

    var serialized_data = $("#newsletter-form [name!=category]").serialize();
    serialized_data += "&category=" + $("#newsletter-form [name=category]:checked").map(function () {
        return $(this).val();
    }).get().join(',');

    $.ajax({
        type: "POST",
        url: '/newsletter/subscribe/',
        data: serialized_data,
        success: function (response) {
            if (response.status == "success") {
                $('#newsletter-form').trigger("reset");
                $("#newsletter-form .status-message").html(`
					<p class="text-success">
						<strong>${response.message}</strong>
					</p>
				`);
            } else {
                $("#newsletter-form .status-message").html(`
					<p class="text-danger">
						<strong>${response.message}</strong>
					</p>
				`);
            }
        },
        error: function (response) {
            $("#newsletter-form .status-message").html(`
                <p class="text-danger">
                    <strong>${response.responseJSON.message}</strong>
                </p>
			`);
        }
    });
});
