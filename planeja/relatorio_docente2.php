<?php

require './classes/fpdf/fpdf.php';

$docente = $_POST['selectdocente'];
$ano = $_POST['selectano'] . $_POST['selectsemestre'];

class PDF extends FPDF
{

  function Header()
  {
    global $docente, $ano;
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
    $this->Cell(170, 15, "Relatório de Distribuição de Componente Curricular por Docente", 0, 0, 'C');
    $this->Line(10, 50, 200, 50);

    $this->SetFont('Arial', 'B', 10);
    $this->SetXY(17, 50);
    $this->Cell(170, 15, "DOCENTE: " . $docente . " - ANO/SEMESTRE: " . $ano[0] . $ano[1] . $ano[2] . $ano[3] . '.' . $ano[4], 0, 0, 'C');

    $this->SetFont('Arial', 'B', 9);
    $this->SetXY(10, 66);
    $this->Cell(50, 8, 'Componente Curricular', 0, 0, 'L');
    $this->SetXY(60, 66);
    $this->Cell(50, 8, 'Turma', 0, 0, 'C');
    $this->SetXY(110, 66);
    $this->Cell(23, 8, 'Turno', 0, 0, 'C');
    $this->SetXY(133, 66);
    $this->Cell(17, 8, 'Dias', 0, 0, 'C');
    $this->SetXY(150, 66);
    $this->Cell(10, 8, 'C.H.', 0, 0, 'C');
    $this->SetXY(160, 66);
    $this->Cell(40, 8, 'Período', 0, 0, 'C');


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

$sql = $connect->query("SELECT * FROM planejamento WHERE docente = '$docente' AND anosemestre = '$ano' ORDER BY anosemestre DESC, data_ini ASC ");
$resultado = $sql->fetchAll();
$l = 5;
$chtotal = 0;
foreach ($resultado as $linha) {
  $componente = $linha['componente'];
  $docente = $linha['docente'];
  $turma = $linha['turma'];
  $turno = $linha['turno'];
  $carga = $linha['ch'];
  $dias = $linha['dia'];
  $pdocente = date('d/m/Y',  strtotime($linha['data_ini'])) . ' A ' . date('d/m/Y',  strtotime($linha['data_fim']));

  if (strlen($componente) > strlen($turma)) {
    $l = 10 * contaLinhas($componente, 50);
  } else {
    $l = 10 * contaLinhas($turma, 50);
  }

  if ($y + $l >= 280) {           // 230 É O TAMANHO MAXIMO ANTES DO RODAPE

    $pdf->AddPage();   // SE ULTRAPASSADO, É ADICIONADO UMA PÁGINA
    $y = 75;             // E O Y INICIAL É RESETADO

  }

  $pdf->SetY($y);
  $pdf->SetX(10);
  $pdf->Multicell(50, 6, $componente, 0, 'L');
  $pdf->SetY($y);
  $pdf->SetX(60);
  $pdf->Multicell(50, 6, $turma, 0, 'C');
  $pdf->SetY($y);
  $pdf->SetX(110);
  $pdf->Multicell(23, 6, $turno, 0, 'C');
  $pdf->SetY($y);
  $pdf->SetX(133);
  $pdf->Multicell(17, 6, $dias, 0, 'C');
  $pdf->SetY($y);
  $pdf->SetX(150);
  $pdf->Multicell(10, 6, $carga, 0, 'C');
  $pdf->SetY($y);
  $pdf->SetX(160);
  $pdf->Multicell(40, 6, $pdocente, 0, 'C');


  $pdf->Ln();
  $y += $l;
  $chtotal += $carga;
  $pdf->Line(10, $y, 200, $y);
}
$pdf->Ln(14);
$pdf->SetFont('Arial', 'B', 12);
$pdf->Cell(190, 8, 'Carga Horária Total: ' . $chtotal . 'H', 0, 0, 'R');
$pdf->Ln();
$pdf->SetFont('Arial', 'B', 10);;
$pdf->cell(200, 8, 'Observação:', 0, 0, 'L');
$sql = $connect->query("SELECT observacaodocente FROM docente WHERE nomedocente = '$docente'");
$resultado = $sql->fetchColumn();
$pdf->Ln(8);
$pdf->SetFont('Arial', '', 8);
$pdf->cell(190, 10, $resultado, 0, 0, 'L');

$pdf->Output();
