
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Frame

import tkinter as tk
from sqlalchemy.ext.declarative import declarative_base
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User,Casa
from connection import engine

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

# Funções

# cadastar usuário
def cadastrar_usuario(nome, sobrenome, cpf, email, senha):
    session = Session()
    try:
        if nome and sobrenome and cpf and email and senha:
            # Cria uma instância de Usuario com os dados inseridos pelo usuário
            usuario = User(nome=nome, sobreNome=sobrenome, cpf=cpf, email=email, senha=senha)
            
            # Adiciona o usuário ao banco de dados
            session.add(usuario)
            
            # Confirma a transação
            session.commit()
            
            # Exibe uma mensagem de sucesso
            print("Usuário cadastrado com sucesso!")
        else:
            # Exibe um aviso se algum campo estiver vazio
            print("Por favor, preencha todos os campos.")
    finally:
        # Fecha a sessão do SQLAlchemy
        session.close()


# Teste da função
nome = "Taylla"
sobreNome = "vilela"
cpf = "00.00.00-20"
email = "taylla@gmail.com"
senha = "123456"

cadastrar_usuario(nome, sobreNome, cpf, email, senha)




# Deletar usuário 
            
def excluir_usuario(usuario_id):
    try:
        # Consulta o usuário no banco de dados pelo ID
        usuario = session.query(User).filter_by(id=usuario_id).first()

        # Verifica se o usuário foi encontrado
        if usuario:
            # Consulta todas as casas associadas ao usuário
            casas = session.query(Casa).filter_by(usuario_id=usuario_id).all()

            # Remove todas as casas associadas ao usuário
            for casa in casas:
                session.delete(casa)

            # Remove o usuário do banco de dados
            session.delete(usuario)
            session.commit()

            # Exibe uma mensagem de sucesso
            print("Usuário e todas as suas casas foram excluídos com sucesso!")
        else:
            # Exibe uma mensagem de erro se o usuário não foi encontrado
            print("Usuário não encontrado.")
    except Exception as e:
        # Em caso de erro, desfaz a transação
        session.rollback()
        
        # Exibe uma mensagem de erro
        print(f"Erro ao excluir usuário: {str(e)}")


# teste da função 
# id_usuario_a_excluir = 2


# excluir_usuario(id_usuario_a_excluir)



# #Pegar o usuário autenticado.
# def ObterUsuarioAutenticado(nome):
#     # Realiza uma consulta para encontrar o usuário autenticado com base no nome de usuário
#     usuario = session.query(User).filter_by(nome_de_usuario=nome).first()
#     if usuario:
#         return usuario.id
#     else: 
#         return None

class CadastroWindow:
    def __init__(self, root):
        self.root = root
        root.title("Cadastro de Usuário")

        # Labels e Entradas
        self.label_nome = tk.Label(root, text="Nome:")
        self.label_nome.grid(row=0, column=0, padx=10, pady=5)
        self.input_nome = tk.Entry(root)
        self.input_nome.grid(row=0, column=1, padx=10, pady=5)

        self.label_sobrenome = tk.Label(root, text="Sobrenome:")
        self.label_sobrenome.grid(row=1, column=0, padx=10, pady=5)
        self.input_sobrenome = tk.Entry(root)
        self.input_sobrenome.grid(row=1, column=1, padx=10, pady=5)

        self.label_cpf = tk.Label(root, text="CPF:")
        self.label_cpf.grid(row=2, column=0, padx=10, pady=5)
        self.input_cpf = tk.Entry(root)
        self.input_cpf.grid(row=2, column=1, padx=10, pady=5)

        self.label_email = tk.Label(root, text="Email:")
        self.label_email.grid(row=3, column=0, padx=10, pady=5)
        self.input_email = tk.Entry(root)
        self.input_email.grid(row=3, column=1, padx=10, pady=5)

        self.label_senha = tk.Label(root, text="Senha:")
        self.label_senha.grid(row=4, column=0, padx=10, pady=5)
        self.input_senha = tk.Entry(root, show="*")
        self.input_senha.grid(row=4, column=1, padx=10, pady=5)

        # Botão de cadastro
        self.botao_cadastrar = tk.Button(root, text="Cadastrar", command=self.cadastrar_usuario)
        self.botao_cadastrar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def criar_tabela_usuario():
        Base.metadata.create_all(engine)

    
def Abrir_janela_cadastro():
    root_login.destroy()
    root_cadastro = tk.Tk()
    app_cadastro = CadastroWindow(root_cadastro)
    root.destroy()


if __name__ == "__main__":
    root_login = tk.Tk()
    root_login.title("Login")
    root = tk.Tk()
