# from sqlalchemy.orm import sessionmaker
# from Projeto.build.models.models import Casa, Base
# from connection import engine
# from sqlalchemy import inspect

from sqlalchemy import inspect
from Projeto.build.models.models import Casa, Base, User
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import Contrato, Pagamento
from tkinter import messagebox
from connection import engine
from auth import get_authenticated_user
import tkinter as tk
from tkinter import ttk
from Projeto.build.Logging import logging_config



Session = sessionmaker(bind=engine)
session = Session()

Session = sessionmaker(bind=engine)
session = Session()

class Cadastro_Casas:

    def __init__(self, master):
        self.master = master
        self.master.title("Página Cadastro Casa")
        self.master.geometry("550x400")  # Ajustado o tamanho da tela
        self.master.config(bg="white")  # Define o fundo da tela como branco

        # Criar um frame para centralizar o conteúdo
        self.frame = tk.Frame(master, bg="white")
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Adiciona o título
        self.titulo = tk.Label(self.frame, text="Cadastrar Casa", font=('Arial', 16, 'bold'), bg="white")
        self.titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Configuração dos rótulos e campos de entrada
        self.label_metro_quadrado = tk.Label(self.frame, text="Área (m²):", bg="white")
        self.label_metro_quadrado.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entry_metro_quadrado = tk.Entry(self.frame, bg="lightgrey")
        self.entry_metro_quadrado.grid(row=1, column=1, padx=10, pady=5)

        self.label_num_banheiro = tk.Label(self.frame, text="Quantidade de Banheiros:", bg="white")
        self.label_num_banheiro.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entry_num_banheiro = tk.Entry(self.frame, bg="lightgrey")
        self.entry_num_banheiro.grid(row=2, column=1, padx=10, pady=5)

        self.label_preco_mensal = tk.Label(self.frame, text="Preço Mensal:", bg="white")
        self.label_preco_mensal.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.entry_preco_mensal = tk.Entry(self.frame, bg="lightgrey")
        self.entry_preco_mensal.grid(row=3, column=1, padx=10, pady=5)

        self.label_endereco = tk.Label(self.frame, text="Endereço:", bg="white")
        self.label_endereco.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.entry_endereco = tk.Entry(self.frame, bg="lightgrey")
        self.entry_endereco.grid(row=4, column=1, padx=10, pady=5)

        self.label_num_quarto = tk.Label(self.frame, text="Quantidade de Quartos:", bg="white")
        self.label_num_quarto.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.entry_num_quarto = tk.Entry(self.frame, bg="lightgrey")
        self.entry_num_quarto.grid(row=5, column=1, padx=10, pady=5)

        self.label_descricao = tk.Label(self.frame, text="Descrição:", bg="white")
        self.label_descricao.grid(row=6, column=0, padx=10, pady=5, sticky="e")

        self.entry_descricao = tk.Entry(self.frame, bg="lightgrey")
        self.entry_descricao.grid(row=6, column=1, padx=10, pady=5)

        # Configuração do botão
        self.botao_cadastrar = tk.Button(self.frame, text="Cadastrar Casa", command=self.cadastrar_casa, bg="lightblue")
        self.botao_cadastrar.grid(row=7, column=0, columnspan=2, pady=20)

    def cadastrar_casa(self):

        session = Session()

        try:
            num_quartos = int(self.entry_num_quarto.get())
            num_banheiros = int(self.entry_num_banheiro.get())
            metro_quadrado = float(self.entry_metro_quadrado.get())
            valor_aluguel_mensal = float(self.entry_preco_mensal.get())

            # Verificar se algum valor é negativo
            if num_quartos < 0 or num_banheiros < 0 or metro_quadrado < 0 or valor_aluguel_mensal < 0:
                messagebox.showerror("Erro", "Os valores não podem ser negativos.")
                return

            authenticated_user = get_authenticated_user()
            if not authenticated_user:
                raise Exception("Usuário não autenticado")

            usuario_id = authenticated_user.id

            inspector = inspect(engine)
            if not inspector.has_table('casas'):
                Base.metadata.create_all(engine)

            casa = Casa(num_quartos=num_quartos, num_banheiros=num_banheiros,
                        metro_quadrado=metro_quadrado, valor_aluguel_mensal=valor_aluguel_mensal,
                        usuario_id=usuario_id)

            session.add(casa)
            session.commit()


            messagebox.showinfo("Casa cadastrada com sucesso!")
            logging_config.logging.info(f'Casa {casa.id} cadastrada , Nome: {authenticated_user.nome},')
        except Exception as e:
            session.rollback()
            print(f"Erro ao cadastrar casa: {str(e)}")
        finally:
            session.close()


def excluir_casa(casa_id):
        session = Session()
        try:
            # Consulta a casa no banco de dados pelo ID
            casa = session.query(Casa).filter_by(id=casa_id).first()

            # Verifica se a casa foi encontrada
            if casa:
                # Remove a casa do banco de dados
                session.delete(casa)
                session.commit()

                # Exibe uma mensagem de sucesso
                print("Casa excluída com sucesso!")
            else:
                # Exibe uma mensagem de erro se a casa não foi encontrada
                print("Casa não encontrada.")
        except Exception as e:
            # Em caso de erro, desfaz a transação
            session.rollback()
            # Exibe uma mensagem de erro
            print(f"Erro ao excluir casa: {str(e)}")
        finally:
            session.close()


def get_mostrar_casas():
    session = Session()

    authenticated_user = get_authenticated_user()
    if not authenticated_user:
        raise Exception("Usuário não autenticado")

    usuario_id = authenticated_user.id

    try:
        # Consulta todas as casas no banco de dados
        casas = session.query(Casa).filter_by(usuario_id=usuario_id).all()
        return casas

        # Verifica se foram encontradas casas
        if casas:
            # Exibe as informações de cada casa
            for casa in casas:
                print(f"ID: {casa.id}, Número de Quartos: {casa.num_quartos}, Número de Banheiros: {casa.num_banheiros}, "
                      f"Metro Quadrado: {casa.metro_quadrado}, Valor do Aluguel Mensal: {casa.valor_aluguel_mensal}, "
                      f"ID do Usuário: {casa.usuario_id}")
        else:
            print("Não há casas cadastradas.")
    except Exception as e:
        print(f"Erro ao mostrar as casas: {str(e)}")
    finally:
        session.close()


def cont_casas(user_id):
    try:
        total_casas_user = session.query(Casa).filter_by(usuario_id=user_id).count()
        return total_casas_user
    except Exception as e:
        print(f"Erro ao contar casas do usuário: {str(e)}")
        return 0