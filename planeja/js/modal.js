$(document).ready(function () {
  //seleciona os elementos a com atributo name="modal"
  $("a[name=modal]").click(function (e) {
    //cancela o comportamento padrão do link
    e.preventDefault();

    //armazena o atributo href do link
    var id = $(this).attr("href");

    //armazena a largura e a altura da tela
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();

    //Define largura e altura do div#mask iguais ás dimensões da tela
    $("#mask").css({ width: maskWidth, height: maskHeight });

    //efeito de transição
    $("#mask").fadeIn(10);
    //	$('#mask').fadeTo(50,0.5);

    //armazena a largura e a altura da janela
    var winH = $(window).height();
    var winW = $(window).width();
    //centraliza na tela a janela popup
    $(id).css("top", -450);
    $(id).css("left", winW / 2 - $(id).width() / 2 - 80);
    //efeito de transição
    $(id).show();
    $(id).animate({ top: "70px" }, 200);

    //se o botãoo fechar for clicado

    $(".window .close").click(function (e) {
      //cancela o comportamento padrão do link
      e.preventDefault();
      //$('#mask, .window').hide();
      $("#mask").hide();
      $(id).animate({ top: "-500" }, 100);
      $(".window").hide(1);
    });

    //se div#mask for clicado
    $("#mask").click(function () {
      $(id).animate({ top: "-500" }, 100);
      $("#mask").hide();
      $(".window").hide(1);
    });
  });
});
function upperCaseF(a) {
  setTimeout(function () {
    a.value = a.value.toUpperCase();
  }, 1);
}
