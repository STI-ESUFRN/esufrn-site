<?php

class deletar
{
  function deletar_feriado($id, $con)
  {

    $sql = "DELETE FROM feriado WHERE id_feriado = $id";

    $data_name = $con->prepare($sql);

    $data_name->execute();

    if ($data_name) {

      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  function deletar_curso($id, $con)
  {

    $sql = "DELETE FROM curso WHERE id = $id";

    $data_name = $con->prepare($sql);

    $data_name->execute();

    if ($data_name) {

      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  function deletar_docente($id, $con)
  {

    $sql = "DELETE FROM docente WHERE id_docente = $id";

    $data_name = $con->prepare($sql);

    $data_name->execute();

    if ($data_name) {

      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  function deletar_turma($id, $con)
  {

    $sql = "DELETE FROM turma WHERE id = $id";

    $data_name = $con->prepare($sql);

    $data_name->execute();

    if ($data_name) {

      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }

  function deletar_componente($id, $con)
  {

    $sql = "DELETE FROM disciplina WHERE id = $id";

    $data_name = $con->prepare($sql);

    $data_name->execute();

    if ($data_name) {

      return 'Sucesso';
    } else {
      return 'Fudeu';
    }
  }
  function deletar_planejamento($id, $con)
  {

    session_start();

    $sql = $con->query("SELECT curso FROM planejamento WHERE id = $id");

    $data = $sql->fetch(PDO::FETCH_ASSOC);

    if ($_SESSION['user_curso'] === $data['curso']) {

      $sql = "DELETE FROM planejamento WHERE id = $id";

      $data_name = $con->prepare($sql);

      $data_name->execute();

      if ($data_name) {
        return 'Sucesso';
      }
    } elseif ($_SESSION['user_curso'] === 'admin') {

      $sql = "DELETE FROM planejamento WHERE id = $id";

      $data_name = $con->prepare($sql);

      $data_name->execute();

      if ($data_name) {
        return 'Sucesso';
      }
    } else {
      return 'CursoDiferente';
    }
  }
}
