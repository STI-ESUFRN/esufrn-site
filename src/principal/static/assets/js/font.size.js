var font_base = {};
function mudaFonteAntigo(escala) {
  var font_aumenta = { ".cabecalho h3": "", ".cabecalho h5": "", ".cabecalho p": "", ".corpo p": ""};
  $.each(font_aumenta, function (i, v) {
      font_aumenta[i] = $(i).css("font-size")
      font_aumenta[i] = font_aumenta[i].substring(0, font_aumenta[i].length-2).toString();
  });
  jQuery.isEmptyObject(font_base) ? font_base = font_aumenta : NaN
  if (escala == 1){
    $.each(font_aumenta, function (i, v) {
      $(i).css({"font-size": v * 0.9})
    });
  } else if (escala == 2) {
    $.each(font_aumenta, function (i, v) {
      $(i).css({"font-size": v * 1.1})
    });
  } else {
    $.each(font_base, function (i, v) {
      $(i).css({"font-size": v * 1})
    });
  }
}
function mudaFonte(escala) {
  var font_aumenta = {
    '.owl-item h2': "",
    'section h1': "",
    'section h3': "",
    'section button': "",
    'section h5': "",
    'section .titulo p': "",
    'section label': "",
    '.cabecalho h3': "",
    '.cabecalho h5': "",
    '.cabecalho p': "",
    '.corpo p': "",
    '.depoimento-item p': "",
  };
  $.each(font_aumenta, function (i, v) {
      font_aumenta[i] = $(i).css("font-size")
      if (font_aumenta[i] == undefined){
        delete font_aumenta[i]
      } else {
        font_aumenta[i] = font_aumenta[i].substring(0, font_aumenta[i].length-2).toString();
      }
  });
  jQuery.isEmptyObject(font_base) ? font_base = font_aumenta : NaN
  if (escala == 1){
    $.each(font_aumenta, function (i, v) {
      $(i).css({"font-size": v * 0.9})
    });
  } else if (escala == 2) {
    $.each(font_aumenta, function (i, v) {
      $(i).css({"font-size": v * 1.1})
    });
  } else {
    $.each(font_base, function (i, v) {
      $(i).css({"font-size": v * 1})
    });
  }
}
