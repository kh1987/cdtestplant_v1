-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: chengdu_test_plant_v1
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

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
  `id` bigint NOT NULL AUTO_INCREMENT,
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
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add 用户表',6,'add_users'),(22,'Can change 用户表',6,'change_users'),(23,'Can delete 用户表',6,'delete_users'),(24,'Can view 用户表',6,'view_users'),(25,'Can add 字典表',7,'add_dict'),(26,'Can change 字典表',7,'change_dict'),(27,'Can delete 字典表',7,'delete_dict'),(28,'Can view 字典表',7,'view_dict'),(29,'Can add 字典表item表',8,'add_dictitem'),(30,'Can change 字典表item表',8,'change_dictitem'),(31,'Can delete 字典表item表',8,'delete_dictitem'),(32,'Can view 字典表item表',8,'view_dictitem'),(33,'Can add 项目信息',9,'add_project'),(34,'Can change 项目信息',9,'change_project'),(35,'Can delete 项目信息',9,'delete_project'),(36,'Can view 项目信息',9,'view_project'),(37,'Can add 轮次信息',10,'add_round'),(38,'Can change 轮次信息',10,'change_round'),(39,'Can delete 轮次信息',10,'delete_round'),(40,'Can view 轮次信息',10,'view_round'),(41,'Can add 被测件信息',11,'add_dut'),(42,'Can change 被测件信息',11,'change_dut'),(43,'Can delete 被测件信息',11,'delete_dut'),(44,'Can view 被测件信息',11,'view_dut'),(45,'Can add 测试需求',12,'add_design'),(46,'Can change 测试需求',12,'change_design'),(47,'Can delete 测试需求',12,'delete_design'),(48,'Can view 测试需求',12,'view_design'),(49,'Can add 核心模型',13,'add_testdemand'),(50,'Can change 核心模型',13,'change_testdemand'),(51,'Can delete 核心模型',13,'delete_testdemand'),(52,'Can view 核心模型',13,'view_testdemand'),(53,'Can add 核心模型',14,'add_testdemandcontent'),(54,'Can change 核心模型',14,'change_testdemandcontent'),(55,'Can delete 核心模型',14,'delete_testdemandcontent'),(56,'Can view 核心模型',14,'view_testdemandcontent'),(57,'Can add 核心模型',15,'add_casestep'),(58,'Can change 核心模型',15,'change_casestep'),(59,'Can delete 核心模型',15,'delete_casestep'),(60,'Can view 核心模型',15,'view_casestep'),(61,'Can add 测试用例',16,'add_case'),(62,'Can change 测试用例',16,'change_case'),(63,'Can delete 测试用例',16,'delete_case'),(64,'Can view 测试用例',16,'view_case'),(65,'Can add 问题单',17,'add_problem'),(66,'Can change 问题单',17,'change_problem'),(67,'Can delete 问题单',17,'delete_problem'),(68,'Can view 问题单',17,'view_problem'),(69,'Can add 委托方、研制方、测试方信息',18,'add_contact'),(70,'Can change 委托方、研制方、测试方信息',18,'change_contact'),(71,'Can delete 委托方、研制方、测试方信息',18,'delete_contact'),(72,'Can view 委托方、研制方、测试方信息',18,'view_contact'),(73,'Can add 缩略语和行业词汇',19,'add_abbreviation'),(74,'Can change 缩略语和行业词汇',19,'change_abbreviation'),(75,'Can delete 缩略语和行业词汇',19,'delete_abbreviation'),(76,'Can view 缩略语和行业词汇',19,'view_abbreviation'),(77,'Can add 用户操作日志表',20,'add_operationlog'),(78,'Can change 用户操作日志表',20,'change_operationlog'),(79,'Can delete 用户操作日志表',20,'delete_operationlog'),(80,'Can view 用户操作日志表',20,'view_operationlog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_gongsi`
--

DROP TABLE IF EXISTS `contact_gongsi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_gongsi` (
  `key` int NOT NULL,
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `entrust_person` varchar(16) NOT NULL,
  `name` varchar(64) NOT NULL,
  `addr` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_gongsi`
--

LOCK TABLES `contact_gongsi` WRITE;
/*!40000 ALTER TABLE `contact_gongsi` DISABLE KEYS */;
INSERT INTO `contact_gongsi` VALUES (1,1,'这是一个公司或单位信息','2023-10-08','2023-08-17',1,'某个法人123','上海微小卫星工程中心','一个有效地址1'),(2,2,'123','2023-10-08','2023-08-17',1,'周冲个','上海翰讯通讯股份有限公司12','一个很好的地址a1'),(3,4,NULL,'2024-03-11','2024-03-11',1,'施敏华','中国科学院卫星软件测评中心','上海市海科路99号');
/*!40000 ALTER TABLE `contact_gongsi` ENABLE KEYS */;
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
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`),
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(7,'dict','dict'),(8,'dict','dictitem'),(19,'project','abbreviation'),(16,'project','case'),(15,'project','casestep'),(18,'project','contact'),(12,'project','design'),(11,'project','dut'),(17,'project','problem'),(9,'project','project'),(10,'project','round'),(13,'project','testdemand'),(14,'project','testdemandcontent'),(5,'sessions','session'),(20,'user','operationlog'),(6,'user','users');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-07-21 11:48:05.013484'),(2,'contenttypes','0002_remove_content_type_name','2023-07-21 11:48:05.071328'),(3,'auth','0001_initial','2023-07-21 11:48:05.270795'),(4,'auth','0002_alter_permission_name_max_length','2023-07-21 11:48:05.315675'),(5,'auth','0003_alter_user_email_max_length','2023-07-21 11:48:05.321659'),(6,'auth','0004_alter_user_username_opts','2023-07-21 11:48:05.329639'),(7,'auth','0005_alter_user_last_login_null','2023-07-21 11:48:05.334624'),(8,'auth','0006_require_contenttypes_0002','2023-07-21 11:48:05.337616'),(9,'auth','0007_alter_validators_add_error_messages','2023-07-21 11:48:05.344599'),(10,'auth','0008_alter_user_username_max_length','2023-07-21 11:48:05.350581'),(11,'auth','0009_alter_user_last_name_max_length','2023-07-21 11:48:05.357563'),(12,'auth','0010_alter_group_name_max_length','2023-07-21 11:48:05.371525'),(13,'auth','0011_update_proxy_permissions','2023-07-21 11:48:05.378507'),(14,'auth','0012_alter_user_first_name_max_length','2023-07-21 11:48:05.385488'),(15,'user','0001_initial','2023-07-21 11:48:05.614950'),(16,'admin','0001_initial','2023-07-21 11:48:05.756570'),(17,'admin','0002_logentry_remove_auto_add','2023-07-21 11:48:05.764549'),(18,'admin','0003_logentry_add_action_flag_choices','2023-07-21 11:48:05.772528'),(19,'sessions','0001_initial','2023-07-21 11:48:05.799456'),(20,'dict','0001_initial','2023-07-24 09:05:57.208781'),(21,'dict','0002_alter_dict_options_alter_dictitem_options','2023-07-25 02:59:56.263591'),(22,'project','0001_initial','2023-07-25 02:59:56.301490'),(23,'project','0002_round','2023-07-25 06:58:38.927891'),(24,'project','0003_alter_round_options_dut','2023-07-25 11:14:06.859830'),(25,'project','0004_design','2023-07-31 11:23:25.528561'),(26,'project','0005_testdemand_alter_design_demandtype_and_more','2023-08-01 11:48:56.871001'),(27,'project','0006_alter_testdemand_testtype','2023-08-02 06:48:35.295572'),(28,'project','0007_alter_testdemand_termination','2023-08-02 11:47:57.363631'),(29,'project','0008_case_casestep','2023-08-02 12:47:30.549759'),(30,'project','0009_problem','2023-08-03 08:16:30.843358'),(31,'project','0010_alter_project_plant_type','2023-08-16 00:45:12.299353'),(32,'dict','0003_alter_dict_status','2023-08-16 12:02:40.431541'),(33,'dict','0004_alter_dictitem_status','2023-08-17 05:19:44.425584'),(34,'dict','0005_alter_dictitem_status','2023-08-17 05:25:01.340956'),(35,'project','0011_remove_project_dev_ident_remove_project_dev_legal_and_more','2023-08-17 08:05:48.764221'),(36,'project','0012_contact','2023-08-17 08:52:30.858415'),(37,'project','0013_project_dev_unit_project_entrust_unit_and_more','2023-08-17 10:26:25.681058'),(38,'project','0014_dut_release_date_dut_release_union_dut_version','2023-08-21 09:18:24.014443'),(39,'project','0015_design_chapter','2023-08-21 10:30:52.790804'),(40,'dict','0006_dictitem_show_title','2023-08-23 10:27:40.862859'),(41,'dict','0007_alter_dictitem_show_title','2023-08-23 10:30:38.810490'),(42,'project','0016_alter_testdemand_testmethod','2023-08-24 06:01:13.027541'),(43,'project','0017_project_config_person_project_quality_person_and_more','2023-08-24 07:46:04.927197'),(44,'dict','0008_dictitem_doc_name_dictitem_ident_and_version_and_more','2023-10-07 02:13:12.463675'),(45,'dict','0009_remove_dictitem_ident_and_version','2023-10-07 02:44:58.077899'),(46,'project','0018_contact_addr','2023-10-08 10:04:01.415498'),(47,'project','0019_dut_ref','2024-02-20 08:48:48.017083'),(48,'project','0020_alter_dut_release_date','2024-02-20 09:19:58.564603'),(49,'project','0021_abbreviation','2024-02-27 02:55:02.115740'),(50,'project','0022_project_abbreviation','2024-02-27 05:34:50.549924'),(51,'project','0023_testdemand_otherdesign_alter_testdemand_design_and_more','2024-03-01 02:35:33.457576'),(52,'project','0024_remove_testdemand_otherdesign_testdemand_otherdesign','2024-03-01 02:40:02.610344'),(53,'project','0025_remove_problem_case_problem_case','2024-03-13 13:41:24.397927'),(54,'project','0026_case_isleaf','2024-03-13 14:25:05.046570'),(55,'project','0027_alter_problem_options_remove_problem_design_and_more','2024-03-13 14:43:40.394018'),(56,'project','0028_problem_project','2024-03-13 15:02:39.918544'),(57,'project','0029_project_soft_type','2024-03-21 09:57:53.980784'),(58,'project','0030_project_devplant_project_runtime','2024-03-21 11:14:40.072223'),(59,'project','0031_alter_project_devplant_alter_project_runtime','2024-03-21 11:15:14.219503'),(60,'project','0032_problem_solve','2024-03-27 14:37:20.566158'),(61,'user','0002_operationlog','2024-04-15 10:07:03.618210'),(62,'user','0003_remove_operationlog_update_datetime','2024-04-15 10:09:00.988266'),(63,'user','0004_remove_operationlog_table_name','2024-04-15 10:34:36.027955'),(64,'user','0005_alter_operationlog_user','2024-04-15 10:35:24.533202'),(65,'user','0006_alter_operationlog_operate_obj','2024-04-15 10:35:45.796603');
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
INSERT INTO `django_session` VALUES ('731p2bqujgdqncstooz97yn7c9jwi5vz','.eJytUk1zgyAU_CsZzokiomKOvfeYU81kgIeR1o8OhFPG_17QHNLUTJ1pLzzn7bL7HusVnbi7NCdnlTlpQHuUoO19T3D5ofoAwDvvz0Mkh_5itIgCJbqhNnodQLUvN-43gYbbxt9mqqYZiKJkQpSqwP4UUtYc6gKyFLOMlBhnrKSkLmSeKEwIFZJjmWKAEvIg2qneWa_1dq1QzztVof2mQgfvUqGt_9J-trlXc7Op-U5qI1s1g12Y0Ab4-_WqckVGmC85SQtfGMvZCj1n2hmLOXS6j8Oy02HjmcABDs85Hr3xhFEcpHGdWJhuxXLjdvPnhcZjgJWGgCYYk8dGsuDCBKdTkYkvGWUyeKZssi5o-tPTBk_baNXCjreX34NRkj5RmV5xJ4fzchrh_4vPZnCfz9O446xM43-WXgps1aKPodDHRjoe0fgFwnUxXA:1rc0SS:dxSxbOFy0CL7_WVwEylJaJh2suoN3QmKyY9HKP1Di00','2024-03-04 10:01:08.066384'),('oi2a8fqgd86lygjz51y0vvm9xa21b7l4','.eJytUk1zgyAU_CsZzokiomKOvfeYU81kgIeR1o8OhFPG_17QHNLUTJ1pLzzn7bL7HusVnbi7NCdnlTlpQHtE0Pa-J7j8UH0A4J335yGSQ38xWkSBEt1QG70OoNqXG_ebQMNt428zVdMMRFEyIUpVYH8KKWsOdQFZillGSowzVlJSFzJPFCaECsmxTDFACXkQ7VTvrNd6u1ao552q0H5ToYN3qdDWf2k_29yrudnUfCe1ka2awS5MaAP8_XpVuSIjzJecpIUvjOVshZ4z7YzFHDrdx2HZ6bDxTOAAh-ccj954wigO0rhOLEy3Yrlxu_nzQuMxwEpDQBOMyWMjWXBhgtOpyMSXjDIZPFM2WRc0_elpg6dttGphx9vL78EoSZ-oTK-4k8N5OY3w_8VnM7jP52nccVam8T9LLwW2atHHUOhjIx2PaPwCxjYxXQ:1qMojm:41Zsj8nb6bLW5bvd-G67qo0Awl3ZWnLHeldZbsEw6ME','2023-08-04 11:55:58.103511');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_log`
--

