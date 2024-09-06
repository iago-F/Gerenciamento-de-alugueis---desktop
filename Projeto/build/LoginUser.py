from tkinter import Tk, Entry, Button, messagebox, Toplevel
from connection import engine
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import User
from Cadastrouser import CadastroWindow
from auth import authenticate_user
from Projeto.build.Logging import logging_config



Session = sessionmaker(bind=engine)
session = Session()

class PaginaLogin:
    def __init__(self):
        # Criando a janela de login
        self.root_login = Tk()
        self.root_login.title("Login")

        self.usuario = Entry(self.root_login)
        self.usuario.pack(pady=10)

        self.senha_entry = Entry(self.root_login, show="*")
        self.senha_entry.pack(pady=10)

        self.button_login = Button(self.root_login, text="Login", command=self.login)
        self.button_login.pack(pady=10)

        self.button_cadastro = Button(self.root_login, text="Cadastre-se", command=self.abrir_janela_cadastro)
        self.button_cadastro.pack(pady=10)

        self.centralizar_janela(self.root_login, 400, 200)

        self.root_login.mainloop()

    def centralizar_janela(self, janela, largura, altura):
        # Obtém a largura e altura da tela
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()

        # Calcula as coordenadas X e Y para centralizar a janela
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        # Define a geometria da janela com base nas coordenadas calculadas
        janela.geometry(f'{largura}x{altura}+{x}+{y}')

    def abrir_janela_cadastro(self):
        root_cadastro = Toplevel(self.root_login)
        app_cadastro = CadastroWindow(root_cadastro)
        self.root_login.withdraw()  # Oculta a janela de login

    def mostrar_pagina_principal(self, nome_usuario, email_usuario, user_id, sobrenome_usuario, cpf_usuario):
        self.root_login.destroy()  # Fecha a janela de login
        root_principal = Tk()
        from PaginaPrincipal import PaginaPrincipal
        app_principal = PaginaPrincipal(root_principal, nome_usuario, email_usuario, sobrenome_usuario, user_id, cpf_usuario)
        root_principal.mainloop()  # Inicia o loop principal da nova janela

    def login(self):
        nome = self.usuario.get()
        senha = self.senha_entry.get()
        success, user = authenticate_user(nome, senha)
        if success:
            # Registra o login bem-sucedido
            logging_config.logging.info(f'Login bem-sucedido: Nome: {user.nome}, Email: {user.email}')
            messagebox.showinfo("Sucesso", f"Login bem-sucedido!\nNome: {user.nome}\nSobrenome: {user.sobreNome}")
            self.mostrar_pagina_principal(user.nome, user.email, user.id, user.sobreNome, user.cpf)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

# Inicializa a tela de login
if __name__ == "__main__":
    PaginaLogin()
