from Projeto.build.models.models import Contrato , Casa, User
import tkinter as tk
from sqlalchemy import inspect, exc, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import Contrato , Casa
from connection import engine
import tkinter as tk
from datetime import datetime
from auth import  get_authenticated_user

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Contratos:

    def __init__(self, master):
        self.master = master
        self.master.title("Página Cadastro Contrato")

        self.label_dt_inicio = tk.Label(master, text="Data Inicial (YYYY-MM-DD): ")
        self.label_dt_inicio.pack()

        self.entry_dt_inicio = tk.Entry(master)
        self.entry_dt_inicio.pack()

        self.label_dt_termino = tk.Label(master, text="Data Final (YYYY-MM-DD): ")
        self.label_dt_termino.pack()

        self.entry_dt_termino = tk.Entry(master)
        self.entry_dt_termino.pack()

        self.label_valor_total = tk.Label(master, text="Valor Total: ")
        self.label_valor_total.pack()

        self.entry_valor_total = tk.Entry(master)
        self.entry_valor_total.pack()

        self.label_id_casa = tk.Label(master, text="ID Casa: ")
        self.label_id_casa.pack()

        self.entry_id_casa = tk.Entry(master)
        self.entry_id_casa.pack()

        self.botao_cadastrar = tk.Button(master, text="Cadastrar Contrato", command=self.cadastrar_contrato)
        self.botao_cadastrar.pack()

    # Função para Cadastrar Contrato
    def cadastrar_contrato(self):

        try:
            dt_inicio_str = self.entry_dt_inicio.get()
            dt_termino_str = self.entry_dt_termino.get()
            valor_total_str = self.entry_valor_total.get()
            casa_id_str = self.entry_id_casa.get()
            usuarioID = get_authenticated_user()

            if usuarioID is None:
                print("Erro: Usuário não autenticado.")
                return

            try:
                dt_inicio = datetime.strptime(dt_inicio_str, '%Y-%m-%d').date()
                dt_termino = datetime.strptime(dt_termino_str, '%Y-%m-%d').date()
                valor_total = float(valor_total_str)
                casa_id = int(casa_id_str)
                usuarioID =  usuarioID.id

            except ValueError as error:
                print(f"Erro de valor: {error}")
                return

            # Verifica se a casa e o usuário existem
            casa = session.query(Casa).filter_by(id=casa_id).first()
            usuario = session.query(User).filter_by(id=usuarioID).first()
            if not casa:
                print(f"Erro: Casa com ID {casa_id} não encontrada.")
                return
            if not usuario:
                print(f"Erro: Usuário com ID {usuarioID} não encontrado.")
                return

            inspector = inspect(engine)
            if not inspector.has_table('contratos'):
                # Se não existir, cria a tabela
                Contrato.__table__.create(bind=engine)

            # Cria uma instância de Contrato com os dados inseridos
            contrato = Contrato(dt_inicio=dt_inicio, dt_termino=dt_termino, casa_id=casa_id,
                                usuario_id=usuarioID, valor_total=valor_total)

            # Adiciona o contrato ao banco de dados
            session.add(contrato)

            # Confirma a transação
            session.commit()

            # Exibe uma mensagem de sucesso
            print("Contrato cadastrado com sucesso!")
        except exc.SQLAlchemyError as e:
            # Em caso de erro, desfaz a transação
            session.rollback()
            # Exibe uma mensagem de erro
            print(f"Erro ao cadastrar contrato: {str(e)}")
        finally:
            session.close()





    # Função para excluir contrato
    def excluir_contrato(contrato_id):
        try:
            # Consulta o contrato no banco de dados pelo ID
            contrato = session.query(Contrato).filter_by(id=contrato_id).first()

            # Verifica se o contrato foi encontrado
            if contrato:
                # Remove o contrato do banco de dados
                session.delete(contrato)
                session.commit()

                # Exibe uma mensagem de sucesso
                print("Contrato deletado com sucesso!")
            else:
                # Exibe uma mensagem de erro se o usuário não foi encontrado
                print("Contrato não encontrado encontrado.")
        except Exception as e:
            # Em caso de erro, desfaz a transação
            session.rollback()

            # Exibe uma mensagem de erro
            print(f"Erro ao excluir contrato: {str(e)}")


    def get_contratos(Self):
        session = Session()

        authenticated_user = get_authenticated_user()
        if not(authenticated_user):
            return Exception("usuário não autenticado")

        usuario_id = authenticated_user.id

        try:
            contratos = session.query(Contrato).filter_by(usuario_id=usuario_id).all()
            return contratos

            if contratos:
                for contrato in contratos:
                    print(f"f ID: {contrato.id}, "
                          f"Data de inicio: {contrato.dt_inicio},"
                          f"Data Final {contrato.dt_termino}, "
                          f"Valor Total{contrato.valor_total} ")
            else:
                print("Não ha cotratos cadastrados")
        except Exception as e:
            print("Erro ao consultar contratos:{str(e)}")
        finally:
            session.close()