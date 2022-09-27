<?php
error_reporting(0);
session_start();

require '../classes/conexao.php';
require '../classes/dbenviar.php';


if (isset($_POST['nomedocente'], $_POST['observacaodocente'])) {


  $connect = new conexao;
  $connect = $connect->conectar();

  $send = new enviar;
  $send = $send->enviar_docente($_POST, $connect);

  if ($send == 'Sucesso') {
    header("location:../docentes.php");
  } else {
    echo "<script>alert('Erro no cadastro!')</script>";
  }
}
