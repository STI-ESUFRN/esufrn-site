
var count = 0;
function refreshBadge(ring = true) {
    $.get("/api/admin/chamados/?status=P", (response) => {
        if (count != response.count) {
            count = response.count;
            $("#badgeChamados").text(count > 0 ? count : "");
            if (ring) {
                playAudio();
            }
        }
    });
}

refreshBadge(false);
setInterval(() => {
    refreshBadge();
}, 10000);
