import tkinter as tk
from tkinter import ttk
import mysql.connector
from PIL import ImageTk, Image

imagem = Image.open("./img/logoUnb.png")
imagem = imagem.resize((150, 90))

texto_avaliacoes = None

def verificar_senha(usuario_id, senha):
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

        # Consultar a senha do usuário
        consulta_senha = "SELECT password FROM users WHERE idusers = %s"
        cursor.execute(consulta_senha, (usuario_id,))
        resultado_senha = cursor.fetchone()

        if resultado_senha is None:
            print("Usuário não encontrado!")
            return False

        senha_correta = resultado_senha[0]

        # Verificar se a senha digitada pelo usuário corresponde à senha armazenada no banco de dados
        if senha == senha_correta:
            return True
        else:
            print("Senha incorreta!")
            return False

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)

def verificar_e_atualizar():
    senha = entry_senha.get()
    usuario_id = entry_usuario_id.get()

    if verificar_senha(usuario_id, senha):

        # Obter os valores atuais da avaliação
        nota_atual = entry_nota.get()
        comentario_atual = entry_comentario.get()

        # Criar uma janela para editar a avaliação
        janela_editar = tk.Toplevel()
        janela_editar.title("Editar Avaliação")

        label_nota = ttk.Label(janela_editar, text="Nova Nota:")
        label_nota.pack()
        entry_nova_nota = ttk.Entry(janela_editar)
        entry_nova_nota.insert(tk.END, nota_atual)
        entry_nova_nota.pack()

        label_comentario = ttk.Label(janela_editar, text="Novo Comentário:")
        label_comentario.pack()
        entry_novo_comentario = ttk.Entry(janela_editar)
        entry_novo_comentario.insert(tk.END, comentario_atual)
        entry_novo_comentario.pack()

        # Função para atualizar a avaliação no banco de dados
        def atualizar_avaliacao():
            nova_nota = entry_nova_nota.get()
            novo_comentario = entry_novo_comentario.get()

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

                # Atualizar os valores da avaliação no banco de dados
                atualizar_query = """
                    UPDATE avaliacoes
                    SET nota = %s, comentario = %s
                    WHERE idavaliacoes = %s
                """
                valores = (nova_nota, novo_comentario, avaliacao_id)
                cursor.execute(atualizar_query, valores)
                conexao.commit()

                # Fechar o cursor e a conexão
                cursor.close()
                conexao.close()

                # Atualizar a exibição das avaliações
                mostrar_avaliacoes_usuario()

                # Fechar a janela de edição
                janela_editar.destroy()

            except mysql.connector.Error as erro:
                print("Erro ao conectar ao MySQL:", erro)

        # Botão para atualizar a avaliação
        botao_atualizar = ttk.Button(janela_editar, text="Atualizar", command=atualizar_avaliacao)
        botao_atualizar.pack()

# Função para mostrar as avaliações do usuário
def mostrar_avaliacoes_usuario():
    usuario_id = entry_usuario_id.get()

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

        # Consulta para obter as avaliações do usuário
        consulta = "SELECT * FROM avaliacoes WHERE userid = %s"
        cursor.execute(consulta, (usuario_id,))  # <- Adicione uma vírgula após (usuario_id,)
        resultados = cursor.fetchall()

        # Limpar a caixa de texto antes de exibir as avaliações
        texto_avaliacoes_usuario.delete("1.0", tk.END)

        # Exibir as avaliações na caixa de texto
        for avaliacao in resultados:
            texto_avaliacoes_usuario.insert(tk.END, f"ID: {avaliacao[0]}\n")
            texto_avaliacoes_usuario.insert(tk.END, f"Nota: {avaliacao[1]}\n")
            texto_avaliacoes_usuario.insert(tk.END, f"Comentário: {avaliacao[2]}\n")
            texto_avaliacoes_usuario.insert(tk.END, "-" * 30 + "\n")

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

    except mysql.connector.Error as erro:
        texto_avaliacoes_usuario.delete("1.0", tk.END)
        texto_avaliacoes_usuario.insert(tk.END, f"Erro ao conectar ao MySQL: {erro}")


