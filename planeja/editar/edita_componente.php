<?php

session_start();

require '../classes/conexao.php';
require '../classes/dbeditar.php';


if (isset($_POST['nomecomp'])) {

  $id = $_GET['id'];
  $connect = new conexao;
  $connect = $connect->conectar();

  $send = new editar;
  $send = $send->editar_componente($_POST, $connect, $id);

  if ($send == 'Sucesso') {
    $_SESSION['atualizado'] = 'Dado atualizado com sucesso !!!';
    header("location:../componentes.php");
  } else {
    echo "<script>alert('Erro no cadastro!')</script>";
  }
}
