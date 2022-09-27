<?php


require './classes/conexao.php';

$connect = new conexao;
$connect = $connect->conectar();
$consulta = $connect->query("SELECT * FROM curso ORDER BY nomecurso");

echo '<ol id="selectable">';
$i = 1;
while ($linha = $consulta->fetch(PDO::FETCH_ASSOC)) {
  $i = $i + 1;
  if (($i % 2) == 0) {
    $parouimpar = 'par';
  } else {
    $parouimpar = 'impar';
  }

  //echo '<li class="li_cursos_'.$parouimpar.'" id="'.$linha["id"].'"> '.$linha["nomecurso"].' <br /></li>';
  echo '<li class="li_cursos_' . $parouimpar . ' " id="' . $linha["id"] . '">'
    . '<table width=530px;>'
    . '<tr>'
    . '<td class="font_li">' . $linha["nomecurso"] . '</td>'
    . '</tr></table></li>';

  echo               '<script>
                                            
                                                document.getElementById(' . $linha["id"] . ').onclick = function(){ 
                                                     window.location.assign("cursos.php?id=' . $linha["id"] . '");
                                                }
                                            
                                            </script>';
}


echo '</ol>';
