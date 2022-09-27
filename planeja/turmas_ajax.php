<?php
require './classes/conexao.php';



$curso = $_POST['curso'];


$connect = new conexao;
$connect = $connect->conectar();
$consulta = $connect->query("SELECT * FROM turma WHERE selectturmas = '$curso' AND statusturma = 'ATIVA'");
echo '<option disabled selected style="display: none;" value=""> Selecione a turma </option>';
while ($linha = $consulta->fetch(PDO::FETCH_ASSOC)) {
  echo '<option value="' . $linha["anosemestre"] . '.' . $linha["semestres"] . '    ' . $linha["selectturmas"] . '">' . $linha["anosemestre"] . '.' . $linha["semestres"] . '    ' . $linha["selectturmas"] . '</option>';
}