def mostrar_avaliacoes():
    global texto_avaliacoes
    professor_id = entry_professorId.get()

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

        # Consulta para obter as avaliações do professor
        consulta = "CALL new_procedure(%s)"
        cursor.execute(consulta, (professor_id,))
        resultados = cursor.fetchall()

        # Limpar a caixa de texto antes de exibir as avaliações
        texto_avaliacoes.delete("1.0", tk.END)

        # Exibir as avaliações na caixa de texto
        for avaliacao in resultados:
            texto_avaliacoes.insert(tk.END, f"ID: {avaliacao[0]}\n")
            texto_avaliacoes.insert(tk.END, f"Nota: {avaliacao[1]}\n")
            texto_avaliacoes.insert(tk.END, f"Comentário: {avaliacao[2]}\n")
            texto_avaliacoes.insert(tk.END, "-" * 30 + "\n")

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

    except mysql.connector.Error as erro:
        texto_avaliacoes.insert(tk.END, f"Erro ao conectar ao MySQL: {erro}")

def criar_avaliacao():
    # Obter os valores inseridos pelo usuário
    email = entry_email.get()
    nota = entry_nota.get()
    comentario = entry_comentario.get()
    turma_id = entry_turma_id.get()  # Obter o ID da turma fornecido pelo usuário
    professor_id = entry_professorId.get()  # Obter o valor do ID do professor

    # Verificar se o ID do professor foi fornecido
    if not professor_id:
        print("ID do professor não fornecido!")
        return

    try:
        professor_id = int(professor_id)  # Converter o valor para um inteiro

        # Estabelecer conexão com o banco de dados
        conexao = mysql.connector.connect(
            host='localhost',     # endereço do servidor MySQL
            database='projeto',     # nome do banco de dados
            user='root',    # nome de usuário do MySQL
            password='root'   # senha do usuário do MySQL
        )

        # Criar um objeto cursor para executar consultas SQL
        cursor = conexao.cursor()

        # Obter o ID do usuário com base no email
        query_id_usuario = "SELECT idusers FROM users WHERE email = %s"
        cursor.execute(query_id_usuario, (email,))
        resultado_id_usuario = cursor.fetchone()
        if resultado_id_usuario is None:
            print("Usuário não encontrado!")
            return

        # Extrair o ID do usuário
        usuario_id = resultado_id_usuario[0]

        # Converter valores para o tipo adequado
        usuario_id = int(usuario_id)
        professor_id = int(professor_id)
        turma_id = int(turma_id)
        nota = int(nota)

        # Executar a instrução de inserção SQL com o ID da turma e do professor
        inserir_query = "INSERT INTO avaliacoes (userid, professor_id, nota, comentario, turma_id) VALUES (%s, %s, %s, %s, %s)"
        valores = (usuario_id, professor_id, nota, comentario, turma_id)
        cursor.execute(inserir_query, valores)

        # Confirmar as alterações no banco de dados
        conexao.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

        print("Avaliação criada com sucesso!")

    except ValueError:
        print("ID do professor inválido! O ID deve ser um número inteiro.")

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)





def fazer_login():
    email = entry_email.get()
    senha = entry_senha.get()

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

        # Executar uma consulta SQL para verificar o login usando o campo "email"
        consulta = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(consulta, (email, senha))

        # Obter o resultado da consulta
        resultado = cursor.fetchone()

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

        # Verificar se o login foi bem-sucedido
        if  resultado :
            label_status["text"] = "Login bem-sucedido!"
            exibir_pagina_principal()
        else:
            label_status["text"] = "Usuário ou senha incorretos."

    except mysql.connector.Error as erro:
        label_status["text"] = "Erro ao conectar ao MySQL: " + str(erro)

