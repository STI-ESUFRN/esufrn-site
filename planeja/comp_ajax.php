<?php
require './classes/conexao.php';

$curso = $_POST['curso'];
$connect = new conexao;
$connect = $connect->conectar();
$consulta = $connect->query("SELECT * FROM curso WHERE nomecurso = '$curso'");

$componente = $consulta->fetch(PDO::FETCH_ASSOC);

$auxilia = explode('*', $componente["cursocomponentes"]);

//echo "<script>alert('".sizeof($auxilia)."');</script>";
echo '<option disabled selected style="display: none;" value=""> Selecione o componente curricular </option>';
$contador = 0;
while ($contador < sizeof($auxilia)) {
  echo '<option value="' . $auxilia[$contador] . '"> ' . $auxilia[$contador] . ' </option>';
  $contador++;
}
