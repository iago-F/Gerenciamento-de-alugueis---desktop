from sqlalchemy import inspect, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import Contrato
from connection import engine

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

# Função para Cadastrar Contrato
def cadastrar_contrato(usuario_id, casa_id, dt_inicio, dt_termino, valor_total):
    try:
        inspector = inspect(engine)
        if not inspector.has_table('contratos'):
            # Se não existir, cria a tabela
            Contrato.__table__.create(bind=engine)

        # Cria uma instância de Contrato com os dados inseridos
        contrato = Contrato(usuario_id=usuario_id, casa_id=casa_id,
                            dt_inicio=dt_inicio, dt_termino=dt_termino,
                            valor_total=valor_total)

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

    cadastrar_contrato(usuario_id=9, casa_id=15, dt_inicio='2024-02-15', dt_termino='2024-02-20', valor_total=2000.00)


# Função para excluir contrato
def excluir_contrato(contrato_id):
    try:
        # Consulta o usuário no banco de dados pelo ID
        contrato = session.query(Contrato).filter_by(id=contrato_id).first()

        # Verifica se o usuário foi encontrado
        if contrato:
            # Remove o usuário do banco de dados
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


# Teste da Função 
# contrato_id = 1 
# excluir_contrato(contrato_id)


# função para exibir os contratos 
def mostrar_contratos():
    try:
        # Consulta todas as casas no banco de dados
        contratos = session.query(Contrato).all()

        # Verifica se foram encontradas casas
        if contratos:
            # Exibe as informações de cada casa
            for contrato in contratos:
                print(f"ID: {contrato.id}, Data de Inicio: {contrato.dt_inicio}, Data de Encerramento: {contrato.dt_termino}, "
                      f"Valor Total: {contrato.valor_total},")
        else:
            print("Não há contratos cadastrados.")
    except Exception as e:
        print(f"Erro ao exibir contratos: {str(e)}")


#testar motrar contratos
mostrar_contratos()


# Função para autalizar o valo do contrato
def atualizar_contrato(contrato_id, novo_valor_total):
    try:
        # Consulta o contrato no banco de dados pelo ID
        contrato = session.query(Contrato).filter_by(id=contrato_id).first()

        # Verifica se o contrato foi encontrado
        if contrato:
            
            contrato.valor_total = novo_valor_total

            # Confirma a transação
            session.commit()

            # Exibe uma mensagem de sucesso
            print("Contrato atualizado com sucesso!")
        else:
            
            print("Contrato não encontrado.")
    except Exception as e:
        # Em caso de erro, desfaz a transação
        session.rollback()
        
        # Exibe uma mensagem de erro
        print(f"Erro ao atualizar contrato: {str(e)}")

# Exemplo de uso da função
# atualizar_contrato(contrato_id=2, novo_valor_total=2500.0)

