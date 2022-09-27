<?php
$con = new conexao;
$con = $con->conectar();
$consulta = $con->query("SELECT * FROM curso WHERE id=$id");
$componentes = $consulta->fetch(PDO::FETCH_ASSOC);

$auxiliar = explode('*', $componentes["cursocomponentes"]);

echo '<ol id="selectable">';
$i = 1;
$j = 0;
while ($j < count($auxiliar)) {
  $i = $i + 1;
  if (($i % 2) == 0) {
    $parouimpar = 'par';
  } else {
    $parouimpar = 'impar';
  }
  // aqui eu mostro os valores de minha consulta
  //echo '<li class="li_feriados_'.$parouimpar.' " id="'.$linha["id_feriado"].'">'.date('d/m',strtotime($linha["data_feriado"])).'&nbsp;&nbsp;&nbsp;&nbsp;'.$linha["descricao_feriado"].'<br /></li>';
  echo '<li class="li_adicionarComponentes_' . $parouimpar . '" id=' . $j . '>'
    . '<table>'
    . '<tr>'
    . '<td class="font_li">' . $auxiliar[$j] . '</td>'
    . '</tr></table></li>';



  echo '
  <script>
    document.getElementById(' . $j . ').onclick = function(){ 
      window.location.assign("./adicionarComponentes.php?id=' . $id . '&comp=' . $j . '");
    }
  </script>';
  $j = $j + 1;
}


echo '</ol>';
