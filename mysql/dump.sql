-- MySQL dump 10.13  Distrib 8.0.30, for Linux (x86_64)
--
-- Host: localhost    Database: esufrn_site
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_interface_theme`
--

DROP TABLE IF EXISTS `admin_interface_theme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_interface_theme` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `title` varchar(50) NOT NULL,
  `title_visible` tinyint(1) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `logo_visible` tinyint(1) NOT NULL,
  `css_header_background_color` varchar(10) NOT NULL,
  `title_color` varchar(10) NOT NULL,
  `css_header_text_color` varchar(10) NOT NULL,
  `css_header_link_color` varchar(10) NOT NULL,
  `css_header_link_hover_color` varchar(10) NOT NULL,
  `css_module_background_color` varchar(10) NOT NULL,
  `css_module_text_color` varchar(10) NOT NULL,
  `css_module_link_color` varchar(10) NOT NULL,
  `css_module_link_hover_color` varchar(10) NOT NULL,
  `css_module_rounded_corners` tinyint(1) NOT NULL,
  `css_generic_link_color` varchar(10) NOT NULL,
  `css_generic_link_hover_color` varchar(10) NOT NULL,
  `css_save_button_background_color` varchar(10) NOT NULL,
  `css_save_button_background_hover_color` varchar(10) NOT NULL,
  `css_save_button_text_color` varchar(10) NOT NULL,
  `css_delete_button_background_color` varchar(10) NOT NULL,
  `css_delete_button_background_hover_color` varchar(10) NOT NULL,
  `css_delete_button_text_color` varchar(10) NOT NULL,
  `list_filter_dropdown` tinyint(1) NOT NULL,
  `related_modal_active` tinyint(1) NOT NULL,
  `related_modal_background_color` varchar(10) NOT NULL,
  `related_modal_rounded_corners` tinyint(1) NOT NULL,
  `logo_color` varchar(10) NOT NULL,
  `recent_actions_visible` tinyint(1) NOT NULL,
  `favicon` varchar(100) NOT NULL,
  `related_modal_background_opacity` varchar(5) NOT NULL,
  `env_name` varchar(50) NOT NULL,
  `env_visible_in_header` tinyint(1) NOT NULL,
  `env_color` varchar(10) NOT NULL,
  `env_visible_in_favicon` tinyint(1) NOT NULL,
  `related_modal_close_button_visible` tinyint(1) NOT NULL,
  `language_chooser_active` tinyint(1) NOT NULL,
  `language_chooser_display` varchar(10) NOT NULL,
  `list_filter_sticky` tinyint(1) NOT NULL,
  `form_pagination_sticky` tinyint(1) NOT NULL,
  `form_submit_sticky` tinyint(1) NOT NULL,
  `css_module_background_selected_color` varchar(10) NOT NULL,
  `css_module_link_selected_color` varchar(10) NOT NULL,
  `logo_max_height` smallint unsigned NOT NULL,
  `logo_max_width` smallint unsigned NOT NULL,
  `foldable_apps` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_interface_theme_name_30bda70f_uniq` (`name`),
  CONSTRAINT `admin_interface_theme_chk_1` CHECK ((`logo_max_height` >= 0)),
  CONSTRAINT `admin_interface_theme_chk_2` CHECK ((`logo_max_width` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_interface_theme`
--

LOCK TABLES `admin_interface_theme` WRITE;
/*!40000 ALTER TABLE `admin_interface_theme` DISABLE KEYS */;
INSERT INTO `admin_interface_theme` VALUES (1,'Django',1,'Django administration',1,'',1,'#0C4B33','#F5DD5D','#44B78B','#FFFFFF','#C9F0DD','#44B78B','#FFFFFF','#FFFFFF','#C9F0DD',1,'#0C3C26','#156641','#0C4B33','#0C3C26','#FFFFFF','#BA2121','#A41515','#FFFFFF',1,1,'#000000',1,'#FFFFFF',1,'','0.3','',1,'#E74C3C',1,1,1,'code',1,0,0,'#FFFFCC','#FFFFFF',100,400,1);
/*!40000 ALTER TABLE `admin_interface_theme` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add Alerta',1,'add_alerta'),(2,'Can change Alerta',1,'change_alerta'),(3,'Can delete Alerta',1,'delete_alerta'),(4,'Can view Alerta',1,'view_alerta'),(5,'Can add Arquivo',2,'add_arquivos'),(6,'Can change Arquivo',2,'change_arquivos'),(7,'Can delete Arquivo',2,'delete_arquivos'),(8,'Can view Arquivo',2,'view_arquivos'),(9,'Can add Notícia',3,'add_blog'),(10,'Can change Notícia',3,'change_blog'),(11,'Can delete Notícia',3,'delete_blog'),(12,'Can view Notícia',3,'view_blog'),(13,'Can add Depoimento',4,'add_depoimentos'),(14,'Can change Depoimento',4,'change_depoimentos'),(15,'Can delete Depoimento',4,'delete_depoimentos'),(16,'Can view Depoimento',4,'view_depoimentos'),(17,'Can add Documento',5,'add_documentos'),(18,'Can change Documento',5,'change_documentos'),(19,'Can delete Documento',5,'delete_documentos'),(20,'Can view Documento',5,'view_documentos'),(21,'Can add Equipe',6,'add_equipe'),(22,'Can change Equipe',6,'change_equipe'),(23,'Can delete Equipe',6,'delete_equipe'),(24,'Can view Equipe',6,'view_equipe'),(25,'Can add Mensagem',7,'add_mensagem'),(26,'Can change Mensagem',7,'change_mensagem'),(27,'Can delete Mensagem',7,'delete_mensagem'),(28,'Can view Mensagem',7,'view_mensagem'),(29,'Can add Newsletter',8,'add_newsletter'),(30,'Can change Newsletter',8,'change_newsletter'),(31,'Can delete Newsletter',8,'delete_newsletter'),(32,'Can view Newsletter',8,'view_newsletter'),(33,'Can add Página',9,'add_paginas'),(34,'Can change Página',9,'change_paginas'),(35,'Can delete Página',9,'delete_paginas'),(36,'Can view Página',9,'view_paginas'),(37,'Can add Publicação',10,'add_publicacoes'),(38,'Can change Publicação',10,'change_publicacoes'),(39,'Can delete Publicação',10,'delete_publicacoes'),(40,'Can view Publicação',10,'view_publicacoes'),(41,'Can add Anexo',11,'add_blogattachments'),(42,'Can change Anexo',11,'change_blogattachments'),(43,'Can delete Anexo',11,'delete_blogattachments'),(44,'Can view Anexo',11,'view_blogattachments'),(45,'Can add Item do menu',12,'add_dashboarditens'),(46,'Can change Item do menu',12,'change_dashboarditens'),(47,'Can delete Item do menu',12,'delete_dashboarditens'),(48,'Can view Item do menu',12,'view_dashboarditens'),(49,'Can add Subitem do menu',13,'add_dashboardsubitens'),(50,'Can change Subitem do menu',13,'change_dashboardsubitens'),(51,'Can delete Subitem do menu',13,'delete_dashboardsubitens'),(52,'Can view Subitem do menu',13,'view_dashboardsubitens'),(53,'Can add Sala',14,'add_classroom'),(54,'Can change Sala',14,'change_classroom'),(55,'Can delete Sala',14,'delete_classroom'),(56,'Can view Sala',14,'view_classroom'),(57,'Can add material reservation',15,'add_materialreservation'),(58,'Can change material reservation',15,'change_materialreservation'),(59,'Can delete material reservation',15,'delete_materialreservation'),(60,'Can view material reservation',15,'view_materialreservation'),(61,'Can add Reserva de período',16,'add_periodreserve'),(62,'Can change Reserva de período',16,'change_periodreserve'),(63,'Can delete Reserva de período',16,'delete_periodreserve'),(64,'Can view Reserva de período',16,'view_periodreserve'),(65,'Can add Responsável',17,'add_userclassroom'),(66,'Can change Responsável',17,'change_userclassroom'),(67,'Can delete Responsável',17,'delete_userclassroom'),(68,'Can view Responsável',17,'view_userclassroom'),(69,'Can add Reserva pontual',18,'add_reserve'),(70,'Can change Reserva pontual',18,'change_reserve'),(71,'Can delete Reserva pontual',18,'delete_reserve'),(72,'Can view Reserva pontual',18,'view_reserve'),(73,'Can add Dia da reserva',19,'add_periodreserveday'),(74,'Can change Dia da reserva',19,'change_periodreserveday'),(75,'Can delete Dia da reserva',19,'delete_periodreserveday'),(76,'Can view Dia da reserva',19,'view_periodreserveday'),(77,'Can add Chamado',20,'add_chamado'),(78,'Can change Chamado',20,'change_chamado'),(79,'Can delete Chamado',20,'delete_chamado'),(80,'Can view Chamado',20,'view_chamado'),(81,'Can add emprestimo',21,'add_emprestimo'),(82,'Can change emprestimo',21,'change_emprestimo'),(83,'Can delete emprestimo',21,'delete_emprestimo'),(84,'Can view emprestimo',21,'view_emprestimo'),(85,'Can add patrimonio',22,'add_patrimonio'),(86,'Can change patrimonio',22,'change_patrimonio'),(87,'Can delete patrimonio',22,'delete_patrimonio'),(88,'Can view patrimonio',22,'view_patrimonio'),(89,'Can add Equipamento',23,'add_patrimonioemprestimo'),(90,'Can change Equipamento',23,'change_patrimonioemprestimo'),(91,'Can delete Equipamento',23,'delete_patrimonioemprestimo'),(92,'Can view Equipamento',23,'view_patrimonioemprestimo'),(93,'Can add Máquina',24,'add_maquina'),(94,'Can change Máquina',24,'change_maquina'),(95,'Can delete Máquina',24,'delete_maquina'),(96,'Can view Máquina',24,'view_maquina'),(97,'Can add Menu nível 1',25,'add_itens'),(98,'Can change Menu nível 1',25,'change_itens'),(99,'Can delete Menu nível 1',25,'delete_itens'),(100,'Can view Menu nível 1',25,'view_itens'),(101,'Can add Menu nível 2',26,'add_subitens'),(102,'Can change Menu nível 2',26,'change_subitens'),(103,'Can delete Menu nível 2',26,'delete_subitens'),(104,'Can view Menu nível 2',26,'view_subitens'),(105,'Can add Menu nível 3',27,'add_subsubitens'),(106,'Can change Menu nível 3',27,'change_subsubitens'),(107,'Can delete Menu nível 3',27,'delete_subsubitens'),(108,'Can view Menu nível 3',27,'view_subsubitens'),(109,'Can add Theme',28,'add_theme'),(110,'Can change Theme',28,'change_theme'),(111,'Can delete Theme',28,'delete_theme'),(112,'Can view Theme',28,'view_theme'),(113,'Can add log entry',29,'add_logentry'),(114,'Can change log entry',29,'change_logentry'),(115,'Can delete log entry',29,'delete_logentry'),(116,'Can view log entry',29,'view_logentry'),(117,'Can add permission',30,'add_permission'),(118,'Can change permission',30,'change_permission'),(119,'Can delete permission',30,'delete_permission'),(120,'Can view permission',30,'view_permission'),(121,'Can add group',31,'add_group'),(122,'Can change group',31,'change_group'),(123,'Can delete group',31,'delete_group'),(124,'Can view group',31,'view_group'),(125,'Can add user',32,'add_user'),(126,'Can change user',32,'change_user'),(127,'Can delete user',32,'delete_user'),(128,'Can view user',32,'view_user'),(129,'Can add content type',33,'add_contenttype'),(130,'Can change content type',33,'change_contenttype'),(131,'Can delete content type',33,'delete_contenttype'),(132,'Can view content type',33,'view_contenttype'),(133,'Can add session',34,'add_session'),(134,'Can change session',34,'change_session'),(135,'Can delete session',34,'delete_session'),(136,'Can view session',34,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chamado_chamado`
--

DROP TABLE IF EXISTS `chamado_chamado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chamado_chamado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` varchar(300) DEFAULT NULL,
  `requester` varchar(50) NOT NULL,
  `course` varchar(100) NOT NULL,
  `contact` varchar(50) DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `solved_at` datetime(6) DEFAULT NULL,
  `lastModified` datetime(6) NOT NULL,
  `obs` longtext,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chamado_chamado`
--

LOCK TABLES `chamado_chamado` WRITE;
/*!40000 ALTER TABLE `chamado_chamado` DISABLE KEYS */;
/*!40000 ALTER TABLE `chamado_chamado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_dashboarditens`
--

DROP TABLE IF EXISTS `dashboard_dashboarditens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_dashboarditens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `link` varchar(255) NOT NULL,
  `order` int NOT NULL,
  `decoration` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_dashboarditens`
--

LOCK TABLES `dashboard_dashboarditens` WRITE;
/*!40000 ALTER TABLE `dashboard_dashboarditens` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_dashboarditens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_dashboardsubitens`
--

DROP TABLE IF EXISTS `dashboard_dashboardsubitens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_dashboardsubitens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `related_name` varchar(50) NOT NULL,
  `link` varchar(255) NOT NULL,
  `order` int NOT NULL,
  `decoration` varchar(100) DEFAULT NULL,
  `aditional` longtext,
  `menu_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dashboard_dashboards_menu_id_b0fc8003_fk_dashboard` (`menu_id`),
  CONSTRAINT `dashboard_dashboards_menu_id_b0fc8003_fk_dashboard` FOREIGN KEY (`menu_id`) REFERENCES `dashboard_dashboarditens` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_dashboardsubitens`
--

LOCK TABLES `dashboard_dashboardsubitens` WRITE;
/*!40000 ALTER TABLE `dashboard_dashboardsubitens` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_dashboardsubitens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (29,'admin','logentry'),(28,'admin_interface','theme'),(31,'auth','group'),(30,'auth','permission'),(32,'auth','user'),(20,'chamado','chamado'),(33,'contenttypes','contenttype'),(12,'dashboard','dashboarditens'),(13,'dashboard','dashboardsubitens'),(21,'inventario','emprestimo'),(24,'inventario','maquina'),(22,'inventario','patrimonio'),(23,'inventario','patrimonioemprestimo'),(25,'menu','itens'),(26,'menu','subitens'),(27,'menu','subsubitens'),(1,'principal','alerta'),(2,'principal','arquivos'),(3,'principal','blog'),(11,'principal','blogattachments'),(4,'principal','depoimentos'),(5,'principal','documentos'),(6,'principal','equipe'),(7,'principal','mensagem'),(8,'principal','newsletter'),(9,'principal','paginas'),(10,'principal','publicacoes'),(14,'reserva','classroom'),(15,'reserva','materialreservation'),(16,'reserva','periodreserve'),(19,'reserva','periodreserveday'),(18,'reserva','reserve'),(17,'reserva','userclassroom'),(34,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-09-20 22:43:06.227055'),(2,'auth','0001_initial','2022-09-20 22:43:06.942092'),(3,'admin','0001_initial','2022-09-20 22:43:07.094414'),(4,'admin','0002_logentry_remove_auto_add','2022-09-20 22:43:07.105391'),(5,'admin','0003_logentry_add_action_flag_choices','2022-09-20 22:43:07.116149'),(6,'admin_interface','0001_initial','2022-09-20 22:43:07.144758'),(7,'admin_interface','0002_add_related_modal','2022-09-20 22:43:07.286970'),(8,'admin_interface','0003_add_logo_color','2022-09-20 22:43:07.332821'),(9,'admin_interface','0004_rename_title_color','2022-09-20 22:43:07.361330'),(10,'admin_interface','0005_add_recent_actions_visible','2022-09-20 22:43:07.398834'),(11,'admin_interface','0006_bytes_to_str','2022-09-20 22:43:07.471313'),(12,'admin_interface','0007_add_favicon','2022-09-20 22:43:07.506803'),(13,'admin_interface','0008_change_related_modal_background_opacity_type','2022-09-20 22:43:07.561288'),(14,'admin_interface','0009_add_enviroment','2022-09-20 22:43:07.629278'),(15,'admin_interface','0010_add_localization','2022-09-20 22:43:07.649708'),(16,'admin_interface','0011_add_environment_options','2022-09-20 22:43:07.771744'),(17,'admin_interface','0012_update_verbose_names','2022-09-20 22:43:07.785130'),(18,'admin_interface','0013_add_related_modal_close_button','2022-09-20 22:43:07.867140'),(19,'admin_interface','0014_name_unique','2022-09-20 22:43:07.913730'),(20,'admin_interface','0015_add_language_chooser_active','2022-09-20 22:43:07.966755'),(21,'admin_interface','0016_add_language_chooser_display','2022-09-20 22:43:08.008353'),(22,'admin_interface','0017_change_list_filter_dropdown','2022-09-20 22:43:08.015548'),(23,'admin_interface','0018_theme_list_filter_sticky','2022-09-20 22:43:08.058627'),(24,'admin_interface','0019_add_form_sticky','2022-09-20 22:43:08.135657'),(25,'admin_interface','0020_module_selected_colors','2022-09-20 22:43:08.223901'),(26,'admin_interface','0021_file_extension_validator','2022-09-20 22:43:08.234303'),(27,'admin_interface','0022_add_logo_max_width_and_height','2022-09-20 22:43:08.386102'),(28,'admin_interface','0023_theme_foldable_apps','2022-09-20 22:43:08.440707'),(29,'admin_interface','0024_remove_theme_css','2022-09-20 22:43:08.474190'),(30,'contenttypes','0002_remove_content_type_name','2022-09-20 22:43:08.570935'),(31,'auth','0002_alter_permission_name_max_length','2022-09-20 22:43:08.643630'),(32,'auth','0003_alter_user_email_max_length','2022-09-20 22:43:08.677223'),(33,'auth','0004_alter_user_username_opts','2022-09-20 22:43:08.693374'),(34,'auth','0005_alter_user_last_login_null','2022-09-20 22:43:08.755683'),(35,'auth','0006_require_contenttypes_0002','2022-09-20 22:43:08.762391'),(36,'auth','0007_alter_validators_add_error_messages','2022-09-20 22:43:08.776644'),(37,'auth','0008_alter_user_username_max_length','2022-09-20 22:43:08.847387'),(38,'auth','0009_alter_user_last_name_max_length','2022-09-20 22:43:08.914781'),(39,'auth','0010_alter_group_name_max_length','2022-09-20 22:43:08.959609'),(40,'auth','0011_update_proxy_permissions','2022-09-20 22:43:08.973141'),(41,'auth','0012_alter_user_first_name_max_length','2022-09-20 22:43:09.033345'),(42,'chamado','0001_initial','2022-09-20 22:43:09.059951'),(43,'dashboard','0001_initial','2022-09-20 22:43:10.796254'),(44,'reserva','0001_initial','2022-09-20 22:43:11.392832'),(45,'inventario','0001_initial','2022-09-20 22:43:11.829621'),(46,'menu','0001_initial','2022-09-20 22:43:12.067649'),(47,'principal','0001_initial','2022-09-20 22:43:12.634847'),(48,'sessions','0001_initial','2022-09-20 22:43:12.693261');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_emprestimo`
--

DROP TABLE IF EXISTS `inventario_emprestimo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_emprestimo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `obs` longtext,
  `borrow_date` datetime(6) NOT NULL,
  `return_date` datetime(6) DEFAULT NULL,
  `status` varchar(1) NOT NULL,
  `classroom_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_emprestim_classroom_id_9e4423cb_fk_reserva_c` (`classroom_id`),
  CONSTRAINT `inventario_emprestim_classroom_id_9e4423cb_fk_reserva_c` FOREIGN KEY (`classroom_id`) REFERENCES `reserva_classroom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_emprestimo`
--

LOCK TABLES `inventario_emprestimo` WRITE;
/*!40000 ALTER TABLE `inventario_emprestimo` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventario_emprestimo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_maquina`
--

DROP TABLE IF EXISTS `inventario_maquina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_maquina` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ram` int DEFAULT NULL,
  `hdd` int DEFAULT NULL,
  `status` varchar(1) NOT NULL,
  `obs` longtext,
  `patrimony_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_maquina_patrimony_id_8ba6e82a_fk_inventari` (`patrimony_id`),
  CONSTRAINT `inventario_maquina_patrimony_id_8ba6e82a_fk_inventari` FOREIGN KEY (`patrimony_id`) REFERENCES `inventario_patrimonio` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_maquina`
--

LOCK TABLES `inventario_maquina` WRITE;
/*!40000 ALTER TABLE `inventario_maquina` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventario_maquina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_patrimonio`
--

DROP TABLE IF EXISTS `inventario_patrimonio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_patrimonio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `model` varchar(64) NOT NULL,
  `dmp` varchar(64) DEFAULT NULL,
  `category` varchar(1) NOT NULL,
  `status` varchar(1) NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_patrimonio`
--

LOCK TABLES `inventario_patrimonio` WRITE;
/*!40000 ALTER TABLE `inventario_patrimonio` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventario_patrimonio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_patrimonioemprestimo`
--

DROP TABLE IF EXISTS `inventario_patrimonioemprestimo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_patrimonioemprestimo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int NOT NULL,
  `loan_id` bigint NOT NULL,
  `patrimony_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_patrimoni_loan_id_314aae86_fk_inventari` (`loan_id`),
  KEY `inventario_patrimoni_patrimony_id_6b0b8fdf_fk_inventari` (`patrimony_id`),
  CONSTRAINT `inventario_patrimoni_loan_id_314aae86_fk_inventari` FOREIGN KEY (`loan_id`) REFERENCES `inventario_emprestimo` (`id`),
  CONSTRAINT `inventario_patrimoni_patrimony_id_6b0b8fdf_fk_inventari` FOREIGN KEY (`patrimony_id`) REFERENCES `inventario_patrimonio` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_patrimonioemprestimo`
--

LOCK TABLES `inventario_patrimonioemprestimo` WRITE;
/*!40000 ALTER TABLE `inventario_patrimonioemprestimo` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventario_patrimonioemprestimo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_itens`
--

DROP TABLE IF EXISTS `menu_itens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_itens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `action_type` varchar(100) NOT NULL,
  `footer` tinyint(1) NOT NULL,
  `link` varchar(255) NOT NULL,
  `order` int NOT NULL,
  `decoration` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_itens`
--

LOCK TABLES `menu_itens` WRITE;
/*!40000 ALTER TABLE `menu_itens` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_itens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_subitens`
--

DROP TABLE IF EXISTS `menu_subitens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_subitens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `action_type` varchar(100) NOT NULL,
  `link` varchar(255) NOT NULL,
  `order` int NOT NULL,
  `decoration` varchar(100) DEFAULT NULL,
  `menu_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_subitens_menu_id_e08ea10f_fk_menu_itens_id` (`menu_id`),
  CONSTRAINT `menu_subitens_menu_id_e08ea10f_fk_menu_itens_id` FOREIGN KEY (`menu_id`) REFERENCES `menu_itens` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_subitens`
--

LOCK TABLES `menu_subitens` WRITE;
/*!40000 ALTER TABLE `menu_subitens` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_subitens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_subsubitens`
--

DROP TABLE IF EXISTS `menu_subsubitens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_subsubitens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `link` varchar(255) NOT NULL,
  `order` int NOT NULL,
  `decoration` varchar(100) DEFAULT NULL,
  `submenu_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_subsubitens_submenu_id_9f167e74_fk_menu_subitens_id` (`submenu_id`),
  CONSTRAINT `menu_subsubitens_submenu_id_9f167e74_fk_menu_subitens_id` FOREIGN KEY (`submenu_id`) REFERENCES `menu_subitens` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_subsubitens`
--

LOCK TABLES `menu_subsubitens` WRITE;
/*!40000 ALTER TABLE `menu_subsubitens` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_subsubitens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_alerta`
--

DROP TABLE IF EXISTS `principal_alerta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_alerta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` longtext NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_alerta`
--

LOCK TABLES `principal_alerta` WRITE;
/*!40000 ALTER TABLE `principal_alerta` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_alerta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_arquivos`
--

DROP TABLE IF EXISTS `principal_arquivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_arquivos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `file` varchar(255) DEFAULT NULL,
  `published_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_arquivos`
--

LOCK TABLES `principal_arquivos` WRITE;
/*!40000 ALTER TABLE `principal_arquivos` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_arquivos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_blog`
--

DROP TABLE IF EXISTS `principal_blog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_blog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(400) NOT NULL,
  `subtitle` varchar(500) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `news` longtext NOT NULL,
  `isImportant` tinyint(1) NOT NULL,
  `author` varchar(50) NOT NULL,
  `category` varchar(8) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `published_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `principal_blog_slug_903a3940` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_blog`
--

LOCK TABLES `principal_blog` WRITE;
/*!40000 ALTER TABLE `principal_blog` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_blog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_blogattachments`
--

DROP TABLE IF EXISTS `principal_blogattachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_blogattachments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `blog_id` int NOT NULL,
  `file_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `principal_blogattachments_blog_id_b022a3b6_fk_principal_blog_id` (`blog_id`),
  KEY `principal_blogattach_file_id_617b6c41_fk_principal` (`file_id`),
  CONSTRAINT `principal_blogattach_file_id_617b6c41_fk_principal` FOREIGN KEY (`file_id`) REFERENCES `principal_arquivos` (`id`),
  CONSTRAINT `principal_blogattachments_blog_id_b022a3b6_fk_principal_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `principal_blog` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_blogattachments`
--

LOCK TABLES `principal_blogattachments` WRITE;
/*!40000 ALTER TABLE `principal_blogattachments` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_blogattachments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_depoimentos`
--

DROP TABLE IF EXISTS `principal_depoimentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_depoimentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `occupation` varchar(100) NOT NULL,
  `testimonial` varchar(100) NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_depoimentos`
--

LOCK TABLES `principal_depoimentos` WRITE;
/*!40000 ALTER TABLE `principal_depoimentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_depoimentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_documentos`
--

DROP TABLE IF EXISTS `principal_documentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_documentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `authors` varchar(250) DEFAULT NULL,
  `category` varchar(32) NOT NULL,
  `document_type` varchar(100) NOT NULL,
  `file` varchar(255) NOT NULL,
  `link` varchar(1024) NOT NULL,
  `date` date DEFAULT NULL,
  `published_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_documentos`
--

LOCK TABLES `principal_documentos` WRITE;
/*!40000 ALTER TABLE `principal_documentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_documentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_equipe`
--

DROP TABLE IF EXISTS `principal_equipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_equipe` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `photo` varchar(100) NOT NULL,
  `kind` varchar(8) NOT NULL,
  `sigaa` varchar(300) NOT NULL,
  `cv` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_equipe`
--

LOCK TABLES `principal_equipe` WRITE;
/*!40000 ALTER TABLE `principal_equipe` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_equipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_mensagem`
--

DROP TABLE IF EXISTS `principal_mensagem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_mensagem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `contact` varchar(100) NOT NULL,
  `message` varchar(500) NOT NULL,
  `sent_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_mensagem`
--

LOCK TABLES `principal_mensagem` WRITE;
/*!40000 ALTER TABLE `principal_mensagem` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_mensagem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_newsletter`
--

DROP TABLE IF EXISTS `principal_newsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_newsletter` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name_person` varchar(110) NOT NULL,
  `email` varchar(110) NOT NULL,
  `category` varchar(21) NOT NULL,
  `subscribed_at` datetime(6) DEFAULT NULL,
  `last_updated` datetime(6) DEFAULT NULL,
  `consent` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_newsletter`
--

LOCK TABLES `principal_newsletter` WRITE;
/*!40000 ALTER TABLE `principal_newsletter` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_newsletter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_paginas`
--

DROP TABLE IF EXISTS `principal_paginas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_paginas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `path` varchar(250) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_paginas`
--

LOCK TABLES `principal_paginas` WRITE;
/*!40000 ALTER TABLE `principal_paginas` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_paginas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal_publicacoes`
--

DROP TABLE IF EXISTS `principal_publicacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal_publicacoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `category` varchar(3) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal_publicacoes`
--

LOCK TABLES `principal_publicacoes` WRITE;
/*!40000 ALTER TABLE `principal_publicacoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal_publicacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva_classroom`
--

DROP TABLE IF EXISTS `reserva_classroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_classroom` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `acronym` varchar(16) DEFAULT NULL,
  `type` varchar(3) NOT NULL,
  `number` varchar(10) NOT NULL,
  `days_required` int NOT NULL,
  `justification_required` tinyint(1) NOT NULL,
  `floor` varchar(25) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_classroom`
--

LOCK TABLES `reserva_classroom` WRITE;
/*!40000 ALTER TABLE `reserva_classroom` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva_classroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva_materialreservation`
--

DROP TABLE IF EXISTS `reserva_materialreservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_materialreservation` (
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_materialreservation`
--

LOCK TABLES `reserva_materialreservation` WRITE;
/*!40000 ALTER TABLE `reserva_materialreservation` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva_materialreservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva_periodreserve`
--

DROP TABLE IF EXISTS `reserva_periodreserve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_periodreserve` (
  `id` int NOT NULL AUTO_INCREMENT,
  `status` varchar(1) NOT NULL,
  `date_begin` date NOT NULL,
  `date_end` date NOT NULL,
  `workload` int DEFAULT NULL,
  `weekdays` varchar(14) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `refresh_at` datetime(6) NOT NULL,
  `classname` varchar(100) NOT NULL,
  `classcode` varchar(16) DEFAULT NULL,
  `course` varchar(8) DEFAULT NULL,
  `period` varchar(8) NOT NULL,
  `class_period` varchar(8) NOT NULL,
  `shift` varchar(6) NOT NULL,
  `requester` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(16) NOT NULL,
  `equipment` varchar(200) DEFAULT NULL,
  `obs` longtext,
  `classroom_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reserva_periodreserv_classroom_id_64499cfc_fk_reserva_c` (`classroom_id`),
  CONSTRAINT `reserva_periodreserv_classroom_id_64499cfc_fk_reserva_c` FOREIGN KEY (`classroom_id`) REFERENCES `reserva_classroom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_periodreserve`
--

LOCK TABLES `reserva_periodreserve` WRITE;
/*!40000 ALTER TABLE `reserva_periodreserve` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva_periodreserve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva_periodreserveday`
--

DROP TABLE IF EXISTS `reserva_periodreserveday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_periodreserveday` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `active` tinyint(1) NOT NULL,
  `shift` varchar(1) NOT NULL,
  `period_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reserva_periodreserv_period_id_89cc5122_fk_reserva_p` (`period_id`),
  CONSTRAINT `reserva_periodreserv_period_id_89cc5122_fk_reserva_p` FOREIGN KEY (`period_id`) REFERENCES `reserva_periodreserve` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_periodreserveday`
--

LOCK TABLES `reserva_periodreserveday` WRITE;
/*!40000 ALTER TABLE `reserva_periodreserveday` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva_periodreserveday` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva_reserve`
--

DROP TABLE IF EXISTS `reserva_reserve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_reserve` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `refresh_at` datetime(6) NOT NULL,
  `event` varchar(100) DEFAULT NULL,
  `shift` varchar(1) NOT NULL,
  `cause` longtext,
  `equipment` varchar(200) DEFAULT NULL,
  `requester` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(16) DEFAULT NULL,
  `status` varchar(1) NOT NULL,
  `obs` longtext,
  `email_response` longtext,
  `declare` tinyint(1) NOT NULL,
  `admin_created` tinyint(1) NOT NULL,
  `classroom_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reserva_reserve_classroom_id_eb9cf55a_fk_reserva_classroom_id` (`classroom_id`),
  CONSTRAINT `reserva_reserve_classroom_id_eb9cf55a_fk_reserva_classroom_id` FOREIGN KEY (`classroom_id`) REFERENCES `reserva_classroom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_reserve`
--

LOCK TABLES `reserva_reserve` WRITE;
/*!40000 ALTER TABLE `reserva_reserve` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva_reserve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva_userclassroom`
--

DROP TABLE IF EXISTS `reserva_userclassroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_userclassroom` (
  `id` int NOT NULL AUTO_INCREMENT,
  `classroom_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reserva_userclassroo_classroom_id_51092bec_fk_reserva_c` (`classroom_id`),
  KEY `reserva_userclassroom_user_id_7a51c7a9_fk_auth_user_id` (`user_id`),
  CONSTRAINT `reserva_userclassroo_classroom_id_51092bec_fk_reserva_c` FOREIGN KEY (`classroom_id`) REFERENCES `reserva_classroom` (`id`),
  CONSTRAINT `reserva_userclassroom_user_id_7a51c7a9_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_userclassroom`
--

LOCK TABLES `reserva_userclassroom` WRITE;
/*!40000 ALTER TABLE `reserva_userclassroom` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva_userclassroom` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-20 22:45:18
