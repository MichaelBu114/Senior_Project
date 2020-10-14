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
  `username` varchar(45) NOT NULL,
  `password` varchar(90) NOT NULL,
  `date_changed` date NOT NULL,
  PRIMARY KEY (`login_id`),
  UNIQUE KEY `Login_username_uindex` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Login`
--

LOCK TABLES `Login` WRITE;
/*!40000 ALTER TABLE `Login` DISABLE KEYS */;
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
  `user_id` int(11) NOT NULL,
  `lastname` varchar(90) NOT NULL,
  `firstname` varchar(90) NOT NULL,
  `email` varchar(150) NOT NULL,
  `activity` tinyint(1) NOT NULL,
  `distance` int(11) NOT NULL,
  `price_range` int(11) DEFAULT NULL,
  `user_rating` int(11) DEFAULT NULL,
  `reservations` int(11) DEFAULT NULL,
  `FK_login_id` int(11) DEFAULT NULL,
  `FK_user_categories` int(11) DEFAULT NULL,
  `FK_user_establishment` int(11) NOT NULL,
  `FK_comment` int(11) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `User_user_id_uindex` (`user_id`),
  KEY `User_Login_login_id_fk` (`FK_login_id`),
  KEY `User_User_Catgories_user_catgories_id_fk` (`FK_user_categories`),
  KEY `User_User_Establishment_user_establishment_fk` (`FK_user_establishment`),
  KEY `User_Comments_comment_id_fk_idx` (`FK_comment`),
  CONSTRAINT `User_Comments_comment_id_fk` FOREIGN KEY (`FK_comment`) REFERENCES `Comments` (`FK_user`),
  CONSTRAINT `User_Login_login_id_fk` FOREIGN KEY (`FK_login_id`) REFERENCES `Login` (`login_id`),
  CONSTRAINT `User_User_Catgories_user_catgories_id_fk` FOREIGN KEY (`FK_user_categories`) REFERENCES `User_Catgeories` (`user_categories_id`),
  CONSTRAINT `User_User_Establishment_user_establishment_fk` FOREIGN KEY (`FK_user_establishment`) REFERENCES `User_Establishment` (`user_establishment`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Catgeories`
--

DROP TABLE IF EXISTS `User_Catgeories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User_Catgeories` (
  `user_categories_id` int(11) NOT NULL AUTO_INCREMENT,
  `FK_user` int(11) NOT NULL,
  `FK_categories` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_categories_id`),
  KEY `FK_usercategories_idx` (`FK_user`),
  KEY `FK_categoriesuser_idx` (`FK_categories`),
  CONSTRAINT `User_Categories_Categories_categories_id_fk` FOREIGN KEY (`FK_categories`) REFERENCES `Categories` (`id`),
  CONSTRAINT `User_Categories_User_user_id_fk` FOREIGN KEY (`FK_user`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Catgeories`
--

LOCK TABLES `User_Catgeories` WRITE;
/*!40000 ALTER TABLE `User_Catgeories` DISABLE KEYS */;
/*!40000 ALTER TABLE `User_Catgeories` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Cuisine`
--

LOCK TABLES `User_Cuisine` WRITE;
/*!40000 ALTER TABLE `User_Cuisine` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Establishment`
--

LOCK TABLES `User_Establishment` WRITE;
/*!40000 ALTER TABLE `User_Establishment` DISABLE KEYS */;
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-14 19:36:58
