<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require "./classes/fpdf/fpdf.php";

$pdo = new PDO("mysql:host=localhost;dbname=sigep", "wordpress01", "pfnt3s,01");
$pdo->exec("set names utf8");

//$curso = $_POST['selectcurso'];
$turma = $_POST['selectturma'];
$divisor = explode('    ', $turma, 2);
$curso = $divisor[1];
//echo $curso;
$ano = $_POST['selectano'] . $_POST['selectsemestre'];

$chtotal = 0;

class myPDF extends FPDF
{
  function header()
  {
    date_default_timezone_set('America/Recife');
    $dataemissao = date('d/m/Y H:i');
    global $curso, $ano, $turma;
    $this->Image('./assets/img/ufrn.jpg', 10, 10, 45, 19);
    $this->Image('./assets/img/esufrn.png', 152, 13, 46, 10);
    $this->SetFont('Arial', 'B', 10);
    $this->CEll(185, 10, 'UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE', 0, 0, 'C');
    $this->Ln(6);
    $this->SetFont('Arial', 'B', 10);
    $this->Cell(190, 10, 'ESCOLA DE SAÚDE', 0, 0, 'C');
    $this->Ln(6);
    $this->SetFont('Arial', '', 9);
    $this->Cell(190, 34, 'Emitido em: ' . $dataemissao, 0, 0, 'C');
    $this->Ln(20);
    $this->cell(188, 0, '', 1, 0, 'C');
    $this->Ln(1);
    $this->SetFont('Arial', '', 10);
    $this->CEll(190, 10, 'Relatório de Distribuição de Componente Curricular por Turma e Semestre', 0, 0, 'C');
    $this->Ln(10);
    $this->cell(188, 0, '', 1, 0, 'C');
    $this->Ln(10);
    $this->SetFont('Arial', 'b', 10);
    $this->Cell(190, 1, 'TURMA: ' . $turma . ' - ANO/SEMESTRE: ' . $ano[0] . $ano[1] . $ano[2] . $ano[3] . '.' . $ano[4], 0, 0, 'C');
    $this->Ln(10);
  }
  function footer()
  {
    $this->SetY(-15);
    $this->SetFont('Arial', '', 8);
    $this->Cell(0, 5, 'Sistema de Gestão e Planejamento Acadêmco - SIGEP | Desenvolvido pelo: Suporte de TI - ESUFRN | Copyright © 2017', 1, 0, 'C');
  }
  function headerTable()
  {
    $this->SetFont('Arial', 'B', 9);
    $this->cell(15, 8, 'Código', 0, 0, 'L');
    $this->cell(40, 8, 'Componente Curricular', 0, 0, 'L');
    $this->cell(45, 8, 'Docente', 0, 0, 'C');
    $this->cell(10, 8, 'Turno', 0, 0, 'C');
    $this->cell(10, 8, 'C.H.', 0, 0, 'C');
    $this->cell(25, 8, 'Período C.C.', 0, 0, 'L');
    $this->cell(50, 8, 'Período Docente', 0, 0, 'L');
    $this->Ln();
    $this->cell(188, 0, '', 1, 0, 'C');
    $this->Ln();
  }
  function viewTable($pdo)
  {
    $this->SetFont('Times', '', 9);
    global $curso, $ano, $turma;
    $query = $pdo->prepare("SELECT * FROM planejamento WHERE turma = '$turma'");
    $query->execute();
    //$busca=$pdo->prepare("SELECT * FROM planejamento WHERE turma=:nome and anosemestre=:ano");
    //$busca->bindValue(":nome",$turma);
    //$busca->bindValue(":ano",$ano);
    //$busca->execute();
    $peido = 0;
    while ($data = $query->fetch(PDO::FETCH_ASSOC)) {

      $aux = explode(" ", $data['componente'], 2);
      $codigo_comp = $aux[0];
      $nome_comp = $aux[1];
      $this->SetXY(10, 81 + $peido);
      $this->MultiCell(15, 5, $codigo_comp, 0, 'L', false);
      $this->SetXY(25, 81 + $peido);
      $this->MultiCell(40, 5, $nome_comp, 0, 'L', false);
      $this->SetXY(65, 81 + $peido);
      $this->MultiCell(45, 6, $data['docente'], 0, 'L', false);
      $this->SetXY(110, 81 + $peido);
      $this->Multicell(10, 6, substr($data['turno'], 0, 3), 0, 'C', false);
      $this->SetXY(120, 81 + $peido);
      $this->Multicell(10, 6, $data['ch'] . 'H', 0, 'C', false);
      $this->SetXY(130, 81 + $peido);
      $this->MultiCell(20, 6, date('d/m/Y',  strtotime($data['data_comp_ini'])) . ' A ' . date('d/m/Y',  strtotime($data['data_comp_out'])), 0, 'C', false);
      $this->SetXY(154, 81 + $peido);
      $this->MultiCell(30, 6, date('d/m/Y',  strtotime($data['data_ini'])) . ' A ' . date('d/m/Y',  strtotime($data['data_fim'])), 0, 'C', false);

      //$peido = $peido + 20;

      global $chtotal;
      $chtotal = $chtotal + $data["ch"];
      $this->cell(0, 5, '', 0, 1, 'C', false);
    }
    $this->Ln();
    $this->cell(188, 0, '', 1, 0, 'C');
    $this->Ln();
  }
  function ch()
  {
    global $chtotal;
    $this->SetFont('Arial', 'B', 11);
    $this->cell(178, 8, 'CH Total: ', 0, 0, 'R');
    $this->cell(10, 8, $chtotal . 'H', 0, 0, 'R');
    $this->Ln(25);
  }
  function obs($pdo)
  {
    global $docente;
    $this->cell(188, 0, '', 1, 0, 'C');
    $this->Ln(1);
    $this->SetFont('Arial', 'B', 12);
    $this->Ln();
    $this->SetFont('Times', '', 10);
    $busca = $pdo->prepare("SELECT observacaodocente FROM docente WHERE nomedocente=:nome");
    $busca->bindValue(":nome", $docente);
    $busca->execute();
    $obs = $busca->fetchColumn();
    $this->SetFont('Arial', 'B', 9);
    $this->cell(190, 8, 'Observação:', 0, 0, 'L');
    $this->Cell(190, 10, utf8_decode($obs), 0, 0, 'R');
  }
}

$pdf = new myPDF();
$pdf->AliasNbPages();
$pdf->AddPage('P', 'A4', 0);
$pdf->headerTable();
$pdf->viewTable($pdo);
$pdf->ch();
$pdf->obs($pdo);
$pdf->Output();
