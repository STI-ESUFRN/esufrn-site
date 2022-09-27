<?php
error_reporting(0);

session_start();

if (isset($_GET['status'])) {

  $status = $_GET['status'];

  if ($status == 'logout') {
    session_destroy();
    echo "<script>window.location.assign('index.php')</script>";
  }
} else if (isset($_SESSION['logged_in']) and $_SESSION['logged_in'] === true) {


  // Display index

?>

  <!DOCTYPE html>
  <html lang="en" class="no-js">

  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SIGEP </title>
    <meta name="description" content="Tab Styles Inspiration: A small collection of styles for tabs" />
    <meta name="keywords" content="tabs, inspiration, web design, css, modern, effects, svg" />
    <meta name="author" content="Codrops" />
    <link rel="shortcut icon" href="../favicon.ico">
    <link rel="stylesheet" type="text/css" href="assets/css/normalize.css" />
    <link rel="stylesheet" type="text/css" href="assets/css/demo.css" />
    <link rel="stylesheet" type="text/css" href="assets/css/tabs.css" />
    <link rel="stylesheet" type="text/css" href="assets/css/tabstyles.css" />
    <link href="https://fonts.googleapis.com/css?family=Orbitron" rel="stylesheet">
    <script src="assets/js/modernizr.custom.js"></script>
    <script type="text/javascript">
      function refreshCursos() {
        document.getElementById("i_cursos").contentWindow.location.reload(true);
      }
    </script>
  </head>

  <body>
    <div class="container">

      <!-- Top Navigation -->
      <div class="codrops-top clearfix" id="css-topbar">
        <a class="codrops-icon codrops-icon-prev" href="http://escoladesaude.ufrn.br"><span>Site ESUFRN</span></a>
        <span class="right"><a href="index.php?status=logout">
            <img style="padding-right:5px;float: left; color: #fff" src="assets/img/poweroff_blue.png"><span>LOGOUT</span></a>
        </span>
      </div>

      <header class="codrops-header" id="css-header">

        <h1>
          <table>
            <tr>
              <td>
                <div style="color:#003b62; width:230px;font-family: 'Orbitron', sans-serif;">SIGEP</div>
              </td>
              <td>
                <img src="./assets/img/logo-suporte.png" style="padding-top: 35px;">
              </td>
            </tr>
          </table>
        </h1>

      </header>


      <div class="tabs tabs-style-flip content-body">
        <nav>
          <ul>
            <li><a href="#section-flip-5" class="icon "><span>Turmas</span></a></li>
            <li><a href="#section-flip-4" class="icon" onclick="refreshCursos()"><span>Cursos</span></a></li>
            <li><a href="#section-flip-2" class="icon "><span>Docentes</span></a></li>
            <li><a href="#section-flip-1" class="icon "><span>Componentes</span></a></li>
            <li><a href="#section-flip-6" class="icon "><span>Planejamentos</span></a></li>
            <li><a href="#section-flip-7" class="icon "><span>Relatórios</span></a></li>
          </ul>
        </nav>
        <div class="content-wrap">
          <section id="section-flip-1">
            <iframe style="border:0;" width="1300" height="630px" src="turmas.php"></iframe>
          </section>
          </section>
          <section id="section-flip-2"><iframe id="i_cursos" style="border:0;" width="1300px" height="630px" src="cursos.php"></iframe></section>
          <section id="section-flip-3"><iframe style="border:0;" width="1300px" height="630px" src="docentes.php"></iframe></section>
          <section id="section-flip-5"><iframe style="border:0;" width="1300px" height="630px" src="componentes.php"></iframe></section>
          <section id="section-flip-6"><iframe style="overflow-y: scroll;border:0;" width="1300px" height="750px" src="planejamentos.php"></iframe></section>
          <section id="section-flip-7"><iframe style="overflow-y: scroll;border:0;" width="1300px" height="750px" src="relatorios.php"></iframe></section>

        </div>
        <!-- /content -->
      </div>
      <!-- /tabs -->


    </div>

    <!-- /container -->
    <script src="assets/js/cbpFWTabs.js"></script>
    <script>
      (function() {

        [].slice.call(document.querySelectorAll('.tabs')).forEach(function(el) {
          new CBPFWTabs(el);
        });

      })();
    </script>
  </body>

  </html>


<?php

} else {
  if (isset($_POST['username'], $_POST['password'])) {

    $username = $_POST['username'];
    $password = $_POST['password'];

    if (empty($username) or empty($password)) {

      $error = 'Usuario ou Senha não preenchida!';
    } else {

      require './classes/conexao.php';

      $connect = new conexao;
      $connect = $connect->conectar();

      $query = $connect->prepare("SELECT * FROM users WHERE user_name = ? AND user_password = ?");

      $query->bindValue(1, $username);
      $query->bindValue(2, $password);
      $query->execute();

      $num = $query->rowCount();

      if ($num == 1) {

        $dados = $query->fetch(PDO::FETCH_ASSOC);

        $_SESSION['logged_in'] = true;
        $_SESSION['user_curso'] = $dados['user_curso'];

        header('Location: index.php');

        exit();
      } else {
        // Nao entrou com o login correto
        $error = 'Conta n&atilde;o existente!';
      }
    }
  }

?>


  <!DOCTYPE html>
  <html lang="en">

  <head>
    <meta charset="UTF-8">
    <title>SIGEP</title>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css">

    <link rel='stylesheet prefetch' href='https://fonts.googleapis.com/css?family=Roboto:400,100,300,500,700,900'>
    <link rel='stylesheet prefetch' href='https://fonts.googleapis.com/css?family=Montserrat:400,700'>
    <link rel='stylesheet prefetch' href='https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css'>

    <link href="https://fonts.googleapis.com/css?family=Orbitron" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">


  </head>

  <body>

    <br><br><br><br><br><br><br><br>

    <div class="form">

      <div class="codrops-header">

        <h1>

          <div style="color:#003b62; width:230px;font-family: 'Orbitron', sans-serif;padding: 0 0 0 37px">SIGEP</div>


        </h1>

      </div>

      <form class="register-form">
        <input type="text" placeholder="name" />
        <input type="password" placeholder="password" />
        <input type="text" placeholder="email address" />
        <button>create</button>
        <p class="message">Already registered? <a href="#">Sign In</a></p>
      </form>

      <?php if (isset($error)) { ?>
        <small style="color:#aa0000;"><?php echo $error; ?></small>
        <br><br>
      <?php } ?>

      <form class="login-form" action="index.php" method="post" autocomplete="off">

        <input type="text" name="username" placeholder="Usuário" />
        <input type="password" name="password" placeholder="Senha" />
        <input type="submit" value="Entrar" style="background-color: #3f95c7; color: white;" />

        <img src="./assets/img/logo-suporte.png" style="padding-top: 15px; ">


        <!--  <p class="message">Not registered? <a href="#">Create an account</a></p>-->
      </form>

    </div>

    <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

    <script src="js/index.js"></script>

  </body>

  </html>




<?php

}

?>