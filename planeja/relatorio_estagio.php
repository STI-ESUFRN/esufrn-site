<?php

require './classes/fpdf/fpdf.php';

$turma = $_POST['selectturma'];
$estagio = $_POST['selectestagio'];
$ano = $_POST['selectano'] . $_POST['selectsemestre'];

class PDF extends FPDF
{

  function Header()
  {
    global $estagio, $turma, $ano, $resultado;
    $l = 5;
    date_default_timezone_set('America/Recife');
    $dataemissao = date('d/m/Y H:i');
    $this->SetXY(10, 10);

    $this->Image('./assets/img/ufrn.jpg', 11, 11, 45, 19);
    $this->Image('./assets/img/esufrn.png', 152, 15, 46, 10);
    $this->SetFont('Arial', 'B', 9);
    $this->SetXY(17, 10);
    $this->Cell(170, 15, "UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE", 0, 0, 'C');
    $this->SetXY(17, 16);
    $this->Cell(170, 15, "ESCOLA DE SAÚDE", 0, 0, 'C');

    $this->SetFont('Arial', '', 8);
    $this->SetXY(18, 30);
    $this->Cell(170, 15, "Emitido: " . $dataemissao, 0, 0, 'C');
    $this->Line(10, 40, 200, 40);
    $this->SetFont('Arial', '', 9);
    $this->SetXY(17, 38);
    $this->Cell(170, 15, "Relatório de Distribuição de Componente Curricular por Docente", 0, 0, 'C');
    $this->Line(10, 50, 200, 50);

    $this->SetFont('Arial', 'B', 10);
    $this->SetXY(17, 50);
    $this->Cell(170, 15, "COMPONENTE CURRICULAR: " . $estagio, 0, 0, 'C');
    $this->Line(10, 64, 200, 64);
  }
  function Footer()
  {
    $this->SetXY(10, 280);
    $this->SetFont('Arial', '', 8);
    $this->Cell(0, 5, 'Sistema de Gestão e Planejamento Acadêmco - SIGEP | Desenvolvido pelo: Suporte de TI - ESUFRN | Copyright © 2017', 1, 0, 'C');
    $this->Ln();
    $this->SetFont('Arial', '', 7);
    $this->Cell(190, 7, 'Página ' . $this->PageNo() . ' de {nb}', 0, 0, 'C');
  }
}

