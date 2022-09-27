  <?php
  error_reporting(0);
  require '../classes/conexao.php';

  if (isset($_POST['selectcursos'])) {

    $curso = $_POST['selectcursos'];
    if (empty($data_name["cursocomponentes"])) {
      $aux = $curso;
      $con = new conexao;
      $con = $con->conectar();
      $id = $_GET['id'];

      $consults = $con->query("SELECT * FROM curso WHERE id=$id");
      $componente = $consults->fetch(PDO::FETCH_ASSOC);
      $auxilia = explode('-', $componente["cursocomponentes"]);
      $sql = "UPDATE curso SET cursocomponentes=? WHERE id=?";

      $enviar = $con->prepare($sql);

      $enviar->execute(array("$aux", "$id"));

      header('location:../adicionarComponentes.php?id=' . $id . '');
    } else {

      if (strrpos($data_name["cursocomponentes"], $curso) === false) {
        $aux = $data_name["cursocomponentes"] . '-' . $curso;
        $con = new conexao;
        $con = $con->conectar();

        $consults = $con->query("SELECT * FROM curso WHERE id=$id");
        $componente = $consults->fetch(PDO::FETCH_ASSOC);
        $auxilia = explode('-', $componente["cursocomponentes"]);

        $sql = "UPDATE curso SET cursocomponentes=? WHERE id=?";

        $enviar = $con->prepare($sql);

        $enviar->execute(array("$aux", "$id"));

        header('location:../adicionarComponentes.php?id=' . $id . '');
      }
    }
    //}                                           
  }

  ?>