def fazer_registro():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()

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

        # Executar uma consulta SQL para inserir os dados de registro
        consulta = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        valores = (nome, email, senha)
        cursor.execute(consulta, valores)

        # Confirmar as alterações no banco de dados
        conexao.commit()

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

        label_status["text"] = "Registro bem-sucedido!"

    except mysql.connector.Error as erro:
        label_status["text"] = "Erro ao conectar ao MySQL: " + str(erro)

def exibir_turmas():
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

        # Consulta para obter as turmas com o nome do professor e o nome da disciplina
        consulta_turmas = """
            SELECT turmas.id, professores.name, disciplinas.nome
            FROM turmas
            JOIN professores ON turmas.professor_id = professores.idprofessores
            JOIN disciplinas ON turmas.disciplina_id = disciplinas.id
        """
        cursor.execute(consulta_turmas)
        resultados_turmas = cursor.fetchall()

        # Limpar a árvore antes de exibir as turmas
        treeview_turmas.delete(*treeview_turmas.get_children())

        # Exibir as turmas na árvore
        for turma in resultados_turmas:
            id_turma = turma[0]
            nome_professor = turma[1]  # Nome do professor
            nome_disciplina = turma[2]  # Nome da disciplina

            # Adicionar a turma à árvore
            treeview_turmas.insert('', 'end', values=(id_turma, nome_professor, nome_disciplina))

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)



def exibir_avaliacoes(event):
    # Obter o item selecionado na árvore de turmas
    item_selecionado = treeview_turmas.selection()
    if item_selecionado:
        # Obter os valores da turma selecionada
        valores_turma = treeview_turmas.item(item_selecionado)['values']
        id_turma = valores_turma[0]

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

            # Consulta para obter as avaliações da turma
            consulta_avaliacoes = "SELECT * FROM avaliacoes WHERE turma_id = %s"
            cursor.execute(consulta_avaliacoes, (id_turma,))
            resultados_avaliacoes = cursor.fetchall()

            # Limpar a árvore antes de exibir as avaliações
            treeview_avaliacoes.delete(*treeview_avaliacoes.get_children())

            # Exibir as avaliações na árvore
            for avaliacao in resultados_avaliacoes:
                id_avaliacao = avaliacao[0]
                nota_avaliacao = avaliacao[1]
                comentario_avaliacao = avaliacao[2]

                # Adicionar a avaliação à árvore
                treeview_avaliacoes.insert('', 'end', values=(id_avaliacao, nota_avaliacao, comentario_avaliacao))

            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()

        except mysql.connector.Error as erro:
            print("Erro ao conectar ao MySQL:", erro)

def criar_denuncia():
    # Obter a avaliação selecionada na árvore de avaliações
    item_selecionado = treeview_avaliacoes.selection()
    if item_selecionado:
        # Obter os valores da avaliação selecionada
        valores_avaliacao = treeview_avaliacoes.item(item_selecionado)['values']
        id_avaliacao = valores_avaliacao[0]

        # Criar uma nova janela para criar a denúncia
        janela_denuncia = tk.Toplevel(janela)
        janela_denuncia.title("Criar Denúncia")

        # Campos de entrada para a denúncia
        label_motivo = ttk.Label(janela_denuncia, text="Motivo:")
        label_motivo.pack()
        entry_motivo = ttk.Entry(janela_denuncia)
        entry_motivo.pack()

        label_status = ttk.Label(janela_denuncia, text="Status:")
        label_status.pack()
        entry_status = ttk.Entry(janela_denuncia)
        entry_status.pack()

        # Botão para salvar a denúncia
        botao_salvar_denuncia = ttk.Button(janela_denuncia, text="Salvar Denúncia", command=lambda: salvar_denuncia(id_avaliacao, entry_motivo.get(), entry_status.get()))
        botao_salvar_denuncia.pack()

        def salvar_denuncia(id_avaliacao, motivo, status):
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

                # Inserir a denúncia no banco de dados
                inserir_denuncia = "INSERT INTO denuncias (avaliacao_id, motivo, status) VALUES (%s, %s, %s)"
                valores_denuncia = (id_avaliacao, motivo, status)
                cursor.execute(inserir_denuncia, valores_denuncia)
                conexao.commit()

                # Fechar o cursor e a conexão
                cursor.close()
                conexao.close()

                # Fechar a janela de denúncia
                janela_denuncia.destroy()

                print("Denúncia criada com sucesso!")

            except mysql.connector.Error as erro:
                print("Erro ao conectar ao MySQL:", erro)

        # Execução do loop principal da janela de denúncia
        janela_denuncia.mainloop()

