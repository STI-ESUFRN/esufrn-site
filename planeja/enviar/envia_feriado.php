<?php
error_reporting(0);
session_start();

require '../classes/conexao.php';
require '../classes/dbenviar.php';


if (isset($_POST['descricaoferiado'], $_POST['dataferiado'])) {


  $connect = new conexao;
  $connect = $connect->conectar();

  $send = new enviar;
  $send = $send->enviar_feriado($_POST, $connect);

  if ($send == 'Sucesso') {
    header("location:../feriados.php");
  } else {
    echo "<script>alert('Erro no cadastro!')</script>";
  }
}
