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
      <title>Cadastro de Turmas</title>
      <meta charset="UTF-8">
      <script src="./js/jquery-3.2.1.min.js"></script>
      <link rel="stylesheet" type="text/css" href="./css/style_planejamentos.css">
      <link rel="stylesheet" type="text/css" href="./css/modal_planejamentos.css">
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

      <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
      <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
      <script>
        $(document).ready(function() {

          $('#plan_curso').change(function() {
            //recupero variabile "discriminante"
            var curso = $("#plan_curso").val();
            //var curso = document.getElementById("#plan_curso").value;
            //chiamata ajax
            $.ajax({
              type: "POST",
              url: "turmas_ajax.php",
              data: "curso=" + curso,
              dataType: "html",
              success: function(msg) {
                $("#plan_turma").html(msg);
              },
              error: function() {
                alert("Chiamata fallita, si prega di riprovare...");
              }
            });

            $.ajax({
              type: "POST",
              url: "comp_ajax.php",
              data: "curso=" + curso,
              dataType: "html",
              success: function(msg) {
                $("#plan_comp").html(msg);
              },
              error: function() {
                alert("Chiamata fallita, si prega di riprovare...");
              }
            });
          });
        }); //(document).ready(function()
      </script>
      <script language="javascript" type="text/javascript" src="./js/modal.js"></script>
    </head>

    <body>

      <div id="mask"></div>

      <div class="content">

        <form method="POST" autocomplete="off" action="enviar/envia_planejamento.php" id="planejar" autocomplete="off">

          <div id="main-title">Planejamento</div>

          <br>
          <div style="padding-left: 17px;">
            <div>
              <font style="font-size: 12px;">Ano:</font>
              <input type="text" value="" minlength="4" maxlength="4" name="plan_ano" class="form-anosemestre" required="True">
              <font style="font-size: 12px;">&nbsp;&nbsp;Semestre:</font>
              <input type="text" name="plan_sem" value="" class="form-anosemestre" min="1" max="2" required="True">
            </div>

            <br>

            <div>

              Selecione o curso:
              <select class="selectcurso" name="plan_curso" id="plan_curso" required="True">
                <option disabled selected style="display: none;" value=""> Selecione o curso </option>
                <?php
                require './classes/conexao.php';

                $connect = new conexao;
                $connect = $connect->conectar();
                $consulta = $connect->query("SELECT * FROM curso ORDER BY nomecurso");

                while ($linha = $consulta->fetch(PDO::FETCH_ASSOC)) {
                  echo '<option value="' . $linha["nomecurso"] . '"> ' . $linha["nomecurso"] . '</option>';
                }
                ?>
              </select>
            </div>

            <div>
              Selecione a turma:
              <select name="plan_turma" class='selectturma' id="plan_turma" required="True">
                <option disabled selected style='display: none;' value=""> Selecione a turma </option>
              </select>
            </div>

            <div>
              Selecione a disciplina:
              <select name="plan_comp" class='selectdisciplina' id="plan_comp" required="True">
                <option disabled selected style='display: none;' value=""> Selecione o componente curricular </option>
              </select>
            </div>
            <div>
              Carga horária: <input type="number" name="plan_ch" id="plan_ch" min="0" maxlength="4" class='form-cargahoraria' val="" readonly="true">
            </div>
            <br>
            <div>
              Selecione o turno:
              <select name="plan_turno" class="selectturno" id="plan_turno" required="True">
                <option disabled selected style='display: none;' value=""> Selecione o turno </option>
                <option value="MATUTINO"> MATUTINO </option>
                <option value="VESPERTINO"> VESPERTINO </option>
                <option value="NOTURNO"> NOTURNO </option>
              </select>
            </div>
            <br><br>
            <div>
              Período da componente curricular:
              <input type="date" name="comp_date_in" id="comp_date_in" class="form-data" style="margin-left: 60px; padding-left: 10px; margin-right: 40px;">à
              <input type="date" name="comp_date_out" id="comp_date_out" class="form-data" style="margin-left: 37px; padding-left: 10px;">

            </div>
            <br><br>
            <div align="left">
              Selecione a frequencia semanal:
              <input type="checkbox" name="plan_dia[]" value="SEG">
              <font style="font-size: 14px">Segunda</font>
              <input type="checkbox" name="plan_dia[]" value="TER">
              <font style="font-size: 14px">Terça</font>
              <input type="checkbox" name="plan_dia[]" value="QUA">
              <font style="font-size: 14px">Quarta</font>
              <input type="checkbox" name="plan_dia[]" value="QUI">
              <font style="font-size: 14px">Quinta</font>
              <input type="checkbox" name="plan_dia[]" value="SEX">
              <font style="font-size: 14px">Sexta</font>
            </div>
            <br><br>
            <div>

              <div id='divCaso1'>
                <input type="checkbox" name="caso1" id="caso1" onchange="check()" value="1">
                <font style="font-size: 12px;">Essa componente curricular é ministrada por <b>MAIS DE UM</b> docente.</font>
              </div>
              <div id='divCaso2' style="display:none;">
                <br>
                <input type="checkbox" name="caso2" id="caso2" onchange="check()" value="2">
                <font style="font-size: 12px;">Esta componente curricular possui carga horária <b>COMPARTILHADA</b>.</font>
              </div>
              <div id='divCaso3' style="display:none;">
                <br>
                <input type="checkbox" name="caso3" id="caso3" onchange="check()" value="3">
                <font style="font-size: 12px;">Esta componente curricular é <b>PRÁTICA</b>.</font>
              </div>
            </div>
            <br>

            <br>
            <div id="doc_primario">
              Selecione o docente:
              <select name="plan_doc" class='selectdocente' id="plan_doc">
                <option disabled selected style='display: none;' value=""> Selecione o docente </option>
                <?php
                $consulta = $connect->query("SELECT * FROM docente ORDER BY nomedocente");
                while ($linha = $consulta->fetch(PDO::FETCH_ASSOC)) {
                  echo '<option value="' . $linha["nomedocente"] . '">' . $linha["nomedocente"] . '</option>';
                }
                ?>
              </select>
            </div>

            <div id="local">
              Local: <input name="plan_loc" class='form-local' id="plan_loc">
            </div>
            <script>
              $(document).ready(function() {
                $('#plan_comp').change(function() {
                  //recupero variabile "discriminante"
                  var componente = $('#plan_comp').val();
                  //chiamata ajax
                  $.ajax({
                    type: "POST",
                    url: "carga_ajax.php",
                    data: "componente=" + componente,
                    dataType: "html",
                    success: function(msg) {
                      $("#plan_ch").html(msg);
                    },
                    error: function() {
                      alert("Chiamata fallita, si prega di riprovare...");
                    }
                  });
                });
              });
            </script>

            <div id="datas">
              <div style="float: left">
                Data inicial: <input type="date" name="plan_date_in" id="plan_date_in" class='form-data' style="margin-left: 60px; padding-left: 10px;">
              </div>
              <div>
                &nbsp;&nbsp;&nbsp;&nbsp;Data final: <input type="date" name="plan_date_out" id="plan_date_out" class='form-data' style="margin-left: 20px; padding-left: 10px;">
              </div>
            </div>
            <div>
              <br>
              <script type="text/javascript">
                function check() {
                  if (document.getElementById("caso1").checked == true) {
                    $('#add_doc').show();
                    $('#qtd_doc').val("");
                    $('#doc_primario').hide();
                    $('#local').hide();
                    $('#datas').hide();
                    $('#divCaso2').show();
                    $('#divCaso3').show();


                  }
                  if (document.getElementById("caso1").checked === false) {
                    $('#add_doc').hide();
                    $('#qtd_doc').val("");
                    $('#add_doc2').hide();
                    $('#divCaso2').hide();
                    $('#divCaso3').hide();
                    $('#doc_primario').show();
                    $('#datas').show();
                    $('#local').show();
                  }
                  if (document.getElementById("caso2").checked == true) {
                    $('#divCaso3').hide();
                  }
                  if (document.getElementById("caso2").checked == false) {
                    $('#divCaso3').show();
                  }
                  if (document.getElementById("caso3").checked == true) {
                    $('#divCaso2').hide();
                  }
                  if (document.getElementById("caso3").checked == false) {
                    $('#divCaso2').show();
                  }
                  if (document.getElementById("caso3").checked == false && document.getElementById("caso2").checked == false && document.getElementById("caso1").checked == false) {
                    $('#divCaso2').hide();
                    $('#divCaso3').hide();
                  }
                }

                $(document).ready(function() {
                  $('#qtd_doc').change(function() {
                    $('#add_doc2').show();
                    var quantidade = $("#qtd_doc").val();
                    if (document.getElementById("caso2").checked == false && document.getElementById("caso3").checked == false) {
                      var carga = $('#plan_ch').val();
                      var checkcarga = $('#plan_ch').val();
                      $.ajax({
                        type: "POST",
                        url: "docentes_ajax.php",
                        //data: "quantidade=" + quantidade,
                        data: {
                          'quantidade': quantidade,
                          'carga': carga,
                          'checkcarga': checkcarga
                        },
                        dataType: "html",
                        success: function(msg) {
                          $("#add_doc2").html(msg);
                        },
                        error: function() {
                          alert("Chiamata fallita, si prega di riprovare...");
                        }
                      });
                    }
                    if (document.getElementById("caso2").checked == true) {
                      var carga = "";
                      var checkcarga = $('#plan_ch').val();
                      $.ajax({
                        type: "POST",
                        url: "docentes_ajax.php",
                        //data: "quantidade=" + quantidade,
                        data: {
                          'quantidade': quantidade,
                          'carga': carga,
                          'checkcarga': checkcarga
                        },
                        dataType: "html",
                        success: function(msg) {
                          $("#add_doc2").html(msg);
                        },
                        error: function() {
                          alert("Chiamata fallita, si prega di riprovare...");
                        }
                      });
                    }
                    if (document.getElementById("caso3").checked == true) {
                      var carga = "caso3";
                      var checkcarga = $('#plan_ch').val();
                      $.ajax({
                        type: "POST",
                        url: "docentes_ajax.php",
                        data: {
                          'quantidade': quantidade,
                          'carga': carga,
                          'checkcarga': checkcarga
                        },
                        dataType: "html",
                        success: function(msg) {
                          $("#add_doc2").html(msg);
                        },
                        error: function() {
                          alert("Chiamata fallita, si prega di riprovare...");
                        }
                      });
                    }
                  });
                });
              </script>
            </div>
            <div id="add_doc" style="display: none; padding-left: 35px;">
              Qual será a quantidade TOTAL de docentes? &nbsp;&nbsp;
              <input type="number" class="form-anosemestre" name="qtd_doc" id="qtd_doc" min="1" max="30" minlength="1" maxlength="2" value=""><br>
              <br>
              <b>OBS: Levar em consideração o docente anteriormente cadastrado.</b>
            </div>
            <br>
            <div id="add_doc2"></div>
            <br>
            <input type="submit" value="Cadastrar" id='btn_action'>

        </form>
      </div>

      </div>

      <div class="sidebar">

        <br>

        <div class="modal-title">Infomações Extras</div>

        <br>

        <p style="font-size: 12px;">- O preechimento deve ser feito de modo sequencial.</p>
        <p style="font-size: 12px;">- A exibição dos campos 'turma', 'disciplina' e 'carga horária' são dependentes do campo 'curso' selecionado.</p>
        <p style="font-size: 12px;">- Uma vez cadastrados, os planejamentos não poderão ser editados. Entretanto, poderão ser refeitos a partir do excluimento do planejamento antigo.</p>
        <p style="font-size: 12px;">- Todos os campos são obrigatórios.</p>

        <table>
          <tr>
            <td>
              <a name="modal" href="#planejamentocadastrados">
                <button id="btn_action_tabela" type="button" class="botao">Planejamentos</button>
              </a>
            </td>
            <td>
              <a target="_blank" href="http://escoladesaude.ufrn.br/?page_id=3436">
                <button id="btn_salas_tabela" type="button" class="botao">Ocupação de Salas</button>
              </a>
            </td>
          </tr>
        </table>

      </div>

      <div id='boxes'>
        <div id='planejamentocadastrados' class="window">

          <div class="modal-header">
            <div class="modal-title">Planejamentos Cadastrados
              <small style="color:#09989b;font-size: 14px;padding-left: 10px"></small>
            </div>

          </div>


          <br>

          <div class="iframe_planejamentos">

            <?php

            require './select/select_planejamento.php';

            ?>

          </div>
          <br>
          <div class="modal-footer">

            <button type="button" class="close" data-dismiss="modal" id="btn_cancel">Fechar</button>
          </div>


        </div>
      </div>

    </body>

    </html>