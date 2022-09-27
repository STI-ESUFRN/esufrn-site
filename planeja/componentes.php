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
  <title>Cadastro de Componentes Curriculares</title>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="./css/style_componentes.css">
  <link rel="stylesheet" type="text/css" href="./css/modal_componentes.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script language="javascript" type="text/javascript" src="./js/modal.js"></script>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
</head>

<body>

  <div id="mask"></div>

  <div class="content">

    <div id="main-title">Cadastro de Componentes</div>

    <br>

    <table style="padding-left: 17px;margin-top: -3px;">
      <tr>
        <td class="title_3" width="65px">
          <font color="#003b62">
            <b>Código</b>
          </font>
        </td>
        <td class="title_3" width="425px">
          <font color="#003b62">
            <b>Componente</b>
          </font>
        </td>
        <td class="title_3">
          <font color="#003b62">
            <b>Carga Horária</b>
          </font>
        </td>
        </font>
      </tr>
    </table>

    <br>

    <div class="iframe_componentes">

      <?php

      require './select/select_componente.php';

      ?>

    </div>

    <br><br>

    <div class="title_2" style="padding-left: 14px">
      <font style="font-size: 12px;">COMPONENTE SELECIONADA:</font>
      <font color="#00999d">
        <?php

        if (isset($_GET['id'])) {
          $id = $_GET['id'];
          $data = $connect->query("SELECT * FROM disciplina WHERE id = $id");
          $data_name = $data->fetch(PDO::FETCH_ASSOC);

          echo '
                            <script>
                                document.getElementById(' . $id . ').style.color = "#fff";
                                document.getElementById(' . $id . ').style.backgroundColor = "#51a6dc";
                                document.getElementById(' . $id . ').style.font = "Verdana, sans-serif";
                            </script>
                            ';

          echo '<font style="font-size: 12px;">' . $data_name["nome_disciplina"] . '</font>';
        } else {
          echo "<font style='font-size: 12px;'>NENHUMA COMPONENTE SELECIONADA.</font>";
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
                            echo '#editar-componente';
                          } else {
                            echo '';
                          } ?>">
      <button type="button" class="botao" id="btn_edit" style="margin-left: 10px;">Editar</button>
    </a>

    <!-- MODAL CONFIRMAÇÃO EDITAR -->

    <div id='boxes'>
      <div id='editar-componente' class="window">

        <div class="modal-header">
          <div class="modal-title">Editar Componente</div>
        </div>

        <br>

        <div>
          <!-- FORMULARIO -->
          <form action="./editar/edita_componente.php?id=<?php echo $id ?>" autocomplete="off" method="post">

            <div class="input-group">
              <font style="font-size: 12px;">Nome da Componente:</font><br>
              <input type="text" onkeydown="upperCaseF(this)" name="nomecomp" required="True" class="form-nome" value="<?php echo $data_name["nome_disciplina"] ?>">

            </div>

            <br />

            <div class="input-group">
              <font style="font-size: 12px;">Código:</font>
              <input type="text" onkeydown="upperCaseF(this)" name="codigocomp" class="form-codigo" value="<?php echo $data_name["codigo"] ?>" />
              <font style="font-size: 12px;margin-left: 10px">Carga Horária:</font>
              <input type="number" onkeydown="upperCaseF(this)" name="cargacomp" class="form-cargahoraria" value="<?php echo $data_name["carga_horario"] ?>" />
            </div>

            <br /><br />

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
                            echo '#delete-componente';
                          } else {
                            echo '';
                          } ?>">

      <button type="button" class="botao" id="btn_cancel">Deletar</button></a>

    <!-- MODAL CONFIRMAÇÃO DELETAR -->

    <div id='boxes'>
      <div id='delete-componente' class="window">

        <div class="modal-header">
          <div class="modal-title">Deletar componente</div>
        </div>

        <br>

        <div class="title_3" style="padding-right:5px">
          Tem certeza de que deseja excluir permanentemente esta componente?
        </div>


        <br />

        <div class="modal-footer">
          <a href="./deletar/delete_componente.php?id=<?php echo $id ?>"><button type="button" data-dismiss="modal" id="btn_action"> Sim</button></a>
          <button type="button" class="close" data-dismiss="modal" id="btn_cancel">Cancelar</button>
        </div>


      </div>
    </div>

  </div>
  <div class="sidebar">


    <!-- Modal Dialog -->

    <br>

    <div class="modal-title">Nova Componente Curricular</div>

    <br>

    <!-- FORMULARIO -->
    <form action="enviar/envia_componente.php" autocomplete="off" method="post">

      <div class="input-group">
        <font style="font-size: 12px;">Nome da Componente:</font><br>
        <input type="text" onkeydown="upperCaseF(this)" name="nomecomp" required="True" class="form-nome" value="">

      </div>

      <br />

      <div class="input-group">
        <font style="font-size: 12px;">Código:</font>
        <input type="text" onkeydown="upperCaseF(this)" maxlength="7" name="codigocomp" class="form-codigo" value="ESU0000" onfocus="this.value=''" />
        <font style="font-size: 12px;margin-left: 10px;">Carga Horária:</font>
        <input type="number" onkeydown="upperCaseF(this)" maxlength="3" name="cargacomp" class="form-cargahoraria" />
      </div>

      <br />



      <div class="modal-footer">
        <input type="submit" id="btn_action" value="Cadastrar">
      </div>

    </form>

  </div>


</body>

</html>