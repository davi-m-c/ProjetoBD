# Cria Esquema projeto
CREATE SCHEMA `projeto`;

# Cria Tabela users
CREATE TABLE `users` (
  `idusers` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idusers`),
  UNIQUE KEY `unique_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

# Cria Tabela departamentos
CREATE TABLE `departamentos` (
  `iddepartamentos` int NOT NULL,
  `nome` varchar(45) NOT NULL,
  PRIMARY KEY (`iddepartamentos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

# Cria Tabela disciplinas
CREATE TABLE `disciplinas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  `departamento_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `departamento_id` (`departamento_id`),
  CONSTRAINT `disciplinas_ibfk_1` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`iddepartamentos`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

# Cria Tabela professores
CREATE TABLE `professores` (
  `idprofessores` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `departamento_id` int DEFAULT NULL,
  PRIMARY KEY (`idprofessores`),
  KEY `departamento_id` (`departamento_id`),
  CONSTRAINT `professores_ibfk_1` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`iddepartamentos`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

# Cria Tabela turmas
CREATE TABLE `turmas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `professor_id` int DEFAULT NULL,
  `disciplina_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `professor_id` (`professor_id`),
  KEY `disciplina_id` (`disciplina_id`),
  CONSTRAINT `turmas_ibfk_1` FOREIGN KEY (`professor_id`) REFERENCES `professores` (`idprofessores`),
  CONSTRAINT `turmas_ibfk_2` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

# Cria Tabela avaliacoes
CREATE TABLE `avaliacoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nota` int NOT NULL,
  `comentario` varchar(200) DEFAULT NULL,
  `userid` int DEFAULT NULL,
  `turma_id` int DEFAULT NULL,
  `professor_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userid_idx` (`userid`),
  KEY `fk_avaliacoes_turmas` (`turma_id`),
  KEY `fk_avaliacoes_professores` (`professor_id`),
  CONSTRAINT `fk_avaliacoes_professores` FOREIGN KEY (`professor_id`) REFERENCES `professores` (`idprofessores`),
  CONSTRAINT `fk_avaliacoes_turmas` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`),
  CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `users` (`idusers`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

# Cria Tabela denuncias
CREATE TABLE `denuncias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `avaliacao_id` int DEFAULT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `status` enum('pendente','avaliada') DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `avaliacao_id` (`avaliacao_id`),
  CONSTRAINT `denuncias_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `users` (`idusers`),
  CONSTRAINT `denuncias_ibfk_2` FOREIGN KEY (`avaliacao_id`) REFERENCES `avaliacoes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

# Cria o procedure new_procedure, que mostra as avaliacoes de um professor  
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_procedure`(varip int)
SELECT * FROM avaliacoes 
    WHERE professor_id = varip