<?php

class conexao
{
  // private $dbhost = 'db';
  // private $dbuser = 'root';
  // private $dbpass = 'pfnt3s,01';
  // private $dbname = 'sigep';
  // public function conectar()
  // {
  //     $mysql_connect_str = "mysql:host=$this->dbhost;dbname=$this->dbname";
  //     $dbConnection      = new PDO($mysql_connect_str, $this->dbuser, $this->dbpass);
  //     $dbConnection->exec("set names utf8");
  //     $dbConnection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  //     return $dbConnection;
  // }

  // private $dbhost = 'localhost';
  // private $dbuser = 'root';
  // private $dbpass = '';
  // private $dbname = 'sigep';
  // public function conectar()
  // {
  //     $mysql_connect_str = "mysql:host=$this->dbhost;dbname=$this->dbname";
  //     $dbConnection      = new PDO($mysql_connect_str, $this->dbuser, $this->dbpass);
  //     $dbConnection->exec("set names utf8");
  //     $dbConnection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  //     return $dbConnection;
  // }

  private $dbhost = '127.0.0.1';
  private $dbuser = 'phpmyadmin';
  private $dbpass = 'Phpmy@dmin1';
  private $dbname = 'sigep';
  public function conectar()
  {
    $mysql_connect_str = "mysql:host=$this->dbhost;dbname=$this->dbname";
    $dbConnection      = new PDO($mysql_connect_str, $this->dbuser, $this->dbpass);
    $dbConnection->exec("set names utf8");
    $dbConnection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    return $dbConnection;
  }
}
