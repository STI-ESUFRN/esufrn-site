<?php

session_start();

if (isset($_SESSION['mensagem'])) {
  echo "<script>alert('Cadastro realizado com sucesso!')</script>";
  session_destroy();
}
if (isset($_SESSION['atualizado'])) {
  echo "<script>alert('Cadastro atualizado com sucesso!')</script>";
  session_destroy();
}
if (isset($_SESSION['errocadastro'])) {
  echo "<script>alert('Erro no cadastro. Tente novamente!')</script>";
  session_destroy();
}

?>

<!DOCTYPE html>

<html lang="pt-br">

<head>
  <title>Cadastro de Cursos</title>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="./css/style_cursos.css">
  <link rel="stylesheet" type="text/css" href="./css/modal_cursos.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script language="javascript" type="text/javascript" src="./js/modal.js"></script>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
</head>

<body>

  <div id="mask"></div>

  <div class="content">

    <div id="main-title">Cadastro de Cursos</div>

    <br>

    <div class="title_3" style="padding-left: 14px;margin-top: 0px;">
      &nbsp;&nbsp;&nbsp;<font color="#003b62"><b>Curso</b></font>
    </div>

    <br>

    <div class="iframe_cursos">

      <?php

      require './select/select_curso.php';

      ?>

    </div>

    <br><br>

    <div class="title_2" style="padding-left: 14px">
      <font style="font-size: 12px;">CURSO SELECIONADO:</font>
      <font color="#00999d">
        <?php

        if (isset($_GET['id'])) {
          $id = $_GET['id'];
          $data = $connect->query("SELECT * FROM curso WHERE id = $id");
          $data_name = $data->fetch(PDO::FETCH_ASSOC);

          echo '
                            <script>
                                document.getElementById(' . $id . ').style.color = "#fff";
                                document.getElementById(' . $id . ').style.backgroundColor = "#51a6dc";
                                document.getElementById(' . $id . ').style.font = "Arial, Helvetica, sans-serif";
                            </script>
                            ';

          echo  '<font style="font-size: 12px;">' . $data_name['nomecurso'] . '</font>';
        } else {
          echo "<font style='font-size: 12px;'>NENHUM CURSO SELECIONADO.</font>";
        }
        ?>
      </font>

    </div>

    <br>


    <a name="editar" href="adicionarComponentes.php?id=<?php echo $id ?>">
      <button type="button" class="botao" id="btn_edit" style="margin-left: 10px; width: 200px;">Adicionar Componentes</button>
    </a>

    <!-- MODAL CONFIRMAÇÃO EDITAR -->

    <div id='boxes'>
      <div id='editar-cursos' class="window">

        <div class="modal-header">
          <div class="modal-title">Editar Curso</div>
        </div>

        <br>

        <div>
          <!-- FORMULARIO -->
          <form action="editar/edita_curso.php?id=<?php echo $id ?>" method="post" autocomplete="off">

            <div class="input-group">
              <font style="font-size: 12px;">Nome do Curso:</font><br>
              <input type="text" required="True" name="nomecursos" class="form-nome" onkeydown="upperCaseF(this)" placeholder="" value="<?php echo $data_name["nomecurso"] ?>" />
            </div>

            <br />

            <div class="modal-footer">
              <input type="submit" id="btn_action" value="Atualizar">
              <button type="button" class="close" data-dismiss="modal" id="btn_cancel">Cancelar</button>
            </div>

          </form>
        </div>


      </div>
    </div>



    <a name="<?php if (isset($_GET['id'])) {
                echo 'modal';
              } else {
                echo 'deletar';
              } ?>" href="<?php if (isset($_GET['id'])) {
                            echo '#delete-cursos';
                          } else {
                            echo '';
                          } ?>">

      <button type="button" class="botao" id="btn_cancel">Deletar</button></a>

    <!-- MODAL CONFIRMAÇÃO DELETAR -->

    <div id='boxes'>
      <div id='delete-cursos' class="window">

        <div class="modal-header">
          <div class="modal-title">Deletar Curso</div>
        </div>

        <br>

        <div class="title_3" style="padding-right:5px">
          Tem certeza de que deseja excluir permanentemente este curso?
        </div>


        <br />

        <div class="modal-footer">
          <a href="deletar/delete_curso.php?id=<?php echo $id ?>"><button type="button" data-dismiss="modal" id="btn_action"> Sim</button></a>
          <button type="button" class="close" data-dismiss="modal" id="btn_cancel">Cancelar</button>
        </div>


      </div>
    </div>

  </div>
  <!-- Modal -->
  <div class="sidebar">


    <br>

    <div class="modal-title">Novo Curso</div>


    <br>

    <div>
      <!-- FORMULARIO -->
      <form action="enviar/envia_curso.php" method="post" autocomplete="off">

        <div class="input-group">
          <font style="font-size: 12px;">Nome do Curso:</font><br>
          <input type="text" required="True" name="nomecurso" class="form-nome" onkeydown="upperCaseF(this)" placeholder="" value="" />
        </div>

        <br />

        <div class="modal-footer">
          <input type="submit" id="btn_action" value="Cadastrar">
        </div>

      </form>
    </div>


  </div>



</body>

</html>