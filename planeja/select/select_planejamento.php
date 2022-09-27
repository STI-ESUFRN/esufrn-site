<?php

$consulta = $connect->query("SELECT * FROM planejamento ORDER BY docente ASC, anosemestre DESC ");

echo '<ol id="selectable">';
$i = 1;
while ($linha = $consulta->fetch(PDO::FETCH_ASSOC)) {
  $i = $i + 1;
  if (($i % 2) == 0) {
    $parouimpar = 'par';
  } else {
    $parouimpar = 'impar';
  }
  $ano = substr($linha["anosemestre"], 0, 4);
  $semestre = substr($linha["anosemestre"], 4, 4);
  // aqui eu mostro os valores de minha consulta
  //echo '<li class="li_feriados_'.$parouimpar.' " id="'.$linha["id_feriado"].'">'.date('d/m',strtotime($linha["data_feriado"])).'&nbsp;&nbsp;&nbsp;&nbsp;'.$linha["descricao_feriado"].'<br /></li>';
  echo '<li class="li_planejamentos_' . $parouimpar . '" id="' . $linha["id"] . '">'
    . '<table width=1020px align="center">'

    . '<tr>
                                    <td class="title_3" style="text-align: center;" width="350px;">
                                        <font color="#594F4F">
                                            <b>Docente</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="60px">
                                        <font  color="#594F4F">
                                            <b>Período</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="250px">
                                        <font  color="#594F4F">
                                            <b>Curso</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="200px">
                                        <font  color="#594F4F">
                                            <b>Turma</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="100px">
                                        <font  color="#594F4F">
                                            <b>Componente</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="100px">
                                        <font  color="#594F4F">
                                            <b>Local</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="50px">
                                        <font  color="#594F4F">
                                            <b>CH</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="100px">
                                        <font  color="#594F4F">
                                            <b>Dias</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="100px">
                                        <font  color="#594F4F">
                                            <b>Início</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="80px">
                                        <font  color="#594F4F">
                                            <b>Final</b>
                                        </font>
                                    </td>
                                    <td class="title_3" style="text-align: center;" width="100px">
                                        <font  color="#594F4F">
                                            <b>Turno</b>
                                        </font>
                                    </td>
                                </tr>'
    . '<tr>'

    . '<td class="font_li" width="350px" height="70px">' . $linha["docente"] . '</td>'
    . '<td class="font_li" width="60px" height="70px">' . $ano . '.' . $semestre . '</td>'
    . '<td class="font_li" width="250px" height="70px">' . $linha["curso"] . '</td>'
    . '<td class="font_li" width="200px" height="70px">' . $linha["turma"] . '</td>'
    . '<td class="font_li" width="100px" height="70px">' . $linha["componente"] . '</td>'
    . '<td class="font_li" width="100px" height="70px">' . $linha["local"] . '</td>'
    . '<td class="font_li" width="50px" height="70px">' . $linha["ch"] . 'h</td>'
    . '<td class="font_li" width="100px" height="70px">' . $linha["dia"] . '</td>'
    . '<td class="font_li" width="100px" height="70px">' . date('d/m/Y',  strtotime($linha["data_ini"])) . '</td>'
    . '<td class="font_li" width="100px" height="70px">' . date('d/m/Y',  strtotime($linha["data_fim"])) . '</td>'
    . '<td class="font_li" width="100px" height="70px">' . $linha["turno"] . '</td>'
    . '<td class="linha' . $linha["id"] . '"  height="70px">
                                        <div  class="trash">
                                             
                                            <div id="btn_del_tabela2" > 
                                               <a href="deletar/delete_planejamento.php?id=' . $linha["id"] . '"> <img src="./assets/img/trash.ico" height="25px" width="25px"> </a>
                                            </div>
                                                  
                                        </div>
                                    </td>'
    . '</tr>'

    . '</table></li>';


  echo '<script>


                            $(document).ready(function(){

                                $(".linha' . $linha["id"] . '").hide();

                                $("#' . $linha["id"] . '").click(function(){
                                    $(".linha' . $linha["id"] . '").toggle();
                                });
                            });

                        </script>';
}
echo '</ol>';
echo '<div id="del"></div>';
