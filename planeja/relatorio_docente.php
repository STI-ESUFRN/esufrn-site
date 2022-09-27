<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require "./classes/fpdf/fpdf.php";

$pdo = new PDO("mysql:host=localhost;dbname=sigep", "wordpress01", "pfnt3s,01");
$pdo->exec("set names utf8");

$docente = $_POST['selectdocente'];
$chtotal = 0;

class myPDF extends FPDF
{
  function header()
  {
    date_default_timezone_set('America/Recife');
    $dataemissao = date('d/m/Y H:i');
    global $docente;
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
    $this->CEll(190, 10, 'Relatório de Distribuição de Componente Curricular por Docente', 0, 0, 'C');
    $this->Ln(10);
    $this->cell(188, 0, '', 1, 0, 'C');
    $this->Ln(10);
    $this->SetFont('Arial', 'b', 10);
    $this->Cell(190, 1, 'Docente: ' . $docente, 0, 0, 'C');
    $this->Ln(10);
  }
  function footer()
  {
    $this->SetY(-15);
    $this->SetFont('Arial', '', 8);
    $this->Cell(0, 5, 'Sistema de Gestão e Planejamento Acadêmco - SIGEP | Desenvolvido pelo: Suporte de TI - ESUFRN | Copyright © 2018', 1, 0, 'C');
  }
  function headerTable()
  {
    $this->SetFont('Arial', 'B', 9);
    $this->cell(56, 8, 'Componente Curricular', 0, 0, 'L');
    $this->cell(50, 8, 'Turma', 0, 0, 'C');
    $this->cell(22, 8, 'Turno', 0, 0, 'C');
    $this->cell(10, 8, 'C.H.', 0, 0, 'C');
    $this->cell(50, 8, 'Período', 0, 0, 'L');
    $this->Ln();
    $this->cell(188, 0, '', 1, 0, 'C');
    $this->Ln();
  }
  function viewTable($pdo)
  {
    $this->SetFont('Times', '', 9);
    global $docente;
    $busca = $pdo->prepare("SELECT docente, componente, turma, turno, ch, data_ini, data_fim FROM planejamento WHERE docente=:nome");
    $busca->bindValue(":nome", $docente);
    $busca->execute();
    $peido = 0;

    while ($data = $busca->fetch(PDO::FETCH_ASSOC)) {
      $this->SetXY(10, 81 + $peido);
      $this->MultiCell(56, 6, $data["componente"], 0, 'L', false);
      $this->SetXY(66, 81 + $peido);
      $this->MultiCell(50, 6, $data["turma"], 0, 'L', false);
      $this->SetXY(116, 81 + $peido);
      $this->Multicell(22, 6, $data["turno"], 0, 'L', false);
      $this->SetXY(138, 81 + $peido);
      $this->Multicell(10, 6, $data["ch"] . 'H', 0, 'L', false);
      $this->SetXY(148, 81 + $peido);
      $this->Multicell(50, 6, date('d/m/Y',  strtotime($data["data_ini"])) . ' A ' . date('d/m/Y',  strtotime($data["data_fim"])), 0, 'L', false);
      $this->Line(10, 81 + $peido, 198, 81 + $peido);

      global $chtotal;
      $chtotal = $chtotal + $data["ch"];
      $peido = $peido + 20;
    }
    $this->Line(10, $this->GetY() + 15, 198, $this->GetY() + 15);
    $this->Ln(15);
  }
  function ch()
  {
    global $chtotal;
    $this->SetFont('Arial', 'B', 11);
    //$this->cell(160,8,'CH Total: '.$chtotal.'H',0,0,'R');
    $this->cell(178, 8, 'CH Total: ', 0, 0, 'R');
    $this->cell(10, 8, $chtotal . 'H', 0, 0, 'R');
    $this->Ln(10);
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
    $this->Ln(4);
    $this->cell(190, 10, $obs, 0, 0, 'L');
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
