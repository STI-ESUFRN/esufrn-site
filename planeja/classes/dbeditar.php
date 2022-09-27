<?php
class editar
{
  function editar_feriado($dados, $con, $id)
  {
    $descricao_feriado = $_POST['descricaoferiado'];
    $data_feriado = $_POST['dataferiado'];

    $sql = 'UPDATE feriado SET descricao_feriado=?, data_feriado=? WHERE id_feriado =?';

    $enviar = $con->prepare($sql);

    $enviar->execute(array("$descricao_feriado", "$data_feriado", "$id"));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  function editar_curso($dados, $con, $id)
  {
    $nomecurso = $_POST['nomecursos'];

    $sql = 'UPDATE curso SET nomecurso=? WHERE id=?';

    $enviar = $con->prepare($sql);

    $enviar->execute(array("$nomecurso", "$id"));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }

  function editar_docente($dados, $con, $id)
  {
    $nomedocente = $_POST['nomedocente'];
    $observacaodocente = $_POST['observacaodocente'];

    $sql = 'UPDATE docente SET nomedocente=?, observacaodocente=? WHERE id_docente=?';

    $enviar = $con->prepare($sql);

    $enviar->execute(array("$nomedocente", "$observacaodocente", "$id"));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }

  function editar_turma($dados, $con, $id)
  {

    if (empty($_POST['statusturma'])) {
      $statusturma = 'INATIVA';
    } else {
      $statusturma = 'ATIVA';
    }

    $sql = 'UPDATE turma SET statusturma=? WHERE id=?';

    $enviar = $con->prepare($sql);

    $enviar->execute(array("$statusturma", "$id"));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  function editar_componente($dados, $con, $id)
  {
    $nome_comp = $_POST['nomecomp'];
    $codigo_comp = $_POST['codigocomp'];
    $carga_comp = $_POST['cargacomp'];

    $sql = 'UPDATE disciplina SET nome_disciplina=?, carga_horario=?, codigo=? WHERE id=?';
    $enviar = $con->prepare($sql);

    $enviar->execute(array("$nome_comp", "$carga_comp", "$codigo_comp", "$id"));

    if ($enviar) {
      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
}
