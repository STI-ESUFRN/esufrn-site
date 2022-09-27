<?php
ini_set('default_charset', 'UTF-8');
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
  <title>Sigep</title>
  <meta charset="UTF-8">
  <script src="./js/jquery-3.2.1.min.js"></script>
  <link rel="stylesheet" type="text/css" href="./css/style_relatorios.css">
  <link rel="stylesheet" type="text/css" href="./css/modal_relatorios.css">
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  <script language="javascript" type="text/javascript" src="./js/modal.js"></script>
</head>

<body>

  <div id="mask"></div>

  <div class="content">


    <div id="main-title">Relatórios</div>

    <br><br>

    <div class="panel-group" id="accordion" style="width:800px;">
      <div class="panel panel-default">
        <form target="_blank" method="POST" autocomplete="off" action="relatorio_docente2.php" id="selectdocentes">

          <a data-toggle="collapse" data-parent="#accordion" href="#collapse1" id="padrao">
            <div class="panel-heading" style="background: #f9f9f9;">
              <h4 class="panel-title">
                Relatório Docente
              </h4>
            </div>
          </a>

          <div id="collapse1" class="panel-collapse collapse ">
            <div class="panel-body">

              <div style="padding-left: 17px;">
                <!--<div >-->
                <font style="font-size: 12px;">Ano:</font>
                <font style="font-size: 12px; padding-left: 63px;">Semestre:</font> <br>
                <input type="text" value="" minlength="4" maxlength="4" name="selectano" class="form-anosemestre" required="True">
                .
                <select class="selectsemestre" name="selectsemestre" required="True">
                  <option value="1">1</option>
                  <option value="2">2</option>
                </select> <br>
                <br>
                <div id="doc_primario">
                  <font style="font-size: 12px;">Docente:</font> <br>
                  <?php

                  require './classes/conexao.php';

                  $connect = new conexao;
                  $connect = $connect->conectar();

                  echo "<select required class='selectdocente' name='selectdocente' form='selectdocentes'>";
                  echo "<option disabled selected style='display: none;'>Selecione um Docente</option>";


                  $data = $connect->query("SELECT nomedocente FROM docente ORDER BY nomedocente");

                  while ($selectdocente = $data->fetch(PDO::FETCH_ASSOC)) {
                    echo '<option  value="' . $selectdocente["nomedocente"] . '">' . $selectdocente['nomedocente'] . '</option>';
                  };

                  echo "</select>";

                  ?>
                </div>
                <br>
                <div>
                  <input type="submit" id="btn_action" value="Emitir">
                </div>
              </div>


            </div>
          </div>
        </form>
      </div>


      <div class="panel panel-default">
        <form target="_blank" method="POST" autocomplete="off" action="relatorio_docente-ano2.php" id="selectdocentes-ano">


          <a data-toggle="collapse" data-parent="#accordion" href="#collapse2" id="padrao">
            <div class="panel-heading" style="background: #f9f9f9">
              <h4 class="panel-title">
                Relatório Docente/Ano
              </h4>
            </div>
          </a>

          <div id="collapse2" class="panel-collapse collapse ">
            <div class="panel-body">

              <div style="padding-left: 17px;">
                <div>
                  <font style="font-size: 12px;">Ano:</font> <br>
                  <input type="text" value="" minlength="4" maxlength="4" name="selectano" class="form-anosemestre" required="True">
                </div>
                <br>
                <div id="doc_primario">
                  <font style="font-size: 12px;">Docente:</font> <br>
                  <?php


                  echo "<select required class='selectdocente' name='selectdocente' form='selectdocentes-ano'>";
                  echo "<option disabled selected style='display: none;'>Selecione um Docente</option>";


                  $data = $connect->query("SELECT nomedocente FROM docente ORDER BY nomedocente");

                  while ($selectdocente = $data->fetch(PDO::FETCH_ASSOC)) {
                    echo '<option  value="' . $selectdocente["nomedocente"] . '">' . $selectdocente['nomedocente'] . '</option>';
                  };

                  echo "</select>";

                  ?>
                </div>
                <br>
                <div>
                  <input type="submit" id="btn_action" value="Emitir">
                </div>
              </div>


            </div>
          </div>
        </form>
      </div>


      <div class="panel panel-default">
        <form target="_blank" method="POST" autocomplete="off" action="relatorio_turma-semestre2.php" id="selectcurso-semestre">


          <a data-toggle="collapse" data-parent="#accordion" href="#collapse3" id="padrao">
            <div class="panel-heading" style="background: #f9f9f9">
              <h4 class="panel-title">
                Relatório Turma/Semestre
              </h4>
            </div>
          </a>

          <div id="collapse3" class="panel-collapse collapse ">
            <div class="panel-body">

              <div style="padding-left: 17px;">
                <div>
                  <font style="font-size: 12px;">Ano:</font>
                  <font style="font-size: 12px; padding-left: 63px;">Semestre:</font> <br>
                  <input type="text" value="" minlength="4" maxlength="4" name="selectano" class="form-anosemestre" required="True">
                  .
                  <select class="selectsemestre" name="selectsemestre" required="True">
                    <option value="1">1</option>
                    <option value="2">2</option>
                  </select> <br> <br>

                </div>
                <br>
                <div id="doc_primario">
                  <font style="font-size: 12px;">Turma:</font><br>
                  <?php


                  echo "<select required class='selectdocente' name='selectturma' form='selectcurso-semestre'>";
                  echo "<option disabled selected style='display: none;'>Selecione uma Turma</option>";


                  $data = $connect->query("SELECT anosemestre, semestres, selectturmas FROM turma");

                  while ($selectturma = $data->fetch(PDO::FETCH_ASSOC)) {
                    echo '<option  value="' . $selectturma["anosemestre"] . '.' . $selectturma["semestres"] . '    ' . $selectturma["selectturmas"] . '">' . $selectturma["anosemestre"] . '.' . $selectturma["semestres"] . '    ' . $selectturma["selectturmas"] . '</option>';
                  };

                  echo "</select>";

                  ?>
                  <!-- <br><br>
                                        <font style="font-size: 12px;">Curso:</font> <br>
                                           <?php


                                            //echo "<select required class='selectdocente' name='selectcurso' form='selectcurso-semestre'>";
                                            //echo "<option disabled selected style='display: none;'>Selecione um Curso</option>";


                                            //$data = $connect->query("SELECT nomecurso FROM curso ORDER BY nomecurso");

                                            //while ($selectcurso = $data->fetch(PDO::FETCH_ASSOC)) {
                                            //echo '<option  value="'.$selectcurso["nomecurso"].'">'.$selectcurso['nomecurso'].'</option>';
                                            //}   ;      

                                            //echo "</select>";

                                            ?> -->
                </div>
                <br>
                <div>
                  <input type="submit" id="btn_action" value="Emitir">
                </div>
              </div>


            </div>
          </div>
        </form>
      </div>

      <div class="panel panel-default">
        <form target="_blank" method="POST" autocomplete="off" action="relatorio_estagio.php" id="selectestagio">


          <a data-toggle="collapse" data-parent="#accordion" href="#collapse4" id="padrao">
            <div class="panel-heading" style="background: #f9f9f9">
              <h4 class="panel-title">
                Relatório de Estágio Supervisionado
              </h4>
            </div>
          </a>

          <div id="collapse4" class="panel-collapse collapse ">
            <div class="panel-body">

              <div style="padding-left: 17px;">
                <div>
                  <font style="font-size: 12px;">Ano:</font>
                  <font style="font-size: 12px; padding-left: 63px;">Semestre:</font> <br>
                  <input type="text" value="" minlength="4" maxlength="4" name="selectano" class="form-anosemestre" required="True">
                  .
                  <select class="selectsemestre" name="selectsemestre" required="True">
                    <option value="1">1</option>
                    <option value="2">2</option>
                  </select> <br> <br>

                </div>
                <br>
                <div id="doc_primario">
                  <font style="font-size: 12px;">Turma:</font><br>
                  <?php


                  echo "<select required class='selectdocente' name='selectturma' form='selectestagio'>";
                  echo "<option disabled selected style='display: none;'>Selecione uma Turma</option>";


                  $data = $connect->query("SELECT anosemestre, semestres, selectturmas FROM turma");

                  while ($selectturma = $data->fetch(PDO::FETCH_ASSOC)) {
                    echo '<option  value="' . $selectturma["anosemestre"] . '.' . $selectturma["semestres"] . '    ' . $selectturma["selectturmas"] . '">' . $selectturma["anosemestre"] . '.' . $selectturma["semestres"] . '    ' . $selectturma["selectturmas"] . '</option>';
                  };

                  echo "</select>";

                  ?>
                  <!-- <br><br>
                                        <font style="font-size: 12px;">Curso:</font> <br>
                                           <?php


                                            //echo "<select required class='selectdocente' name='selectcurso' form='selectcurso-semestre'>";
                                            //echo "<option disabled selected style='display: none;'>Selecione um Curso</option>";


                                            //$data = $connect->query("SELECT nomecurso FROM curso ORDER BY nomecurso");

                                            //while ($selectcurso = $data->fetch(PDO::FETCH_ASSOC)) {
                                            //echo '<option  value="'.$selectcurso["nomecurso"].'">'.$selectcurso['nomecurso'].'</option>';
                                            //}   ;      

                                            //echo "</select>";

                                            ?> -->
                </div>
                <br>
                <div id="doc_primario">
                  <font style="font-size: 12px;">Estágio Supervisionado:</font><br>
                  <select required class='selectdocente' name='selectestagio' form='selectestagio'>
                    <option disabled selected style='display: none;'>Selecione um estágio supervisionado</option>
                    <option value="ESTÁGIO SUPERVISIONADO I">ESTÁGIO SUPERVISIONADO I</option>
                    <option value="ESTÁGIO SUPERVISIONADO II">ESTÁGIO SUPERVISIONADO II</option>
                    <option value="ESTÁGIO SUPERVISIONADO III">ESTÁGIO SUPERVISIONADO III</option>
                    <option value="ESTÁGIO SUPERVISIONADO IV">ESTÁGIO SUPERVISIONADO IV</option>
                    <option value="ESTÁGIO SUPERVISIONADO V">ESTÁGIO SUPERVISIONADO V</option>
                  </select>
                </div>
                <br>
                <div>
                  <input type="submit" id="btn_action" value="Emitir">
                </div>
              </div>


            </div>
          </div>
        </form>
      </div>

    </div>

    <br>




  </div>

</body>

</html>