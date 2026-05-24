-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: pobreza
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Current Database: `pobreza`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `pobreza` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `pobreza`;

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `id_audit` int NOT NULL AUTO_INCREMENT,
  `log_date` datetime DEFAULT NULL,
  `log_user` varchar(255) DEFAULT NULL,
  `log_table` varchar(255) DEFAULT NULL,
  `operation` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id_audit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `economy_indicator`
--

DROP TABLE IF EXISTS `economy_indicator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `economy_indicator` (
  `id_eco` int NOT NULL AUTO_INCREMENT,
  `id_period` int DEFAULT NULL,
  `gini_index` decimal(5,2) DEFAULT NULL,
  `per_capita_income` decimal(12,2) DEFAULT NULL,
  `inflation` decimal(7,4) DEFAULT NULL,
  `gdp_per_worker` decimal(14,2) DEFAULT NULL,
  `poverty_rate` decimal(5,2) DEFAULT NULL,
  `health_spending_pct` decimal(5,4) DEFAULT NULL,
  PRIMARY KEY (`id_eco`),
  KEY `id_period` (`id_period`),
  CONSTRAINT `economy_indicator_ibfk_1` FOREIGN KEY (`id_period`) REFERENCES `period` (`id_period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `insert_aud_economy_indicator` AFTER INSERT ON `economy_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'economy_indicator', 'insert');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_aud_economy_indicator` BEFORE UPDATE ON `economy_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'economy_indicator', 'update');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `delete_aud_economy_indicator` AFTER DELETE ON `economy_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'economy_indicator', 'delete');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `education_indicator`
--

DROP TABLE IF EXISTS `education_indicator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `education_indicator` (
  `id_edu` int NOT NULL AUTO_INCREMENT,
  `id_period` int DEFAULT NULL,
  `average_years_of_schooling` decimal(5,2) DEFAULT NULL,
  `literacy_rate` decimal(5,2) DEFAULT NULL,
  `education_spend` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`id_edu`),
  KEY `id_period` (`id_period`),
  CONSTRAINT `education_indicator_ibfk_1` FOREIGN KEY (`id_period`) REFERENCES `period` (`id_period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `insert_aud_education_indicator` AFTER INSERT ON `education_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'education_indicator', 'insert');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_aud_education_indicator` BEFORE UPDATE ON `education_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'education_indicator', 'update');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `delete_aud_education_indicator` AFTER DELETE ON `education_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'education_indicator', 'delete');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `employment_indicator`
--

