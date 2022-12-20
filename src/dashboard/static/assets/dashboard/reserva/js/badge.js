
var numberCalls = 0;

function refreshBadge(ring = true) {
    $.get("/api/reservas/dashboard/",
        function (data, t, j) {
            if (data.length != numberCalls) {
                numberCalls = data.length
                $("#badgeChamados").text(data.length)
                if (ring) {
                    playAudio();
                }
            }
        }
    );
}

refreshBadge(false);

setInterval(() => {
    refreshBadge();
}, 10000);
