<?php

session_start();

require '../classes/conexao.php';
require '../classes/dbenviar.php';


if (isset($_POST['nomecurso'])) {


  $connect = new conexao;
  $connect = $connect->conectar();

  $send = new enviar;
  $send = $send->enviar_curso($_POST, $connect);

  if ($send == 'Sucesso') {
    $_SESSION['mensagem'] = 'Dado atualizado com sucesso !!!';
    header("location:../cursos.php");
  } else {
    echo "<script>alert('Erro no cadastro!')</script>";
  }
}
