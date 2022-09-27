<?php
require './classes/conexao.php';

$connect = new conexao;
$connect = $connect->conectar();


$quantidade = $_POST['quantidade'];
$carga = $_POST['carga'];
$checkcarga = $_POST['checkcarga'];
$inc = 0;
$i = 0;
echo '<br>';

echo '<script>  var valor = 0; </script>';
while ($inc < $quantidade) {

  $consulta = $connect->query("SELECT * FROM docente ORDER BY nomedocente");
  echo '<br>';
  echo '<div>';
  echo '	Selecione o docente:';
  echo '	<select name="plan_doc' . $inc . '" class="selectdocente" id="plan_doc' . $inc . '">';
  echo '		<option disabled selected style="display: none;"" value=""> Selecione o docente </option>';
  while ($linha = $consulta->fetch(PDO::FETCH_ASSOC)) {
    echo "<option val=" . $linha['nomedocente'] . "> " . $linha['nomedocente'] . "</option>";
  }
  echo '	</select>';
  echo '</div>';
  echo '<div>';
  echo   'Local: <input name="plan_loc' . $inc . '" class="form-local" id="plan_loc' . $inc . '">';
  echo '</div>';
  echo '<div>';
  if ($carga === $checkcarga) {
    echo   'Carga Horária: <input type="number" name="plan_ch' . $inc . '" class="form-cargahoraria" id="plan_ch' . $inc . '" value="' . $carga . '" readonly="true" min="0">';
  } else if ($carga === "caso3") {
    echo   'Carga Horária: <input type="number" name="plan_ch' . $inc . '" class="form-cargahoraria" id="plan_ch' . $inc . '" value="0" min="0">';
  } else {

    echo '<script>
                
                
                var valor = Array(' . $quantidade . ').fill(0);

                $("#plan_ch' . $inc . '").change(function() {
                      
                    var i = ' . $inc . ';

                    valor[i] = parseInt($("#plan_ch' . $inc . '").val());
                    
                    if(valor.length == ' . $quantidade . '){

                        var sum=0;

                        for(cont = 0; cont < valor.length; cont++ ){
                            sum += valor[cont];
                        }
                        if(sum > ' . $checkcarga . '){
                            alert("Limite da Carga Horária (CH) da disciplina foi ultrapassado!");
                        }
                        if(sum < ' . $checkcarga . '){
                            alerta("Limite da Carga Horária (CH) da disciplina abaixo do esperado em "' . $checkcarga . '-sum" horas!");
                        }
                    }
                });

                </script>';

    echo    'Carga Horária: <input type="number" name="plan_ch' . $inc . '" class="form-cargahoraria"  id="plan_ch' . $inc . '" value="0" min="0">';
  }
  echo '</div>';
  //echo    '<br>';
  echo    '<div style="float:left">';
  //echo    '<div>';
  echo    'Data inicial: <input type="date" name="plan_date_in' . $inc . '" id="plan_date_in' . $inc . '"  class="form-data" style="margin-left: 60px; padding-left: 10px;">';
  echo    '</div>';
  echo    '<div>  ';
  echo    ' &nbsp;&nbsp;&nbsp;&nbsp;Data final: <input type="date" name="plan_date_out' . $inc . '" id="plan_date_out' . $inc . '"  class="form-data" style="margin-left: 20px; padding-left: 10px;">';
  echo    '</div>';



  $inc++;
}
