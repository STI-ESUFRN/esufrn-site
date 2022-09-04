
function playAudio() {
    var audio = document.getElementById("notificationAudio");
    audio.play();
}

function loadAudio() {
    audio = $("<audio />", {
        id: "notificationAudio",
    });
    source = $("<source />", {
        src: "/static/assets/dashboard/media/notification.mp3",
        type: "audio/mpeg"
    });

    audio.append(source, "Your browser does not support the audio element.");

    $("body").append(audio);
}

loadAudio();