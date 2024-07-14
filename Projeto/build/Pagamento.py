from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import Contrato, Pagamento
from tkinter import messagebox
from connection import engine
from auth import get_authenticated_user
import tkinter as tk

from tkinter import ttk
# Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class PaginaPagamento:
    def __init__(self, master):
        self.master = master
        self.master.title("Página de Pagamento")

        self.label_contrato_id = tk.Label(master, text="ID do Contrato:")
        self.label_contrato_id.pack()

        self.entry_contrato_id = tk.Entry(master)
        self.entry_contrato_id.pack()

        self.label_dt_pagamento = tk.Label(master, text="Data do Pagamento (YYYY-MM-DD):")
        self.label_dt_pagamento.pack()

        self.entry_dt_pagamento = tk.Entry(master)
        self.entry_dt_pagamento.pack()

        self.label_valor_pagamento = tk.Label(master, text="Valor do Pagamento:")
        self.label_valor_pagamento.pack()

        self.entry_valor_pagamento = tk.Entry(master)
        self.entry_valor_pagamento.pack()

        self.botao_cadastrar = tk.Button(master, text="Cadastrar Pagamento", command=self.cadastrar_pagamento)
        self.botao_cadastrar.pack()

    def cadastrar_pagamento(self):
        try:
            contrato_id = int(self.entry_contrato_id.get())
            dt_pagamento = self.entry_dt_pagamento.get()
            valor_pagamento = float(self.entry_valor_pagamento.get())

            inspector = inspect(engine)
            if not inspector.has_table('pagamentos'):
                Pagamento.__table__.create(bind=engine)

            contrato = session.query(Contrato).filter_by(id=contrato_id).first()

            if contrato:
                pagamento = Pagamento(contrato_id=contrato_id, dt_pagamento=dt_pagamento, valor_pagamento=valor_pagamento)
                contrato.pagamentos.append(pagamento)
                session.add(pagamento)
                session.commit()
                messagebox.showinfo("Sucesso", "Pagamento cadastrado com sucesso!")
            else:
                messagebox.showerror("Erro", "Contrato não encontrado.")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Erro ao cadastrar pagamento: {str(e)}")


    # # Teste de cadastro de Pagamento
    # dt_pagamento = datetime(2024, 2, 15)
    # valor_pagamento = 5000.0
    # cadastrar_pagamento(contrato_id=2, dt_pagamento=dt_pagamento, valor_pagamento=valor_pagamento)


    # Função para consultar pagamentos
    def get_mostrar_pagamentos(self):

        session = Session()

        authenticated_user = get_authenticated_user()
        if not authenticated_user:
            raise Exception("usuário não autenticado")

        usuario_id=authenticated_user.id

        try:
            pagamentos = session.query(Pagamento).filter_by(usuario_id=usuario_id).all()
            return pagamentos

            if pagamentos:
                for pagamento in pagamentos:
                    print(f"ID: {pagamento.id} , Data Do pagamento: {pagamento.dt_pagamento}, Valor do pagamento: {pagamento.valor_pagamento}")
            else:
                messagebox.showerror("Erro", "pagamentos não cadastrados")
        except Exception as e:
            print(f"Erro ao mostrar pagamentos:{str(e)}")
        finally:
            session.close()


    # Função para excluir Pagamento
    def excluir_pagamento(pagamento_id):
        try:
            # Consulta o usuário no banco de dados pelo ID
            pagamento = session.query(Pagamento).filter_by(id=pagamento_id).first()

            # Verifica se o usuário foi encontrado
            if pagamento:
                # Remove o usuário do banco de dados
                session.delete(pagamento)
                session.commit()

                # Exibe uma mensagem de sucesso
                print("Pagamento deletado com sucesso!")
            else:
                # Exibe uma mensagem de erro se o usuário não foi encontrado
                print("Pagamento não encontrado encontrado.")
        except Exception as e:
            # Em caso de erro, desfaz a transação
            session.rollback()

            # Exibe uma mensagem de erro
            print(f"Erro ao excluir pagamento: {str(e)}")


    # id_excluir_contrato = 1

    # excluir_pagamento(id_excluir_contrato)


    # função para atulizar o pagamento
    def atualizar_pagamento(pagamento_id, novo_valor, nova_data):
        try:

            pagamento = session.query(Pagamento).filter_by(id=pagamento_id).first()

            if pagamento:

                pagamento.valor_pagamento = novo_valor
                pagamento.dt_pagamento = nova_data
                # Confirma a transação
                session.commit()

                # Exibe uma mensagem de sucesso
                print("Pagamento atualizado com sucesso!")
            else:

                print("Pagamento não encontrado.")
        except Exception as e:
            # Em caso de erro, desfaz a transação
            session.rollback()

            # Exibe uma mensagem de erro
            print(f"Erro ao atualizar Pagamento: {str(e)}")

    # testar a função
    # pagamento_id = 2
    # novo_valor = 2500.0
    # nova_data = "2024-02-15"


    # atualizar_pagamento(pagamento_id, novo_valor, nova_data)
