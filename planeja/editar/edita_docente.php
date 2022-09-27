<?php

session_start();

require '../classes/conexao.php';
require '../classes/dbeditar.php';


if (isset($_POST['nomedocente'], $_POST['observacaodocente'])) {

  $id = $_GET['id'];
  $connect = new conexao;
  $connect = $connect->conectar();

  $send = new editar;
  $send = $send->editar_docente($_POST, $connect, $id);

  if ($send == 'Sucesso') {
    $_SESSION['atualizado'] = 'Dado atualizado com sucesso !!!';
    header("location:../docentes.php");
  } else {
    echo "<script>alert('Erro no cadastro!')</script>";
  }
}
