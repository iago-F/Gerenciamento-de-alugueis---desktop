# from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox , Toplevel
# from connection import engine
# from sqlalchemy.orm import sessionmaker
# from models import Usuario
# from gui import window,  usuario, senha

# Session = sessionmaker(bind=engine)
# session = Session()

# # def abri_janela_cadastro():
# #     janela_cadastro = Toplevel(window)  # Cria uma nova janela de nível superior
# #     janela_cadastro.title("Cadastre-se")

# def login(): 
#     # Obtém o texto inserido pelo usuário nos campos de entrada
#     username = usuario.get()
#     password = senha.get()

#     user = session.query(Usuario).filter_by(username=username, password=password).first()
#     # Validação dos dados de login
    
#     if user is not None:
#         messagebox.showinfo("Sucesso", "Login bem-sucedido!")
#     else:
#         messagebox.showerror("Erro", "Usuário ou senha incorretos.")
