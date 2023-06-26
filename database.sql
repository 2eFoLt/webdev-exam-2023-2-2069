-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_2069_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('5eeccc418601');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_authors_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authors`
--

LOCK TABLES `authors` WRITE;
/*!40000 ALTER TABLE `authors` DISABLE KEYS */;
INSERT INTO `authors` VALUES (2,'Геннадий Крокодил'),(4,'Кот Бегемот'),(1,'Палата №13'),(3,'Терентий');
/*!40000 ALTER TABLE `authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` text NOT NULL,
  `year` varchar(4) NOT NULL,
  `publishing_house` varchar(45) NOT NULL,
  `size` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  `cover_id` varchar(100) NOT NULL,
  `rating_sum` int(11) DEFAULT '0',
  `rating_num` int(11) DEFAULT '0',
  `visit_number` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_book_name` (`name`),
  KEY `genre_id` (`genre_id`),
  KEY `cover_id` (`cover_id`),
  KEY `fk_book_author_id_authors` (`author_id`),
  CONSTRAINT `fk_book_author_id_authors` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`),
  CONSTRAINT `fk_book_cover_id_cover` FOREIGN KEY (`cover_id`) REFERENCES `cover` (`id`),
  CONSTRAINT `fk_book_genre_id_genre` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (6,'От зарплаты до зарплаты','','2005','Новый дом',21,2,2,'0551b627-54b7-406d-8b90-d135be6e27cf',4,2,5),(7,'История одной пятилетки','Как завершить проект за 2 дня и не сойти с ума','2023','Плакали всей маршруткой',1,4,4,'7698ada9-f965-4b65-88a8-68a55186bbd7',8,2,10),(8,'Как проснуться к первой и не умереть','afa','2015','Политех',2,1,1,'c8bc4353-7ea2-4ef2-ac66-5e6b6964977e',9,3,8),(17,'Кто украл стипендию и другие сказки','Тестовое описание для книги','1914','Новый дом',11,3,3,'322a6671-bea5-45a8-af71-eb59797d6e38',4,1,1),(18,'AA','AA','1902','AA',28,2,3,'9fce6cad-70c8-4706-b9b6-0cc3b420db83',0,0,1),(19,'AB','AB','1903','AB',28,2,2,'9fce6cad-70c8-4706-b9b6-0cc3b420db83',0,0,1),(20,'AC','AC','1923','AC',14,4,3,'5a563ab4-38c6-412f-bb7f-e044be6954f0',0,0,2),(21,'AD','AD','1907','AD',14,2,1,'004b89bd-8202-4874-839a-51aa8e334fc8',0,0,4),(22,'AE','AE','1906','AE',14,1,1,'448f7266-a465-4208-ad00-4e188b1b2a27',0,0,2),(23,'AF','AF','1905','AF',28,4,3,'20ca88e8-49e3-404d-9c23-0b06ad57f8ba',0,0,2),(24,'AG','AG','1903','AG',28,1,3,'7c8fb3bd-1e8d-4eae-aeee-7094f4f3c544',0,0,2);
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_to_genre`
--

DROP TABLE IF EXISTS `book_to_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_to_genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) DEFAULT NULL,
  `genre_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_book_to_genre_book_id_book` (`book_id`),
  KEY `fk_book_to_genre_genre_id_genre` (`genre_id`),
  CONSTRAINT `fk_book_to_genre_book_id_book` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `fk_book_to_genre_genre_id_genre` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_to_genre`
--

