-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: database-1.c3uqbgd0mbrv.ap-south-1.rds.amazonaws.com    Database: haus
-- ------------------------------------------------------
-- Server version	8.0.32

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `bid`
--

DROP TABLE IF EXISTS `bid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bid` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `location` varchar(30) NOT NULL,
  `phone` bigint NOT NULL,
  `address` varchar(100) NOT NULL,
  `approval_status` varchar(30) NOT NULL,
  `timeline` varchar(30) NOT NULL,
  `sqft` varchar(40) NOT NULL,
  `budget` varchar(30) NOT NULL,
  `build_type` varchar(50) NOT NULL,
  `room` varchar(20) NOT NULL,
  `bricks` varchar(30) NOT NULL,
  `steel` varchar(30) NOT NULL,
  `cement` varchar(30) NOT NULL,
  `sand` varchar(30) NOT NULL,
  `wood` varchar(30) NOT NULL,
  `plumb` varchar(30) NOT NULL,
  `wires` varchar(30) NOT NULL,
  `floor` varchar(30) NOT NULL,
  `sanitary` varchar(30) NOT NULL,
  `paint` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bid`
--

LOCK TABLES `bid` WRITE;
/*!40000 ALTER TABLE `bid` DISABLE KEYS */;
INSERT INTO `bid` VALUES (14,1001,'MariSelvam','selva.nellai72@gmail.com','Tirunelveli',9385707886,'Saliyar street','Yes','Within 6 months','1500 sqft','20 lakhs','Single-family detached house','4','Concrete Bricks','JSW Steel','Valimai Cement','M-sand','Country Teakwood','Astral pipes','Plaza Cables','Cement Concrete Flooring','kohler','Nippon');
/*!40000 ALTER TABLE `bid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bidd`
--

DROP TABLE IF EXISTS `bidd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bidd` (
  `bid_id` int NOT NULL,
  `builderid` int NOT NULL,
  `buildername` varchar(30) NOT NULL,
  `userid` int NOT NULL,
  `username` varchar(30) NOT NULL,
  `bid` varchar(30) NOT NULL,
  `selects` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bidd`
--

