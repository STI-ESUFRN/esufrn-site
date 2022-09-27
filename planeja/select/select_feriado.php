<?php

require './classes/conexao.php';

$connect = new conexao;
$connect = $connect->conectar();
$consulta = $connect->query("SELECT * FROM feriado ORDER BY data_feriado");

echo '<ol id="selectable">';
$i = 1;
while ($linha = $consulta->fetch(PDO::FETCH_ASSOC)) {
  $i = $i + 1;
  if (($i % 2) == 0) {
    $parouimpar = 'par';
  } else {
    $parouimpar = 'impar';
  }
  // aqui eu mostro os valores de minha consulta
  //echo '<li class="li_feriados_'.$parouimpar.' " id="'.$linha["id_feriado"].'">'.date('d/m',strtotime($linha["data_feriado"])).'&nbsp;&nbsp;&nbsp;&nbsp;'.$linha["descricao_feriado"].'<br /></li>';
  echo '<li class="li_feriados_' . $parouimpar . ' " id="' . $linha["id_feriado"] . '">'
    . '<table width=530px>'
    . '<tr>'
    . '<td class="font_li" width="54px">' . date('d/m', strtotime($linha["data_feriado"])) . '</td>'
    . '<td class="font_li" width="450px" >' . $linha["descricao_feriado"] . '</td>'
    . '</tr></table></li>';



  echo               '<script>
                                            
                                                document.getElementById(' . $linha["id_feriado"] . ').onclick = function(){ 
                                                     window.location.assign("feriados.php?id=' . $linha["id_feriado"] . '");
                                                }
                                            
                                            </script>';
}


echo '</ol>';