DROP TABLE IF EXISTS `employment_indicator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employment_indicator` (
  `id_emp` int NOT NULL AUTO_INCREMENT,
  `id_period` int DEFAULT NULL,
  `employed_population` bigint DEFAULT NULL,
  `unemployed_population` bigint DEFAULT NULL,
  `total_population` bigint DEFAULT NULL,
  `labor_activity_rate` decimal(5,2) DEFAULT NULL,
  `unemployment_rate` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_emp`),
  KEY `id_period` (`id_period`),
  CONSTRAINT `employment_indicator_ibfk_1` FOREIGN KEY (`id_period`) REFERENCES `period` (`id_period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `insert_aud_employment_indicator` AFTER INSERT ON `employment_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'employment_indicator', 'insert');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_aud_employment_indicator` BEFORE UPDATE ON `employment_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'employment_indicator', 'update');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `delete_aud_employment_indicator` AFTER DELETE ON `employment_indicator` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'employment_indicator', 'delete');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `period`
--

DROP TABLE IF EXISTS `period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `period` (
  `id_period` int NOT NULL AUTO_INCREMENT,
  `year_` year DEFAULT NULL,
  PRIMARY KEY (`id_period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `insert_aud_period` AFTER INSERT ON `period` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'period', 'insert');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_aud_period` BEFORE UPDATE ON `period` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'period', 'update');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `delete_aud_period` AFTER DELETE ON `period` FOR EACH ROW begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'period', 'delete');
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary view structure for view `v_audit_activity`
--

DROP TABLE IF EXISTS `v_audit_activity`;
/*!50001 DROP VIEW IF EXISTS `v_audit_activity`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_audit_activity` AS SELECT 
 1 AS `log_date`,
 1 AS `log_user`,
 1 AS `log_table`,
 1 AS `operation`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_education_vs_unemployment`
--

DROP TABLE IF EXISTS `v_education_vs_unemployment`;
/*!50001 DROP VIEW IF EXISTS `v_education_vs_unemployment`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_education_vs_unemployment` AS SELECT 
 1 AS `year_`,
 1 AS `average_years_of_schooling`,
 1 AS `literacy_rate`,
 1 AS `education_spend`,
 1 AS `unemployment_rate`,
 1 AS `employed_population`,
 1 AS `unemployed_population`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_full_indicators`
--

DROP TABLE IF EXISTS `v_full_indicators`;
/*!50001 DROP VIEW IF EXISTS `v_full_indicators`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_full_indicators` AS SELECT 
 1 AS `year_`,
 1 AS `average_years_of_schooling`,
 1 AS `literacy_rate`,
 1 AS `education_spend`,
 1 AS `gini_index`,
 1 AS `per_capita_income`,
 1 AS `inflation`,
 1 AS `gdp_per_worker`,
 1 AS `poverty_rate`,
 1 AS `health_spending_pct`,
 1 AS `employed_population`,
 1 AS `unemployed_population`,
 1 AS `total_population`,
 1 AS `labor_activity_rate`,
 1 AS `unemployment_rate`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_indicator_averages`
--

DROP TABLE IF EXISTS `v_indicator_averages`;
/*!50001 DROP VIEW IF EXISTS `v_indicator_averages`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_indicator_averages` AS SELECT 
 1 AS `avg_literacy_rate`,
 1 AS `avg_schooling_years`,
 1 AS `avg_education_spend`,
 1 AS `avg_gini_index`,
 1 AS `avg_per_capita_income`,
 1 AS `avg_poverty_rate`,
 1 AS `avg_inflation`,
 1 AS `avg_unemployment_rate`,
 1 AS `avg_labor_activity_rate`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_population_distribution`
--

DROP TABLE IF EXISTS `v_population_distribution`;
/*!50001 DROP VIEW IF EXISTS `v_population_distribution`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_population_distribution` AS SELECT 
 1 AS `year_`,
 1 AS `total_population`,
 1 AS `employed_population`,
 1 AS `unemployed_population`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_poverty_trend`
--

DROP TABLE IF EXISTS `v_poverty_trend`;
/*!50001 DROP VIEW IF EXISTS `v_poverty_trend`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_poverty_trend` AS SELECT 
 1 AS `year_`,
 1 AS `poverty_rate`,
 1 AS `gini_index`,
 1 AS `per_capita_income`,
 1 AS `literacy_rate`,
 1 AS `unemployment_rate`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_spending_vs_outcomes`
--

DROP TABLE IF EXISTS `v_spending_vs_outcomes`;
/*!50001 DROP VIEW IF EXISTS `v_spending_vs_outcomes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_spending_vs_outcomes` AS SELECT 
 1 AS `year_`,
 1 AS `education_spend`,
 1 AS `health_spending_pct`,
 1 AS `literacy_rate`,
 1 AS `average_years_of_schooling`,
 1 AS `unemployment_rate`,
 1 AS `poverty_rate`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_unemployment_vs_economy`
--

DROP TABLE IF EXISTS `v_unemployment_vs_economy`;
/*!50001 DROP VIEW IF EXISTS `v_unemployment_vs_economy`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_unemployment_vs_economy` AS SELECT 
 1 AS `year_`,
 1 AS `unemployment_rate`,
 1 AS `labor_activity_rate`,
 1 AS `gini_index`,
 1 AS `per_capita_income`,
 1 AS `poverty_rate`,
 1 AS `inflation`,
 1 AS `gdp_per_worker`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_year_over_year`
--

DROP TABLE IF EXISTS `v_year_over_year`;
/*!50001 DROP VIEW IF EXISTS `v_year_over_year`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_year_over_year` AS SELECT 
 1 AS `year_`,
 1 AS `unemployment_rate`,
 1 AS `poverty_rate`,
 1 AS `gini_index`,
 1 AS `literacy_rate`,
 1 AS `per_capita_income`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'pobreza'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_compare_periods` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_compare_periods`(
    in p_year_a year,
    in p_year_b year
)
begin
    select
        p.year_,
        ec.gini_index,
        ec.per_capita_income,
        ed.literacy_rate,
        emp.unemployment_rate
    from period p
    join economy_indicator ec on ec.id_period = p.id_period
    join education_indicator ed on ed.id_period = p.id_period
    join employment_indicator emp on emp.id_period = p.id_period
    where p.year_ in (p_year_a, p_year_b)
    order by p.year_;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_all_economy` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_economy`()
begin
    select
        id_period,
        gini_index,
        per_capita_income,
        inflation,
        gdp_per_worker,
        poverty_rate,
        health_spending_pct
    from economy_indicator
    order by id_period;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_all_education` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_education`()
begin
    select
        id_period,
        average_years_of_schooling,
        literacy_rate,
        education_spend
    from education_indicator
    order by id_period;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_all_employment` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_employment`()
begin
    select
        id_period,
        employed_population,
        unemployed_population,
        total_population,
        labor_activity_rate,
        unemployment_rate
    from employment_indicator
    order by id_period;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_all_periods` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_all_periods`()
begin
    select id_period, year_
    from period
    order by year_;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_audit_summary` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_audit_summary`(
    in p_table varchar(255),
    in p_operation varchar(10),
    in p_limit int
)
begin
    select
        id_audit,
        log_date,
        log_user,
        log_table,
        operation
    from audit_log
    where
        (p_table is null or log_table = p_table)
        and (p_operation is null or operation = p_operation)
    order by log_date desc
    limit p_limit;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_indicators_by_year` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_indicators_by_year`(
    in p_year year
)
begin
    select
        p.year_,
        e.average_years_of_schooling,
        e.literacy_rate,
        ec.gini_index,
        ec.per_capita_income,
        emp.employed_population,
        emp.unemployed_population,
        emp.unemployment_rate
    from period p
    join education_indicator e on e.id_period = p.id_period
    join economy_indicator ec on ec.id_period = p.id_period
    join employment_indicator emp on emp.id_period = p.id_period
    where p.year_ = p_year;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_insert_economy` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_economy`(
    in p_id_period int,
    in p_gini_index decimal(5, 2),
    in p_per_capita_income decimal(12, 2),
    in p_inflation decimal(7, 4),
    in p_gdp_per_worker decimal(14, 2),
    in p_poverty_rate decimal(5, 2),
    in p_health_spending_pct decimal(5, 4)
)
begin
    insert into economy_indicator
        (id_period, gini_index, per_capita_income, inflation, gdp_per_worker, poverty_rate, health_spending_pct)
    values (p_id_period, p_gini_index, p_per_capita_income, p_inflation, p_gdp_per_worker, p_poverty_rate, p_health_spending_pct);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_insert_education` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_education`(
    in p_id_period int,
    in p_avg_schooling decimal(5, 2),
    in p_literacy_rate decimal(5, 2),
    in p_education_spend decimal(10, 4)
)
begin
    insert into education_indicator
        (id_period, average_years_of_schooling, literacy_rate, education_spend)
    values (p_id_period, p_avg_schooling, p_literacy_rate, p_education_spend);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_insert_employment` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_employment`(
    in p_id_period int,
    in p_employed bigint,
    in p_unemployed bigint,
    in p_total_population bigint,
    in p_labor_activity_rate decimal(5, 2),
    in p_unemployment_rate decimal(5, 2)
)
begin
    insert into employment_indicator
        (id_period, employed_population, unemployed_population, total_population, labor_activity_rate, unemployment_rate)
    values (p_id_period, p_employed, p_unemployed, p_total_population, p_labor_activity_rate, p_unemployment_rate);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_insert_full_period` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_full_period`(
    in p_year year,
    in p_avg_schooling decimal(5, 2),
    in p_literacy_rate decimal(5, 2),
    in p_education_spend decimal(10, 4),
    in p_gini_index decimal(5, 4),
    in p_per_capita_income decimal(12, 2),
    in p_inflation decimal(7, 4),
    in p_gdp_per_worker decimal(14, 2),
    in p_poverty_rate decimal(5, 2),
    in p_health_spending_pct decimal(5, 4),
    in p_employed bigint,
    in p_unemployed bigint,
    in p_total_population bigint,
    in p_labor_activity_rate decimal(5, 2),
    in p_unemployment_rate decimal(5, 2)
)
begin
    declare v_id_period int;
    insert into period (year_) values (p_year);
    set v_id_period = last_insert_id();
    insert into education_indicator
        (id_period, average_years_of_schooling, literacy_rate, education_spend)
    values (v_id_period, p_avg_schooling, p_literacy_rate, p_education_spend);
    insert into economy_indicator
        (id_period, gini_index, per_capita_income, inflation, gdp_per_worker, poverty_rate, health_spending_pct)
    values (v_id_period, p_gini_index, p_per_capita_income, p_inflation, p_gdp_per_worker, p_poverty_rate, p_health_spending_pct);
    insert into employment_indicator
        (id_period, employed_population, unemployed_population, total_population, labor_activity_rate, unemployment_rate)
    values (v_id_period, p_employed, p_unemployed, p_total_population, p_labor_activity_rate, p_unemployment_rate);
    select v_id_period as created_period_id;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_insert_period` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insert_period`(
    in p_year year
)
begin
    insert into period (year_) values (p_year);
    select last_insert_id() as created_period_id;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Current Database: `pobreza`
--

USE `pobreza`;

--
-- Final view structure for view `v_audit_activity`
--

/*!50001 DROP VIEW IF EXISTS `v_audit_activity`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_audit_activity` AS select `audit_log`.`log_date` AS `log_date`,`audit_log`.`log_user` AS `log_user`,`audit_log`.`log_table` AS `log_table`,`audit_log`.`operation` AS `operation` from `audit_log` order by `audit_log`.`log_date` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_education_vs_unemployment`
--

/*!50001 DROP VIEW IF EXISTS `v_education_vs_unemployment`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_education_vs_unemployment` AS select `p`.`year_` AS `year_`,`e`.`average_years_of_schooling` AS `average_years_of_schooling`,`e`.`literacy_rate` AS `literacy_rate`,`e`.`education_spend` AS `education_spend`,`emp`.`unemployment_rate` AS `unemployment_rate`,`emp`.`employed_population` AS `employed_population`,`emp`.`unemployed_population` AS `unemployed_population` from ((`period` `p` join `education_indicator` `e` on((`e`.`id_period` = `p`.`id_period`))) join `employment_indicator` `emp` on((`emp`.`id_period` = `p`.`id_period`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_full_indicators`
--

/*!50001 DROP VIEW IF EXISTS `v_full_indicators`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_full_indicators` AS select `p`.`year_` AS `year_`,`e`.`average_years_of_schooling` AS `average_years_of_schooling`,`e`.`literacy_rate` AS `literacy_rate`,`e`.`education_spend` AS `education_spend`,`ec`.`gini_index` AS `gini_index`,`ec`.`per_capita_income` AS `per_capita_income`,`ec`.`inflation` AS `inflation`,`ec`.`gdp_per_worker` AS `gdp_per_worker`,`ec`.`poverty_rate` AS `poverty_rate`,`ec`.`health_spending_pct` AS `health_spending_pct`,`emp`.`employed_population` AS `employed_population`,`emp`.`unemployed_population` AS `unemployed_population`,`emp`.`total_population` AS `total_population`,`emp`.`labor_activity_rate` AS `labor_activity_rate`,`emp`.`unemployment_rate` AS `unemployment_rate` from (((`period` `p` join `education_indicator` `e` on((`e`.`id_period` = `p`.`id_period`))) join `economy_indicator` `ec` on((`ec`.`id_period` = `p`.`id_period`))) join `employment_indicator` `emp` on((`emp`.`id_period` = `p`.`id_period`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_indicator_averages`
--

/*!50001 DROP VIEW IF EXISTS `v_indicator_averages`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_indicator_averages` AS select avg(`e`.`literacy_rate`) AS `avg_literacy_rate`,avg(`e`.`average_years_of_schooling`) AS `avg_schooling_years`,avg(`e`.`education_spend`) AS `avg_education_spend`,avg(`ec`.`gini_index`) AS `avg_gini_index`,avg(`ec`.`per_capita_income`) AS `avg_per_capita_income`,avg(`ec`.`poverty_rate`) AS `avg_poverty_rate`,avg(`ec`.`inflation`) AS `avg_inflation`,avg(`emp`.`unemployment_rate`) AS `avg_unemployment_rate`,avg(`emp`.`labor_activity_rate`) AS `avg_labor_activity_rate` from (((`period` `p` join `education_indicator` `e` on((`e`.`id_period` = `p`.`id_period`))) join `economy_indicator` `ec` on((`ec`.`id_period` = `p`.`id_period`))) join `employment_indicator` `emp` on((`emp`.`id_period` = `p`.`id_period`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_population_distribution`
--

/*!50001 DROP VIEW IF EXISTS `v_population_distribution`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_population_distribution` AS select `p`.`year_` AS `year_`,`emp`.`total_population` AS `total_population`,`emp`.`employed_population` AS `employed_population`,`emp`.`unemployed_population` AS `unemployed_population` from (`period` `p` join `employment_indicator` `emp` on((`emp`.`id_period` = `p`.`id_period`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_poverty_trend`
--

/*!50001 DROP VIEW IF EXISTS `v_poverty_trend`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_poverty_trend` AS select `p`.`year_` AS `year_`,`ec`.`poverty_rate` AS `poverty_rate`,`ec`.`gini_index` AS `gini_index`,`ec`.`per_capita_income` AS `per_capita_income`,`e`.`literacy_rate` AS `literacy_rate`,`emp`.`unemployment_rate` AS `unemployment_rate` from (((`period` `p` join `economy_indicator` `ec` on((`ec`.`id_period` = `p`.`id_period`))) join `education_indicator` `e` on((`e`.`id_period` = `p`.`id_period`))) join `employment_indicator` `emp` on((`emp`.`id_period` = `p`.`id_period`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_spending_vs_outcomes`
--

/*!50001 DROP VIEW IF EXISTS `v_spending_vs_outcomes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_spending_vs_outcomes` AS select `p`.`year_` AS `year_`,`e`.`education_spend` AS `education_spend`,`ec`.`health_spending_pct` AS `health_spending_pct`,`e`.`literacy_rate` AS `literacy_rate`,`e`.`average_years_of_schooling` AS `average_years_of_schooling`,`emp`.`unemployment_rate` AS `unemployment_rate`,`ec`.`poverty_rate` AS `poverty_rate` from (((`period` `p` join `education_indicator` `e` on((`e`.`id_period` = `p`.`id_period`))) join `economy_indicator` `ec` on((`ec`.`id_period` = `p`.`id_period`))) join `employment_indicator` `emp` on((`emp`.`id_period` = `p`.`id_period`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_unemployment_vs_economy`
--

/*!50001 DROP VIEW IF EXISTS `v_unemployment_vs_economy`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_unemployment_vs_economy` AS select `p`.`year_` AS `year_`,`emp`.`unemployment_rate` AS `unemployment_rate`,`emp`.`labor_activity_rate` AS `labor_activity_rate`,`ec`.`gini_index` AS `gini_index`,`ec`.`per_capita_income` AS `per_capita_income`,`ec`.`poverty_rate` AS `poverty_rate`,`ec`.`inflation` AS `inflation`,`ec`.`gdp_per_worker` AS `gdp_per_worker` from ((`period` `p` join `employment_indicator` `emp` on((`emp`.`id_period` = `p`.`id_period`))) join `economy_indicator` `ec` on((`ec`.`id_period` = `p`.`id_period`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_year_over_year`
--

/*!50001 DROP VIEW IF EXISTS `v_year_over_year`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_year_over_year` AS select `p`.`year_` AS `year_`,`emp`.`unemployment_rate` AS `unemployment_rate`,`ec`.`poverty_rate` AS `poverty_rate`,`ec`.`gini_index` AS `gini_index`,`e`.`literacy_rate` AS `literacy_rate`,`ec`.`per_capita_income` AS `per_capita_income` from (((`period` `p` join `employment_indicator` `emp` on((`emp`.`id_period` = `p`.`id_period`))) join `economy_indicator` `ec` on((`ec`.`id_period` = `p`.`id_period`))) join `education_indicator` `e` on((`e`.`id_period` = `p`.`id_period`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-24 13:29:29