function contaLinhas($text, $maxwidth)
{
  $lines = 0;
  if ($text == '') {
    $cont = 1;
  } else {
    $cont = strlen($text);
  }
  if ($cont < $maxwidth) {
    $lines = 2;
  } else {
    if ($cont % $maxwidth > 0) {
      $lines = ($cont / $maxwidth) + 1;
    } else {
      $lines = ($cont / $maxwidth);
    }
  }
  $lines = $lines + substr_count(nl2br($text), '
');
  return $lines;
}

require './classes/conexao.php';

$connect = new conexao;
$connect = $connect->conectar();
$pdf = new PDF('P', 'mm', 'A4');
$pdf->AddPage();
$pdf->AliasNbPages();
$pdf->SetFont('Arial', '', 8);

$nl = chr(10);

if ($estagio == 'ESTÁGIO SUPERVISIONADO I') {
  $y = 66;
  $x = 10;
  $l = 25;
  $estagio1 = 'ESU0112 ' . $estagio . ' / TEC ENF';
  $caso1 = true;
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio1' AND anosemestre = '$ano'");
  $resultado = $sql->fetchAll();
  foreach ($resultado as $linha) {

    $data = date('d/m/Y',  strtotime($linha['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($linha['data_comp_out']));
    $dados = $linha['docente'] . $nl . $linha['local'];

    $pdf->SetY($y);
    $pdf->SetX(10);
    $pdf->Multicell(30, 12.5, $data, 'RLBT', 'C');

    $pdf->SetY($y);
    $pdf->SetX(40);
    $pdf->Multicell(160, 12.5, $dados, 'RLBT', 'C');

    $y += $l;

    $l = 10 * contaLinhas($data, 50);
    if ($y + $l >= 300) {
      $pdf->AddPage();
      $y = 66;
    }
  }
} else if ($estagio == 'ESTÁGIO SUPERVISIONADO II') {
  $estagio21 = 'ES0115A ' . $estagio . ' / ETAPA 1 / TEC ENF';
  $estagio22 = 'ES0115B ' . $estagio . ' / ETAPA 2 / TEC ENF';
  $estagio23 = 'ES0115C ' . $estagio . ' / ETAPA 3 / TEC ENF';
  $estagio24 = 'ES0115D ' . $estagio . ' / ETAPA 4 / TEC ENF';

  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio21' AND anosemestre = '$ano'");
  $resultado1 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio22' AND anosemestre = '$ano'");
  $resultado2 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio23' AND anosemestre = '$ano'");
  $resultado3 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio24' AND anosemestre = '$ano'");
  $resultado4 = $sql->rowCount() ? $sql->fetchAll() : [];

  $y = 90;
  $x = 10;
  $l = 40;
  if (count($resultado1) == count($resultado2) && count($resultado3) == count($resultado4)) {
    $pdf->SetXY(10, 65);
    $pdf->Cell(100, 5, 'Turma: ' . $turma, 0, 0, 'L');
    $pdf->SetXY(10, 70);
    $pdf->Cell(100, 5, 'Turno: ' . $resultado1[0]['turno'], 0, 0, 'L');
    $pdf->Line(10, 76, 200, 76);
    $pdf->SetFont('Arial', 'B', 8);
    $pdf->SetXY(10, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado1[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado1[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(57.5, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado2[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado2[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(105, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado3[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado3[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(152.5, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado4[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado4[0]['data_comp_out'])), 0, 'C');
    $pdf->Line(10, 88, 200, 88);
    $pdf->SetFont('Arial', '', 8);
    foreach ($resultado1 as $key => $value) {
      $dados1 = $value['docente'] . $nl . $value['local'];
      $dados2 = $resultado2[$key]['docente'] . $nl . $resultado2[$key]['local'];
      $dados3 = $resultado3[$key]['docente'] . $nl . $resultado3[$key]['local'];
      $dados4 = $resultado4[$key]['docente'] . $nl . $resultado4[$key]['local'];

      $pdf->SetY($y);
      $pdf->SetX(10);
      $pdf->Multicell(47.5, 6, $dados1, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(57.5);
      $pdf->Multicell(47.5, 6, $dados2, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(105);
      $pdf->Multicell(47.5, 6, $dados3, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(152.5);
      $pdf->Multicell(47.5, 6, $dados4, 0, 'C');

      $y += $l;
      $pdf->Line(10, $y, 200, $y);

      if (strlen($dados1) > strlen($dados2) &&  strlen($dados1) > strlen($dados3) && strlen($dados1) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados1, 50);
      } else if (strlen($dados2) > strlen($dados1) &&  strlen($dados2) > strlen($dados3) && strlen($dados2) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados2, 50);
      } else if (strlen($dados3) > strlen($dados1) &&  strlen($dados3) > strlen($dados2) && strlen($dados3) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados3, 50);
      } else if (strlen($dados4) > strlen($dados1) &&  strlen($dados4) > strlen($dados2) && strlen($dados4) > strlen($dados3)) {
        $l = 10 * contaLinhas($dados4, 50);
      }

      if ($y + $l >= 270) {
        $pdf->AddPage();
        $pdf->SetXY(10, 65);
        $pdf->Cell(100, 5, 'Turma: ' . $turma, 0, 0, 'L');
        $pdf->SetXY(10, 70);
        $pdf->Cell(100, 5, 'Turno: ' . $resultado1[0]['turno'], 0, 0, 'L');
        $pdf->Line(10, 76, 200, 76);
        $pdf->SetFont('Arial', 'B', 8);
        $pdf->SetXY(10, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado1[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado1[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(57.5, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado2[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado2[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(105, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado3[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado3[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(152.5, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado4[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado4[0]['data_comp_out'])), 0, 'C');
        $pdf->Line(10, 88, 200, 88);
        $pdf->SetFont('Arial', '', 8);
        $y = 90;
      }
    }
  }
} else if ($estagio == 'ESTÁGIO SUPERVISIONADO III') {

  $estagio31 = 'ES0119A ' . $estagio . ' / ETAPA 1 / TEC ENF';
  $estagio32 = 'ES0119B ' . $estagio . ' / ETAPA 2 / TEC ENF';
  $estagio33 = 'ES0119C ' . $estagio . ' / ETAPA 3 / TEC ENF';
  $estagio34 = 'ES0119D ' . $estagio . ' / ETAPA 4 / TEC ENF';

  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio31' AND anosemestre = '$ano'");
  $resultado1 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio32' AND anosemestre = '$ano'");
  $resultado2 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio33' AND anosemestre = '$ano'");
  $resultado3 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio34' AND anosemestre = '$ano'");
  $resultado4 = $sql->rowCount() ? $sql->fetchAll() : [];

  $y = 90;
  $x = 10;
  $l = 40;
  $pdf->Cell(100, 5, count($resultado1) . ' - ' . count($resultado2) . ' - ' . count($resultado3) . ' - ' . count($resultado4), 0, 0, 'L');
  if (count($resultado1) == count($resultado2) && count($resultado3) == count($resultado4)) {

    $pdf->SetXY(10, 65);
    $pdf->Cell(100, 5, 'Turma: ' . $turma, 0, 0, 'L');
    $pdf->SetXY(10, 70);
    $pdf->Cell(100, 5, 'Turno: ' . $resultado1[0]['turno'], 0, 0, 'L');
    $pdf->Line(10, 76, 200, 76);
    $pdf->SetFont('Arial', 'B', 8);
    $pdf->SetXY(10, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado1[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado1[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(57.5, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado2[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado2[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(105, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado3[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado3[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(152.5, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado4[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado4[0]['data_comp_out'])), 0, 'C');
    $pdf->Line(10, 88, 200, 88);
    $pdf->SetFont('Arial', '', 8);
    foreach ($resultado1 as $key => $value) {
      $dados1 = $value['docente'] . $nl . $value['local'];
      $dados2 = $resultado2[$key]['docente'] . $nl . $resultado2[$key]['local'];
      $dados3 = $resultado3[$key]['docente'] . $nl . $resultado3[$key]['local'];
      $dados4 = $resultado4[$key]['docente'] . $nl . $resultado4[$key]['local'];

      $pdf->SetY($y);
      $pdf->SetX(10);
      $pdf->Multicell(47.5, 6, $dados1, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(57.5);
      $pdf->Multicell(47.5, 6, $dados2, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(105);
      $pdf->Multicell(47.5, 6, $dados3, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(152.5);
      $pdf->Multicell(47.5, 6, $dados4, 0, 'C');

      $y += $l;
      $pdf->Line(10, $y, 200, $y);

      if (strlen($dados1) > strlen($dados2) &&  strlen($dados1) > strlen($dados3) && strlen($dados1) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados1, 50);
      } else if (strlen($dados2) > strlen($dados1) &&  strlen($dados2) > strlen($dados3) && strlen($dados2) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados2, 50);
      } else if (strlen($dados3) > strlen($dados1) &&  strlen($dados3) > strlen($dados2) && strlen($dados3) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados3, 50);
      } else if (strlen($dados4) > strlen($dados1) &&  strlen($dados4) > strlen($dados2) && strlen($dados4) > strlen($dados3)) {
        $l = 10 * contaLinhas($dados4, 50);
      }

      if ($y + $l >= 270) {
        $pdf->AddPage();
        $pdf->SetXY(10, 65);
        $pdf->Cell(100, 5, 'Turma: ' . $turma, 0, 0, 'L');
        $pdf->SetXY(10, 70);
        $pdf->Cell(100, 5, 'Turno: ' . $resultado1[0]['turno'], 0, 0, 'L');
        $pdf->Line(10, 76, 200, 76);
        $pdf->SetFont('Arial', 'B', 8);
        $pdf->SetXY(10, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado1[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado1[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(57.5, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado2[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado2[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(105, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado3[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado3[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(152.5, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado4[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado4[0]['data_comp_out'])), 0, 'C');
        $pdf->Line(10, 88, 200, 88);
        $pdf->SetFont('Arial', '', 8);
        $y = 90;
      }
    }
  }
} else if ($estagio == 'ESTÁGIO SUPERVISIONADO IV') {
  $estagio41 = 'ES0128A ' . $estagio . ' / ETAPA 1 / TEC ENF';
  $estagio42 = 'ES0128B ' . $estagio . ' / ETAPA 2 / TEC ENF';
  $estagio43 = 'ES0128C ' . $estagio . ' / ETAPA 3 / TEC ENF';
  $estagio44 = 'ES0128D ' . $estagio . ' / ETAPA 4 / TEC ENF';

  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio41' AND anosemestre = '$ano'");
  $resultado1 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio42' AND anosemestre = '$ano'");
  $resultado2 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio43' AND anosemestre = '$ano'");
  $resultado3 = $sql->rowCount() ? $sql->fetchAll() : [];
  $sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND componente = '$estagio44' AND anosemestre = '$ano'");
  $resultado4 = $sql->rowCount() ? $sql->fetchAll() : [];

  $y = 90;
  $x = 10;
  $l = 40;
  if (count($resultado1) == count($resultado2) && count($resultado3) == count($resultado4)) {
    $pdf->SetXY(10, 65);
    $pdf->Cell(100, 5, 'Turma: ' . $turma, 0, 0, 'L');
    $pdf->SetXY(10, 70);
    $pdf->Cell(100, 5, 'Turno: ' . $resultado1[0]['turno'], 0, 0, 'L');
    $pdf->Line(10, 76, 200, 76);
    $pdf->SetFont('Arial', 'B', 8);
    $pdf->SetXY(10, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado1[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado1[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(57.5, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado2[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado2[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(105, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado3[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado3[0]['data_comp_out'])), 0, 'C');
    $pdf->SetXY(152.5, 76);
    $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado4[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado4[0]['data_comp_out'])), 0, 'C');
    $pdf->Line(10, 88, 200, 88);
    $pdf->SetFont('Arial', '', 8);
    foreach ($resultado1 as $key => $value) {
      $dados1 = $value['docente'] . $nl . $value['local'];
      $dados2 = $resultado2[$key]['docente'] . $nl . $resultado2[$key]['local'];
      $dados3 = $resultado3[$key]['docente'] . $nl . $resultado3[$key]['local'];
      $dados4 = $resultado4[$key]['docente'] . $nl . $resultado4[$key]['local'];

      $pdf->SetY($y);
      $pdf->SetX(10);
      $pdf->Multicell(47.5, 6, $dados1, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(57.5);
      $pdf->Multicell(47.5, 6, $dados2, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(105);
      $pdf->Multicell(47.5, 6, $dados3, 0, 'C');

      $pdf->SetY($y);
      $pdf->SetX(152.5);
      $pdf->Multicell(47.5, 6, $dados4, 0, 'C');

      $y += $l;
      $pdf->Line(10, $y, 200, $y);

      if (strlen($dados1) > strlen($dados2) &&  strlen($dados1) > strlen($dados3) && strlen($dados1) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados1, 50);
      } else if (strlen($dados2) > strlen($dados1) &&  strlen($dados2) > strlen($dados3) && strlen($dados2) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados2, 50);
      } else if (strlen($dados3) > strlen($dados1) &&  strlen($dados3) > strlen($dados2) && strlen($dados3) > strlen($dados4)) {
        $l = 10 * contaLinhas($dados3, 50);
      } else if (strlen($dados4) > strlen($dados1) &&  strlen($dados4) > strlen($dados2) && strlen($dados4) > strlen($dados3)) {
        $l = 10 * contaLinhas($dados4, 50);
      }

      if ($y + $l >= 270) {
        $pdf->AddPage();
        $pdf->SetXY(10, 65);
        $pdf->Cell(100, 5, 'Turma: ' . $turma, 0, 0, 'L');
        $pdf->SetXY(10, 70);
        $pdf->Cell(100, 5, 'Turno: ' . $resultado1[0]['turno'], 0, 0, 'L');
        $pdf->Line(10, 76, 200, 76);
        $pdf->SetFont('Arial', 'B', 8);
        $pdf->SetXY(10, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado1[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado1[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(57.5, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado2[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado2[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(105, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado3[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado3[0]['data_comp_out'])), 0, 'C');
        $pdf->SetXY(152.5, 76);
        $pdf->Multicell(47.5, 6, date('d/m/Y',  strtotime($resultado4[0]['data_comp_ini'])) . $nl . date('d/m/Y',  strtotime($resultado4[0]['data_comp_out'])), 0, 'C');
        $pdf->Line(10, 88, 200, 88);
        $pdf->SetFont('Arial', '', 8);
        $y = 90;
      }
    }
  }
}




$pdf->Output();
