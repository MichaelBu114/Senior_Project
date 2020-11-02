CREATE DATABASE  IF NOT EXISTS `dp_sp` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dp_sp`;
-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: dp_sp
-- ------------------------------------------------------
-- Server version	8.0.17

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
-- Table structure for table `Categories`
--

DROP TABLE IF EXISTS `Categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Categories` (
  `id` int(11) NOT NULL,
  `name` varchar(90) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `categories_id_uindex` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Categories`
--

LOCK TABLES `Categories` WRITE;
/*!40000 ALTER TABLE `Categories` DISABLE KEYS */;
INSERT INTO `Categories` VALUES (1,'Delivery'),(2,'Dine-out'),(3,'Nightlife'),(4,'Catching-up'),(5,'Takeaway'),(6,'Cafes'),(7,'Daily Menus'),(8,'Breakfast'),(9,'Lunch'),(10,'Dinner'),(11,'Pubs & Bars'),(13,'Pocket Friendly Delivery'),(14,'Clubs & Lounges');
/*!40000 ALTER TABLE `Categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Comments`
--

DROP TABLE IF EXISTS `Comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Comments` (
  `comment_id` int(11) NOT NULL,
  `FK_user` int(11) NOT NULL,
  `comment` varchar(1500) DEFAULT NULL,
  `restaurant_id` int(11) NOT NULL,
  PRIMARY KEY (`comment_id`),
  UNIQUE KEY `Comments_comment_id_uindex` (`comment_id`),
  KEY `User_Comment_User_user_id_fk_idx` (`FK_user`),
  CONSTRAINT `User_Comment_User_user_id_fk` FOREIGN KEY (`FK_user`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Comments`
--

LOCK TABLES `Comments` WRITE;
/*!40000 ALTER TABLE `Comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `Comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cuisine`
--

DROP TABLE IF EXISTS `Cuisine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cuisine` (
  `cuisine_id` int(11) NOT NULL,
  `cuisine_name` varchar(45) NOT NULL,
  PRIMARY KEY (`cuisine_id`),
  UNIQUE KEY `Cuisine_cuisine_id_uindex` (`cuisine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cuisine`
--

LOCK TABLES `Cuisine` WRITE;
/*!40000 ALTER TABLE `Cuisine` DISABLE KEYS */;
INSERT INTO `Cuisine` VALUES (1,'American'),(3,'Asian'),(5,'Bakery'),(25,'Chinese'),(30,'Cafe'),(38,'European'),(40,'Fast Food'),(45,'French'),(55,'Italian'),(60,'Japanese'),(67,'Korean'),(70,'Mediterranean'),(73,'Mexican'),(82,'Pizza'),(83,'Seafood'),(89,'Spanish'),(95,'Thai'),(99,'Vietnamese'),(100,'Desserts'),(121,'Cantonese'),(134,'German'),(135,'Irish'),(141,'Steak'),(143,'Healthy Food'),(148,'Indian'),(150,'Tex-Mex'),(152,'African'),(153,'Cuban'),(156,'Greek'),(161,'Coffee and Tea'),(168,'Burger'),(177,'Sushi'),(181,'Grill'),(182,'Breakfast'),(192,'Deli'),(193,'BBQ'),(207,'Jamaican'),(219,'Polish'),(227,'Bar Food'),(233,'Ice Cream'),(265,'Jewish'),(298,'Fish and Chips'),(304,'Sandwich'),(308,'Vegetarian'),(318,'Fondue'),(361,'Puerto Rican'),(461,'Soul Food'),(491,'Cajun'),(501,'Frozen Yogurt'),(541,'Diner'),(921,'Southern American'),(955,'Bagels'),(959,'Donuts'),(966,'Southwestern'),(971,'Chili'),(983,'Pub Food'),(997,'Taco'),(998,'Salad');
/*!40000 ALTER TABLE `Cuisine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Establishment`
--

DROP TABLE IF EXISTS `Establishment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Establishment` (
  `id` int(11) NOT NULL,
  `name` varchar(90) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Establishment`
--

LOCK TABLES `Establishment` WRITE;
/*!40000 ALTER TABLE `Establishment` DISABLE KEYS */;
INSERT INTO `Establishment` VALUES (1,'Café'),(5,'Lounge'),(6,'Pub'),(7,'Bar'),(8,'Club'),(16,'Casual Dining'),(18,'Fine Dining'),(20,'Food Court'),(21,'Quick Bites'),(23,'Dessert Parlour'),(24,'Deli'),(31,'Bakery'),(41,'Beverage Shop'),(81,'Food Truck'),(91,'Bistro'),(101,'Diner'),(161,'Microbrewery'),(271,'Sandwich Shop'),(272,'Cocktail Bar'),(275,'Pizzeria'),(278,'Wine Bar'),(281,'Fast Food'),(282,'Taqueria'),(283,'Brewery'),(284,'Juice Bar'),(285,'Fast Casual'),(286,'Coffee Shop'),(290,'Vineyard'),(291,'Sweet Shop'),(292,'Beer Garden'),(295,'Noodle Shop'),(309,'Steakhouse');
/*!40000 ALTER TABLE `Establishment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Friends`
--

DROP TABLE IF EXISTS `Friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Friends` (
  `friends_id` int(11) NOT NULL AUTO_INCREMENT,
  `Fk_user` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`friends_id`),
  KEY `Friends_User_user_id_fk` (`Fk_user`),
  CONSTRAINT `Friends_User_user_id_fk` FOREIGN KEY (`Fk_user`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Friends`
--

LOCK TABLES `Friends` WRITE;
/*!40000 ALTER TABLE `Friends` DISABLE KEYS */;
/*!40000 ALTER TABLE `Friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Groups`
--

DROP TABLE IF EXISTS `Groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Groups` (
  `group_id` int(11) NOT NULL,
  `group_name` varchar(45) NOT NULL,
  PRIMARY KEY (`group_id`),
  UNIQUE KEY `Groups_group_id_uindex` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Groups`
--

LOCK TABLES `Groups` WRITE;
/*!40000 ALTER TABLE `Groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `Groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Login`
--

DROP TABLE IF EXISTS `Login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `password` varchar(90) NOT NULL,
  `date_changed` date NOT NULL,
  PRIMARY KEY (`login_id`),
  UNIQUE KEY `Login_username_uindex` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Login`
--

LOCK TABLES `Login` WRITE;
/*!40000 ALTER TABLE `Login` DISABLE KEYS */;
INSERT INTO `Login` VALUES (1,'burkem35','password123','2020-10-16'),(2,'L1MBO','test456','2020-10-16'),(3,'Michael','Burke','2020-10-19'),(4,'test','test','2020-10-19'),(5,'sprint','test789','2020-10-19'),(6,'test2','testpassword','2020-10-23'),(7,'jsmith@gmail.com','9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05','2020-11-02'),(8,'test1@gmail.com','9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05','2020-11-02'),(9,'test2@gmail.com','262f30c8a91241c31e144b286c3aad30d7ef9af6030b68201d54421c681285b6','2020-11-02');
/*!40000 ALTER TABLE `Login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Survey`
--

DROP TABLE IF EXISTS `Survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Survey` (
  `survey_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Survey`
--

LOCK TABLES `Survey` WRITE;
/*!40000 ALTER TABLE `Survey` DISABLE KEYS */;
/*!40000 ALTER TABLE `Survey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `lastname` varchar(90) NOT NULL,
  `firstname` varchar(90) NOT NULL,
  `email` varchar(150) NOT NULL,
  `activity` tinyint(1) NOT NULL,
  `default_zip` varchar(5) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  `price_range` int(11) DEFAULT NULL,
  `user_rating` int(11) DEFAULT NULL,
  `reservations` int(11) DEFAULT NULL,
  `FK_login_id` int(11) DEFAULT NULL,
  `FK_user_categories` int(11) DEFAULT NULL,
  `FK_user_establishment` int(11) DEFAULT NULL,
  `FK_comment` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `User_user_id_uindex` (`user_id`),
  KEY `User_Login_login_id_fk` (`FK_login_id`),
  KEY `User_User_Catgories_user_catgories_id_fk` (`FK_user_categories`),
  KEY `User_User_Establishment_user_establishment_fk` (`FK_user_establishment`),
  KEY `User_Comments_comment_id_fk_idx` (`FK_comment`),
  CONSTRAINT `User_Comments_comment_id_fk` FOREIGN KEY (`FK_comment`) REFERENCES `Comments` (`FK_user`),
  CONSTRAINT `User_Login_login_id_fk` FOREIGN KEY (`FK_login_id`) REFERENCES `Login` (`login_id`),
  CONSTRAINT `User_User_Catgories_user_catgories_id_fk` FOREIGN KEY (`FK_user_categories`) REFERENCES `User_Categories` (`user_categories_id`),
  CONSTRAINT `User_User_Establishment_user_establishment_fk` FOREIGN KEY (`FK_user_establishment`) REFERENCES `User_Establishment` (`user_establishment`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'Smith','John','jsmith@gmail.com',1,NULL,NULL,NULL,NULL,NULL,7,NULL,NULL,NULL),(2,'Test1','Test1','test1@gmail.com',1,NULL,40233,3,3,NULL,8,NULL,NULL,NULL),(3,'Test2','Test2','test2@gmail.com',1,NULL,24140,2,2,NULL,9,NULL,NULL,NULL);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Categories`
--

DROP TABLE IF EXISTS `User_Categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User_Categories` (
  `user_categories_id` int(11) NOT NULL AUTO_INCREMENT,
  `FK_user` int(11) NOT NULL,
  `FK_categories` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_categories_id`),
  KEY `FK_usercategories_idx` (`FK_user`),
  KEY `FK_categoriesuser_idx` (`FK_categories`),
  CONSTRAINT `User_Categories_Categories_categories_id_fk` FOREIGN KEY (`FK_categories`) REFERENCES `Categories` (`id`),
  CONSTRAINT `User_Categories_User_user_id_fk` FOREIGN KEY (`FK_user`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Categories`
--

LOCK TABLES `User_Categories` WRITE;
/*!40000 ALTER TABLE `User_Categories` DISABLE KEYS */;
INSERT INTO `User_Categories` VALUES (1,2,2),(2,2,7),(3,2,9),(4,3,1),(5,3,3),(6,3,4),(7,3,8),(8,3,11),(9,3,13),(10,3,14);
/*!40000 ALTER TABLE `User_Categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Cuisine`
--

DROP TABLE IF EXISTS `User_Cuisine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User_Cuisine` (
  `user_cuisine_id` int(11) NOT NULL AUTO_INCREMENT,
  `FK_user` int(11) NOT NULL,
  `FK_cuisine` int(11) NOT NULL,
  PRIMARY KEY (`user_cuisine_id`),
  KEY `FK_user_idx` (`FK_user`),
  KEY `FK_cuisine_idx` (`FK_cuisine`),
  CONSTRAINT `User_Cuisine_Cuisine_cuisine_id_fk` FOREIGN KEY (`FK_cuisine`) REFERENCES `Cuisine` (`cuisine_id`),
  CONSTRAINT `User_Cuisine_User_user_id_fk` FOREIGN KEY (`FK_user`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Cuisine`
--

LOCK TABLES `User_Cuisine` WRITE;
/*!40000 ALTER TABLE `User_Cuisine` DISABLE KEYS */;
INSERT INTO `User_Cuisine` VALUES (1,2,1),(2,2,25),(3,2,55),(4,2,73),(5,2,83),(6,2,193),(7,3,3),(8,3,38),(9,3,45),(10,3,67),(11,3,70),(12,3,95),(13,3,121),(14,3,135),(15,3,143),(16,3,150),(17,3,461),(18,3,966);
/*!40000 ALTER TABLE `User_Cuisine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Establishment`
--

DROP TABLE IF EXISTS `User_Establishment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User_Establishment` (
  `user_establishment` int(11) NOT NULL AUTO_INCREMENT,
  `FK_user` int(11) NOT NULL,
  `FK_establishment` int(11) NOT NULL,
  PRIMARY KEY (`user_establishment`),
  KEY `FK_userestablishment_idx` (`FK_user`),
  KEY `FK_establishmentuser_idx` (`FK_establishment`),
  CONSTRAINT `User_Establishment_Establishment_establishment_id_fk` FOREIGN KEY (`FK_establishment`) REFERENCES `Establishment` (`id`),
  CONSTRAINT `User_Establishment_User_user_id_fk` FOREIGN KEY (`FK_user`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Establishment`
--

LOCK TABLES `User_Establishment` WRITE;
/*!40000 ALTER TABLE `User_Establishment` DISABLE KEYS */;
INSERT INTO `User_Establishment` VALUES (18,2,1),(19,2,16),(20,2,18),(21,2,285),(22,3,5),(23,3,6),(24,3,18),(25,3,20),(26,3,23),(27,3,24),(28,3,91),(29,3,161),(30,3,281),(31,3,284),(32,3,292),(33,3,295),(34,3,309);
/*!40000 ALTER TABLE `User_Establishment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Group`
--

DROP TABLE IF EXISTS `User_Group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User_Group` (
  `user_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `Fk_user` int(11) NOT NULL,
  `Fk_group` int(11) NOT NULL,
  PRIMARY KEY (`user_group_id`),
  KEY `User_Group_Groups_group_id_fk` (`Fk_group`),
  KEY `User_Group_User_user_id_fk` (`Fk_user`),
  CONSTRAINT `User_Group_Groups_group_id_fk` FOREIGN KEY (`Fk_group`) REFERENCES `Groups` (`group_id`),
  CONSTRAINT `User_Group_User_user_id_fk` FOREIGN KEY (`Fk_user`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Group`
--

LOCK TABLES `User_Group` WRITE;
/*!40000 ALTER TABLE `User_Group` DISABLE KEYS */;
/*!40000 ALTER TABLE `User_Group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'dp_sp'
--

--
-- Dumping routines for database 'dp_sp'
--
/*!50003 DROP PROCEDURE IF EXISTS `addUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addUser`(IN newFirstName varchar(90), IN newLastName varchar(90),
                                         IN newEmail varchar(150), IN FKLogin int)
BEGIN
    INSERT INTO User (lastname, firstname, email, activity, distance, price_range, user_rating, reservations, FK_login_id, FK_user_categories, FK_user_establishment, FK_comment)
VALUES (newLastName, newFirstName, newEmail, 1,null,null,null,null ,FKLogin,null,null,null);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `addUserCategories` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addUserCategories`(IN user_id int(11), IN category_id int(11))
BEGIN
INSERT INTO User_Categories (FK_user, FK_categories) VALUES (user_id, category_id);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `addUserCuisine` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addUserCuisine`(IN user_id int(11), IN cuisine_id int(11))
BEGIN
INSERT INTO User_Cuisine (FK_user, FK_cuisine) VALUES (user_id, cuisine_id);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `addUserEstablishment` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addUserEstablishment`(IN user_id int(11), IN establishment_id int(11))
BEGIN
INSERT INTO User_Establishment (FK_user, FK_establishment) VALUES (user_id, establishment_id);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetLogin` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `GetLogin`(IN username varchar(150), IN password varchar(90))
BEGIN
    SELECT * FROM Login as l WHERE l.username = username AND l.password = password;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetName` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `GetName`(IN uname varchar(150))
BEGIN
    SELECT u.firstname from User u
    JOIN Login l ON l.login_id = u.FK_login_id
    WHERE l.username = uname;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetUsername` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `GetUsername`(IN checkUser varchar(150))
BEGIN
    SELECT l.username FROM Login AS l WHERE l.username =  checkUser;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `newUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `newUser`(IN newPassword varchar(90),
                                         IN firstName varchar(90), IN lastName varchar(90), IN Email varchar(150))
BEGIN
    INSERT INTO Login (username,password,date_changed) VALUES (email,newPassword,curdate());
    call addUser(firstName,lastName,Email,LAST_INSERT_ID());
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `updateRange` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `updateRange`(IN FKrange int, IN uid int(11))
BEGIN
	UPDATE `dp_sp`.`User` u
    SET `price_range` = FKrange
    WHERE u.user_id = uid ;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `updateRating` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `updateRating`(IN FKrating int, IN uid int(11))
BEGIN
	UPDATE `dp_sp`.`User` u
    SET `user_rating` = FKrating
    WHERE u.user_id = uid ;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `updateZipcode` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `updateZipcode`(IN userZipcode varchar(5), IN uid int(11))
BEGIN
	UPDATE `dp_sp`.`User` u
    SET `default_zip` = userZipcode
    WHERE u.user_id = uid ;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-02 14:44:07
