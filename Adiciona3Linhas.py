import mysql.connector

try:
    # Estabelecer conexão com o banco de dados
    conexao = mysql.connector.connect(
        host='localhost',     # endereço do servidor MySQL
        database='projeto',     # nome do banco de dados
        user='root',    # nome de usuário do MySQL
        password='root'   # senha do usuário do MySQL
    )

    # Criar um objeto cursor para executar consultas SQL
    cursor = conexao.cursor()

    # Adicionar 3 usuários
    inserir_usuario = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    valores_usuarios = [
        ("João", "joao@aluno.unb.br", "123456"),
        ("Maria", "maria@aluno.unb.br", "abcdef"),
        ("Pedro", "pedro@aluno.unb.br", "qwerty")
    ]
    cursor.executemany(inserir_usuario, valores_usuarios)
    conexao.commit()

    # Adicionar 3 departamentos
    inserir_departamento = "INSERT INTO departamentos (nome,iddepartamentos) VALUES (%s,%s)"
    valores_departamentos = [
        ("Cic", 1),
        ("Est", 2),
        ("Mat", 3)
    ]
    cursor.executemany(inserir_departamento, valores_departamentos)
    conexao.commit()

    # Adicionar 3 disciplinas
    inserir_disciplina = "INSERT INTO disciplinas (nome, departamento_id) VALUES (%s, %s)"
    valores_disciplinas = [
        ("Banco de Dados", 1),
        ("Introducao a inteligencia Artificial", 1),
        ("Calculo 1", 3)
    ]
    cursor.executemany(inserir_disciplina, valores_disciplinas)
    conexao.commit()

    # Adicionar 3 professores
    inserir_professor = "INSERT INTO professores (name, departamento_id) VALUES (%s, %s)"
    valores_professores = [
        ("Li", 1),
        ("Pedro", 1),
        ("Carla", 3)
    ]
    cursor.executemany(inserir_professor, valores_professores)
    conexao.commit()

    # Adicionar 3 turmas
    inserir_turma = "INSERT INTO turmas (professor_id, disciplina_id) VALUES (%s, %s)"
    valores_turmas = [
        (1, 1),
        (2, 2),
        (3, 3)
    ]
    cursor.executemany(inserir_turma, valores_turmas)
    conexao.commit()

    # Adicionar 3 avaliações
    inserir_avaliacao = "INSERT INTO avaliacoes (userid, professor_id, nota, comentario, turma_id) VALUES (%s, %s, %s, %s, %s)"
    valores_avaliacoes = [
        (8, 1, 5, "Gostei", 1),
        (8, 6, 4, "tranquila", 2),
        (8, 6, 3, "ruim", 3)
    ]
    cursor.executemany(inserir_avaliacao, valores_avaliacoes)
    conexao.commit()

# Adicionar 3 denúncias
    inserir_denuncia = "INSERT INTO denuncias (usuario_id, avaliacao_id, motivo, status) VALUES (%s, %s, %s, %s)"
    valores_denuncias = [
        (1, 1, "Ofensivo", "pendente"),
        (2, 2, "Vazia", "pendente"),
        (3, 3, "Agressiva", "pendente")
    ]
    cursor.executemany(inserir_denuncia, valores_denuncias)
    conexao.commit()

except mysql.connector.Error as erro:
    print("Erro ao conectar ao MySQL:", erro)

finally:
    # Fechar o cursor e a conexão
    cursor.close()
    conexao.close()

print("Elementos adicionados com sucesso!")