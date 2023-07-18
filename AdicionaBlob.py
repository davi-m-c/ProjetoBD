import mysql.connector

# Ler o arquivo de imagem como bytes
with open("./img/logoUnb.png", 'rb') as file:
    imagem_bytes = file.read()
with open("./img/bolha.jpg", 'rb') as file:
    imagem1_bytes = file.read()
with open("./img/raio.jpg", 'rb') as file:
    imagem2_bytes = file.read()

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
consulta = "INSERT INTO imagem (nome,arquivo) VALUES (logoUnb,%s)"

# Executar a consulta com o valor do BLOB como parâmetro
cursor.execute(consulta, (imagem_bytes,))
# Consulta SQL para inserir o BLOB no banco de dados
consulta = "INSERT INTO imagem (arquivo) VALUES (bolha,%s)"

# Executar a consulta com o valor do BLOB como parâmetro
cursor.execute(consulta, (imagem1_bytes,))
# Consulta SQL para inserir o BLOB no banco de dados
consulta = "INSERT INTO imagem (arquivo) VALUES (raio,%s)"

# Executar a consulta com o valor do BLOB como parâmetro
cursor.execute(consulta, (imagem2_bytes,))

# Confirmar a transação
conexao.commit()

# Fechar o cursor e a conexão
cursor.close()
conexao.close()
