<?php
error_reporting(0);
session_start();

require '../classes/conexao.php';
require '../classes/dbenviar.php';


if (isset($_POST['anosemestre'], $_POST['semestres'], $_POST['selectturmas']) and $_POST['selectturmas'] != 'Selecione um curso') {


  $connect = new conexao;
  $connect = $connect->conectar();

  $send = new enviar;
  $send = $send->enviar_turma($_POST, $connect);

  if ($send == 'Sucesso') {
    header("location:../turmas.php");
  } else {
    echo "<script>alert('Erro no cadastro!')</script>";
    header("location:../turmas.php");
  }
} else {
  $_SESSION['errocadastro'] = 'erro';
  header("location:../turmas.php");
}
