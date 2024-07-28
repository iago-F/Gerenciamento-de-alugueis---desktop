
import tkinter as tk
from connection import engine
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import User


Session = sessionmaker(bind=engine)
session = Session()
class EditarInformacoes:
    def __init__(self, master,nome, email, cpf, callback, sobrenome, user_id):
        self.master = master
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.callback = callback
        self.sobrenome = sobrenome
        self.user_id = user_id

        self.top = tk.Toplevel(master)
        self.top.title("Editar Informações do Usuário")
        self.top.geometry("300x200")

        tk.Label(self.top, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_nome = tk.Entry(self.top)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)
        self.entry_nome.insert(0, self.nome)

        tk.Label(self.top, text="Sobrenome:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_sobrenome = tk.Entry(self.top)
        self.entry_sobrenome.grid(row=1, column=1, padx=10, pady=10)
        self.entry_sobrenome.insert(0, self.sobrenome)

        tk.Label(self.top, text="Email:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_email = tk.Entry(self.top)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10)
        self.entry_email.insert(0, self.email)

        tk.Label(self.top, text="CPF:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_cpf = tk.Entry(self.top)
        self.entry_cpf.grid(row=3, column=1, padx=10, pady=10)
        self.entry_cpf.insert(0, self.cpf)

        self.btn_salvar = tk.Button(self.top, text="Salvar", command=self.salvar_informacoes)
        self.btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

    def salvar_informacoes(self):
        novo_nome = self.entry_nome.get()
        novo_sobrenome = self.entry_sobrenome.get()
        novo_email = self.entry_email.get()
        novo_cpf = self.entry_cpf.get()

        try:
            # Buscar o usuário com base no ID
            usuario = session.query(User).filter_by(id=self.user_id).first()

            if usuario:
                # Atualizar os campos do usuário
                usuario.nome = novo_nome
                usuario.email = novo_email
                usuario.cpf = novo_cpf
                usuario.sobrenome = novo_sobrenome

                # Salvar as alterações
                session.commit()
                print("Informações atualizadas com sucesso.")
            else:
                print("Usuário não encontrado.")
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            session.rollback()

        self.callback(novo_nome, novo_email, novo_cpf, novo_sobrenome)
        self.top.destroy()