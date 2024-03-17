
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox , Toplevel
from connection import engine
from sqlalchemy.orm import sessionmaker
from models import User
from Cadastrouser import CadastroWindow

Session = sessionmaker(bind=engine)
session = Session()



#FUNÇÕES
Session = sessionmaker(bind=engine)
session = Session()

def Abrir_janela_cadastro():
    root_cadastro = Toplevel(root_login)
    app_cadastro = CadastroWindow(root_cadastro)
    root_login.withdraw()  # Oculta a janela de login

def login(): 
    nome = usuario.get()
    senha = senha.get()

    # Consulta ao banco de dados para verificar se o usuário existe e a senha está correta
    user = session.query(User).filter_by(nome=nome, senha=senha).first()

    # Verifica se o usuário foi encontrado no banco de dados e se a senha está correta
    if user:
        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")
root_login = Tk()
root_login.title("Login")

usuario = Entry(root_login)
usuario.pack(pady=10)

senha = Entry(root_login, show="*")
senha.pack(pady=10)

button_login = Button(root_login, text="Login", command=login)
button_login.pack(pady=10)

button_cadastro = Button(root_login, text="Cadastre-se", command=Abrir_janela_cadastro)
button_cadastro.pack(pady=10)

root_login.mainloop()