LOCK TABLES `bidd` WRITE;
/*!40000 ALTER TABLE `bidd` DISABLE KEYS */;
INSERT INTO `bidd` VALUES (14,2,'Maharaja',1001,'MariSelvam','18 lakhs','Selected'),(14,1,'MariSelvam',1001,'MariSelvam','18 lakhs','not selected');
/*!40000 ALTER TABLE `bidd` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `builder`
--

LOCK TABLES `builder` WRITE;
/*!40000 ALTER TABLE `builder` DISABLE KEYS */;
INSERT INTO `builder` VALUES (1,'MariSelvam','vijaymari10131@gmail.com','9ee6916e0445335c0b4474fa4e15b339fe67ae8b3474c9c1cd60a705ea8c35d4','9ee6916e0445335c0b4474fa4e15b339fe67ae8b3474c9c1cd60a705ea8c35d4','Selva','Selva','Tirunelveli',9385707886,NULL,_binary 'img1.jpg'),(2,'Maharaja','maharaja190222@gmail.com','96385006174d6576e3996862cbceaf31d636a08f9adc13755e720075c88e501b','96385006174d6576e3996862cbceaf31d636a08f9adc13755e720075c88e501b','Raja','Raja','Tirunelveli',9632587014,NULL,_binary 'img4.jpg'),(3,'Anantha Krishnan','pananthakrishnan939@gmail.com','f65a52cf0c7723da9218a725b8b706de48face8ba50a7b6a20ac8edcb179a7dc','f65a52cf0c7723da9218a725b8b706de48face8ba50a7b6a20ac8edcb179a7dc','Anantha','Anantha','Tirunelveli',9512863470,7,_binary 'img3.jpg'),(5,'Manickavasagam','manickavasagam600@gmail.com','cc395883ac924839f26dac57e98b41e2a3bbd081129be1ede96a6f37dc71eedc','cc395883ac924839f26dac57e98b41e2a3bbd081129be1ede96a6f37dc71eedc','Manickam','Manickam','Tirunelveli',8523014769,NULL,_binary 'pexels-aleksandar-pasaric-2341830.jpg'),(6,'Kula Sekaran','smartsekar2006@gmail.com','bdbd0361a58e2bf348ab39cd52941d57fabd098e25f025aafa96a4c5275298e9','bdbd0361a58e2bf348ab39cd52941d57fabd098e25f025aafa96a4c5275298e9','Sekar','Sekar','Tirunelveli',9512368740,4,_binary 'pexels-jeremy-bishop-2422915.jpg'),(8,'Ganes','ganesanlakz007@gmail.com','5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5','5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5','Ganesh builders','University','Tenkasi',856321470,9,_binary '1103337 (1).jpg');
/*!40000 ALTER TABLE `builder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` int NOT NULL,
  `location` varchar(50) NOT NULL,
  `sqft` int NOT NULL,
  `build_type` varchar(50) NOT NULL,
  `budget` int NOT NULL,
  `room` varchar(20) NOT NULL,
  `image` blob NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES (6,1,'Tirunelveli',1500,'Single-family detached house',2000000,'3',_binary 'WhatsApp Image 2023-05-22 at 7.02.30 PM.jpeg','completed'),(7,1,'Tenkasi',2000,'Commercial buildings',1200000,'5',_binary 'WhatsApp Image 2023-05-22 at 7.24.44 PM.jpeg','In-progress'),(8,1,'Tirunelveli',2350,'Residential buildings/Apartments',3500000,'10',_binary 'WhatsApp Image 2023-05-22 at 7.24.42 PM.jpeg','In-progress'),(9,2,'Chennai',2500,'Commercial buildings',2000000,'6',_binary 'WhatsApp Image 2023-05-22 at 7.24.45 PM.jpeg','completed'),(10,2,'Tenkasi',1800,'Commercial buildings',5000000,'6',_binary 'WhatsApp Image 2023-05-22 at 7.24.46 PM.jpeg','In-progress');
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `material`
--

DROP TABLE IF EXISTS `material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `material` (
  `uid` int NOT NULL,
  `cement` varchar(30) NOT NULL,
  `steel` varchar(30) NOT NULL,
  `wood` varchar(30) NOT NULL,
  `bricks` varchar(30) NOT NULL,
  `floor` varchar(30) NOT NULL,
  `wires` varchar(30) NOT NULL,
  `sand` varchar(30) NOT NULL,
  `plumb` varchar(30) NOT NULL,
  `sanitary` varchar(30) NOT NULL,
  `paint` varchar(30) NOT NULL,
  `glass` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `material`
--

LOCK TABLES `material` WRITE;
/*!40000 ALTER TABLE `material` DISABLE KEYS */;
INSERT INTO `material` VALUES (1,'Ramco','TMT','Teak','Clay Bricks','Tiles','RR Cables','M-Sand','Astral pipes','kohler','Nippon','Glass'),(2,'sankar','agni tmt','Teak','Bricks','Tiles','RR Cables','M-Sand','Astral pipes','kohler','Nippon','Glass');
/*!40000 ALTER TABLE `material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (74,1004,1,'Hello','2023-05-08 18:45:05'),(75,1001,1,'Hai Mariselvam','2023-05-08 18:45:39'),(76,1,1001,'Hai Selva','2023-05-08 18:46:18'),(77,1001,1,'hlo','2023-05-08 18:48:43'),(78,1,1001,'hi','2023-05-09 15:54:30'),(79,1002,1,'Hi','2023-05-11 19:58:28'),(80,1,1002,'hello','2023-05-11 19:58:45'),(81,1002,1,'I am okay with your bid price for my requirement','2023-05-11 19:59:29'),(82,1,1002,'That\'s nice','2023-05-11 20:00:00'),(83,1,1002,'We always do best thing for best price definitely we will give a dream house for you','2023-05-11 20:00:37'),(84,1002,1,'Thank you','2023-05-11 20:00:56'),(85,1001,1,'Hai','2023-05-16 13:17:01'),(86,1002,3,'We always do best thing for best price definitely we will give a dream house for you','2023-05-16 13:39:03'),(87,1006,3,'Hello','2023-05-18 13:17:52'),(88,1006,3,'Hello','2023-05-18 13:17:53'),(89,1001,1,'hai','2023-05-22 15:36:01'),(90,1001,1,'Hello MariSelvam','2023-06-10 13:07:30'),(91,1001,1,'Hello MariSelvam','2023-06-10 13:07:31'),(92,1,1001,'Hello Selva','2023-06-12 12:11:42');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=1007 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1001,'Selva','selva.nellai72@gmail.com','b3190fd933e4acd88e3f293d06c47236c2f71237e81b0d62722b2fcdfbbd4298','b3190fd933e4acd88e3f293d06c47236c2f71237e81b0d62722b2fcdfbbd4298','Tirunelveli',9385707886,406757,_binary 'pexels-photo-1049622.jpeg'),(1002,'Maharaja','maharaja190222@gmail.com','96385006174d6576e3996862cbceaf31d636a08f9adc13755e720075c88e501b','96385006174d6576e3996862cbceaf31d636a08f9adc13755e720075c88e501b','Tirunelveli',9876543210,83,_binary 'pexels-sourav-mishra-3136673.jpg'),(1003,'Safeer Ali','msabeer208@gmail.com','ea878f959275275221fe94d8350da9a9d01d10b753cee5b835080e75474f44e4','ea878f959275275221fe94d8350da9a9d01d10b753cee5b835080e75474f44e4','Tirunelveli',9629141240,64,_binary 'WhatsApp Image 2023-03-14 at 12.51.42 PM.jpeg'),(1004,'Manickavasagam','manickavasagam600@gmail.com','cdeaad9dceca124e0e605cec3eafe99597572b3b4b94719a2238b8731901e484','cdeaad9dceca124e0e605cec3eafe99597572b3b4b94719a2238b8731901e484','Thanjavur',8838098841,39,_binary 'pexels-jeremy-bishop-2422915.jpg'),(1005,'Anantha Krishnan P','pananthakrishnan939@gmail.com','f65a52cf0c7723da9218a725b8b706de48face8ba50a7b6a20ac8edcb179a7dc','f65a52cf0c7723da9218a725b8b706de48face8ba50a7b6a20ac8edcb179a7dc','Tirunelveli',9876543210,38,_binary 'img4.jpg');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-27 10:21:53
