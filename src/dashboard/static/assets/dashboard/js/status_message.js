
var msgCounter = 0;

function showMessage(message, classes) {
    $("#status-message").append(`
        <div id="msg-${msgCounter}" class="rounded-0 alert alert-dismissible fade show ${classes}" role="alert">
            <strong>${message}</strong>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true"><i class="fas fa-times" aria-hidden="true"></i></span>
            </button>
        </div>
	`);
    setAnimation($(`#msg-${msgCounter}`));
    msgCounter += 1;
};

function setAnimation(element) {
    element.animate({ opacity: '0' }, 4000,
        function () {
            $(this).remove();
        }).hover(function () {
            $(this).stop(true).fadeTo(200, 1);
        }, function () {
            setAnimation(element);
        });
};
