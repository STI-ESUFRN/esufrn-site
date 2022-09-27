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
  <title>Cadastro de Turmas</title>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="./css/style_turmas.css">
  <link rel="stylesheet" type="text/css" href="./css/modal_turmas.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script language="javascript" type="text/javascript" src="./js/modal.js"></script>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
</head>

<body>

  <div id="mask"></div>

  <div class="content">

    <div id="main-title">Cadastro de Turmas</div>

    <br>

    <table style="padding-left: 17px;margin-top: -3px;">
      <tr>
        <td class="title_3" width="53px">
          <font color="#003b62">
            <b>Período</b>
          </font>
        </td>
        <td class="title_3" width="58px">
          <font color="#003b62">
            <b>Status</b>
          </font>
        </td>
        <td class="title_3">
          <font color="#003b62">
            <b>Curso</b>
          </font>
        </td>
        </font>
      </tr>
    </table>


    <br>

    <div class="iframe_turmas">

      <?php

      require './select/select_turma.php';

      ?>

    </div>

    <br><br>

    <div class="title_2" style="padding-left: 14px">
      <font style="font-size: 12px;">TURMA SELECIONADA:</font>
      <font color="#00999d">
        <?php

        if (isset($_GET['id'])) {
          $id = $_GET['id'];
          $data = $connect->query("SELECT * FROM turma WHERE id = $id");
          $turmas = $data->fetch(PDO::FETCH_ASSOC);

          echo '
                            <script>
                                document.getElementById(' . $id . ').style.color = "#fff";
                                document.getElementById(' . $id . ').style.backgroundColor = "#51a6dc";
                                document.getElementById(' . $id . ').style.font = "Verdana, sans-serif";
                            </script>
                            ';

          echo  '<font style="font-size: 12px;">' . $turmas['selectturmas'] . '</font>';
        } else {
          echo "<font style='font-size: 12px;'>NENHUMA TURMA SELECIONADA.</font>";
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
                            echo '#editar-turma';
                          } else {
                            echo '';
                          } ?>">
      <button type="button" class="botao" id="btn_edit" style="margin-left: 10px;">Editar</button>
    </a>

    <!-- MODAL CONFIRMAÇÃO EDITAR -->

    <div id='boxes'>
      <div id='editar-turma' class="window">

        <div class="modal-header">
          <div class="modal-title">Editar Turma</div>
        </div>

        <br>

        <div>
          <!-- FORMULARIO -->
          <form action="./editar/edita_turma.php?id=<?php echo $id ?>" method="post" autocomplete="off" id="editarturmas">
            <table>
              <tr>
                <td>
                  <div class="input-group">
                    <font style="font-size: 12px;">Ano:</font> <input type="number" name="anosemestre" placeholder='' minlength="4" maxlength="4" required="True" class="form-anosemestre" value="<?php echo $turmas["anosemestre"] ?>" readonly>
                  </div>
                </td>
                <td>
                  <div class="input-group">
                    <font style="font-size: 12px;">Semestre:</font>
                    <input type="text" name="semestres" class="selectsemestre_edit" value="<?php echo $turmas["semestres"]; ?>" readonly>
                  </div>
                </td>
              </tr>
            </table>

            <br />
            <table>
              <tr>
                <td style="padding-left: 13px;">
                  <font style="font-size: 12px;">Curso:</font>
                </td>
                <td>
                  <input type="text" name="selectturmas" class="selectsemestre_cursos" value="<?php echo $turmas["selectturmas"]; ?>" readonly>
                </td>

              </tr>
              <tr>
                <td style="padding-left: 10px;padding-top: 25px;">

                  <input name="statusturma" value="ATIVA" id="turmaativa" type="checkbox" <?php if ($turmas["statusturma"] == 'ATIVA') {
                                                                                            echo "checked";
                                                                                          } ?>>
                  <font style="font-size: 16px;"> Ativa</font>

                </td>
              </tr>
            </table>

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
                            echo '#deletar-turma';
                          } else {
                            echo '';
                          } ?>">

      <button type="button" class="botao" id="btn_cancel">Deletar</button></a>

    <!-- MODAL CONFIRMAÇÃO DELETAR -->

    <div id='boxes'>
      <div id='deletar-turma' class="window">

        <div class="modal-header">
          <div class="modal-title">Deletar Turma</div>
        </div>

        <br>

        <div class="title_3" style="padding-right:5px">
          Tem certeza de que deseja excluir permanentemente esta turma?
        </div>


        <br />

        <div class="modal-footer">
          <a href="deletar/delete_turma.php?id=<?php echo $_GET['id'] ?>"><button type="button" data-dismiss="modal" id="btn_action"> Sim</button></a>
          <button type="button" class="close" data-dismiss="modal" id="btn_cancel">Cancelar</button>
        </div>


      </div>
    </div>

  </div>
  <div class="sidebar">


    <br>

    <div class="modal-title">Nova Turma</div>

    <br>


    <!-- FORMULARIO -->
    <form action="enviar/envia_turma.php" method="post" autocomplete="off" id="enviarturmas">
      <table>
        <tr>
          <td>
            <div class="input-group">
              <font style="font-size: 12px;">Ano:</font> <input type="number" name="anosemestre" placeholder='' minlength="4" maxlength="4" max="<?php echo date('Y') + 100; ?>" min="2016" required="True" class="form-anosemestre-new" value="<?php echo date('Y'); ?>">
            </div>
          </td>
          <td>
            <div class="input-group">
              <font style="font-size: 12px;">Semestre:</font>
              <select required="True" class="selectsemestre" name="semestres" form="enviarturmas">
                <option value="1">1</option>
                <option value="2">2</option>
              </select>
            </div>
          </td>
        </tr>
      </table>

      <table>
        <tr>
          <td style="padding-left: 13px;padding-top:10px;">
            <font style="font-size: 12px;">Curso:</font> <br>

            <?php

            echo "<select required class='selectsemestre_cursos2' name='selectturmas' form='enviarturmas'>";
            echo "<option disabled selected style='display: none;'>Selecione um Curso</option>";


            $data = $connect->query("SELECT * FROM curso ORDER BY nomecurso");

            while ($selectturma = $data->fetch(PDO::FETCH_ASSOC)) {
              echo '<option  value="' . $selectturma["nomecurso"] . '">' . $selectturma['nomecurso'] . '</option>';
            };

            echo "</select>";

            ?>
          </td>
        </tr>
        <tr>
          <td style="padding-left: 10px;padding-top: 25px;">
            <input name="statusturma" value="ATIVA" id="turmaativa" type="checkbox">
            <font style="font-size: 16px;"> Ativa</font>
          </td>
        </tr>
      </table>



      <div class="modal-footer" style="padding-top: 5px;">
        <input type="submit" id="btn_action" value="Cadastrar">

      </div>

    </form>








  </div>


</body>

</html>