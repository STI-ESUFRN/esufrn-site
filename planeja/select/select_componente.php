<?php

require './classes/conexao.php';

$connect = new conexao;
$connect = $connect->conectar();
$consulta = $connect->query("SELECT * FROM disciplina ORDER BY nome_disciplina");

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
  echo '<li class="li_componentes_' . $parouimpar . ' " id="' . $linha["id"] . '">'
    . '<table>'
    . '<tr>'
    . '<td width="70px" class="font_li">' . $linha["codigo"] . '</td>'
    . '<td width="480px" class="font_li">' . $linha["nome_disciplina"] . '</td>'
    . '<td width="50px" class="font_li">' . $linha["carga_horario"] . 'h</td>'
    . '</tr></table></li>';



  echo               '<script>
                                            
                                                document.getElementById(' . $linha["id"] . ').onclick = function(){ 
                                                     window.location.assign("./componentes.php?id=' . $linha["id"] . '");
                                                }
                                            
                                            </script>';
}


echo '</ol>';