LOCK TABLES `book_to_genre` WRITE;
/*!40000 ALTER TABLE `book_to_genre` DISABLE KEYS */;
INSERT INTO `book_to_genre` VALUES (1,6,3),(2,6,4),(3,7,1),(4,7,4),(15,8,1),(16,8,2),(17,8,4),(20,17,3),(21,17,1);
/*!40000 ALTER TABLE `book_to_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cover`
--

DROP TABLE IF EXISTS `cover`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cover` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(45) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cover`
--

LOCK TABLES `cover` WRITE;
/*!40000 ALTER TABLE `cover` DISABLE KEYS */;
INSERT INTO `cover` VALUES ('004b89bd-8202-4874-839a-51aa8e334fc8','dWIdiNvW-Cs.jpg','image/jpeg','8d7fcba64bce1d5d16ac5db02a8ddb9b'),('0551b627-54b7-406d-8b90-d135be6e27cf','aeRYdJPJwvY.jpg','image/jpeg','84b7cb589065694fbb49dfc740586011'),('07264526-fd8f-48f0-99a9-1b21abb635dd','YmasCcn8624.jpg','image/jpeg','65d25dbf5ec6a5768487c63c10c519d9'),('20ca88e8-49e3-404d-9c23-0b06ad57f8ba','splE2x2IFtI.jpg','image/jpeg','eb8ac8fe93168037e775288a090e600b'),('322a6671-bea5-45a8-af71-eb59797d6e38','o7_QbzOr3FA.jpg','image/jpeg','7648cf8983a6a761822db2b144868aa5'),('448f7266-a465-4208-ad00-4e188b1b2a27','bCd7CTSb3GQ.jpg','image/jpeg','368e5a8e05071c66d1ad71b1a1ad9986'),('5a563ab4-38c6-412f-bb7f-e044be6954f0','1i3XF4m_l8Y.jpg','image/jpeg','18c88563bf5753472064915434c66030'),('7698ada9-f965-4b65-88a8-68a55186bbd7','006.png','image/png','631232774914314ddd9c9edb37487537'),('7c8fb3bd-1e8d-4eae-aeee-7094f4f3c544','Q8upnC85pwQ.jpg','image/jpeg','85efae517f8da0eed7aced84e68463b7'),('9fce6cad-70c8-4706-b9b6-0cc3b420db83','1.PNG','image/png','223e940337723cf04166fbd478d66061'),('c8bc4353-7ea2-4ef2-ac66-5e6b6964977e','smvWkf0QPLA.jpg','image/jpeg','b22ac6409049627fbe28b3de2c13a95b');
/*!40000 ALTER TABLE `cover` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genre`
--

DROP TABLE IF EXISTS `genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genre_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genre`
--

LOCK TABLES `genre` WRITE;
/*!40000 ALTER TABLE `genre` DISABLE KEYS */;
INSERT INTO `genre` VALUES (3,'Детектив'),(1,'Научпоп'),(2,'Романтика'),(4,'Хоррор');
/*!40000 ALTER TABLE `genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text,
  `given_rating` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `fk_reviews_book_id_book` (`book_id`),
  CONSTRAINT `fk_reviews_book_id_book` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (44,'фцфмц',1,6,1,'2023-06-25 17:27:03'),(45,'фмц',5,7,1,'2023-06-25 17:27:08'),(46,'й3м3ейм',2,8,1,'2023-06-25 17:27:16'),(48,'*Moder markdown review*',3,7,3,'2023-06-25 20:43:16'),(49,'* li1\n* li2\n* li3\n* markdown test',3,8,3,'2023-06-25 20:44:11'),(50,'User review\n&lt;script&gt;SCRIPTED&lt;/script&gt;\nbleach test',3,6,2,'2023-06-25 20:44:59'),(51,'*&lt;script&gt;&lt;/script&gt;*\nbleach+EasyMD test',4,8,2,'2023-06-25 20:45:33'),(52,'Тестовая рецензия',4,17,1,'2023-06-26 00:48:29');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_roles_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin','full rights'),(2,'moder','partial rights'),(3,'user','plain user');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_login` (`login`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'root','pbkdf2:sha256:600000$2igivyaANJf9R2K1$e0fc95d7be099c01750548c72ddb1d31481e6dfdbe96f363fa853861919e1994','root','root','root',1),(2,'IvanovIvan','pbkdf2:sha256:600000$3uSHxqAQsSTAnKrq$b0217b90280bd5a4579500aa24c936bb1ffa8c0d6407319601ace9a8a16cd524','Иван','Иванович','Иванов',3),(3,'moder','pbkdf2:sha256:600000$TZV30PDc7YaJ4c01$2faf2a31b17ec5647d0b397baf16be97ed92838c52e3bb75cf914e7a7fecdc30','moder','moder','moder',2);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visit_stat`
--

DROP TABLE IF EXISTS `visit_stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visit_stat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `visit_number` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_visit_stat_book_id_book` (`book_id`),
  KEY `fk_visit_stat_user_id_users` (`user_id`),
  CONSTRAINT `fk_visit_stat_book_id_book` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `fk_visit_stat_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visit_stat`
--

LOCK TABLES `visit_stat` WRITE;
/*!40000 ALTER TABLE `visit_stat` DISABLE KEYS */;
INSERT INTO `visit_stat` VALUES (4,7,3,10,'2023-06-20 16:08:36'),(5,8,3,8,'2023-06-04 16:08:36'),(6,6,3,5,'2023-06-17 16:08:36'),(7,20,3,2,'2023-06-21 16:08:36'),(8,22,3,2,'2023-06-08 16:08:36'),(9,23,3,2,'2023-06-26 16:08:36'),(10,19,3,1,'2023-06-04 16:08:36'),(11,24,3,2,'2023-06-01 16:08:36'),(12,18,3,1,'2023-06-02 16:08:36'),(13,17,3,1,'2023-06-03 16:08:36'),(14,21,3,4,'2023-06-25 16:08:36');
/*!40000 ALTER TABLE `visit_stat` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-26 16:20:23
