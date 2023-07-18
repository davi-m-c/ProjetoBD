import tkinter as tk
from tkinter import ttk
import mysql.connector
from PIL import ImageTk, Image
import io

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

def exibir_view_relacionamento():
    try:
        # Estabelecer conexão com o banco de dados
        conexao = mysql.connector.connect(
            host='localhost',     # endereço do servidor MySQL
            database='projeto',   # nome do banco de dados
            user='root',          # nome de usuário do MySQL
            password='root'       # senha do usuário do MySQL
        )

        # Criar um objeto cursor para executar consultas SQL
        cursor = conexao.cursor()

        # Consulta para obter os dados da View
        consulta_view = "SELECT * FROM view_relacionamento"
        cursor.execute(consulta_view)
        resultados_view = cursor.fetchall()

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

        # Criar uma janela para exibir os dados
        janela = tk.Tk()
        janela.title("View de Relacionamento")

        # Criação do Treeview para exibir os dados
        treeview = ttk.Treeview(janela, columns=("Nome do Professor", "Nome da Disciplina", "Média da Nota"))
        treeview.heading("#0", text="")
        treeview.heading("Nome do Professor", text="Nome do Professor")
        treeview.heading("Nome da Disciplina", text="Nome da Disciplina")
        treeview.heading("Média da Nota", text="Média da Nota")
        treeview.column("#0", width=1)
        treeview.column("Nome do Professor", width=200)
        treeview.column("Nome da Disciplina", width=200)
        treeview.column("Média da Nota", width=100)

        # Adicionar os dados ao Treeview
        for row in resultados_view:
            nome_professor = row[0]
            nome_disciplina = row[1]
            media_nota = row[2]
            treeview.insert('', 'end', values=(nome_professor, nome_disciplina, media_nota))

        treeview.pack()

        # Execução do loop principal da janela
        janela.mainloop()

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)

def adicionar_departamento():
    nome = entry_nomed.get()

    if nome:
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

            # Inserir o departamento no banco de dados
            inserir_departamento = "INSERT INTO departamentos (nome) VALUES (%s)"
            valores_departamento = (nome,)
            cursor.execute(inserir_departamento, valores_departamento)
            conexao.commit()

            messagebox.showinfo("Sucesso", "Departamento adicionado com sucesso!")

            # Limpar o campo de entrada
            entry_nome.delete(0, tk.END)

        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", "Erro ao adicionar departamento: " + str(erro))

        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()
    else:
        messagebox.showerror("Erro", "Por favor, insira um nome para o departamento.")

# Função para exibir os departamentos
def exibir_departamentos():
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

        # Consulta para obter todos os departamentos
        consulta_departamentos = "SELECT * FROM departamentos"
        cursor.execute(consulta_departamentos)
        resultados_departamentos = cursor.fetchall()

        # Exibir os departamentos na janela
        text_departamentos.delete("1.0", tk.END)
        for departamento in resultados_departamentos:
            text_departamentos.insert(tk.END, f"ID: {departamento[0]}, Nome: {departamento[1]}\n")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", "Erro ao conectar ao MySQL: " + str(erro))

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

# Função para excluir um departamento
def excluir_departamento():
    id_departamento = entry_id.get()

    if id_departamento:
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

            # Excluir o departamento do banco de dados
            excluir_departamento = "DELETE FROM departamentos WHERE iddepartamentos = %s"
            valor_exclusao = (id_departamento,)
            cursor.execute(excluir_departamento, valor_exclusao)
            conexao.commit()

            messagebox.showinfo("Sucesso", "Departamento excluído com sucesso!")

            # Limpar o campo de entrada
            entry_id.delete(0, tk.END)

        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", "Erro ao excluir departamento: " + str(erro))

        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()
    else:
        messagebox.showerror("Erro", "Por favor, insira um ID de departamento.")

