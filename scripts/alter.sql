-- MySQL Workbench Synchronization

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

ALTER TABLE `default_schema`.`auth_user`
CHANGE COLUMN `first_name` `first_name` VARCHAR(150) NOT NULL ;

ALTER TABLE `default_schema`.`chamado_chamado`
CHANGE COLUMN `solved_at` `solved_at` DATETIME NULL DEFAULT NULL AFTER `date`;

ALTER TABLE `default_schema`.`dashboard_dashboardsubitens`
CHANGE COLUMN `related_name` `related_name` VARCHAR(50) NOT NULL AFTER `name`,
CHANGE COLUMN `aditional` `aditional` LONGTEXT NULL DEFAULT NULL AFTER `decoration`;

ALTER TABLE `default_schema`.`menu_subitens`
CHANGE COLUMN `action_type` `action_type` VARCHAR(100) NOT NULL AFTER `name`;

ALTER TABLE `default_schema`.`principal_blog`
DROP COLUMN `event_date`;

ALTER TABLE `default_schema`.`principal_documentos`
CHANGE COLUMN `authors` `authors` VARCHAR(250) NULL DEFAULT NULL AFTER `name`,
CHANGE COLUMN `category` `category` VARCHAR(32) NOT NULL AFTER `authors`,
CHANGE COLUMN `date` `date` DATE NULL DEFAULT NULL AFTER `link`,
CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `default_schema`.`principal_newsletter`
CHANGE COLUMN `subscribed_at` `subscribed_at` DATETIME NULL DEFAULT NULL AFTER `category`,
CHANGE COLUMN `last_updated` `last_updated` DATETIME NULL DEFAULT NULL AFTER `subscribed_at`;

ALTER TABLE `default_schema`.`reserva_classroom`
CHANGE COLUMN `type` `type` VARCHAR(3) NOT NULL AFTER `acronym`,
CHANGE COLUMN `number` `number` VARCHAR(10) NOT NULL AFTER `type`,
CHANGE COLUMN `floor` `floor` VARCHAR(25) NOT NULL AFTER `justification_required`,
CHANGE COLUMN `days_required` `days_required` INT(11) NOT NULL ,
CHANGE COLUMN `justification_required` `justification_required` TINYINT(1) NOT NULL ;

ALTER TABLE `default_schema`.`reserva_periodreserve`
CHANGE COLUMN `status` `status` VARCHAR(1) NOT NULL AFTER `id`,
CHANGE COLUMN `workload` `workload` INT(11) NULL DEFAULT NULL AFTER `date_end`,
CHANGE COLUMN `weekdays` `weekdays` VARCHAR(14) NOT NULL AFTER `workload`,
CHANGE COLUMN `classcode` `classcode` VARCHAR(16) NULL DEFAULT NULL AFTER `classname`,
CHANGE COLUMN `course` `course` VARCHAR(8) NULL DEFAULT NULL AFTER `classcode`,
CHANGE COLUMN `period` `period` VARCHAR(8) NOT NULL AFTER `course`,
CHANGE COLUMN `class_period` `class_period` VARCHAR(8) NOT NULL AFTER `period`,
CHANGE COLUMN `obs` `obs` LONGTEXT NULL DEFAULT NULL AFTER `equipment`;

ALTER TABLE `default_schema`.`reserva_periodreserveday`
CHANGE COLUMN `period_id` `period_id` INT(11) NOT NULL AFTER `shift`;

ALTER TABLE `default_schema`.`reserva_reserve`
CHANGE COLUMN `cause` `cause` LONGTEXT NULL DEFAULT NULL AFTER `shift`,
CHANGE COLUMN `email_response` `email_response` LONGTEXT NULL DEFAULT NULL AFTER `obs`,
CHANGE COLUMN `classroom_id` `classroom_id` INT(11) NOT NULL AFTER `admin_created`,
CHANGE COLUMN `declare` `declare` TINYINT(1) NOT NULL ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
