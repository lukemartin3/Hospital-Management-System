-- MySQL dump 10.13  Distrib 8.0.32, for macos13 (x86_64)
--
-- Host: localhost    Database: fsedb
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `pin` varchar(4) NOT NULL,
  `fname` varchar(45) NOT NULL,
  `lname` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `dob` date NOT NULL,
  `phone` varchar(12) NOT NULL,
  `address` varchar(45) NOT NULL,
  `city` varchar(45) NOT NULL,
  `states` varchar(45) NOT NULL,
  `zip` varchar(5) NOT NULL,
  `insurance` varchar(45) NOT NULL,
  `history` varchar(255) NOT NULL,
  `billing` decimal(10,2) DEFAULT '0.00',
  `roles` tinyint(1) DEFAULT '1',
  `specialization` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('admin','pbkdf2:sha256:260000$uL82lL7uLgWLA2zN$112bd7b4bfdba2d8a2f061a4289bccfc490fb03078a7c9a20f9d109e0c07b5f6','5020','Luke','Martin','admin@mail.com','2000-10-28','712-281-4090','5020 Christy Rd','Sioux City','IA','51106','Blue Cross Blue Shield','Shellfish',0.00,0,NULL),('drluke','pbkdf2:sha256:260000$vPGqfFZX0inTkET5$e62fa01cffd70577f702cb8bae21e09791f0ba00cf94b00fb99a7d3971244d94','5020','Luke','Martin','doctor@mail.com','2000-10-28','712-281-4090','5020 Christy Rd','Sioux City','IA','51106','Blue Cross Blue Shield','Shellfish',0.00,3,NULL),('lmartin9','pbkdf2:sha256:260000$1yx7ooktSiW0adnN$c68167d4cdbb5e3794a81e0e0386cd8a73c8cf0fc3dea975613aaece34a7bd36','5020','Luke','Martin','lmart5020@gmail.com','2000-10-28','712-281-4090','5020 Christy Rd','Sioux City','IA','51106','Blue Cross Blue Shield','Shellfish',0.00,1,NULL),('nurseluke','pbkdf2:sha256:260000$trdmpgxW2jndm0RL$0bdf95de3901d074cc0d7319317f73ddd5fb5d09859c4c856fb380b8c807262b','5020','Luke','Martin','nurse@mail.com','2000-10-28','712-281-4090','5020 Christy Rd','Sioux City','IA','51106','Blue Cross Blue Shield','Shellfish',0.00,2,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-21  0:02:38