def exibir_professores():
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

        # Consulta para obter os dados dos professores
        consulta_professores = "SELECT * FROM professores"
        cursor.execute(consulta_professores)
        resultados_professores = cursor.fetchall()

        # Limpar a árvore antes de exibir os professores
        treeview_professores.delete(*treeview_professores.get_children())

        # Exibir os professores na árvore
        for professor in resultados_professores:
            id_professor = professor[0]
            nome_professor = professor[1]
            departamento_id = professor[2]

            # Adicionar o professor à árvore
            treeview_professores.insert('', 'end', values=(id_professor, nome_professor, departamento_id))

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)

# Função para adicionar um novo professor
# Função para adicionar um novo professor
def adicionar_professor():
    nome = entry_nomep.get()
    departamento_id = entry_departamento_id.get()

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

        # Inserir o novo professor na tabela
        inserir_professor = "INSERT INTO professores (name, departamento_id) VALUES (%s, %s)"
        valores_professor = (nome, departamento_id)
        cursor.execute(inserir_professor, valores_professor)
        conexao.commit()

        # Exibir mensagem de sucesso
        mensagem_status.configure(text="Professor adicionado com sucesso", foreground="green")

        # Limpar os campos de entrada
        entry_nome.delete(0, tk.END)
        entry_departamento_id.delete(0, tk.END)

        # Atualizar a exibição dos professores
        exibir_professores()

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)
        # Exibir mensagem de erro
        mensagem_status.configure(text="Erro ao adicionar professor", foreground="red")


# Função para excluir um professor
# Função para excluir um professor
def excluir_professor():
    item_selecionado = treeview_professores.focus()
    if item_selecionado:
        professor_id = treeview_professores.item(item_selecionado)['values'][0]

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

            # Excluir o professor da tabela
            excluir_professor = "DELETE FROM professores WHERE idprofessores = %s"
            cursor.execute(excluir_professor, (professor_id,))
            conexao.commit()

            # Exibir mensagem de sucesso
            mensagem_status.configure(text="Professor excluído com sucesso", foreground="green")

            # Atualizar a exibição dos professores
            exibir_professores()

            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()

        except mysql.connector.Error as erro:
            print("Erro ao conectar ao MySQL:", erro)
            # Exibir mensagem de erro
            mensagem_status.configure(text="Erro ao excluir professor", foreground="red")
    else:
        # Exibir mensagem de erro se nenhum professor estiver selecionado
        mensagem_status.configure(text="Nenhum professor selecionado", foreground="red")

