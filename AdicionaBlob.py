import mysql.connector

# Ler o arquivo de imagem como bytes
with open("./img/logoUnb.png", 'rb') as file:
    imagem_bytes = file.read()
with open("./img/bolha.jpg", 'rb') as file:
    imagem1_bytes = file.read()
with open("./img/raio.jpg", 'rb') as file:
    imagem2_bytes = file.read()

try:
    # Estabelecer conexão com o banco de dados
    conexao = mysql.connector.connect(
        host='localhost',
        database='projeto',
        user='root',
        password='root'
    )

    # Criar um objeto cursor para executar consultas SQL
    cursor = conexao.cursor()

    # Consulta SQL para inserir o BLOB no banco de dados
    consulta = "INSERT INTO imagem (nome, arquivo) VALUES (%s, %s)"

    # Executar a consulta com o valor do BLOB e o nome como parâmetros
    cursor.execute(consulta, ('logoUnb', imagem_bytes))

    # Consulta SQL para inserir o BLOB no banco de dados
    consulta = "INSERT INTO imagem (arquivo) VALUES (%s)"

    # Executar a consulta com o valor do BLOB como parâmetro
    cursor.execute(consulta, (imagem1_bytes,))

    # Consulta SQL para inserir o BLOB no banco de dados
    consulta = "INSERT INTO imagem (arquivo) VALUES (%s)"

    # Executar a consulta com o valor do BLOB como parâmetro
    cursor.execute(consulta, (imagem2_bytes,))

    # Confirmar a transação
    conexao.commit()

    print("Imagens adicionadas com sucesso!")

except mysql.connector.Error as erro:
    print("Erro ao conectar ao MySQL:", erro)

finally:
    # Fechar o cursor e a conexão
    cursor.close()
    conexao.close()
