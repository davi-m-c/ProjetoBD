# Cria Esquema projeto
CREATE SCHEMA `projeto`;

# Cria Tabela users
CREATE TABLE `users` (
  `idusers` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `matricula` varchar(255) DEFAULT NULL,
  `curso` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idusers`),
  UNIQUE KEY `unique_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

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

# Cria Tabela imagem
CREATE TABLE imagem (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) ,
    arquivo LONGBLOB ,
    PRIMARY KEY (id)
);

# Cria a view view_relacionamento, que mostra a medias das notas, o nome e a disciplina do professor
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_relacionamento` AS select `p`.`name` AS `professor_nome`,`d`.`nome` AS `disciplina_nome`,avg(`a`.`nota`) AS `media_nota` from (((`professores` `p` join `turmas` `t` on((`p`.`idprofessores` = `t`.`professor_id`))) join `disciplinas` `d` on((`t`.`disciplina_id` = `d`.`id`))) join `avaliacoes` `a` on((`t`.`id` = `a`.`turma_id`))) group by `p`.`name`,`d`.`nome`
