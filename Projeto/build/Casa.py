# from sqlalchemy.orm import sessionmaker
# from Projeto.build.models.models import Casa, Base
# from connection import engine
# from sqlalchemy import inspect

from sqlalchemy import inspect
from Projeto.build.models.models import Casa, Base
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

Session = sessionmaker(bind=engine)
session = Session()

class Cadastro_Casas:

    def __init__(self, master):
        self.master = master
        self.master.title("Página Cadastro Casa")

        self.label_metro_quadrado = tk.Label(master, text="area:")
        self.label_metro_quadrado.pack()

        self.entry_metro_quadrado = tk.Entry(master)
        self.entry_metro_quadrado.pack()

        self.label_num_banheiro = tk.Label(master, text="Quantidade de banheiros:")
        self.label_num_banheiro.pack()

        self.entry_num_banheiro = tk.Entry(master)
        self.entry_num_banheiro.pack()

        self.label_preco_mensal = tk.Label(master, text="Preço mensal")
        self.label_preco_mensal.pack()

        self.entry_preco_mensal = tk.Entry(master)
        self.entry_preco_mensal.pack()

        self.label_endereco = tk.Label(master, text="endereço")
        self.label_endereco.pack()

        self.entry_endereco = tk.Entry(master)
        self.entry_endereco.pack()

        self.label_num_quarto = tk.Label(master, text="quantidade de quartos")
        self.label_num_quarto.pack()

        self.entry_num_quarto = tk.Entry(master)
        self.entry_num_quarto.pack()

        self.label_descricao = tk.Label(master, text="Descrição")
        self.label_descricao.pack()

        self.entry_descricao = tk.Entry(master)
        self.entry_descricao.pack()

        self.botao_cadastrar = tk.Button(master, text="Cadastrar Casa", command=self.cadastrar_casa)
        self.botao_cadastrar.pack()


    def cadastrar_casa(self):

        session = Session()

        try:
            num_quartos = int(self.entry_num_quarto.get())
            num_banheiros = int(self.entry_num_banheiro.get())
            metro_quadrado = float(self.entry_metro_quadrado.get())
            valor_aluguel_mensal = float(self.entry_preco_mensal.get())

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

            print("Casa cadastrada com sucesso!")
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