DROP TABLE IF EXISTS `operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `create_datetime` datetime(6) DEFAULT NULL,
  `operate_obj` varchar(256) NOT NULL,
  `operate_des` varchar(1024) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `operation_log_user_id_dab8694c` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_log`
--

LOCK TABLES `operation_log` WRITE;
/*!40000 ALTER TABLE `operation_log` DISABLE KEYS */;
INSERT INTO `operation_log` VALUES (158,'2024-04-15 10:37:44.072779','缩略语:阿萨德','新增',1),(159,'2024-04-15 10:38:22.546193','缩略语:阿萨德','删除',1),(160,'2024-04-15 13:13:22.636528','缩略语:asdasd','删除',1),(161,'2024-04-15 13:13:24.248076','缩略语:asdas','删除',1),(162,'2024-04-15 14:40:00.631582','项目R2233-一个正式的项目','修改',1),(163,'2024-04-15 14:40:46.317278','项目R2233-一个正式的项目','修改',1),(164,'2024-04-15 14:41:34.808968','项目R2233-一个正式的项目','修改',1),(165,'2024-04-15 14:41:53.118056','项目R2233-一个正式的项目','修改',1),(166,'2024-04-15 14:42:12.483971','项目R2233-一个正式的项目','修改',1),(167,'2024-04-15 14:43:23.374831','项目R2233-一个正式的项目','修改',1),(168,'2024-04-15 14:47:15.047989','项目R2233-一个正式的项目','修改',1),(169,'2024-04-15 14:47:20.422173','项目R2234-一个正式的项目','修改',1),(170,'2024-04-15 15:00:13.003858','项目R2231-测试文件移动','新增',1),(171,'2024-04-15 15:00:13.006850','第1轮次','新增',1),(172,'2024-04-15 15:00:36.143721','被测件:软件源代码','新增',1),(173,'2024-04-15 15:06:53.400621','被测件:软件源代码','删除',1),(174,'2024-04-15 15:06:53.402595','第1轮次','删除',1),(175,'2024-04-15 15:06:53.403628','项目R2231-测试文件移动','删除',1);
/*!40000 ALTER TABLE `operation_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_abbreviation`
--

DROP TABLE IF EXISTS `project_abbreviation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_abbreviation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `des` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_abbreviation`
--

LOCK TABLES `project_abbreviation` WRITE;
/*!40000 ALTER TABLE `project_abbreviation` DISABLE KEYS */;
INSERT INTO `project_abbreviation` VALUES (1,'UDP','User Datagram Protocol用户数据包协议'),(2,'TCP','Transmission Control Protocol传输控制协议'),(4,'HTML','Hyper Text Markup Language超文本标记语言'),(5,'HTTP','Hypertext Transfer Protocol超文本传输协议'),(41,'123','321'),(42,'321','321'),(43,'3412','3123');
/*!40000 ALTER TABLE `project_abbreviation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_case`
--

DROP TABLE IF EXISTS `project_case`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_case` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `ident` varchar(64) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `initialization` varchar(128) DEFAULT NULL,
  `premise` varchar(128) DEFAULT NULL,
  `summarize` varchar(256) DEFAULT NULL,
  `designPerson` varchar(16) DEFAULT NULL,
  `testPerson` varchar(16) DEFAULT NULL,
  `monitorPerson` varchar(16) DEFAULT NULL,
  `title` varchar(64) DEFAULT NULL,
  `key` varchar(64) DEFAULT NULL,
  `level` varchar(64) DEFAULT NULL,
  `design_id` bigint NOT NULL,
  `dut_id` bigint NOT NULL,
  `project_id` bigint NOT NULL,
  `round_id` bigint NOT NULL,
  `test_id` bigint NOT NULL,
  `isLeaf` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_case_design_id_409fd368` (`design_id`),
  KEY `project_case_dut_id_b3c95b5c` (`dut_id`),
  KEY `project_case_project_id_31efaa4f` (`project_id`),
  KEY `project_case_round_id_adcbbeb2` (`round_id`),
  KEY `project_case_test_id_9dedbb3e` (`test_id`)
) ENGINE=InnoDB AUTO_INCREMENT=248 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_case`
--

LOCK TABLES `project_case` WRITE;
/*!40000 ALTER TABLE `project_case` DISABLE KEYS */;
INSERT INTO `project_case` VALUES (23,NULL,'2024-03-13','2023-08-24',1,'RS422','123123','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','13212','翁上力','翁上力','翁上力','123123','0-0-0-0-0','4',14,39,6,13,25,1),(24,NULL,'2024-03-13','2024-03-11',1,'RS422','初始化功能测试用例','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','这是用例的综述，看看生成情况是否正确','李鑫','翁上力','王光宗','初始化功能测试用例','0-0-0-1-0','4',14,39,6,13,27,1),(25,NULL,'2024-03-13','2024-03-11',1,'RS422','测试项3下面的一个用例','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综素1111','王光宗','翁上力','无敌的小麦','测试项3下面的一个用例','0-0-0-2-0','4',14,39,6,13,28,1),(26,NULL,'2024-03-22','2024-03-11',1,'TST','测试用例A','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','测试用例综述A','翁上力','尧颖婷','李鑫','测试用例A','0-1-0-0-0','4',19,40,6,13,31,1),(27,NULL,'2024-03-22','2024-03-11',1,'TST','测试用例B','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述B','王小雷','王小雷','尧颖婷','测试用例B','0-1-0-0-1','4',19,40,6,13,31,1),(28,NULL,'2024-03-13','2024-03-11',1,'TST','测试用例C','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述C','翁上力','尧颖婷','李鑫','测试用例C','0-1-0-1-0','4',19,40,6,13,32,1),(29,NULL,'2024-03-13','2024-03-11',1,'CKTL','测试用例D','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','DDDD综述','翁上力','翁上力','王小雷','测试用例D','0-1-1-0-0','4',20,40,6,13,33,1),(30,NULL,'2024-03-13','2024-03-11',1,'CKTL','测试用例E','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述E','王光宗','李莉','陈鹏','测试用例E','0-1-1-1-0','4',20,40,6,13,34,1),(32,NULL,'2024-03-13','2024-03-13',1,'CKTL','看看空值情况测试','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述1','李莉','李莉','李莉','看看空值情况测试','0-1-1-0-1','4',20,40,6,13,33,1),(33,NULL,'2024-03-22','2024-03-22',1,'TST','测试文档审查问题','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','这是用例综述','翁上力','王小雷','王小雷','测试文档审查问题','0-1-0-2-0','4',19,40,6,13,36,1),(230,NULL,'2024-04-02','2024-04-02',1,'TST','测试用例A','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','测试用例综述A','翁上力','尧颖婷','李鑫','测试用例A','1-0-0-0-0','4',108,142,6,94,204,1),(231,NULL,'2024-04-02','2024-04-02',1,'TST','测试用例B','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述B','王小雷','王小雷','尧颖婷','测试用例B','1-0-0-0-1','4',108,142,6,94,204,1),(232,NULL,'2024-04-02','2024-04-02',1,'TST','测试用例C','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述C','翁上力','尧颖婷','李鑫','测试用例C','1-0-0-1-0','4',108,142,6,94,205,1),(233,NULL,'2024-04-02','2024-04-02',1,'TST','测试文档审查问题','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','这是用例综述','翁上力','王小雷','王小雷','测试文档审查问题','1-0-0-2-0','4',108,142,6,94,206,1),(234,NULL,'2024-04-02','2024-04-02',1,'CKTL','测试用例D','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','DDDD综述','翁上力','翁上力','王小雷','测试用例D','1-0-1-0-0','4',109,142,6,94,207,1),(235,NULL,'2024-04-02','2024-04-02',1,'CKTL','看看空值情况测试','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述1','李莉','李莉','李莉','看看空值情况测试','1-0-1-0-1','4',109,142,6,94,207,1),(236,NULL,'2024-04-02','2024-04-02',1,'CKTL','测试用例E','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述E','王光宗','李莉','陈鹏','测试用例E','1-0-1-1-0','4',109,142,6,94,208,1),(244,NULL,'2024-04-02','2024-04-02',1,'TST','测试用例A','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','测试用例综述A','翁上力','尧颖婷','李鑫','测试用例A','2-1-0-0-0','4',112,146,6,96,214,1),(245,NULL,'2024-04-02','2024-04-02',1,'TST','测试用例B','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述B','王小雷','王小雷','尧颖婷','测试用例B','2-1-0-0-1','4',112,146,6,96,214,1),(246,NULL,'2024-04-02','2024-04-02',1,'TST','测试用例C','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','综述C','翁上力','尧颖婷','李鑫','测试用例C','2-1-0-1-0','4',112,146,6,96,215,1),(247,NULL,'2024-04-02','2024-04-02',1,'TST','测试文档审查问题','软件正常启动，正常登录进软件','软件正常启动，各界面显示工作正常','这是用例综述','翁上力','王小雷','王小雷','测试文档审查问题','2-1-0-2-0','4',112,146,6,96,216,1);
/*!40000 ALTER TABLE `project_case` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_casestep`
--

DROP TABLE IF EXISTS `project_casestep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_casestep` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `operation` longtext,
  `expect` varchar(64) DEFAULT NULL,
  `result` longtext,
  `passed` varchar(8) DEFAULT NULL,
  `status` varchar(8) DEFAULT NULL,
  `case_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_casestep_case_id_d7d0bf55` (`case_id`)
) ENGINE=InnoDB AUTO_INCREMENT=283 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_casestep`
--

LOCK TABLES `project_casestep` WRITE;
/*!40000 ALTER TABLE `project_casestep` DISABLE KEYS */;
INSERT INTO `project_casestep` VALUES (46,NULL,'2024-03-13','2024-03-13',1,'<p>132</p>','123','<p>123</p>','1','1',23),(47,NULL,'2024-03-13','2024-03-13',1,'<p>测试步骤A</p>','预期结果A','<p>测试结果A</p>','1','1',24),(48,NULL,'2024-03-13','2024-03-13',1,'<p>测试步骤B</p>','测试预期B','<p>测试结果B</p>','3','3',24),(49,NULL,'2024-03-13','2024-03-13',1,'<p>123</p>','123','<p>321</p>','1','1',25),(52,NULL,'2024-03-13','2024-03-13',1,'<p>CCCC</p>','CCCC','<p>CCCC</p>','1','1',28),(53,NULL,'2024-03-13','2024-03-13',1,'<p>EEE</p>','EEE','<p>EE</p>','1','1',30),(56,NULL,'2024-03-13','2024-03-13',1,'<p>123</p>','321','<p>456</p>','1','1',31),(57,NULL,'2024-03-13','2024-03-13',1,'<p>DDD</p>','DDD','<p>DDD</p>','3','3',29),(58,NULL,'2024-03-13','2024-03-13',1,'<p>123</p>','321','<p>123</p>','1','1',32),(59,NULL,'2024-03-22','2024-03-22',1,'<p>123</p>','','<p>321</p>','2','1',33),(61,NULL,'2024-03-22','2024-03-22',1,'<p>123</p>','AAAAA','<p>321</p>','2','1',26),(62,NULL,'2024-03-22','2024-03-22',1,'<p>321</p>','BBBBBBB','<p>321</p>','2','1',27),(265,NULL,'2024-04-02','2024-04-02',1,'<p>123</p>','AAAAA','<p>321</p>','2','1',230),(266,NULL,'2024-04-02','2024-04-02',1,'<p>321</p>','BBBBBBB','<p>321</p>','2','1',231),(267,NULL,'2024-04-02','2024-04-02',1,'<p>CCCC</p>','CCCC','<p>CCCC</p>','1','1',232),(268,NULL,'2024-04-02','2024-04-02',1,'<p>123</p>','','<p>321</p>','2','1',233),(269,NULL,'2024-04-02','2024-04-02',1,'<p>DDD</p>','DDD','<p>DDD</p>','3','3',234),(270,NULL,'2024-04-02','2024-04-02',1,'<p>123</p>','321','<p>123</p>','1','1',235),(271,NULL,'2024-04-02','2024-04-02',1,'<p>EEE</p>','EEE','<p>EE</p>','1','1',236),(279,NULL,'2024-04-02','2024-04-02',1,'<p>123</p>','AAAAA','<p>321</p>','2','1',244),(280,NULL,'2024-04-02','2024-04-02',1,'<p>321</p>','BBBBBBB','<p>321</p>','2','1',245),(281,NULL,'2024-04-02','2024-04-02',1,'<p>CCCC</p>','CCCC','<p>CCCC</p>','1','1',246),(282,NULL,'2024-04-02','2024-04-02',1,'<p>123</p>','','<p>321</p>','2','1',247);
/*!40000 ALTER TABLE `project_casestep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_design`
--

DROP TABLE IF EXISTS `project_design`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_design` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `ident` varchar(64) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `demandType` varchar(8) DEFAULT NULL,
  `description` longtext,
  `title` varchar(64) DEFAULT NULL,
  `key` varchar(64) DEFAULT NULL,
  `level` varchar(64) DEFAULT NULL,
  `dut_id` bigint NOT NULL,
  `project_id` bigint NOT NULL,
  `round_id` bigint NOT NULL,
  `chapter` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_design_dut_id_13b4dbe6` (`dut_id`),
  KEY `project_design_project_id_b512a383` (`project_id`),
  KEY `project_design_round_id_65c3db9f` (`round_id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_design`
--

LOCK TABLES `project_design` WRITE;
/*!40000 ALTER TABLE `project_design` DISABLE KEYS */;
INSERT INTO `project_design` VALUES (14,NULL,'2024-03-29','2023-08-23',1,'RS422','初始化功能','1','<p>1.北风吹过的夏天</p>\n<p>2.以下内容为接口图片</p>\n<p><img src=\"data:image/png;base64,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\"></p>','初始化功能','0-0-0','2',39,6,13,'123123'),(19,NULL,'2024-03-29','2024-02-28',1,'TST','调试台功能','1','<p>测试调试台功能</p>','调试台功能','0-1-0','2',40,6,13,'3.1.2.1'),(20,NULL,'2024-03-29','2024-02-28',1,'CKTL','串口调试功能','1','<p>一个串口调试功能</p>','串口调试功能','0-1-1','2',40,6,13,'3.2.2.1'),(108,NULL,'2024-04-02','2024-04-02',1,'TST','调试台功能','1','<p>测试调试台功能</p>','调试台功能','1-0-0','2',142,6,94,'3.1.2.1'),(109,NULL,'2024-04-02','2024-04-02',1,'CKTL','串口调试功能','1','<p>一个串口调试功能</p>','串口调试功能','1-0-1','2',142,6,94,'3.2.2.1'),(112,NULL,'2024-04-02','2024-04-02',1,'TST','调试台功能','1','<p>测试调试台功能</p>','调试台功能','2-1-0','2',146,6,96,'3.1.2.1');
/*!40000 ALTER TABLE `project_design` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_dut`
--

DROP TABLE IF EXISTS `project_dut`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_dut` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `ident` varchar(64) DEFAULT NULL,
  `type` varchar(16) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `black_line` varchar(64) DEFAULT NULL,
  `pure_code_line` varchar(64) DEFAULT NULL,
  `mix_line` varchar(64) DEFAULT NULL,
  `total_comment_line` varchar(64) DEFAULT NULL,
  `total_code_line` varchar(64) DEFAULT NULL,
  `total_line` varchar(64) DEFAULT NULL,
  `comment_line` varchar(64) DEFAULT NULL,
  `title` varchar(64) DEFAULT NULL,
  `key` varchar(64) DEFAULT NULL,
  `level` varchar(64) DEFAULT NULL,
  `project_id` bigint NOT NULL,
  `round_id` bigint NOT NULL,
  `release_date` date DEFAULT NULL,
  `release_union` varchar(64) DEFAULT NULL,
  `version` varchar(64) DEFAULT NULL,
  `ref` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_dut_project_id_eace5041` (`project_id`),
  KEY `project_dut_round_id_6d1c076b` (`round_id`)
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_dut`
--

LOCK TABLES `project_dut` WRITE;
/*!40000 ALTER TABLE `project_dut` DISABLE KEYS */;
INSERT INTO `project_dut` VALUES (39,NULL,'2024-03-29','2023-08-18',1,'R2233-R1-UT1','YZ','研制总要求A','','','','','','','','研制总要求A','0-0','1',6,13,'2023-08-21','上海微小卫星工程中心','1.01','biaoshi1'),(40,NULL,'2024-03-29','2023-08-21',1,'R2233-R1-UT2','XQ','一个需求说明','','','','','','','','一个需求说明','0-1','1',6,13,'2024-02-20','上海微小卫星工程中心','1.02','biaoshi2'),(52,NULL,'2024-03-29','2024-03-29',1,'R2233-R1-UT3','SO','软件源代码','123','123','123','123','12','3123',NULL,'软件源代码','0-2','1',6,13,'2024-03-29','上海微小卫星工程中心','1.21','SSS'),(142,NULL,'2024-04-02','2024-04-02',1,'R2233-R2-UT1','XQ','一个需求说明','','','','','','','','一个需求说明','1-0','1',6,94,'2024-04-02','上海微小卫星工程中心','1.07','biaoshi2'),(143,NULL,'2024-04-02','2024-04-02',1,'R2233-R2-UT2','SO','软件源代码','123','123','123','123','123','3123','1.00','软件源代码','1-1','1',6,94,'2024-04-02','上海微小卫星工程中心','1.24','HSM2LUN'),(145,NULL,'2024-04-02','2024-04-02',1,'R2233-R3-UT1','SO','软件源代码','123','123','123','123','123','3123','1.00','软件源代码','2-0','1',6,96,'2024-04-02','上海微小卫星工程中心','1.29','HSM9LUN'),(146,NULL,'2024-04-02','2024-04-02',1,'R2233-R3-UT2','XQ','一个需求说明','','','','','','','','一个需求说明','2-1','1',6,96,'2024-04-02','上海微小卫星工程中心','1.09','biaoshi2');
/*!40000 ALTER TABLE `project_dut` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_problem`
--

DROP TABLE IF EXISTS `project_problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_problem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `ident` varchar(64) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `status` varchar(8) DEFAULT NULL,
  `grade` varchar(8) DEFAULT NULL,
  `type` varchar(8) DEFAULT NULL,
  `closeMethod` json DEFAULT NULL,
  `operation` longtext,
  `expect` varchar(1024) DEFAULT NULL,
  `result` longtext,
  `rules` varchar(512) DEFAULT NULL,
  `suggest` varchar(512) DEFAULT NULL,
  `postPerson` varchar(16) DEFAULT NULL,
  `postDate` date DEFAULT NULL,
  `designerPerson` varchar(16) DEFAULT NULL,
  `designDate` date DEFAULT NULL,
  `verifyPerson` varchar(16) DEFAULT NULL,
  `verifyDate` date DEFAULT NULL,
  `revokePerson` varchar(16) DEFAULT NULL,
  `revokeDate` date DEFAULT NULL,
  `project_id` bigint NOT NULL,
  `solve` longtext,
  PRIMARY KEY (`id`),
  KEY `project_problem_project_id_67aec7c3` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_problem`
--

LOCK TABLES `project_problem` WRITE;
/*!40000 ALTER TABLE `project_problem` DISABLE KEYS */;
INSERT INTO `project_problem` VALUES (30,NULL,'2024-03-27','2024-03-13',1,'1','123451234','2','1','3','[\"2\"]','<p>问题操作</p>','期望','<p>问题操作</p>','1','321123','翁上力','2024-03-13','12345','2024-03-13','王光宗','2024-03-13','无敌的小麦','2024-03-13',6,'123阿萨德'),(34,NULL,'2024-03-13','2024-03-13',1,'2','问题单5','2','1','3','[\"2\"]','<p>123</p>','2341','<p>1234</p>','1234','1234','王小雷','2024-03-13','阿萨德','2024-03-13','李鑫','2024-03-13','尧颖婷','2024-03-13',6,NULL),(35,NULL,'2024-03-13','2024-03-13',1,'3','问题单7','2','1','3','[\"2\"]','<p>123</p>','123','<p>123</p>','3421','234','王小雷','2024-03-13','2134','2024-03-13','李鑫','2024-03-13','无敌的小麦','2024-03-13',6,NULL),(36,NULL,'2024-03-22','2024-03-22',1,'4','新增一个建议问题关闭的','1','3','2','[\"1\"]','<p>建议问题</p>','建议问题','<p>建议问题</p>','建议问题','建议问题','翁上力','2024-03-22','123','2024-03-22','尧颖婷','2024-03-22','王光宗','2024-03-22',6,NULL),(37,NULL,'2024-03-22','2024-03-22',1,'5','一个文档问题1','1','2','2','[\"1\"]','<p>修改文档</p>','修改文档','<p>修改文档</p>','修改文档','修改文档','王小雷','2024-03-22','小蕾蕾','2024-03-22','李鑫','2024-03-22','王光宗','2024-03-22',6,NULL),(38,NULL,'2024-03-22','2024-03-22',1,'6','静态分析问题单一个','1','1','2','[\"2\"]','<p>123</p>','321','<p>123</p>','123','123','翁上力','2024-03-22','123','2024-03-22','尧颖婷','2024-03-22','王光宗','2024-03-22',6,NULL),(39,NULL,'2024-03-27','2024-03-25',1,'7','文档问题2','1','2','2','[\"1\"]','<p>文档问题</p>','文档问题','<p>文档问题</p>','文档问题','文档问题','王小雷','2024-03-25','123','2024-03-25','李鑫','2024-03-25','李鑫','2024-03-25',6,NULL),(40,NULL,'2024-03-25','2024-03-25',1,'8','文档审查的一个问题','1','2','2','[\"1\"]','<p>123</p>','3123','<p>21</p>','312','312','王小雷','2024-03-25','123','2024-03-25','尧颖婷','2024-03-25','李鑫','2024-03-25',6,NULL);
/*!40000 ALTER TABLE `project_problem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_problem_case`
--

DROP TABLE IF EXISTS `project_problem_case`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_problem_case` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `problem_id` bigint NOT NULL,
  `case_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_problem_case_problem_id_case_id_16bb73f3_uniq` (`problem_id`,`case_id`),
  KEY `project_problem_case_problem_id_7a9d47db` (`problem_id`),
  KEY `project_problem_case_case_id_a9d4819d` (`case_id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_problem_case`
--

LOCK TABLES `project_problem_case` WRITE;
/*!40000 ALTER TABLE `project_problem_case` DISABLE KEYS */;
INSERT INTO `project_problem_case` VALUES (47,30,26),(49,30,27),(48,34,26),(38,35,26),(50,36,26),(51,37,33),(59,38,29),(60,39,29),(61,40,29);
/*!40000 ALTER TABLE `project_problem_case` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_project`
--

DROP TABLE IF EXISTS `project_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_project` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `ident` varchar(64) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `engin_model` varchar(64) DEFAULT NULL,
  `section_system` varchar(64) DEFAULT NULL,
  `sub_system` varchar(64) DEFAULT NULL,
  `device` varchar(64) DEFAULT NULL,
  `beginTime` date DEFAULT NULL,
  `endTime` date DEFAULT NULL,
  `duty_person` varchar(64) NOT NULL,
  `member` json DEFAULT NULL,
  `security_level` varchar(8) DEFAULT NULL,
  `test_level` json DEFAULT NULL,
  `plant_type` json DEFAULT NULL,
  `report_type` varchar(64) DEFAULT NULL,
  `language` json DEFAULT NULL,
  `standard` json DEFAULT NULL,
  `entrust_contact` varchar(64) DEFAULT NULL,
  `entrust_contact_phone` varchar(64) DEFAULT NULL,
  `entrust_email` varchar(64) DEFAULT NULL,
  `dev_contact` varchar(64) DEFAULT NULL,
  `dev_contact_phone` varchar(64) DEFAULT NULL,
  `dev_email` varchar(64) DEFAULT NULL,
  `test_contact` varchar(64) DEFAULT NULL,
  `test_contact_phone` varchar(64) DEFAULT NULL,
  `test_email` varchar(64) DEFAULT NULL,
  `step` varchar(8) DEFAULT NULL,
  `dev_unit` varchar(64) NOT NULL,
  `entrust_unit` varchar(64) NOT NULL,
  `test_unit` varchar(64) NOT NULL,
  `config_person` varchar(64) NOT NULL,
  `quality_person` varchar(64) NOT NULL,
  `vise_person` varchar(64) NOT NULL,
  `abbreviation` json DEFAULT NULL,
  `soft_type` smallint NOT NULL,
  `devplant` varchar(8) DEFAULT NULL,
  `runtime` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_project`
--

LOCK TABLES `project_project` WRITE;
/*!40000 ALTER TABLE `project_project` DISABLE KEYS */;
INSERT INTO `project_project` VALUES (6,NULL,'2024-04-15','2023-08-17',1,'R2234','一个正式的项目','是一个工程型号','一个分系统','一个子系统','设备信息','2023-08-02','2023-08-17','王小雷','[\"尧颖婷\", \"翁上力\", \"李鑫\", \"张敏\", \"宋敏\"]','3','[\"6\"]','[\"3\"]','9','[\"1\"]','[\"1\", \"3\"]','张广智','18888888888','314298729@qq.com','张广智','18888888888','314298729@qq.com','施敏华','18888888888','314298729@qq.com','1','上海翰讯通讯股份有限公司12','上海微小卫星工程中心','中国科学院卫星软件测评中心','王小雷','王小雷','王小雷','[\"UDP\"]',1,'1','1');
/*!40000 ALTER TABLE `project_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_round`
--

DROP TABLE IF EXISTS `project_round`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_round` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `ident` varchar(64) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `beginTime` date DEFAULT NULL,
  `endTime` date DEFAULT NULL,
  `speedGrade` varchar(64) DEFAULT NULL,
  `package` varchar(64) DEFAULT NULL,
  `grade` varchar(64) DEFAULT NULL,
  `best_condition_voltage` varchar(64) DEFAULT NULL,
  `best_condition_tem` varchar(64) DEFAULT NULL,
  `typical_condition_voltage` varchar(64) DEFAULT NULL,
  `typical_condition_tem` varchar(64) DEFAULT NULL,
  `low_condition_voltage` varchar(64) DEFAULT NULL,
  `low_condition_tem` varchar(64) DEFAULT NULL,
  `level` varchar(15) NOT NULL,
  `key` varchar(15) NOT NULL,
  `title` varchar(15) NOT NULL,
  `project_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_round_project_id_371f4800` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_round`
--

LOCK TABLES `project_round` WRITE;
/*!40000 ALTER TABLE `project_round` DISABLE KEYS */;
INSERT INTO `project_round` VALUES (13,'第一轮测试','2024-04-02','2023-08-17',1,'R2233-R1','第1轮测试','2023-08-17','2023-08-17','123','123','1','','','','','','','0','0','第1轮测试',6),(94,'第2轮测试','2024-04-02','2024-04-02',1,'R2233-R2','第2轮测试','2024-04-02','2024-04-02','123','123','1','','','','','','','0','1','第2轮测试',6),(96,'第3轮测试','2024-04-02','2024-04-02',1,'R3333-R3','第3轮测试','2024-04-02','2024-04-02','123','123','1','','','','','','','0','2','第3轮测试',6);
/*!40000 ALTER TABLE `project_round` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_testdemand`
--

DROP TABLE IF EXISTS `project_testdemand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_testdemand` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `ident` varchar(64) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `adequacy` varchar(256) DEFAULT NULL,
  `termination` varchar(1024) DEFAULT NULL,
  `premise` varchar(256) DEFAULT NULL,
  `priority` varchar(8) DEFAULT NULL,
  `testType` varchar(8) DEFAULT NULL,
  `testMethod` json NOT NULL,
  `title` varchar(64) DEFAULT NULL,
  `key` varchar(64) DEFAULT NULL,
  `level` varchar(64) DEFAULT NULL,
  `design_id` bigint NOT NULL,
  `dut_id` bigint NOT NULL,
  `project_id` bigint NOT NULL,
  `round_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_testdemand_design_id_1d5b026e` (`design_id`),
  KEY `project_testdemand_dut_id_79457aa5` (`dut_id`),
  KEY `project_testdemand_project_id_99174744` (`project_id`),
  KEY `project_testdemand_round_id_a3d8a040` (`round_id`)
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_testdemand`
--

LOCK TABLES `project_testdemand` WRITE;
/*!40000 ALTER TABLE `project_testdemand` DISABLE KEYS */;
INSERT INTO `project_testdemand` VALUES (25,NULL,'2024-03-11','2023-08-24',1,'RS422','测试项1','覆盖需求相关功能123','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[\"1\"]','测试项1','0-0-0-0','3',14,39,6,13),(27,NULL,'2024-03-11','2023-08-24',1,'RS422','测试项2','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','16','[\"1\"]','测试项2','0-0-0-1','3',14,39,6,13),(28,NULL,'2024-03-11','2024-02-26',1,'RS422','测试项3','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','2','4','[\"1\"]','测试项3','0-0-0-2','3',14,39,6,13),(31,NULL,'2024-02-28','2024-02-28',1,'TST','调试台功能测试1号','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[]','调试台功能测试1号','0-1-0-0','3',19,40,6,13),(32,NULL,'2024-02-28','2024-02-28',1,'TST','开始了功能测试','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[]','开始了功能测试','0-1-0-1','3',19,40,6,13),(33,NULL,'2024-02-28','2024-02-28',1,'CKTL','串口调试1号测试项','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[]','串口调试1号测试项','0-1-1-0','3',20,40,6,13),(34,NULL,'2024-02-28','2024-02-28',1,'CKTL','串口调试的接口功能测试项','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','5','[]','串口调试的接口功能测试项','0-1-1-1','3',20,40,6,13),(36,NULL,'2024-03-22','2024-03-22',1,'TST','一个需求文档审查的问题','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','8','[\"1\"]','一个需求文档审查的问题','0-1-0-2','3',19,40,6,13),(204,NULL,'2024-04-02','2024-04-02',1,'TST','调试台功能测试1号','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[]','调试台功能测试1号','1-0-0-0','3',108,142,6,94),(205,NULL,'2024-04-02','2024-04-02',1,'TST','开始了功能测试','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[]','开始了功能测试','1-0-0-1','3',108,142,6,94),(206,NULL,'2024-04-02','2024-04-02',1,'TST','一个需求文档审查的问题','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','8','[\"1\"]','一个需求文档审查的问题','1-0-0-2','3',108,142,6,94),(207,NULL,'2024-04-02','2024-04-02',1,'CKTL','串口调试1号测试项','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[]','串口调试1号测试项','1-0-1-0','3',109,142,6,94),(208,NULL,'2024-04-02','2024-04-02',1,'CKTL','串口调试的接口功能测试项','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','5','[]','串口调试的接口功能测试项','1-0-1-1','3',109,142,6,94),(214,NULL,'2024-04-02','2024-04-02',1,'TST','调试台功能测试1号','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[]','调试台功能测试1号','2-1-0-0','3',112,146,6,96),(215,NULL,'2024-04-02','2024-04-02',1,'TST','开始了功能测试','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','4','[]','开始了功能测试','2-1-0-1','3',112,146,6,96),(216,NULL,'2024-04-02','2024-04-02',1,'TST','一个需求文档审查的问题','覆盖需求相关功能','1.测试正常终止：测试项分解的所有用例执行完毕，达到充分性要求，相关记录完整;\n2.测试异常终止：由于某些特殊原因导致该测试项分解的测试用例不能完全执行，无法执行的原因已记录','软件正常运行，外部接口通信正常','1','8','[\"1\"]','一个需求文档审查的问题','2-1-0-2','3',112,146,6,96);
/*!40000 ALTER TABLE `project_testdemand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_testdemand_otherdesign`
--

DROP TABLE IF EXISTS `project_testdemand_otherdesign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_testdemand_otherdesign` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `testdemand_id` bigint NOT NULL,
  `design_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_testdemand_other_testdemand_id_design_id_dafa4a01_uniq` (`testdemand_id`,`design_id`),
  KEY `project_testdemand_otherDesign_testdemand_id_ff4118c4` (`testdemand_id`),
  KEY `project_testdemand_otherDesign_design_id_b4a53848` (`design_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_testdemand_otherdesign`
--

LOCK TABLES `project_testdemand_otherdesign` WRITE;
/*!40000 ALTER TABLE `project_testdemand_otherdesign` DISABLE KEYS */;
INSERT INTO `project_testdemand_otherdesign` VALUES (28,25,19),(29,27,19),(30,28,19),(26,31,14);
/*!40000 ALTER TABLE `project_testdemand_otherdesign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_testdemandcontent`
--

DROP TABLE IF EXISTS `project_testdemandcontent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_testdemandcontent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `testXuQiu` varchar(1024) DEFAULT NULL,
  `testYuQi` varchar(1024) DEFAULT NULL,
  `testDemand_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_testdemandcontent_testDemand_id_9c47240e` (`testDemand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=291 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_testdemandcontent`
--

LOCK TABLES `project_testdemandcontent` WRITE;
/*!40000 ALTER TABLE `project_testdemandcontent` DISABLE KEYS */;
INSERT INTO `project_testdemandcontent` VALUES (66,NULL,'2024-02-28','2024-02-28',1,'输入1号','预期1号',31),(67,NULL,'2024-02-28','2024-02-28',1,'输入2号','预期2号',31),(69,NULL,'2024-02-28','2024-02-28',1,'输入1号','预期1号',32),(70,NULL,'2024-02-28','2024-02-28',1,'123','321',33),(71,NULL,'2024-02-28','2024-02-28',1,'321','312',34),(73,NULL,'2024-03-11','2024-03-11',1,'123','123',25),(74,NULL,'2024-03-11','2024-03-11',1,'AAA','AAA',25),(75,NULL,'2024-03-11','2024-03-11',1,'12412','4124',27),(76,NULL,'2024-03-11','2024-03-11',1,'查看是否有东西A','有东西A',28),(79,NULL,'2024-03-22','2024-03-22',1,'123','321',36),(275,NULL,'2024-04-02','2024-04-02',1,'输入1号','预期1号',204),(276,NULL,'2024-04-02','2024-04-02',1,'输入2号','预期2号',204),(277,NULL,'2024-04-02','2024-04-02',1,'输入1号','预期1号',205),(278,NULL,'2024-04-02','2024-04-02',1,'123','321',206),(279,NULL,'2024-04-02','2024-04-02',1,'123','321',207),(280,NULL,'2024-04-02','2024-04-02',1,'321','312',208),(287,NULL,'2024-04-02','2024-04-02',1,'输入1号','预期1号',214),(288,NULL,'2024-04-02','2024-04-02',1,'输入2号','预期2号',214),(289,NULL,'2024-04-02','2024-04-02',1,'输入1号','预期1号',215),(290,NULL,'2024-04-02','2024-04-02',1,'123','321',216);
/*!40000 ALTER TABLE `project_testdemandcontent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_dict`
--

DROP TABLE IF EXISTS `system_dict`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_dict` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  `status` varchar(8) DEFAULT NULL,
  `remark` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_dict`
--

LOCK TABLES `system_dict` WRITE;
/*!40000 ALTER TABLE `system_dict` DISABLE KEYS */;
INSERT INTO `system_dict` VALUES (1,'2023-08-17','2023-06-26',1,'data_status','data_status','1','用户状态字典'),(2,'2023-06-26','2023-06-26',1,'report_type','report_type','1','报告类型字典'),(3,'2023-06-26','2023-06-26',1,'step','step','1','测评阶段'),(4,'2023-06-26','2023-06-26',1,'security_level','security_level','1','安全等级'),(5,'2023-06-26','2023-06-26',1,'test_level','test_level','1','测试级别'),(6,'2023-06-26','2023-06-26',1,'plant_type','plant_type','1','平台类型'),(7,'2023-06-26','2023-06-26',1,'language','language','1','编程语言'),(8,'2023-06-26','2023-06-26',1,'standard','standard','1','测试标准'),(9,'2023-06-26','2023-06-26',1,'demandType','demandType','1','需求类型'),(10,'2023-06-26','2023-06-26',1,'priority','priority','1','优先级'),(11,'2023-06-26','2023-06-26',1,'testType','testType','1','测试类型'),(12,'2023-06-26','2023-06-26',1,'passType','passType','1','通过类型'),(13,'2023-06-26','2023-06-26',1,'execType','execType','1','用例执行情况'),(14,'2023-06-26','2023-06-26',1,'problemStatu','problemStatu','1','问题状态'),(15,'2023-06-26','2023-06-26',1,'problemType','problemType','1','问题类型'),(16,'2023-06-26','2023-06-26',1,'problemGrade','problemGrade','1','问题级别'),(17,'2023-06-26','2023-06-26',1,'closeMethod','closeMethod','1','问题闭环方式'),(18,'2023-08-24','2023-08-24',1,'testMethod','testMethod','1','测试方法'),(19,'2024-03-21','2024-03-21',1,'runtime','runtime','1','运行环境'),(20,'2024-03-21','2024-03-21',1,'devplant','devplant','1','开发环境');
/*!40000 ALTER TABLE `system_dict` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_dict_item`
--

DROP TABLE IF EXISTS `system_dict_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_dict_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `key` varchar(100) DEFAULT NULL,
  `status` varchar(8) DEFAULT NULL,
  `remark` varchar(2000) DEFAULT NULL,
  `dict_id` bigint NOT NULL,
  `show_title` varchar(64) NOT NULL,
  `doc_name` varchar(64) DEFAULT NULL,
  `publish_date` varchar(64) DEFAULT NULL,
  `source` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_dict_item_dict_id_787b070f` (`dict_id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_dict_item`
--

LOCK TABLES `system_dict_item` WRITE;
/*!40000 ALTER TABLE `system_dict_item` DISABLE KEYS */;
INSERT INTO `system_dict_item` VALUES (1,'2024-02-29','2023-06-26',1,'正常','1','1','用户正常状态',1,'',' ',' ',' '),(2,'2023-06-26','2023-06-26',1,'停用','2','1','用户停用状态',1,'',' ',' ',' '),(3,'2023-06-26','2023-06-26',1,'可编程逻辑器件软件仿真验证报告(二方)','1','1','FPGA仿真验证报告',2,'',' ',' ',' '),(4,'2024-02-28','2023-06-26',1,'可编程逻辑器件软件配置项三方测评报告','2','1','FPGA三方测评报告',2,'FT',' ',' ',' '),(7,'2023-06-26','2023-06-26',1,'可编程逻辑器件软件配置项确认测试报告(二方)','3','1','FPGA二方确认',2,'',' ',' ',' '),(8,'2023-06-26','2023-06-26',1,'处理器软件单元测试报告(二方)','4','1','CPU单元二方',2,'',' ',' ',' '),(9,'2023-06-26','2023-06-26',1,'处理器软件部件测试报告(二方）','5','1','CPU部件二方',2,'',' ',' ',' '),(11,'2024-02-28','2023-06-26',1,'处理器软件配置项三方测评报告','6','1','CPU配置项三方',2,'R',' ',' ',' '),(12,'2023-06-26','2023-06-26',1,'处理器软件配置项确认测试报告（二方)','7','1','CPU确认测试二方',2,'',' ',' ',' '),(13,'2023-06-26','2023-06-26',1,'系统测试报告(二方)','8','1','系统测试二方',2,'',' ',' ',' '),(14,'2024-02-28','2023-06-26',1,'鉴定测评报告','9','1','鉴定测评报告',2,'JD',' ',' ',' '),(15,'2023-08-17','2023-06-26',1,'刚开始','1','1','刚开始',3,'',' ',' ',' '),(16,'2023-06-26','2023-06-26',1,'进行中','2','1','进行中',3,'',' ',' ',' '),(17,'2023-06-26','2023-06-26',1,'已完成','3','1','已完成',3,'',' ',' ',' '),(18,'2023-06-26','2023-06-26',1,'已废除','4','1','已废除',3,'',' ',' ',' '),(19,'2024-02-28','2023-06-26',1,'A','1','1','A',4,'重要','',' ',' '),(20,'2024-02-28','2023-06-26',1,'B','2','1','B',4,'关键',' ',' ',' '),(21,'2024-02-28','2023-06-26',1,'C','3','1','C',4,'一般',' ',' ',' '),(22,'2024-02-28','2023-06-26',1,'D','4','1','D',4,'不重要',' ',' ',' '),(23,'2023-06-26','2023-06-26',1,'分系统测试','1','1','分系统测试',5,'',' ',' ',' '),(24,'2023-06-26','2023-06-26',1,'单元测试','2','1','单元测试',5,'',' ',' ',' '),(25,'2023-06-26','2023-06-26',1,'子系统测试','3','1','子系统测试',5,'',' ',' ',' '),(26,'2023-06-26','2023-06-26',1,'系统测试','4','1','系统测试',5,'',' ',' ',' '),(27,'2023-06-26','2023-06-26',1,'部件测试','5','1','部件测试',5,'',' ',' ',' '),(28,'2023-06-26','2023-06-26',1,'配置项测试','6','1','配置项测试',5,'',' ',' ',' '),(29,'2023-08-17','2023-06-26',5,'可编程逻辑器件','1','1','可编程逻辑器件',6,'',' ',' ',' '),(30,'2024-02-19','2023-06-26',1,'嵌入式处理器','2','1','嵌入式处理器',6,'',' ',' ',' '),(31,'2023-06-26','2023-06-26',1,'嵌入式操作系统','3','1','嵌入式操作系统',6,'',' ',' ',' '),(32,'2023-06-26','2023-06-26',1,'桌面操作系统','4','1','桌面操作系统',6,'',' ',' ',' '),(33,'2023-08-17','2023-06-26',0,'C','1','1','C',7,'',' ',' ',' '),(34,'2023-08-17','2023-06-26',1,'C#','2','1','C#',7,'',' ',' ',' '),(35,'2023-08-17','2023-06-26',0,'C++','3','1','C++',7,'',' ',' ',' '),(36,'2023-08-17','2023-06-26',0,'Java','4','1','Java',7,'',' ',' ',' '),(37,'2023-08-17','2023-06-26',1,'Python','5','1','Python',7,'',' ',' ',' '),(38,'2023-08-17','2023-06-26',0,'Verilog','6','1','Verilog',7,'',' ',' ',' '),(39,'2023-08-17','2023-06-26',0,'VHDL','7','1','VHDL',7,'',' ',' ',' '),(40,'2023-08-17','2023-06-26',1,'Rust','8','1','Rust',7,'',' ',' ',' '),(41,'2023-08-17','2023-06-26',1,'JavaScript','9','1','JavaScript',7,'',' ',' ',' '),(42,'2023-08-17','2023-06-26',2,'Golang','10','1','Golang',7,'',' ',' ',' '),(43,'2023-08-17','2023-06-26',5,'其他请在字典里加','11','1','其他请在字典里加',7,'',' ',' ',' '),(44,'2023-10-07','2023-06-26',1,'GJB 10157-2021','5','1','GJB 10157',8,'国军标10157','军用可编程逻辑器件软件语言编程安全子集','2021-12-30','中央军委装备发展部'),(45,'2023-10-07','2023-06-26',1,'GJB 438B-2009 ','6','1','GJB 438b',8,'','军用软件开发文档通用要求',' 2009-05-25',' 中国人民解放军总装备部'),(46,'2023-10-07','2023-06-26',1,'GJB 9433-2018','7','1','GJB 9433-2018',8,'','军用可编程逻辑器件软件测试要求',' 2018-03-27',' 中央军委装备发展部'),(47,'2023-10-07','2023-06-26',1,'GJB Z 141-2004 ','8','1','GJB/Z 141',8,'','军用软件测试指南',' 2004-09-20','中国人民解放军总装备部'),(55,'2024-02-26','2023-06-26',1,'功能','1','1','功能',9,'FT',' ',' ',' '),(56,'2023-08-23','2023-06-26',1,'性能','2','1','性能',9,'PT',' ',' ',' '),(57,'2023-08-23','2023-06-26',1,'接口','3','1','接口',9,'IT',' ',' ',' '),(58,'2023-08-23','2023-06-26',1,'可靠性','4','1','可靠性',9,'RT',' ',' ',' '),(59,'2023-08-23','2023-06-26',1,'安全性','5','1','安全性',9,'AT',' ',' ',' '),(60,'2024-03-27','2023-06-26',1,'静态分析/文档审查/代码审查/走查','6','1','其他',9,'OT',' ',' ',' '),(61,'2023-08-24','2023-06-26',1,'高','1','1','高',10,'high',' ',' ',' '),(62,'2023-08-24','2023-06-26',1,'中','2','1','中',10,'medium',' ',' ',' '),(63,'2023-08-24','2023-06-26',1,'低','3','1','低',10,'low',' ',' ',' '),(64,'2023-09-01','2023-06-26',3,'代码审查','2','1','代码审查',11,'CR',' ',' ',' '),(65,'2023-09-01','2023-06-26',4,'代码走查','3','1','代码走查',11,'CW',' ',' ',' '),(66,'2023-09-01','2023-06-26',5,'功能测试','4','1','功能测试',11,'FT',' ',' ',' '),(67,'2023-09-01','2023-06-26',6,'接口测试','5','1','接口测试',11,'IT',' ',' ',' '),(68,'2023-09-01','2023-06-26',7,'性能测试','6','1','性能测试',11,'PT',' ',' ',' '),(69,'2023-09-01','2023-06-26',8,'安全性测试','7','1','安全性测试',11,'SC',' ',' ',' '),(70,'2023-08-23','2023-06-26',1,'文档审查','8','1','文档审查',11,'DC',' ',' ',' '),(71,'2023-09-01','2023-06-26',9,'边界测试','9','1','边界测试',11,'BT',' ',' ',' '),(72,'2023-09-01','2023-06-26',10,'余量测试','10','1','余量测试',11,'SP',' ',' ',' '),(73,'2023-09-01','2023-06-26',11,'强度测试','11','1','强度测试',11,'ST',' ',' ',' '),(74,'2023-09-01','2023-06-26',12,'人机交互界面测试','12','1','人机交互界面测试',11,'GT',' ',' ',' '),(75,'2023-09-01','2023-06-26',13,'逻辑测试','13','1','逻辑测试',11,'LT',' ',' ',' '),(76,'2023-09-01','2023-06-26',14,'恢复性测试','14','1','恢复性测试',11,'RT',' ',' ',' '),(77,'2023-09-01','2023-06-26',2,'静态分析','15','1','静态分析',11,'SA',' ',' ',' '),(78,'2023-09-01','2023-06-26',15,'时序测试','1','1','时序测试',11,'TT',' ',' ',' '),(79,'2023-09-01','2023-06-26',16,'功耗分析','16','1','功耗分析',11,'PA',' ',' ',' '),(80,'2024-03-13','2023-06-26',1,'通过','1','1','普通人员不能修改标签',12,'Passed',' ',' ',' '),(81,'2024-03-13','2023-06-26',1,'未通过','2','1','普通人员不能修改标签',12,'Fail',' ',' ',' '),(82,'2024-03-13','2023-06-26',1,'未执行','3','1','普通人员不能修改标签',12,'Unexecute',' ',' ',' '),(83,'2024-03-13','2023-06-26',1,'完整执行','1','1','普通人员不允许修改',13,'seitai_exe',' ',' ',' '),(84,'2024-03-13','2023-06-26',1,'部分执行','2','1','普通人员不允许修改',13,'partial_exe',' ',' ',' '),(85,'2024-03-13','2023-06-26',1,'未执行','3','1','普通人员不允许修改',13,'nonexecute',' ',' ',' '),(86,'2023-06-26','2023-06-26',1,'关闭','1','1','关闭',14,'',' ',' ',' '),(87,'2023-06-26','2023-06-26',1,'开放','2','1','开放',14,'',' ',' ',' '),(88,'2023-06-26','2023-06-26',1,'推迟','3','1','推迟',14,'',' ',' ',' '),(89,'2023-06-26','2023-06-26',1,'撤销','4','1','撤销',14,'',' ',' ',' '),(90,'2023-06-26','2023-06-26',1,'其他问题','1','1','其他问题',15,'',' ',' ',' '),(91,'2023-06-26','2023-06-26',1,'文档问题','2','1','文档问题',15,'',' ',' ',' '),(92,'2023-06-26','2023-06-26',1,'程序问题','3','1','程序问题',15,'',' ',' ',' '),(93,'2023-06-26','2023-06-26',1,'设计问题','4','1','设计问题',15,'',' ',' ',' '),(94,'2023-06-26','2023-06-26',1,'一般','1','1','一般',16,'',' ',' ',' '),(95,'2023-06-26','2023-06-26',1,'严重','2','1','严重',16,'',' ',' ',' '),(96,'2023-06-26','2023-06-26',1,'建议','3','1','建议',16,'',' ',' ',' '),(97,'2023-06-26','2023-06-26',1,'致命','4','1','致命',16,'',' ',' ',' '),(98,'2023-06-26','2023-06-26',1,'修改文档','1','1','修改文档',17,'',' ',' ',' '),(99,'2023-06-26','2023-06-26',1,'修改程序','2','1','修改程序',17,'',' ',' ',' '),(102,'2023-08-17','2023-08-17',1,'dark','12','1','dark',7,'',' ',' ',' '),(103,'2023-08-17','2023-08-17',1,'swift','13','1','swift',7,'',' ',' ',' '),(104,'2024-03-13','2023-08-24',1,'时序仿真','1','1','时序仿真',18,'SXFZ',' ',' ',' '),(105,'2023-08-24','2023-08-24',1,'正交分解法','2','1','正交分解法',18,'ZJFJ',' ',' ',' '),(106,'2023-10-07','2023-10-07',1,'GJB-2725A','1','1','GJB-2725A',8,'','测试实验室和校准实验室通用要求','2001-05-31','中国人民解放军总装备部'),(107,'2023-10-07','2023-10-07',1,'〔2005〕装电字第324号','2','1','〔2005〕装电字第324号',8,'','军用软件测评实验室测评过程和技术能力要求','2005-12','总装备部电子信息基础部'),(108,'2023-10-07','2023-10-07',1,'TE-BTCG-003-2021','3','1',NULL,8,'','军用软件测试指南','2021-09','中央军委装备发展部'),(109,'2023-10-07','2023-10-07',1,'TE-BTCG-007-2021','4','1',NULL,8,'','军用软件鉴定测评大纲和报告','2021-09','中央军委装备发展部'),(110,'2023-10-07','2023-10-07',1,'GJB 438C-2021','9','1','GJB 438C-2021',8,'','军用软件开发文档通用要求','2022-03-01','中央军委装备发展部'),(111,'2023-10-07','2023-10-07',1,'GJB 8114-2013','10','1','GJB 8114-2013',8,'','C/C++语言编程安全子集','2013-04-11','国防科学技术工业委员会'),(112,'2023-10-07','2023-10-07',1,'TE-BTCG-004-2021','11','1','TE-BTCG-004-2021',8,'','军用软件鉴定测评指南','2021-09','中央军委装备发展部'),(113,'2023-10-07','2023-10-07',1,'TE-BTCG-005-2021','12','1','TE-BTCG-005-2021',8,'','军用软件能力评估指南','2021-09','中央军委装备发展部'),(114,'2023-10-07','2023-10-07',1,'TE-BTCG-006-2021','13','1','TE-BTCG-006-2021',8,'','军用软件测评机构能力评价','2021-09','中央军委装备发展部'),(115,'2023-10-07','2023-10-07',1,'载人航天工程软件工程化技术标准','14','1',NULL,8,'','载人航天工程软件工程化技术标准','2014-12','总装备部载人工程办公室'),(116,'2023-10-07','2023-10-07',1,'QJ 3027A-2016','15','1',NULL,8,'','航天型号软件测试规范','2016-01-19','国家国防科技工业局'),(117,'2024-03-21','2024-03-21',1,'gcc','1','1',NULL,19,'gcc',' ',' ',' '),(118,'2024-03-21','2024-03-21',1,'Linux','1','1','开发环境',20,'Linux',' ',' ',' '),(119,'2024-03-22','2024-03-22',1,'需求问题','5','1',NULL,15,'',NULL,NULL,NULL),(120,'2024-03-22','2024-03-22',1,'数据问题','6','1',NULL,15,'',NULL,NULL,NULL);
/*!40000 ALTER TABLE `system_dict_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user`
--

DROP TABLE IF EXISTS `user_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `id` bigint NOT NULL AUTO_INCREMENT,
  `remark` varchar(255) DEFAULT NULL,
  `update_datetime` date DEFAULT NULL,
  `create_datetime` date DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `username` varchar(150) NOT NULL,
  `name` varchar(40) NOT NULL,
  `avatar` longtext,
  `email` varchar(255) DEFAULT NULL,
  `status` varchar(15) NOT NULL,
  `job` varchar(255) DEFAULT NULL,
  `jobName` varchar(255) DEFAULT NULL,
  `organization` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `locationName` varchar(255) DEFAULT NULL,
  `introduction` varchar(255) DEFAULT NULL,
  `personalWebsite` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `accountId` varchar(255) DEFAULT NULL,
  `role` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user`
--

LOCK TABLES `user_user` WRITE;
/*!40000 ALTER TABLE `user_user` DISABLE KEYS */;
INSERT INTO `user_user` VALUES ('pbkdf2_sha256$600000$2xc983Z4Xlcdz0lgQNfZ6o$tVqiLyGeod18GrsIo0wbYAoQmB1ltnEDHOBpmTXlilw=','2024-02-19 09:55:45.199012',1,'chen','junyi',1,1,'2023-07-21 11:53:02.181849',1,'这是超级用户','2023-07-21','2023-07-21',1,'superAdmin','陈俊亦','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','15012312300','1','admin'),('pbkdf2_sha256$600000$3WxtAiG7llVRMBhUb5uNNv$/EWgN/vn0BfxiGDYwrcjesOrCEh5YbY4CbbPCIfQhFA=',NULL,0,'','',0,1,'2023-07-24 08:29:06.326410',3,NULL,'2023-07-25','2023-07-24',1,'string','翁上力','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','user@example.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','13882995216','1','admin'),('pbkdf2_sha256$600000$oRyCINlhS10kJVCM6xp2QA$9WrsVmA24NYuyrPtUsAh1uaEMwXdarNT9ZoTJN6UEQY=',NULL,0,'','',0,1,'2023-07-24 11:35:50.341621',5,NULL,'2023-07-24','2023-07-24',1,'尧颖婷','无敌的小麦','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18280441905','1','admin'),('pbkdf2_sha256$600000$uBQHR5wP74AgGv9dor5Rm2$+5bV/GPfiwKmWsyOZsrg1kYY8ldygqLnYpXq6COxCP0=',NULL,0,'','',0,1,'2023-07-24 11:36:28.156266',6,NULL,'2023-07-24','2023-07-24',1,'1241234','尧颖婷','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18782947123','1','admin'),('pbkdf2_sha256$600000$2cdbH2qipe7PCT6gnnrMpw$bhGWA8FSJqC/jS245FZre1+A3AZDGV0I8nLMZWe9KXc=',NULL,0,'','',0,1,'2023-07-24 11:36:34.939588',7,NULL,'2023-07-24','2023-07-24',1,'12423','李鑫','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18782947123','1','admin'),('pbkdf2_sha256$600000$NUAVF0CcpfFCriIkM2l0Xv$yvHY6QsiZuq9STuqL2lOZSsEzIIeIDlVHchC+AkBOss=',NULL,0,'','',0,1,'2023-07-24 11:36:53.125662',8,NULL,'2023-07-24','2023-07-24',1,'124234512345','王光宗','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18852163214','1','admin'),('pbkdf2_sha256$600000$szJ2a5FAF0Wfr25WRwCKmn$4NehFr1dk07OdWdFavTzJFhyKY4K9NIVIuc5mtnqvvw=',NULL,0,'','',0,1,'2023-07-24 11:37:11.397682',9,NULL,'2023-07-24','2023-07-24',1,'sdfds1','李莉','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18782947123','1','admin'),('pbkdf2_sha256$600000$XWIxjAV9QADgTKe09RWRkz$4wAlfrvsLVwIeHKMZZBC1xHoKdBz4AgjrIm8uJstk8E=',NULL,0,'','',0,1,'2023-07-24 11:37:21.566977',10,NULL,'2023-07-24','2023-07-24',1,'xdfas1231','张敏','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18782947123','1','admin'),('pbkdf2_sha256$600000$vGfWWuxEni9m7AG08mshv6$fhFNeK+RhNxEzeIHdqMxjvgCJSDn2o6MbiKnr2tCr4M=',NULL,0,'','',0,1,'2023-07-24 11:37:44.047243',11,NULL,'2023-07-24','2023-07-24',1,'sdfgew','宋敏','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18782947123','1','admin'),('pbkdf2_sha256$600000$mXx8UG1pEaDXDFdFhQkBFU$0ND6iSfhmABEDqMO6hD5HtPymBZ45gm3NRD4eRJ2YHo=',NULL,0,'','',0,1,'2023-07-24 11:37:59.347372',12,NULL,'2023-07-24','2023-07-24',1,'asfg234','陈鹏','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','314298729@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18782947123','1','admin'),('pbkdf2_sha256$600000$SFYzkIFQ0OZMyH9iDL1kIn$JkOIjUQcTLgOyPWO0urJx547UeK4gJ2nCZJfmSVPaw0=',NULL,0,'','',0,1,'2023-07-25 02:29:50.680918',14,NULL,'2024-02-29','2023-07-25',1,'24sdf23123123','王小雷','//lf1-xgcdn-tos.pstatp.com/obj/vcloud/vadmin/start.8e0e4855ee346a46ccff8ff3e24db27b.png','123@qq.com','1','前端艺术家','Frontend','chengdu','成都','四川省','这是我的自我介绍','https://www.arco.design','18874562159','1','admin');
/*!40000 ALTER TABLE `user_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_groups`
--

DROP TABLE IF EXISTS `user_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `users_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_groups_users_id_group_id_9b0d65e5_uniq` (`users_id`,`group_id`),
  KEY `user_user_groups_group_id_c57f13c0_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_user_groups_group_id_c57f13c0_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_user_groups_users_id_dfb9bea8_fk_user_user_id` FOREIGN KEY (`users_id`) REFERENCES `user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_groups`
--

LOCK TABLES `user_user_groups` WRITE;
/*!40000 ALTER TABLE `user_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `users_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_user_permissions_users_id_permission_id_3b0c24ea_uniq` (`users_id`,`permission_id`),
  KEY `user_user_user_permi_permission_id_ce49d4de_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_user_user_permi_permission_id_ce49d4de_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_user_user_permissions_users_id_30ebaa7f_fk_user_user_id` FOREIGN KEY (`users_id`) REFERENCES `user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_user_permissions`
--

LOCK TABLES `user_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-15 15:17:31
