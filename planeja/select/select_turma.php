<?php

require './classes/conexao.php';

$connect = new conexao;
$connect = $connect->conectar();
$consulta = $connect->query("SELECT * FROM turma ORDER BY anosemestre DESC, semestres DESC ");

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
  echo '<li class="li_turmas_' . $parouimpar . '" id="' . $linha["id"] . '">'
    . '<table width="530px" >'
    . '<tr>'
    . '<td class="font_li" width="60px">' . $linha["anosemestre"] . '.' . $linha["semestres"] . '</td>'
    . '<td class="font_li" width="60px" >' . $linha["statusturma"] . '</td>'
    . '<td class="font_li" width="400px" >' . $linha["selectturmas"] . '</td>'
    . '</tr></table></li>';



  echo               '<script>
                                            
                                                document.getElementById(' . $linha["id"] . ').onclick = function(){ 
                                                     window.location.assign("turmas.php?id=' . $linha["id"] . '");
                                                }
                                            
                                            </script>';
}


echo '</ol>';
