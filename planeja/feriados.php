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
  <title>Cadastro de Feriados</title>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="./css/style_feriados.css">
  <link rel="stylesheet" type="text/css" href="./css/modal_feriados.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script language="javascript" type="text/javascript" src="./js/modal.js"></script>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
</head>

<body>

  <div id="mask"></div>

  <div class="content">

    <div id="main-title">Cadastro de Feriados</div>

    <br>

    <table style="padding-left: 17px;margin-top: -3px;">
      <tr>
        <td class="title_3" width="51px">
          <font color="#003b62">
            <b>Data</b>
          </font>
        </td>
        <td class="title_3">
          <font color="#003b62">
            <b>Descrição</b>
          </font>
        </td>
      </tr>
    </table>

    <br>

    <div class="iframe_feriados">

      <?php

      require './select/select_feriado.php';

      ?>

    </div>

    <br><br>

    <div class="title_2" style="padding-left: 14px">
      <font style="font-size: 12px;">FERIADO SELECIONADO:</font>
      <font color="#00999d">
        <?php

        if (isset($_GET['id'])) {
          $id = $_GET['id'];
          $data = $connect->query("SELECT * FROM feriado WHERE id_feriado = $id");
          $data_name = $data->fetch(PDO::FETCH_ASSOC);

          echo '
                            <script>
                                document.getElementById(' . $id . ').style.color = "#fff";
                                document.getElementById(' . $id . ').style.backgroundColor = "#51a6dc";                                
                                document.getElementById(' . $id . ').style.font = "Verdana, sans-serif";
                            </script>
                            ';

          echo  '<font style="font-size: 12px;">' . date('d/m', strtotime($data_name["data_feriado"])) . '</font>' . '&nbsp;' . '<font style="font-size: 12px;">' . $data_name['descricao_feriado'] . '</font>';
        } else {
          echo "<font style='font-size: 12px;'>NENHUM FERIADO SELECIONADO.</font>";
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
                            echo '#editar-feriado';
                          } else {
                            echo '';
                          } ?>">
      <button type="button" class="botao" id="btn_edit" style="margin-left: 10px;">Editar</button>
    </a>

    <!-- MODAL CONFIRMAÇÃO EDITAR -->

    <div id='boxes'>
      <div id='editar-feriado' class="window">

        <div class="modal-header">
          <div class="modal-title">Editar Feriado</div>
        </div>

        <br>

        <div>
          <!-- FORMULARIO -->
          <form action="editar/edita_feriado.php?id=<?php echo $id ?>" autocomplete="off" method="post">

            <div class="input-group">
              <font style="font-size: 12px;">Descrição:</font><br>
              <input type="text" name="descricaoferiado" required="True" class="form-descricao" onkeydown="upperCaseF(this)" value="<?php echo $data_name["descricao_feriado"] ?>">

            </div>

            <br />

            <div class="input-group">
              <font style="font-size: 12px;">Data:</font><br>
              <input type="date" required="True" name="dataferiado" class="form-data" placeholder="dd/mm/aaaa" onkeydown="upperCaseF(this)" value="<?php echo $data_name["data_feriado"] ?>" />
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
                            echo '#delete-feriado';
                          } else {
                            echo '';
                          } ?>">

      <button type="button" class="botao" id="btn_cancel">Deletar</button></a>

    <!-- MODAL CONFIRMAÇÃO DELETAR -->

    <div id='boxes'>
      <div id='delete-feriado' class="window">

        <div class="modal-header">
          <div class="modal-title">Deletar Feriado</div>
        </div>

        <br>

        <div class="title_3" style="padding-right:5px">
          Tem certeza de que deseja excluir permanentemente este feriado?
        </div>


        <br />

        <div class="modal-footer">
          <a href="deletar/delete_feriado.php?id=<?php echo $id ?>"><button type="button" data-dismiss="modal" id="btn_action"> Sim</button></a>
          <button type="button" class="close" data-dismiss="modal" id="btn_cancel">Cancelar</button>
        </div>


      </div>
    </div>


  </div>
  <div class="sidebar">

    <!-- Modal Dialog -->

    <br>

    <div class="modal-title">Novo Feriado</div>

    <br>

    <div>
      <!-- FORMULARIO -->
      <form action="enviar/envia_feriado.php" method="post" autocomplete="off">

        <div class="input-group">
          <font style="font-size: 12px;">Descrição:</font><br>
          <input type="text" name="descricaoferiado" required="True" onkeydown="upperCaseF(this)" class="form-descricao" value="">

        </div>

        <br />

        <div class="input-group">
          <font style="font-size: 12px;">Data:</font><br>
          <input type="date" required="True" name="dataferiado" class="form-data" placeholder="dd/mm/aaaa" />
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