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
  <title>Cadastro de Docentes</title>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="./css/style_docentes.css">
  <link rel="stylesheet" type="text/css" href="./css/modal_docentes.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script language="javascript" type="text/javascript" src="./js/modal.js"></script>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
</head>

<body>

  <div id="mask"></div>

  <div class="content">

    <div id="main-title">Cadastro de Docentes</div>

    <br>

    <div class="title_3" style="padding-left: 11px; margin-top: -3px;">
      <font color="#003b62"><b>
          <table width=700px>
            <tr>
              <td width="230px">&nbsp;&nbsp;&nbsp;Nome</td>
              <td width="250px">&nbsp;&nbsp;&nbsp;Observação</td>
            </tr>
          </table>
        </b>
      </font>
    </div>

    <br>

    <div class="iframe_docentes">

      <?php

      require './select/select_docente.php';

      ?>

    </div>

    <br><br>

    <div class="title_2" style="padding-left: 14px">
      <font style="font-size: 12px;">DOCENTE SELECIONADO:</font>
      <font color="#00999d">
        <?php

        if (isset($_GET['id'])) {
          $id = $_GET['id'];
          $data = $connect->query("SELECT * FROM docente WHERE id_docente = $id");
          $data_name = $data->fetch(PDO::FETCH_ASSOC);

          echo '
                            <script>
                                document.getElementById(' . $id . ').style.color = "#fff";
                                document.getElementById(' . $id . ').style.backgroundColor = "#51a6dc";
                                document.getElementById(' . $id . ').style.font = "Arial, Helvetica, sans-serif";
                            </script>
                            ';

          echo  '<font style="font-size: 12px;">' . $data_name["nomedocente"] . '</font>';
        } else {
          echo "<font style='font-size: 12px;'>NENHUM DOCENTE SELECIONADO.</font>";
        }
        ?>
      </font>

    </div>

    <br>

    <a name="<?php if (isset($_GET['id'])) {
                echo 'modal';
              } else {
                echo 'editar';
              } ?>" href="<?php if (isset($_GET['id'])) {
                            echo '#editar-docente';
                          } else {
                            echo '';
                          } ?>">
      <button type="button" class="botao" id="btn_edit" style="margin-left: 10px;">Editar</button>
    </a>

    <!-- MODAL CONFIRMAÇÃO EDITAR -->

    <div id='boxes'>
      <div id='editar-docente' class="window">

        <div class="modal-header">
          <div class="modal-title">Editar Docente</div>
        </div>

        <br>

        <div>
          <!-- FORMULARIO -->
          <form action="./editar/edita_docente.php?id=<?php echo $id ?>" autocomplete="off" method="post">

            <div class="input-group">
              <font style="font-size: 12px;">Nome:</font><br>
              <input type="text" name="nomedocente" required="True" class="form-descricao" onkeydown="upperCaseF(this)" value="<?php echo $data_name["nomedocente"] ?>">

            </div>

            <br />

            <div class="input-group">
              <font style="font-size: 12px;">Observação:</font><br>
              <input type="text" name="observacaodocente" class="form-descricao" onkeydown="upperCaseF(this)" value="<?php echo $data_name["observacaodocente"] ?>" />
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
                            echo '#delete-docente';
                          } else {
                            echo '';
                          } ?>">

      <button type="button" class="botao" id="btn_cancel">Deletar</button></a>

    <!-- MODAL CONFIRMAÇÃO DELETAR -->

    <div id='boxes'>
      <div id='delete-docente' class="window">

        <div class="modal-header">
          <div class="modal-title">Deletar Docente</div>
        </div>

        <br>

        <div class="title_3" style="padding-right:5px">
          Tem certeza de que deseja excluir permanentemente este docente?
        </div>


        <br />

        <div class="modal-footer">
          <a href="./deletar/delete_docente.php?id=<?php echo $id ?>"><button type="button" data-dismiss="modal" id="btn_action"> Sim</button></a>
          <button type="button" class="close" data-dismiss="modal" id="btn_cancel">Cancelar</button>
        </div>


      </div>
    </div>



  </div>
  <div class="sidebar">

    <!-- Modal Dialog -->

    <br>

    <div class="modal-title">Novo Docente</div>

    <br>

    <div>
      <!-- FORMULARIO -->
      <form action="./enviar/envia_docente.php" method="post" autocomplete="off">

        <div class="input-group">
          <font style="font-size: 12px;">Nome:</font><br>
          <input type="text" name="nomedocente" required="True" onkeydown="upperCaseF(this)" maxlength="45" class="form-descricao" value="">

        </div>

        <br />

        <div class="input-group">
          <font style="font-size: 12px;">Observação:</font><br>
          <input type="text" name="observacaodocente" onkeydown="upperCaseF(this)" maxlength="25" class="form-descricao" />
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