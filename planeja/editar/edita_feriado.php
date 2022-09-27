<?php

session_start();

require '../classes/conexao.php';
require '../classes/dbeditar.php';


if (isset($_POST['descricaoferiado'], $_POST['dataferiado'])) {

  $id = $_GET['id'];
  $connect = new conexao;
  $connect = $connect->conectar();

  $send = new editar;
  $send = $send->editar_feriado($_POST, $connect, $id);

  if ($send == 'Sucesso') {
    $_SESSION['atualizado'] = 'Dado atualizado com sucesso !!!';
    header("location:../feriados.php");
  } else {
    echo "<script>alert('Erro no cadastro!')</script>";
  }
}