def exibir_pagina_principal():
    global entry_email, entry_nota, entry_comentario, entry_turma_id, entry_professorId, texto_avaliacoes, entry_usuario_id, texto_avaliacoes_usuario, treeview_turmas, treeview_avaliacoes
    # Criar uma nova janela para a página principal
    janela_principal =  tk.Toplevel()
    janela_principal.title("Criar Avaliação")
    abas = ttk.Notebook(janela_principal)
    
    aba_criar = ttk.Frame(abas)

    label_email = ttk.Label(aba_criar, text="Email:")
    label_email.pack()
    entry_email = ttk.Entry(aba_criar)
    entry_email.pack()

    label_nota = ttk.Label(aba_criar, text="Nota:")
    label_nota.pack()
    entry_nota = ttk.Entry(aba_criar)
    entry_nota.pack()

    label_comentario = ttk.Label(aba_criar, text="Comentário:")
    label_comentario.pack()
    entry_comentario = ttk.Entry(aba_criar)
    entry_comentario.pack()

    label_comentario = ttk.Label(aba_criar, text="Id da turma:")
    label_comentario.pack()
    entry_turma_id = ttk.Entry(aba_criar)
    entry_turma_id.pack()

    label_comentario = ttk.Label(aba_criar, text="ID do Professor:")
    label_comentario.pack()
    entry_professorId = ttk.Entry(aba_criar)
    entry_professorId.pack()

    botao_criar_avaliacao = ttk.Button(aba_criar, text="Criar Avaliação", command=criar_avaliacao)
    botao_criar_avaliacao.pack()
    
    abas.add(aba_criar, text="Criar Avaliacao")

    aba_ver = ttk.Frame(abas)

    # Rótulo e campo de entrada para o ID do professor
    label_professor_id = ttk.Label(aba_ver, text="ID do Professor:")
    label_professor_id.pack()
    entry_professor_id = ttk.Entry(aba_ver)
    entry_professor_id.pack()

    # Botão para mostrar as avaliações do professor
    botao_mostrar_avaliacoes = ttk.Button(aba_ver, text="Mostrar Avaliações", command=mostrar_avaliacoes)
    botao_mostrar_avaliacoes.pack()

    # Caixa de texto para exibir as avaliações
    texto_avaliacoes = tk.Text(aba_ver)
    texto_avaliacoes.pack()
    abas.add(aba_ver, text="Ver Avaliacoes")

    aba_avaliacoes_usuario = ttk.Frame(abas)

    label_usuario_id = ttk.Label(aba_avaliacoes_usuario, text="ID do Usuário:")
    label_usuario_id.pack()
    entry_usuario_id = ttk.Entry(aba_avaliacoes_usuario)
    entry_usuario_id.pack()

    # Botão para mostrar as avaliações do usuário
    botao_mostrar_avaliacoes_usuario = ttk.Button(aba_avaliacoes_usuario, text="Mostrar Avaliações",
                                                  command=mostrar_avaliacoes_usuario)
    botao_mostrar_avaliacoes_usuario.pack()

    # Caixa de texto para exibir as avaliações do usuário
    texto_avaliacoes_usuario = tk.Text(aba_avaliacoes_usuario)
    texto_avaliacoes_usuario.pack()

    # Botão para verificar a senha
    botao_verificar_senha = ttk.Button(aba_avaliacoes_usuario, text="Verificar Senha", command=verificar_e_atualizar)
    botao_verificar_senha.pack()

    abas.add(aba_avaliacoes_usuario, text="Avaliações do Usuário")
    abas.pack()


    aba_turmas = ttk.Frame(abas)
    treeview_turmas = ttk.Treeview(aba_turmas, columns=("ID", "Professor", "Nome"))
    treeview_turmas.heading("#0", text="")
    treeview_turmas.heading("ID", text="ID")
    treeview_turmas.heading("Professor", text="Professor")
    treeview_turmas.heading("Nome", text="Nome")
    treeview_turmas.column("#0", width=1)
    treeview_turmas.column("ID", width=50)
    treeview_turmas.column("Professor", width=100)
    treeview_turmas.column("Nome", width=200)
    treeview_turmas.bind("<<TreeviewSelect>>", exibir_avaliacoes)
    treeview_turmas.pack()

    # Criação do Treeview para exibir as avaliações da turma selecionada
    treeview_avaliacoes = ttk.Treeview(aba_turmas, columns=("ID", "Nota", "Comentário"))
    treeview_avaliacoes.heading("#0", text="")
    treeview_avaliacoes.heading("ID", text="ID")
    treeview_avaliacoes.heading("Nota", text="Nota")
    treeview_avaliacoes.heading("Comentário", text="Comentário")
    treeview_avaliacoes.column("#0", width=1)
    treeview_avaliacoes.column("ID", width=50)
    treeview_avaliacoes.column("Nota", width=50)
    treeview_avaliacoes.column("Comentário", width=200)
    treeview_avaliacoes.pack()

    # Botão para exibir as turmas
    botao_exibir_turmas = ttk.Button(aba_turmas, text="Exibir Turmas", command=exibir_turmas)
    botao_exibir_turmas.pack()

    # Botão para criar denúncia
    botao_criar_denuncia = ttk.Button(aba_turmas, text="Criar Denúncia", command=criar_denuncia)
    botao_criar_denuncia.pack()

    abas.add(aba_turmas, text="Avaliacoes Turmas")
    abas.pack()

    janela_principal.mainloop()

