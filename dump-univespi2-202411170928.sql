-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 145.223.31.145    Database: univespi2
-- ------------------------------------------------------
-- Server version	5.5.5-10.6.18-MariaDB-0ubuntu0.22.04.1

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
-- Table structure for table `compartilhamento`
--

DROP TABLE IF EXISTS `compartilhamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compartilhamento` (
  `usuorigem` int(11) NOT NULL,
  `usudestino` int(11) NOT NULL,
  `autorizar` tinyint(1) DEFAULT NULL,
  KEY `compartilhamento_usuarios_FK` (`usuorigem`),
  KEY `compartilhamento_usuarios_FK_1` (`usudestino`),
  CONSTRAINT `compartilhamento_usuarios_FK` FOREIGN KEY (`usuorigem`) REFERENCES `usuarios` (`codusuario`),
  CONSTRAINT `compartilhamento_usuarios_FK_1` FOREIGN KEY (`usudestino`) REFERENCES `usuarios` (`codusuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compartilhamento`
--

LOCK TABLES `compartilhamento` WRITE;
/*!40000 ALTER TABLE `compartilhamento` DISABLE KEYS */;
INSERT INTO `compartilhamento` VALUES (47,48,1),(47,49,1),(49,48,1),(48,47,1);
/*!40000 ALTER TABLE `compartilhamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dadosusuario`
--

DROP TABLE IF EXISTS `dadosusuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dadosusuario` (
  `codusuario` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `dtnascimento` date NOT NULL,
  PRIMARY KEY (`codusuario`),
  CONSTRAINT `dadosusuario_usuarios_FK` FOREIGN KEY (`codusuario`) REFERENCES `usuarios` (`codusuario`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dadosusuario`
--

LOCK TABLES `dadosusuario` WRITE;
/*!40000 ALTER TABLE `dadosusuario` DISABLE KEYS */;
INSERT INTO `dadosusuario` VALUES (47,'001 completo','1901-01-01'),(48,'002 completo','1900-01-01'),(49,'003 completo','1900-01-01'),(50,'004usuario','1900-01-01');
/*!40000 ALTER TABLE `dadosusuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registros`
--

DROP TABLE IF EXISTS `registros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registros` (
  `codregistro` int(11) NOT NULL AUTO_INCREMENT,
  `pesokg` float NOT NULL,
  `alturam` float NOT NULL,
  `dtregistro` datetime NOT NULL,
  `regcodusuario` int(11) NOT NULL,
  PRIMARY KEY (`codregistro`),
  KEY `registros_usuarios_FK` (`regcodusuario`),
  CONSTRAINT `registros_usuarios_FK` FOREIGN KEY (`regcodusuario`) REFERENCES `usuarios` (`codusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros`
--

LOCK TABLES `registros` WRITE;
/*!40000 ALTER TABLE `registros` DISABLE KEYS */;
INSERT INTO `registros` VALUES (70,70,1.7,'2024-01-01 00:00:00',47),(71,72,1.7,'2024-02-01 00:00:00',47),(72,74,1.7,'2024-03-01 00:00:00',47),(73,73,1.7,'2024-04-01 00:00:00',47),(74,78,1.7,'2024-05-01 00:00:00',47),(75,80,1.7,'2024-06-01 00:00:00',47),(76,82,1.7,'2024-07-01 00:00:00',47),(77,84,1.7,'2024-08-01 00:00:00',47),(78,86,1.7,'2024-09-01 00:00:00',47),(79,88,1.7,'2024-10-01 00:00:00',47),(80,90,1.7,'2024-11-01 00:00:00',47),(81,65,1.6,'2023-01-01 00:00:00',48),(82,67,1.6,'2023-02-01 00:00:00',48),(83,69,1.6,'2023-03-01 00:00:00',48),(84,71,1.6,'2023-04-01 00:00:00',48),(85,73,1.6,'2023-05-01 00:00:00',48),(86,75,1.6,'2023-06-01 00:00:00',48),(87,77,1.6,'2023-07-01 00:00:00',48),(88,79,1.6,'2023-08-01 00:00:00',48),(89,81,1.6,'2023-09-01 00:00:00',48),(90,83,1.6,'2023-10-01 00:00:00',48),(91,85,1.6,'2023-11-01 00:00:00',48),(92,87,1.6,'2023-12-01 00:00:00',48);
/*!40000 ALTER TABLE `registros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sugestoes`
--

DROP TABLE IF EXISTS `sugestoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sugestoes` (
  `idmsg` int(11) NOT NULL AUTO_INCREMENT,
  `de` int(11) NOT NULL,
  `para` int(11) NOT NULL,
  `dt` datetime NOT NULL,
  `mensagem` text NOT NULL,
  PRIMARY KEY (`idmsg`),
  KEY `sugestoes_usuarios_FK` (`de`),
  KEY `sugestoes_usuarios_FK_1` (`para`),
  CONSTRAINT `sugestoes_usuarios_FK` FOREIGN KEY (`de`) REFERENCES `usuarios` (`codusuario`) ON UPDATE CASCADE,
  CONSTRAINT `sugestoes_usuarios_FK_1` FOREIGN KEY (`para`) REFERENCES `usuarios` (`codusuario`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sugestoes`
--

LOCK TABLES `sugestoes` WRITE;
/*!40000 ALTER TABLE `sugestoes` DISABLE KEYS */;
INSERT INTO `sugestoes` VALUES (2,48,47,'2024-11-17 00:35:08','1º: foco em carga – muita intensidade!\r\nA: Ombros, peito e tríceps;\r\n\r\nB: Bíceps, costas e abdômen;\r\n\r\nC: Treino de pernas completo.'),(3,47,48,'2024-11-17 00:35:48','1º: foco em carga – muita intensidade!\r\nA: Ombros, peito e tríceps;\r\n\r\nB: Bíceps, costas e abdômen;\r\n\r\nC: Treino de pernas completo.\r\n\r\n1º: foco em carga – muita intensidade!\r\nA: Ombros, peito e tríceps;\r\n\r\nB: Bíceps, costas e abdômen;\r\n\r\nC: Treino de pernas completo.\r\n1º: foco em carga – muita intensidade!\r\nA: Ombros, peito e tríceps;\r\n\r\nB: Bíceps, costas e abdômen;\r\n\r\nC: Treino de pernas completo.\r\n\r\n\r\n1º: foco em carga – muita intensidade!\r\nA: Ombros, peito e tríceps;\r\n\r\nB: Bíceps, costas e abdômen;\r\n\r\nC: Treino de pernas completo.\r\n1º: foco em carga – muita intensidade!\r\nA: Ombros, peito e tríceps;\r\n\r\nB: Bíceps, costas e abdômen;\r\n\r\nC: Treino de pernas completo.');
/*!40000 ALTER TABLE `sugestoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `codusuario` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `senha` varchar(128) NOT NULL,
  `nome` varchar(255) NOT NULL,
  PRIMARY KEY (`codusuario`),
  UNIQUE KEY `email_unique` (`email`),
  UNIQUE KEY `usuarios_unique` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (47,'001@001.com','001','001'),(48,'002@002.com','002','002'),(49,'003@003.com','003','003'),(50,'004@004.com','004','004usuario');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'univespi2'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-17  9:28:20
