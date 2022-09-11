var tries = 0

function check_jquery() {
  if (typeof jQuery == 'undefined') {
    alert("AQUI")
    var headTag = document.getElementsByTagName("head")[0];
    var jqTag = document.createElement('script');
    jqTag.type = 'text/javascript';
    jqTag.src = 'assets/js/jquery-3.3.1.min.js';
    jqTag.onload = myJQueryCode;
    headTag.appendChild(jqTag);
  } else {
    set_admin_event();
  }
}

function set_admin_event() {

  if (tries == 3) {
    return;
  }

  try {

    $(document).ready(function () {

      if ($("#id_category").val() != 'evento') {
        $(".field-event_date").hide()
      }

      $("#id_category").change(function (e) {
        if ($(this).val() == 'evento') {
          $(".field-event_date").slideDown()
        } else {
          $(".field-event_date").hide()
        }
      });
    });

  }
  catch {
    check_jquery()
  }

}

check_jquery()