# Criação da janela principal
janela = tk.Tk()
janela.title("Tela de Login e Registro")

imagem_tk = ImageTk.PhotoImage(imagem)
rotulo = tk.Label(janela, image=imagem_tk)
rotulo.pack()

# Abas para Login e Registro
abas = ttk.Notebook(janela)

# Aba de Login
aba_login = ttk.Frame(abas)

label_usuario = ttk.Label(aba_login, text="Email:")
label_usuario.pack()
entry_usuario = ttk.Entry(aba_login)
entry_usuario.pack()

label_senha = ttk.Label(aba_login, text="Senha:")
label_senha.pack()
entry_senha = ttk.Entry(aba_login, show="*")
entry_senha.pack()

botao_login = ttk.Button(aba_login, text="Login", command=fazer_login)
botao_login.pack()

abas.add(aba_login, text="Login")

# Aba de Registro
aba_registro = ttk.Frame(abas)

label_nome = ttk.Label(aba_registro, text="Nome:")
label_nome.pack()
entry_nome = ttk.Entry(aba_registro)
entry_nome.pack()

label_email = ttk.Label(aba_registro, text="Email:")
label_email.pack()
entry_email = ttk.Entry(aba_registro)
entry_email.pack()

label_senha = ttk.Label(aba_registro, text="Senha:")
label_senha.pack()
entry_senha = ttk.Entry(aba_registro, show="*")
entry_senha.pack()

botao_registro = ttk.Button(aba_registro, text="Registrar", command=fazer_registro)
botao_registro.pack()

abas.add(aba_registro, text="Registro")


abas.pack()

# Label para exibir o status do login/registro
label_status = ttk.Label(janela, text="")
label_status.pack()

# Executa o loop principal da janela
janela.mainloop()
