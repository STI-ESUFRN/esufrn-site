<?php
session_start();

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
  <title>Adicionar Componentes ao Curso</title>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="./css/style_adicionarComponentes.css">
  <link rel="stylesheet" type="text/css" href="./css/modal_adicionarComponentes.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script language="javascript" type="text/javascript" src="./js/modal.js"></script>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>


</head>


<body>
  <div id="mask"></div>

  <div class="content">

    <div id="main-title">Adicionar Componentes ao Curso</div>

    <br>

    <div class="title_3" style="padding-left: 14px;margin-top: 0px;">
      &nbsp;&nbsp;&nbsp;<font color="#003b62"><b>Componente</b></font>
    </div>

    <br>

    <div class="iframe_adicionarComponentes">

      <?php

      require './classes/conexao.php';

      if (isset($_GET['id'])) {
        $id = $_GET['id'];
        $connect = new conexao;
        $connect = $connect->conectar();
        $data = $connect->query("SELECT * FROM curso WHERE id = $id");
        $data_name = $data->fetch(PDO::FETCH_ASSOC);
      }

      require './select/select_adicionarComponentes.php';
      ?>

    </div>

    <br><br>

    <div class="title_2" style="padding-left: 14px">
      <font style="font-size: 12px;">COMPONENTE SELECIONADA:</font>
      <font color="#00999d">
        <?php

        if (isset($_GET['comp'])) {
          $comp = $_GET['comp'];

          echo '  
                            <script>
                                document.getElementById(' . $comp . ').style.color = "#fff";
                                document.getElementById(' . $comp . ').style.backgroundColor = "#51a6dc";
                                document.getElementById(' . $comp . ').style.font = "Verdana, sans-serif";
                            </script>';

          echo  '<font style="font-size: 12px; color="#3f95c7"">' . $auxiliar[$comp] . '</font>';
        } else {
          echo "<font style='font-size: 12px;'>NENHUMA COMPONENTE SELECIONADA.</font>";
        }

        ?>
      </font>


    </div>

    <br>

    <a name="<?php if (isset($_GET['comp'])) {
                echo 'modal';
              } else {
                echo 'deletar';
              } ?>" href="<?php if (isset($_GET['comp'])) {
                                                                                              echo '#deletar-turma';
                                                                                            } else {
                                                                                              echo '';
                                                                                            } ?>" onclick="clickou()">

      <button type="button" class="botao" id="btn_cancel">Deletar</button></a>

    <a name="voltar" href="./cursos.php">
      <button type="button" class="botao" id="btn_edit" style="margin-left: 10px;">Voltar</button>
    </a>

    <?php


    if (isset($_GET['del']) and isset($_GET['comp'])) {
      $auxiliar = array_diff($auxiliar, array($auxiliar[$_GET['comp']]));

      $auxiliar2 = implode('-', $auxiliar);

      $sql = "UPDATE curso SET cursocomponentes=? WHERE id=?";
      $con = new conexao;
      $con = $con->conectar();
      $enviar = $con->prepare($sql);

      $enviar->execute(array("$auxiliar2", "$id"));

      echo '<script> window.location.assign("adicionarComponentes.php?id=' . $_GET['id'] . '")</script>';
    }

    ?>
    <!-- MODAL CONFIRMAÇÃO DELETAR -->

    <div id='boxes'>
      <div id='deletar-turma' class="window">

        <div class="modal-header">
          <div class="modal-title">Deletar componente do curso</div>
        </div>

        <br>

        <div class="title_3" style="padding-right:5px">
          Tem certeza de que deseja excluir permanentemente esta componente?
        </div>


        <br />

        <div class="modal-footer">
          <a href="adicionarComponentes.php?id=<?php echo $_GET['id'] ?>&comp=<?php echo $_GET['comp'] ?>&del=True">
            <button type="button" data-dismiss="modal" id="btn_action"> Sim</button></a>
          <button type="button" class="close" data-dismiss="modal" id="btn_cancel">Cancelar</button>
        </div>



      </div>
    </div>


  </div>

  <div class="sidebar">

    <br>

    <div class="modal-title">Nova Componente</div>

    <br>

    <div class="input-group">
      <font style="font-size: 12px;">Curso:</font><br>

      <input type="text" name="cursoAddComponente" class="form-cursoaddcomp" value="<?php echo $data_name["nomecurso"]; ?>" readonly>

    </div>

    <br />

    <form id="enviarcurso" method="post">

      <div class="input-group">
        <font style="font-size: 12px;">Componentes:</font><br>

        <?php

        echo "<select required class='selectcurso' name='selectcursos' form='enviarcurso'>";
        echo "<option disabled selected style='display: none;'>Selecione uma componente</option>";

        $data = $connect->query("SELECT * FROM disciplina ORDER BY nome_disciplina");

        while ($selectcurso = $data->fetch(PDO::FETCH_ASSOC)) {
          echo '<option  value="' . $selectcurso['codigo'] . ' ' . $selectcurso["nome_disciplina"] . '">
                                                    ' . $selectcurso['codigo'] . ' - ' . $selectcurso['nome_disciplina'] . '
                                                    </option>';
        };

        echo "</select>";

        ?>
      </div>

      <br>

      <div class="modal-footer">
        <input type="submit" id="btn_action" value="Cadastrar">
      </div>

    </form>


    <?php



    if (isset($_POST['selectcursos'])) {


      $curso = $_POST['selectcursos'];

      if (empty($data_name["cursocomponentes"])) {
        $aux = $curso;
        $con = new conexao;
        $con = $con->conectar();

        $consults = $con->query("SELECT * FROM curso WHERE id=$id");
        $componente = $consults->fetch(PDO::FETCH_ASSOC);
        $auxilia = explode('*', $componente["cursocomponentes"]);
        $sql = "UPDATE curso SET cursocomponentes=? WHERE id=?";

        $enviar = $con->prepare($sql);

        $enviar->execute(array("$aux", "$id"));

        $_SESSION['mensagem'] = true;

        echo '<script>window.location.href = "adicionarComponentes.php?id=' . $id . '"</script>';
      } else {

        if (strrpos($data_name["cursocomponentes"], $curso) === false) {
          $aux = $data_name["cursocomponentes"] . '*' . $curso;
          $con = new conexao;
          $con = $con->conectar();

          $consults = $con->query("SELECT * FROM curso WHERE id=$id");
          $componente = $consults->fetch(PDO::FETCH_ASSOC);
          $auxilia = explode('-', $componente["cursocomponentes"]);

          $sql = "UPDATE curso SET cursocomponentes=? WHERE id=?";

          $enviar = $con->prepare($sql);

          $enviar->execute(array("$aux", "$id"));

          $_SESSION['mensagem'] = true;


          echo '<script>window.location.href = "adicionarComponentes.php?id=' . $id . '"</script>';
        }
      }
    }

    ?>

  </div>


</body>

</html>