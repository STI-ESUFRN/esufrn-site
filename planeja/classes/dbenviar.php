<?php

class enviar
{
  public function enviar_feriado($dados, $con)
  {
    $descricao_feriado = $_POST['descricaoferiado'];
    $data_feriado      = $_POST['dataferiado'];

    $sql = "INSERT INTO feriado (descricao_feriado, data_feriado) VALUE (?, ?)";

    $enviar = $con->prepare($sql);

    $enviar->bindParam(1, $descricao_feriado, PDO::PARAM_STR);
    $enviar->bindParam(2, $data_feriado, PDO::PARAM_STR);
    $enviar->execute(array($descricao_feriado, $data_feriado));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  public function enviar_componente($dados, $con)
  {
    $nome_comp   = $_POST['nomecomp'];
    $codigo_comp = $_POST['codigocomp'];
    $carga_comp  = $_POST['cargacomp'];
    try {
      $sql = "INSERT INTO disciplina (nome_disciplina , carga_horario, codigo) VALUE (?, ?, ?)";

      $enviar = $con->prepare($sql);

      $enviar->bindParam(1, $nome_comp, PDO::PARAM_STR);
      $enviar->bindParam(2, $carga_comp, PDO::PARAM_INT);
      $enviar->bindParam(3, $codigo_comp, PDO::PARAM_STR);
      $enviar->execute(array($nome_comp, $carga_comp, $codigo_comp));
    } catch (PDOException $e) {
      return $e->getCode() . ' ' . $e->getMessage();
    }
    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  public function enviar_docente($dados, $con)
  {
    $nomedocente       = $_POST['nomedocente'];
    $observacaodocente = $_POST['observacaodocente'];

    $sql = "INSERT INTO docente (nomedocente, observacaodocente) VALUE (?, ?)";

    $enviar = $con->prepare($sql);

    $enviar->bindParam(1, $nomedocente, PDO::PARAM_STR);
    $enviar->bindParam(2, $observacaodocente, PDO::PARAM_STR);
    $enviar->execute(array($nomedocente, $observacaodocente));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  public function enviar_curso($dados, $con)
  {
    $nomecurso = $_POST['nomecurso'];

    $sql = "INSERT INTO curso (nomecurso, cursocomponentes) VALUE (?,?)";

    $enviar = $con->prepare($sql);

    $enviar->bindParam(1, $nomecurso, PDO::PARAM_STR);
    $enviar->execute(array($nomecurso, ''));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  public function enviar_turma($dados, $con)
  {

    $anosemestre  = $_POST['anosemestre'];
    $semestres    = $_POST['semestres'];
    $selectturmas = $_POST['selectturmas'];
    if (empty($_POST['statusturma'])) {
      $status = 'INATIVA';
    } else {
      $status = $_POST['statusturma'];
    }

    $sql = "INSERT INTO turma (anosemestre,semestres,selectturmas,statusturma) VALUE (?,?,?,?)";

    $enviar = $con->prepare($sql);

    $enviar->bindParam(1, $anosemestre, PDO::PARAM_STR);
    $enviar->bindParam(2, $semestres, PDO::PARAM_STR);
    $enviar->bindParam(3, $selectturmas, PDO::PARAM_STR);
    $enviar->bindParam(4, $status, PDO::PARAM_STR);
    $enviar->execute(array($anosemestre, $semestres, $selectturmas, $status));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  public function enviar_planejamento($dados, $con)
  {

    $anosemestre   = $_POST['plan_ano'] . $_POST['plan_sem'];
    $checkch       = (int) $_POST['plan_ch'];
    $curso         = $_POST['plan_curso'];
    $turma         = $_POST['plan_turma'];
    $componente    = $_POST['plan_comp'];
    $turno         = $_POST['plan_turno'];
    $data_comp_ini = $_POST['comp_date_in'];
    $data_comp_out = $_POST['comp_date_out'];
    $dia           = $_POST['plan_dia'];
    $dia_str       = implode("-", $dia);
    $teste_carga   = 0;


    if (isset($_POST['caso1']) and isset($_POST['caso2'])) {

      $quantidade = $_POST['qtd_doc'];
      $qtd_int    = (int) $quantidade;
      $save       = true;

      for ($i = 0; $i < $qtd_int; $i++) {

        $docente[$i]  = $_POST['plan_doc' . $i];
        $ch[$i]       = $_POST['plan_ch' . $i];
        $data_ini[$i] = $_POST['plan_date_in' . $i];
        $data_fim[$i] = $_POST['plan_date_out' . $i];
        $local[$i]    = $_POST['plan_loc' . $i];

        $checkdados = $con->query("SELECT dia,data_ini,data_fim FROM planejamento WHERE docente='$docente[$i]' and turno='$turno' and anosemestre='$anosemestre'");

        $dias = array();

        while ($check = $checkdados->fetch(PDO::FETCH_ASSOC)) {

          list($dias[0], $dias[1], $dias[2], $dias[3], $dias[4], $dias[5]) = explode("-", $check['dia']);

          for ($a = 0; $a < sizeof($dia); $a++) {

            for ($b = 0; $b < 6; $b++) {

              // Filtro para cadastro entre/igual a data inicio e data fim já cadastrados
              if (($data_ini >= $check["data_ini"]) && ($data_fim <= $check["data_fim"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro1'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
                //Filtro para cadastro menor/igual a data inicio e menor/igual data fim
              } elseif (($data_ini <= $check["data_ini"]) && ($data_fim >= $check["data_ini"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro2'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
              } elseif (($data_ini <= $check["data_fim"]) && ($data_fim >= $check["data_fim"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro3'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
              }
            }
          }
        }

        //echo $checkch;
        $j = 0;
        while ($j < $qtd_int) {
          $teste_carga += $_POST['plan_ch' . $j];
          $j++;
        }
        //echo $teste_carga."<br>";
        //echo $checkch;
        if ($teste_carga < $checkch) {
          //echo 'menor';
          $_SESSION['checkdados-filtro6'] = true;
          $save                           = false;
          $teste_carga                    = 0;
          return 'Fudeu';
        } elseif ($teste_carga > $checkch) {
          //echo 'maior';
          $_SESSION['checkdados-filtro5'] = true;
          $save                           = false;
          $teste_carga                    = 0;
          return 'Fudeu';
        } else {
          $save        = true;
          $teste_carga = 0;
        }

        if ($save == true) {

          $sql = "INSERT INTO planejamento (docente, anosemestre, curso, turma, componente, local, ch, data_comp_ini, data_comp_out, dia, data_ini, data_fim, turno) VALUE (?,?,?,?,?,?,?,?,?,?,?,?,?)";

          $enviar = $con->prepare($sql);

          $enviar->bindParam(1, $docente[$i], PDO::PARAM_STR);
          $enviar->bindParam(2, $anosemestre, PDO::PARAM_STR);
          $enviar->bindParam(3, $curso, PDO::PARAM_STR);
          $enviar->bindParam(4, $turma, PDO::PARAM_STR);
          $enviar->bindParam(5, $componente, PDO::PARAM_STR);
          $enviar->bindParam(6, $local[$i], PDO::PARAM_STR);
          $enviar->bindParam(7, $ch[$i], PDO::PARAM_STR);
          $enviar->bindParam(8, $data_comp_ini, PDO::PARAM_STR);
          $enviar->bindParam(9, $data_comp_out, PDO::PARAM_STR);
          $enviar->bindParam(10, $dia_str, PDO::PARAM_STR);
          $enviar->bindParam(11, $data_ini[$i], PDO::PARAM_STR);
          $enviar->bindParam(12, $data_fim[$i], PDO::PARAM_STR);
          $enviar->bindParam(13, $turno, PDO::PARAM_STR);

          $enviar->execute(array($docente[$i], $anosemestre, $curso, $turma, $componente, $local[$i], $ch[$i], $data_comp_ini, $data_comp_out, $dia_str, $data_ini[$i], $data_fim[$i], $turno));
        }
      }

      if ($enviar) {
        return 'Sucesso';
      } else {
        return 'Fudeu';
      }
    } else if (isset($_POST['caso1']) and isset($_POST['caso3'])) {
      $quantidade = $_POST['qtd_doc'];
      $qtd_int    = (int)$quantidade;
      //echo "<script>alert('oi to aqui');</script>";

      //echo gettype($qtd_int);
      $save       = true;

      //$docente[0]   = $_POST['plan_doc0'];
      //$ch[0]        = $_POST['plan_ch'];
      //$data_ini[0]  = $_POST['plan_date_in0'];
      //$data_fim[0]  = $_POST['plan_date_out0'];
      //$local[0]     = $_POST['plan_loc0'];

      for ($i = 0; $i < $qtd_int; $i++) {

        $docente[$i]  = $_POST['plan_doc' . $i];
        $ch[$i]       = $_POST['plan_ch' . $i];
        $data_ini[$i] = $_POST['plan_date_in' . $i];
        $data_fim[$i] = $_POST['plan_date_out' . $i];
        $local[$i]    = $_POST['plan_loc' . $i];

        $checkdados = $con->query("SELECT dia,data_ini,data_fim FROM planejamento WHERE docente='$docente[$i]' and turno='$turno' and anosemestre='$anosemestre'");

        $dias = array();

        while ($check = $checkdados->fetch(PDO::FETCH_ASSOC)) {
          /*
                    list($dias[0], $dias[1], $dias[2], $dias[3], $dias[4], $dias[5]) = explode("-", $check['dia']);

                    for ($cont = 0; $cont < sizeof($dia); $cont++) {

                        for ($j = 0; $j < 6; $j++) {

                            // Filtro para cadastro entre/igual a data inicio e data fim já cadastrados
                            if (($data_ini >= $check["data_ini"]) && ($data_fim <= $check["data_fim"])) {
                                if ($dia[$cont] == $dias[$j]) {
                                    $_SESSION['checkdados-filtro1'] = true;
                                    $save                           = false;
                                    break;
                                }
                                //Filtro para cadastro menor/igual a data inicio e menor/igual data fim
                            } else if (($data_ini <= $check["data_ini"]) && ($data_fim >= $check["data_ini"])) {
                                if ($dia[$cont] == $dias[$j]) {
                                    $_SESSION['checkdados-filtro2'] = true;
                                    $save                           = false;
                                    break;
                                }
                            } else if (($data_ini <= $check["data_fim"]) && ($data_fim >= $check["data_fim"])) {
                                if ($dia[$cont] == $dias[$j]) {
                                    $_SESSION['checkdados-filtro3'] = true;
                                    $save                           = false;
                                    break;
                                }
                            }

                        }
                    }*/
          list($dias[0], $dias[1], $dias[2], $dias[3], $dias[4], $dias[5]) = explode("-", $check['dia']);

          for ($a = 0; $a < sizeof($dia); $a++) {

            for ($b = 0; $b < 6; $b++) {

              // Filtro para cadastro entre/igual a data inicio e data fim já cadastrados
              if (($data_ini[$i] >= $check["data_ini"]) && ($data_fim[$i] <= $check["data_fim"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro1'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
                //Filtro para cadastro menor/igual a data inicio e menor/igual data fim
              } elseif (($data_ini[$i] <= $check["data_ini"]) && ($data_fim[$i] >= $check["data_ini"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro2'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
              } elseif (($data_ini[$i] <= $check["data_fim"]) && ($data_fim[$i] >= $check["data_fim"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro3'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
              }
            }
          }
        }

        if ($save == true) {
          try {
            /*
                    $data = [
                                'docente'       =>  $docente[$i], 
                                'anosemestre'   =>  $anosemestre, 
                                'curso, turma'  =>  $curso, 
                                'componente'    =>  $turma, 
                                'local'         =>  $componente, 
                                'ch'            =>  $local[$i], 
                                'data_comp_ini' =>  $ch[$i], 
                                'data_comp_out' =>  $data_comp_ini, 
                                'dia'           =>  $data_comp_out, 
                                'data_ini'      =>  $dia_str, 
                                'data_fim'      =>  $data_ini[$i], 
                                'turno'         =>  $data_fim[$i],
                            ];
                    */

            $sql = "INSERT INTO planejamento (docente, anosemestre, curso, turma, componente, local, ch, data_comp_ini, data_comp_out, dia, data_ini, data_fim, turno) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)";
            //$sql = "INSERT INTO planejamento (docente, anosemestre, curso, turma, componente, local, ch, data_comp_ini, data_comp_out, dia, data_ini, data_fim, turno) VALUES (:docente, :anosemestre, :curso, :turma, :componente, :local, :ch, :data_comp_ini, :data_comp_out, :dia, :data_ini, :data_fim, :turno)";

            $enviar = $con->prepare($sql);

            $enviar->bindParam(1, $docente[$i], PDO::PARAM_STR);
            $enviar->bindParam(2, $anosemestre, PDO::PARAM_STR);
            $enviar->bindParam(3, $curso, PDO::PARAM_STR);
            $enviar->bindParam(4, $turma, PDO::PARAM_STR);
            $enviar->bindParam(5, $componente, PDO::PARAM_STR);
            $enviar->bindParam(6, $local[$i], PDO::PARAM_STR);
            $enviar->bindParam(7, $ch[$i], PDO::PARAM_STR);
            $enviar->bindParam(8, $data_comp_ini, PDO::PARAM_STR);
            $enviar->bindParam(9, $data_comp_out, PDO::PARAM_STR);
            $enviar->bindParam(10, $dia_str, PDO::PARAM_STR);
            $enviar->bindParam(11, $data_ini[$i], PDO::PARAM_STR);
            $enviar->bindParam(12, $data_fim[$i], PDO::PARAM_STR);
            $enviar->bindParam(13, $turno, PDO::PARAM_STR);

            $enviar->execute(array($docente[$i], $anosemestre, $curso, $turma, $componente, $local[$i], $ch[$i], $data_comp_ini, $data_comp_out, $dia_str, $data_ini[$i], $data_fim[$i], $turno));
            //$enviar->execute($data);

          } catch (PDOException $e) {
            return var_dump($e);
          }
        }
      }

      if ($enviar) {
        return 'Sucesso';
        //$enviar = $con->close();
      } else {
        return 'Fudeu';
      }
    } else if (isset($_POST['caso1'])) {

      $quantidade = $_POST['qtd_doc'];
      $qtd_int    = (int)$quantidade;
      //echo "<script>alert(".$qtd_int.");</script>";

      //echo gettype($qtd_int);
      $save       = true;

      //$docente[0]   = $_POST['plan_doc0'];
      //$ch[0]        = $_POST['plan_ch'];
      //$data_ini[0]  = $_POST['plan_date_in0'];
      //$data_fim[0]  = $_POST['plan_date_out0'];
      //$local[0]     = $_POST['plan_loc0'];

      for ($i = 0; $i < $qtd_int; $i++) {

        $docente[$i]  = $_POST['plan_doc' . $i];
        $ch[$i]       = $_POST['plan_ch'];
        $data_ini[$i] = $_POST['plan_date_in' . $i];
        $data_fim[$i] = $_POST['plan_date_out' . $i];
        $local[$i]    = $_POST['plan_loc' . $i];

        $checkdados = $con->query("SELECT dia,data_ini,data_fim FROM planejamento WHERE docente='$docente[$i]' and turno='$turno' and anosemestre='$anosemestre'");

        $dias = array();

        while ($check = $checkdados->fetch(PDO::FETCH_ASSOC)) {
          /*
                    list($dias[0], $dias[1], $dias[2], $dias[3], $dias[4], $dias[5]) = explode("-", $check['dia']);

                    for ($cont = 0; $cont < sizeof($dia); $cont++) {

                        for ($j = 0; $j < 6; $j++) {

                            // Filtro para cadastro entre/igual a data inicio e data fim já cadastrados
                            if (($data_ini >= $check["data_ini"]) && ($data_fim <= $check["data_fim"])) {
                                if ($dia[$cont] == $dias[$j]) {
                                    $_SESSION['checkdados-filtro1'] = true;
                                    $save                           = false;
                                    break;
                                }
                                //Filtro para cadastro menor/igual a data inicio e menor/igual data fim
                            } else if (($data_ini <= $check["data_ini"]) && ($data_fim >= $check["data_ini"])) {
                                if ($dia[$cont] == $dias[$j]) {
                                    $_SESSION['checkdados-filtro2'] = true;
                                    $save                           = false;
                                    break;
                                }
                            } else if (($data_ini <= $check["data_fim"]) && ($data_fim >= $check["data_fim"])) {
                                if ($dia[$cont] == $dias[$j]) {
                                    $_SESSION['checkdados-filtro3'] = true;
                                    $save                           = false;
                                    break;
                                }
                            }

                        }
                    }*/
          list($dias[0], $dias[1], $dias[2], $dias[3], $dias[4], $dias[5]) = explode("-", $check['dia']);

          for ($a = 0; $a < sizeof($dia); $a++) {

            for ($b = 0; $b < 6; $b++) {

              // Filtro para cadastro entre/igual a data inicio e data fim já cadastrados
              if (($data_ini[$i] >= $check["data_ini"]) && ($data_fim[$i] <= $check["data_fim"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro1'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
                //Filtro para cadastro menor/igual a data inicio e menor/igual data fim
              } elseif (($data_ini[$i] <= $check["data_ini"]) && ($data_fim[$i] >= $check["data_ini"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro2'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
              } elseif (($data_ini[$i] <= $check["data_fim"]) && ($data_fim[$i] >= $check["data_fim"])) {
                if ($dia[$a] == $dias[$b]) {
                  $_SESSION['checkdados-filtro3'] = true;
                  $save                           = false;
                  return 'Fudeu';
                }
              }
            }
          }
        }

        if ($save == true) {
          try {
            /*
                    $data = [
                                'docente'       =>  $docente[$i], 
                                'anosemestre'   =>  $anosemestre, 
                                'curso, turma'  =>  $curso, 
                                'componente'    =>  $turma, 
                                'local'         =>  $componente, 
                                'ch'            =>  $local[$i], 
                                'data_comp_ini' =>  $ch[$i], 
                                'data_comp_out' =>  $data_comp_ini, 
                                'dia'           =>  $data_comp_out, 
                                'data_ini'      =>  $dia_str, 
                                'data_fim'      =>  $data_ini[$i], 
                                'turno'         =>  $data_fim[$i],
                            ];
                    */

            $sql = "INSERT INTO planejamento (docente, anosemestre, curso, turma, componente, local, ch, data_comp_ini, data_comp_out, dia, data_ini, data_fim, turno) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)";
            //$sql = "INSERT INTO planejamento (docente, anosemestre, curso, turma, componente, local, ch, data_comp_ini, data_comp_out, dia, data_ini, data_fim, turno) VALUES (:docente, :anosemestre, :curso, :turma, :componente, :local, :ch, :data_comp_ini, :data_comp_out, :dia, :data_ini, :data_fim, :turno)";

            $enviar = $con->prepare($sql);

            $enviar->bindParam(1, $docente[$i], PDO::PARAM_STR);
            $enviar->bindParam(2, $anosemestre, PDO::PARAM_STR);
            $enviar->bindParam(3, $curso, PDO::PARAM_STR);
            $enviar->bindParam(4, $turma, PDO::PARAM_STR);
            $enviar->bindParam(5, $componente, PDO::PARAM_STR);
            $enviar->bindParam(6, $local[$i], PDO::PARAM_STR);
            $enviar->bindParam(7, $ch[$i], PDO::PARAM_STR);
            $enviar->bindParam(8, $data_comp_ini, PDO::PARAM_STR);
            $enviar->bindParam(9, $data_comp_out, PDO::PARAM_STR);
            $enviar->bindParam(10, $dia_str, PDO::PARAM_STR);
            $enviar->bindParam(11, $data_ini[$i], PDO::PARAM_STR);
            $enviar->bindParam(12, $data_fim[$i], PDO::PARAM_STR);
            $enviar->bindParam(13, $turno, PDO::PARAM_STR);

            $enviar->execute(array($docente[$i], $anosemestre, $curso, $turma, $componente, $local[$i], $ch[$i], $data_comp_ini, $data_comp_out, $dia_str, $data_ini[$i], $data_fim[$i], $turno));
            //$enviar->execute($data);

          } catch (PDOException $e) {
            return var_dump($e);
          }
        }
      }

      if ($enviar) {
        return 'Sucesso';
        //$enviar = $con->close();
      } else {
        return 'Fudeu';
      }
    } else {
      $docente  = $_POST['plan_doc'];
      $ch       = $_POST['plan_ch'];
      $data_ini = $_POST['plan_date_in'];
      $data_fim = $_POST['plan_date_out'];
      $local    = $_POST['plan_loc'];

      $checkdados = $con->query("SELECT dia,data_ini,data_fim FROM planejamento WHERE docente='$docente' and turno='$turno' and anosemestre='$anosemestre'");

      $dias = array();
      $save = true;

      while ($check = $checkdados->fetch(PDO::FETCH_ASSOC)) {

        list($dias[0], $dias[1], $dias[2], $dias[3], $dias[4], $dias[5]) = explode("-", $check['dia']);

        for ($i = 0; $i < sizeof($dia); $i++) {

          for ($j = 0; $j < 6; $j++) {

            // Filtro para cadastro entre/igual a data inicio e data fim já cadastrados
            if (($data_ini >= $check["data_ini"]) && ($data_fim <= $check["data_fim"])) {
              if ($dia[$i] == $dias[$j]) {
                $_SESSION['checkdados-filtro1'] = true;
                $save                           = false;
                break;
              }
              //Filtro para cadastro menor/igual a data inicio e menor/igual data fim
            } else if (($data_ini <= $check["data_ini"]) && ($data_fim >= $check["data_ini"])) {
              if ($dia[$i] == $dias[$j]) {
                $_SESSION['checkdados-filtro2'] = true;
                $save                           = false;
                break;
              }
            } else if (($data_ini <= $check["data_fim"]) && ($data_fim >= $check["data_fim"])) {
              if ($dia[$i] == $dias[$j]) {
                $_SESSION['checkdados-filtro3'] = true;
                $save                           = false;
                break;
              }
            }
          }
        }
      }

      if ($save == true) {
        try {

          $sql = "INSERT INTO planejamento (docente, anosemestre, curso, turma, componente, local, ch, data_comp_ini, data_comp_out, dia, data_ini, data_fim, turno) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)";

          $enviar = $con->prepare($sql);

          $enviar->bindParam(1, $docente, PDO::PARAM_STR);
          $enviar->bindParam(2, $anosemestre, PDO::PARAM_INT);
          $enviar->bindParam(3, $curso, PDO::PARAM_STR);
          $enviar->bindParam(4, $turma, PDO::PARAM_STR);
          $enviar->bindParam(5, $componente, PDO::PARAM_STR);
          $enviar->bindParam(6, $local, PDO::PARAM_STR);
          $enviar->bindParam(7, $ch, PDO::PARAM_INT);
          $enviar->bindParam(8, $data_comp_ini, PDO::PARAM_STR);
          $enviar->bindParam(9, $data_comp_out, PDO::PARAM_STR);
          $enviar->bindParam(10, $dia_str, PDO::PARAM_STR);
          $enviar->bindParam(11, $data_ini, PDO::PARAM_STR);
          $enviar->bindParam(12, $data_fim, PDO::PARAM_STR);
          $enviar->bindParam(13, $turno, PDO::PARAM_STR);

          $enviar->execute(array($docente, $anosemestre, $curso, $turma, $componente, $local, $ch, $data_comp_ini, $data_comp_out, $dia_str, $data_ini, $data_fim, $turno));
        } catch (PDOException $e) {
          return 'Fudeu';
        }

        if ($enviar) {
          return 'Sucesso';
        } else {
          return 'Fudeu';
        }
      }
    }
  }
}
