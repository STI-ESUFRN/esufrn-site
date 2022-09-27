<?php
require './classes/conexao.php';

//echo '<script>alert("Entrouuu");</script>';//Esta funfando
$componente = $_POST['componente'];
$aux = explode(" ", $componente, 2);
$codigo_comp = $aux[0];
$nome_comp = $aux[1];
$connect = new conexao;
$connect = $connect->conectar();
$consulta = $connect->query("SELECT * FROM disciplina WHERE nome_disciplina = '$nome_comp'");
$disciplina = $consulta->fetch(PDO::FETCH_ASSOC);
//echo '<script>alert("'.$disciplina['carga_horario'].'");</script>';
echo '<script>$("#plan_ch").val("' . $disciplina['carga_horario'] . '");</script>';
