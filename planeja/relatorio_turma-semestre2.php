<?php

require './classes/fpdf/fpdf.php';

$turma = $_POST['selectturma'];
$divisor = explode('    ', $turma, 2);
$curso = $divisor[1];
$ano = $_POST['selectano'] . $_POST['selectsemestre'];


class PDF extends FPDF
{

  function Header()
  {
    global $codigo, $turma, $ano;
    $l = 5;
    date_default_timezone_set('America/Recife');
    $dataemissao = date('d/m/Y H:i');
    $this->SetXY(10, 10);
    //$this->Rect(10,10,190,280);
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
    $this->Cell(170, 15, "Relatório de Distribuição de Componente Curricular por Turma e Semestre", 0, 0, 'C');
    $this->Line(10, 50, 200, 50);

    $this->SetFont('Arial', 'B', 10);
    $this->SetXY(17, 50);
    $this->Cell(170, 15, "TURMA: " . $turma . " - ANO/SEMESTRE: " . $ano[0] . $ano[1] . $ano[2] . $ano[3] . '.' . $ano[4], 0, 0, 'C');

    $this->SetFont('Arial', 'B', 9);
    $this->SetXY(10, 66);
    $this->Cell(15, 8, 'Código', 0, 0, 'C');
    $this->SetXY(25, 66);
    $this->Cell(50, 8, 'Componente Curricular', 0, 0, 'C');
    $this->SetXY(75, 66);
    $this->Cell(45, 8, 'Docente', 0, 0, 'C');
    $this->SetXY(120, 66);
    $this->Cell(10, 8, 'Turno', 0, 0, 'C');
    $this->SetXY(130, 66);
    $this->Cell(10, 8, 'C.H.', 0, 0, 'C');
    $this->SetXY(140, 66);
    $this->Cell(30, 8, 'Período C.C.', 0, 0, 'C');
    $this->SetXY(170, 66);
    $this->Cell(30, 8, 'Período Docente', 0, 0, 'C');

    $this->Line(10, 74, 200, 74);
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
    $lines = 1.5;
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
$y = 75;

$sql = $connect->query("SELECT * FROM planejamento WHERE turma = '$turma' AND anosemestre = '$ano'");
$resultado = $sql->fetchAll();
$l = 5;

foreach ($resultado as $linha) {
  $aux = explode(" ", $linha['componente'], 2);
  $codigo_comp = $aux[0];
  $nome_comp = $aux[1];
  $docente = $linha['docente'];
  $turno = $linha['turno'];
  $carga = $linha['ch'];
  $pcomponente = date('d/m/Y',  strtotime($linha['data_comp_ini'])) . ' A ' . date('d/m/Y',  strtotime($linha['data_comp_out']));
  $pdocente = date('d/m/Y',  strtotime($linha['data_ini'])) . ' A ' . date('d/m/Y',  strtotime($linha['data_fim']));

  $l = 10 * contaLinhas($nome_comp, 50);
  if ($y + $l >= 280) {           // 230 É O TAMANHO MAXIMO ANTES DO RODAPE

    $pdf->AddPage();   // SE ULTRAPASSADO, É ADICIONADO UMA PÁGINA
    $y = 75;             // E O Y INICIAL É RESETADO

  }

  $pdf->SetY($y);
  $pdf->SetX(10);
  $pdf->Multicell(15, 6, $codigo_comp, 0, 'L');
  $pdf->SetY($y);
  $pdf->SetX(25);
  $pdf->Multicell(50, 6, $nome_comp, 0, 'L');
  $pdf->SetY($y);
  $pdf->SetX(75);
  $pdf->Multicell(45, 6, $docente, 0, 'L');
  $pdf->SetY($y);
  $pdf->SetX(120);
  $pdf->Multicell(10, 6, substr($turno, 0, 3), 0, 'C');
  $pdf->SetY($y);
  $pdf->SetX(130);
  $pdf->Multicell(10, 6, $carga . 'h', 0, 'C');
  $pdf->SetY($y);
  $pdf->SetX(140);
  $pdf->Multicell(30, 6, $pcomponente, 0, 'C');
  $pdf->SetY($y);
  $pdf->SetX(170);
  $pdf->Multicell(30, 6, $pdocente, 0, 'C');

  $pdf->Ln();

  $y += $l;
  $pdf->Line(10, $y, 200, $y);
}

$pdf->Output();
