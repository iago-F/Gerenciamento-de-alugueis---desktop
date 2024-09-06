from sqlalchemy import inspect, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import Contrato, Pagamento
from tkinter import messagebox
from connection import engine
from auth import get_authenticated_user
import tkinter as tk
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from tkinter import ttk
# Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class PaginaPagamento:
    def __init__(self, master):
        self.master = master
        self.master.title("Página de Pagamento")
        self.master.geometry("550x350")  # Diminuindo o tamanho da tela
        self.master.config(bg="white")  # Define o fundo da tela como branco

        # Criar um frame para centralizar o conteúdo
        self.frame = tk.Frame(master, bg="white")
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Adiciona o título
        self.titulo = tk.Label(self.frame, text="Cadastrar Pagamento", font=('Arial', 16, 'bold'), bg="white")
        self.titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Configuração dos rótulos e campos de entrada
        self.label_contrato_id = tk.Label(self.frame, text="ID do Contrato:", bg="white")
        self.label_contrato_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entry_contrato_id = tk.Entry(self.frame, bg="lightgrey")
        self.entry_contrato_id.grid(row=1, column=1, padx=10, pady=5)

        self.label_dt_pagamento = tk.Label(self.frame, text="Data do Pagamento (YYYY-MM-DD):", bg="white")
        self.label_dt_pagamento.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entry_dt_pagamento = tk.Entry(self.frame, bg="lightgrey")
        self.entry_dt_pagamento.grid(row=2, column=1, padx=10, pady=5)

        self.label_valor_pagamento = tk.Label(self.frame, text="Valor do Pagamento:", bg="white")
        self.label_valor_pagamento.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.entry_valor_pagamento = tk.Entry(self.frame, bg="lightgrey")
        self.entry_valor_pagamento.grid(row=3, column=1, padx=10, pady=5)

        # Configuração do botão
        self.botao_cadastrar = tk.Button(self.frame, text="Cadastrar Pagamento", command=self.cadastrar_pagamento,
                                         bg="lightblue")
        self.botao_cadastrar.grid(row=4, column=0, columnspan=2, pady=20)


    def verificar_limite_pagamentos(self, contrato_id, novo_pagamento_valor):
        try:
            # Obter o contrato específico
            contrato = session.query(Contrato).filter_by(id=contrato_id).first()
            if not contrato:
                raise Exception("Contrato não encontrado")

            # Calcular a soma de todos os pagamentos existentes para o contrato
            soma_pagamentos = session.query(func.sum(Pagamento.valor_pagamento)).filter_by(contrato_id=contrato_id).scalar() or 0

            # Verificar se a soma dos pagamentos com o novo pagamento ultrapassa o valor total do contrato
            if soma_pagamentos + novo_pagamento_valor > contrato.valor_total:
                return False

            return True
        except Exception as e:
            print(f"Erro ao verificar limite de pagamentos: {e}")
            return False

    def cadastrar_pagamento(self):
        try:
            contrato_id = int(self.entry_contrato_id.get())
            dt_pagamento = self.entry_dt_pagamento.get()
            valor_pagamento = float(self.entry_valor_pagamento.get())

            inspector = inspect(engine)
            if not inspector.has_table('pagamentos'):
                Pagamento.__table__.create(bind=engine)

            # Verificar se o pagamento excede o limite do contrato
            if not self.verificar_limite_pagamentos(contrato_id, valor_pagamento):
                messagebox.showerror("Erro", "O valor do pagamento excede o valor total do contrato.")
                return

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




    # Função para consultar pagamentos
    def get_mostrar_pagamentos():
        session = Session()

        authenticated_user = get_authenticated_user()
        if not authenticated_user:
            raise Exception("Usuário não autenticado")

        usuario_id = authenticated_user.id

        try:
            # Primeiro, obtenha os contratos do usuário
            contratos = session.query(Contrato).filter_by(usuario_id=usuario_id).all()
            if not contratos:
                messagebox.showerror("Erro", "Nenhum contrato encontrado para o usuário.")
                return

            # Obtenha os IDs dos contratos
            contrato_ids = [contrato.id for contrato in contratos]

            # busca os pagamentos associados a esses contratos
            pagamentos = session.query(Pagamento).filter(Pagamento.contrato_id.in_(contrato_ids)).all()

            if pagamentos:
                for pagamento in pagamentos:
                    print(
                        f"ID: {pagamento.id} , Data Do Pagamento: {pagamento.dt_pagamento}, Valor do Pagamento: {pagamento.valor_pagamento}")
            else:
                messagebox.showerror("Erro", "Nenhum pagamento encontrado para os contratos do usuário.")

            return pagamentos

        except SQLAlchemyError as e:
            print(f"Erro ao mostrar pagamentos: {str(e)}")
        finally:
            session.close()

    def carregar_pagamentos(self):
        try:
            # Chama a função para obter os pagamentos
            pagamentos = self.get_mostrar_pagamentos()
            for pagamento in pagamentos:
                self.lista_pagamentos.insert(
                    tk.END,
                    f"ID: {pagamento['id']}, Valor: R${pagamento['valor']:.2f}, Data: {pagamento['data']}"
                )
        except Exception as e:
            messagebox.showerror("Erro ao mostrar os pagamentos", str(e))

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
