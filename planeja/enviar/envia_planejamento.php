<?php
ini_set('default_charset', 'UTF-8');
error_reporting(0);

session_start();

require '../classes/conexao.php';
require '../classes/dbenviar.php';

$connect = new conexao;
$connect = $connect->conectar();

$send = new enviar;
$send = $send->enviar_planejamento($_POST, $connect);

echo $send;

if ($send == 'Sucesso') {
  $_SESSION['mensagem'] = 'Dado atualizado com sucesso !!!';
  header("location:../planejamentos.php");
} elseif (isset($_SESSION['checkdados-filtro1'])) {

  echo "<script>alert('Erro no cadastro! O docente já está cadastrado em uma disciplina neste ano, semestre, turno e período.');
              window.location= '../planejamentos.php';</script> ";

  unset($_SESSION['checkdados-filtro1']);
} elseif (isset($_SESSION['checkdados-filtro2'])) {

  echo "<script>alert('Erro no cadastro! O docente já está cadastrado em uma disciplina neste ano, semestre, turno e período.');
              window.location= '../planejamentos.php';</script> ";

  unset($_SESSION['checkdados-filtro2']);
} elseif (isset($_SESSION['checkdados-filtro3'])) {

  echo "<script>alert('Erro no cadastro! O docente já está cadastrado em uma disciplina neste ano, semestre, turno e período.');
              window.location= '../planejamentos.php';</script> ";

  unset($_SESSION['checkdados-filtro3']);
} elseif (isset($_SESSION['checkdados-filtro4'])) {

  echo "<script>alert('Erro no cadastro! O docente já está cadastrado em uma disciplina neste ano, semestre, turno e período.');
              window.location= '../planejamentos.php';</script> ";

  unset($_SESSION['checkdados-filtro4']);
} elseif (isset($_SESSION['checkdados-filtro5'])) {

  echo "<script>alert('Erro no cadastro! A carga horária dos docentes está acima da carga horária total da disciplina!');
              window.location= '../planejamentos.php';</script>";

  unset($_SESSION['checkdados-filtro5']);
} elseif (isset($_SESSION['checkdados-filtro6'])) {

  echo "<script>alert('Erro no cadastro! A carga horária dos docentes está abaixo da carga horária total da disciplina!');
              window.location= '../planejamentos.php';</script>";

  unset($_SESSION['checkdados-filtro6']);
} else {
  echo "<script>alert('Erro no cadastro!')</script>";
}