def exibir_pagina_principal():
    global entry_email, entry_nota, entry_comentario, entry_turma_id, entry_professorId, texto_avaliacoes, entry_usuario_id, texto_avaliacoes_usuario, treeview_turmas, treeview_avaliacoes, text_departamentos, treeview_professores, entry_departamento_id, mensagem_status, entry_nomep, entry_id, entry_nomed
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
    botao_mostrar_avaliacoes_usuario = ttk.Button(aba_avaliacoes_usuario, text="Mostrar Avaliações",command=mostrar_avaliacoes_usuario)
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

    aba_view = ttk.Frame(abas)
    # Criação do Treeview para exibir os professores
    treeview_professores = ttk.Treeview(aba_view, columns=("ID", "Nome", "Departamento ID"))
    treeview_professores.heading("#0", text="")
    treeview_professores.heading("ID", text="ID")
    treeview_professores.heading("Nome", text="Nome")
    treeview_professores.heading("Departamento ID", text="Departamento ID")
    treeview_professores.column("#0", width=1)
    treeview_professores.column("ID", width=50)
    treeview_professores.column("Nome", width=200)
    treeview_professores.column("Departamento ID", width=100)
    treeview_professores.pack()

    # Criação do frame para os campos de entrada
    frame_campos = ttk.Frame(aba_view)
    frame_campos.pack(pady=10)

    # Criação dos rótulos e campos de entrada
    label_nome = ttk.Label(frame_campos, text="Nome:")
    label_nome.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
    entry_nomep = ttk.Entry(frame_campos)
    entry_nomep.grid(row=0, column=1, padx=5, pady=5)

    label_departamento_id = ttk.Label(frame_campos, text="Departamento ID:")
    label_departamento_id.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
    entry_departamento_id = ttk.Entry(frame_campos)
    entry_departamento_id.grid(row=1, column=1, padx=5, pady=5)

    # Criação dos botões
    frame_botoes = ttk.Frame(aba_view)
    frame_botoes.pack(pady=10)

    botao_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=adicionar_professor)
    botao_adicionar.grid(row=0, column=0, padx=5, pady=5)

    botao_excluir = ttk.Button(frame_botoes, text="Excluir", command=excluir_professor)
    botao_excluir.grid(row=0, column=1, padx=5, pady=5)

    # Criação da mensagem de status
    mensagem_status = ttk.Label(aba_view, text="")
    mensagem_status.pack()
    
    exibir_professores()

    botao_registro = ttk.Button(aba_view, text="Ver medias", command=exibir_view_relacionamento)
    botao_registro.pack()
    abas.add(aba_view, text="Professores")
    abas.pack()

    aba_departamentos = ttk.Frame(abas)
    label_nome = tk.Label(aba_departamentos, text="Nome do Departamento:")
    label_nome.pack()

    entry_nomed = tk.Entry(aba_departamentos)
    entry_nomed.pack()

    button_adicionar = tk.Button(aba_departamentos, text="Adicionar", command=adicionar_departamento)
    button_adicionar.pack()

    label_departamentos = tk.Label(aba_departamentos, text="Departamentos:")
    label_departamentos.pack()

    text_departamentos = tk.Text(aba_departamentos, width=40, height=10)
    text_departamentos.pack()

    button_exibir = tk.Button(aba_departamentos, text="Exibir Departamentos", command=exibir_departamentos)
    button_exibir.pack()

    label_id = tk.Label(aba_departamentos, text="ID do Departamento:")
    label_id.pack()

    entry_id = tk.Entry(aba_departamentos)
    entry_id.pack()

    button_excluir = tk.Button(aba_departamentos, text="Excluir", command=excluir_departamento)
    button_excluir.pack()
    abas.add(aba_departamentos, text="Departamentos")
    abas.pack()

    janela_principal.mainloop()

def recuperar_imagem(id_imagem):
    try:
        # Estabelecer conexão com o banco de dados
        conexao = mysql.connector.connect(
            host='localhost',     # endereço do servidor MySQL
            database='projeto',   # nome do banco de dados
            user='root',          # nome de usuário do MySQL
            password='root'       # senha do usuário do MySQL
        )

        # Criar um objeto cursor para executar consultas SQL
        cursor = conexao.cursor()

        # Consulta para recuperar a imagem pelo ID
        consulta_imagem = "SELECT arquivo FROM imagem WHERE id = %s"
        cursor.execute(consulta_imagem, (id_imagem,))
        resultado = cursor.fetchone()

        if resultado is not None:
            # Recuperar o blob da coluna "arquivo"
            blob_imagem = resultado[0]

            # Carregar o blob em um objeto de imagem usando a biblioteca Pillow
            imagem = Image.open(io.BytesIO(blob_imagem))
            return imagem

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

    return None

# Criação da janela principal
janela = tk.Tk()
janela.title("Tela de Login e Registro")

id_imagem = 1  # ID da imagem que você deseja exibir
imagem = recuperar_imagem(id_imagem)

if imagem is not None:
    # Redimensionar a imagem para um tamanho máximo de largura e altura de 300 pixels
    max_width = 200
    max_height = 200
    imagem.thumbnail((max_width, max_height))

    # Exibir a imagem em um widget Label
    img_label = ttk.Label(janela)
    img_label.image = ImageTk.PhotoImage(imagem)
    img_label.configure(image=img_label.image)
    img_label.pack()

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

# Label para exibir o status do login/registro
label_status = ttk.Label(janela, text="")
label_status.pack()
abas.pack()

# Executa o loop principal da janela
janela.mainloop()
