-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: haus
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
-- Table structure for table `bit`
--

DROP TABLE IF EXISTS `bit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `location` varchar(30) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone` bigint NOT NULL,
  `approval_status` varchar(30) NOT NULL,
  `timeline` varchar(30) NOT NULL,
  `sqft` varchar(10) NOT NULL,
  `build_type` varchar(50) NOT NULL,
  `budget` int NOT NULL,
  `wood` varchar(50) NOT NULL,
  `room` int NOT NULL,
  `additional` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bit`
--

LOCK TABLES `bit` WRITE;
/*!40000 ALTER TABLE `bit` DISABLE KEYS */;
INSERT INTO `bit` VALUES (1,4,'Manickavasagam','selva.nellai72@gmail.com','Thanjavur','address',9385707886,'No','Within 6 months','5000','Commercial buildings',2000000,'Without furniture',5,'Additional Information','Solved'),(2,1,'Selva','selva.nellai72@gmail.com','Tirunelveli','address',9385707886,'No','Within 1 year','5000','Commercial buildings',5000000,'Without furniture',5,'Additional','Assigned');
/*!40000 ALTER TABLE `bit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `builder`
--

DROP TABLE IF EXISTS `builder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `builder` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `hashed_password` varchar(100) NOT NULL,
  `hashed_conpassword` varchar(100) NOT NULL,
  `companyname` varchar(100) NOT NULL,
  `industry` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `phone` bigint NOT NULL,
  `reset_otp` int DEFAULT NULL,
  `image` blob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `builder`
--

LOCK TABLES `builder` WRITE;
/*!40000 ALTER TABLE `builder` DISABLE KEYS */;
INSERT INTO `builder` VALUES (1,'MariSelvam','vijaymari10131@gmail.com','fbc835d2c63c85a2af298286581b9b77e8f1d5436a7ccbe391fceecce2a4729e','fbc835d2c63c85a2af298286581b9b77e8f1d5436a7ccbe391fceecce2a4729e','Selva','Selva','Tirunelveli',9385707886,NULL,_binary 'img1.jpg'),(2,'Maharaja','maharaja190222@gmail.com','96385006174d6576e3996862cbceaf31d636a08f9adc13755e720075c88e501b','96385006174d6576e3996862cbceaf31d636a08f9adc13755e720075c88e501b','Raja','Raja','Tirunelveli',9632587014,NULL,_binary 'img4.jpg'),(3,'Anantha Krishnan','pananthakrishnan939@gmail.com','f65a52cf0c7723da9218a725b8b706de48face8ba50a7b6a20ac8edcb179a7dc','f65a52cf0c7723da9218a725b8b706de48face8ba50a7b6a20ac8edcb179a7dc','Anantha','Anantha','Tirunelveli',9512863470,7,_binary 'img3.jpg'),(5,'Manickavasagam','manickavasagam600@gmail.com','cc395883ac924839f26dac57e98b41e2a3bbd081129be1ede96a6f37dc71eedc','cc395883ac924839f26dac57e98b41e2a3bbd081129be1ede96a6f37dc71eedc','Manickam','Manickam','Tirunelveli',8523014769,NULL,_binary 'pexels-aleksandar-pasaric-2341830.jpg'),(6,'Kula Sekaran','smartsekar2006@gmail.com','bdbd0361a58e2bf348ab39cd52941d57fabd098e25f025aafa96a4c5275298e9','bdbd0361a58e2bf348ab39cd52941d57fabd098e25f025aafa96a4c5275298e9','Sekar','Sekar','Tirunelveli',9512368740,4,_binary 'pexels-jeremy-bishop-2422915.jpg');
/*!40000 ALTER TABLE `builder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` int NOT NULL,
  `image` blob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (1,2,_binary 'img1.jpg'),(2,1,_binary 'img7.jpg'),(3,1,_binary 'img5.jpg'),(4,1,_binary 'img9.jpg'),(5,1,_binary 'img1.jpg'),(6,1,_binary 'img19.jpg'),(7,1,_binary 'img6.jpg'),(8,1,_binary 'img7.jpg'),(9,2,_binary 'img1.jpg'),(10,2,_binary 'img20.jpg'),(11,2,_binary 'img18.jpg');
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `hashed_password` varchar(100) NOT NULL,
  `hashed_conpassword` varchar(100) NOT NULL,
  `location` varchar(50) NOT NULL,
  `phone` bigint NOT NULL,
  `reset_otp` int DEFAULT NULL,
  `image` blob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Selva','selva.nellai72@gmail.com','8b22ffae8cb82195c2102efada37b19842cd3c7fb1906bdd70af1496861d284f','8b22ffae8cb82195c2102efada37b19842cd3c7fb1906bdd70af1496861d284f','Tirunelveli',9385707886,306898,_binary 'pexels-mentatdgt-1049622.jpg'),(2,'Maharaja','maharaja190222@gmail.com','96385006174d6576e3996862cbceaf31d636a08f9adc13755e720075c88e501b','96385006174d6576e3996862cbceaf31d636a08f9adc13755e720075c88e501b','Tirunelveli',9875462150,NULL,_binary 'pexels-sourav-mishra-3136673.jpg'),(4,'Manickavasagam','manickavasagam600@gmail.com','cdeaad9dceca124e0e605cec3eafe99597572b3b4b94719a2238b8731901e484','cdeaad9dceca124e0e605cec3eafe99597572b3b4b94719a2238b8731901e484','Thanjavur',9514728630,99,_binary 'tree-736885__480.jpg'),(5,'Anantha Krishnan P','pananthakrishnan939@gmail.com','f65a52cf0c7723da9218a725b8b706de48face8ba50a7b6a20ac8edcb179a7dc','f65a52cf0c7723da9218a725b8b706de48face8ba50a7b6a20ac8edcb179a7dc','Tirunelveli',9638527014,43,_binary 'img8.png'),(6,'Safeer','msabeer208@gmail.com','ea878f959275275221fe94d8350da9a9d01d10b753cee5b835080e75474f44e4','ea878f959275275221fe94d8350da9a9d01d10b753cee5b835080e75474f44e4','Tirunelveli',8838098841,92,_binary 'WhatsApp Image 2023-03-14 at 12.51.42 PM.jpeg'),(7,'Jothi Mani','subramanian2841974@gmail.com','1a13d23042ca89dbeac5963b982c7e89826dccb9b0802cb62a6a9d319b2a31f8','1a13d23042ca89dbeac5963b982c7e89826dccb9b0802cb62a6a9d319b2a31f8','Tirunelveli',6383318275,59,_binary '1103337 (1).jpg');
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

-- Dump completed on 2023-04-06 17:30:39
