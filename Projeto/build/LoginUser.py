# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Entry, Button, messagebox , Toplevel
from connection import engine
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import User
from Cadastrouser import CadastroWindow
from PaginaPrincipal import PaginaPrincipal
from auth import  authenticate_user

Session = sessionmaker(bind=engine)
session = Session()



#FUNÇÕES
Session = sessionmaker(bind=engine)
session = Session()



def centralizar_janela(janela, largura, altura):
    # Obtém a largura e altura da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calcula as coordenadas X e Y para centralizar a janela
    x = (largura_tela - largura) // 2
    y = (altura_tela - altura) // 2

    # Define a geometria da janela com base nas coordenadas calculadas
    janela.geometry(f'{largura}x{altura}+{x}+{y}')

# Criando a janela de login
root_login = Tk()
root_login.title("Login")

# Definindo o tamanho da janela e centralizando-a na tela
largura_janela = 400
altura_janela = 200
centralizar_janela(root_login, largura_janela, altura_janela)

def Abrir_janela_cadastro():
    root_cadastro = Toplevel(root_login)
    app_cadastro = CadastroWindow(root_cadastro)
    root_login.withdraw()  # Oculta a janela de login

def mostrar_pagina_principal(nome_usuario, email_usuario, user_id):
    root_login.destroy()  # Fecha a janela de login
    from PaginaPrincipal import PaginaPrincipal
    root_principal = Tk()
    minha_pagina_principal = PaginaPrincipal(root_principal,nome_usuario, email_usuario,user_id)


# def login():
#     # Obtém o nome de usuário e senha inseridos pelo usuário
#     nome = usuario.get()
#     senha = senha_entry.get()
#
#     # Consulta ao banco de dados para verificar se o usuário existe e a senha está correta
#     user = session.query(User).filter_by(nome=nome, senha=senha).first()
#
#     # Verifica se o usuário foi encontrado no banco de dados e se a senha está correta
#     if user:
#         # Obtém o ID do usuário autenticado
#         id_usuario = session.query(User).filter_by(nome=nome).first()
#         if id_usuario:
#             messagebox.showinfo("Sucesso", f"Login bem-sucedido!\nNome: {id_usuario.nome}\nEmail: {id_usuario.email}")
#             mostrar_pagina_principal(id_usuario.nome, id_usuario.email)
#         else:
#             messagebox.showerror("Erro", "Falha ao obter o ID do usuário.")
#     else:
#         messagebox.showerror("Erro", "Usuário ou senha incorretos.")
#

# root_login = Tk()
# root_login.title("Login")

def login():
    nome = usuario.get()
    senha = senha_entry.get()
    success, user = authenticate_user(nome, senha)
    if success:
        messagebox.showinfo("Sucesso", f"Login bem-sucedido!\nNome: {user.nome}\nEmail: {user.email}")
        mostrar_pagina_principal(user.nome, user.email, user.id)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")


usuario = Entry(root_login)
usuario.pack(pady=10)

senha_entry = Entry(root_login, show="*")
senha_entry.pack(pady=10)

button_login = Button(root_login, text="Login", command=login)
button_login.pack(pady=10)

button_cadastro = Button(root_login, text="Cadastre-se", command=Abrir_janela_cadastro)
button_cadastro.pack(pady=10)

root_login.mainloop()