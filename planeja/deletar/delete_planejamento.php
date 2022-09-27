<?php
if (isset($_GET['id'])) {
  require '../classes/conexao.php';
  require '../classes/dbdeletar.php';

  $connect = new conexao;
  $connect = $connect->conectar();

  $id = $_GET['id'];

  $delete = new deletar;
  $delete = $delete->deletar_planejamento($id, $connect);

  if ($delete == 'Sucesso') {
    header("location:../planejamentos.php#planejamentocadastrados");
  }
  if ($delete == 'CursoDiferente') {
    echo '<script>alert("Erro! Usuário não possui permissão para deletar planejamentos de outros cursos."); 
                          window.location.assign("../planejamentos.php#planejamentocadastrados")
                  </script>';
  }
} else {
  header('location:../planejamentos.php');
}
