<?php
if (isset($_GET['id'])) {
  require '../classes/conexao.php';
  require '../classes/dbdeletar.php';

  $connect = new conexao;
  $connect = $connect->conectar();

  $id = $_GET['id'];

  $delete = new deletar;
  $delete = $delete->deletar_curso($id, $connect);


  if ($delete == 'Sucesso') {
    header("location:../cursos.php");
  } else {
    echo "<script>alert('Erro!')</script>";
  }
} else {
  header('location:../cursos.php');
}
