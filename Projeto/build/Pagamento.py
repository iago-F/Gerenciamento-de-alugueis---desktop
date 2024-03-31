from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import Contrato, Pagamento
from connection import engine

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

#função para cadastrar pagamento
def cadastrar_pagamento(contrato_id, dt_pagamento, valor_pagamento):
    try:

        inspector = inspect(engine)
        if not inspector.has_table('pagamentos'):
            # Se não existir, cria a tabela
            Pagamento.__table__.create(bind=engine)
        
            
        # Verifica se o contrato existe
        contrato = session.query(Contrato).filter_by(id=contrato_id).first()

        if contrato:
            # Cria uma instância de Pagamento com os dados fornecidos
            pagamento = Pagamento(contrato_id=contrato_id, dt_pagamento=dt_pagamento, valor_pagamento=valor_pagamento)
            
            # Adiciona o pagamento ao contrato
            contrato.pagamentos.append(pagamento)
            
            # Adiciona o pagamento ao banco de dados
            session.add(pagamento)
            
            # Confirma a transação
            session.commit()
            
            # Exibe uma mensagem de sucesso
            print("Pagamento cadastrado com sucesso!")
        else:
            print("Contrato não encontrado.")
    except Exception as e:
        # Em caso de erro, desfaz a transação
        session.rollback()
        # Exibe uma mensagem de erro
        print(f"Erro ao cadastrar pagamento: {str(e)}")

# Teste de cadastro de Pagamento
# dt_pagamento = date(2024, 2, 15)
# valor_pagamento = 1000.0
# cadastrar_pagamento(contrato_id=2, dt_pagamento=dt_pagamento, valor_pagamento=valor_pagamento)


# Função para consultar pagamentos        
def mostrar_pagamentos():
    try:
        
        pagamentos = session.query(Pagamento).all()

        if pagamentos:
            
            for pagamento in pagamentos:
                print(f"ID: {pagamento.id}, Data do pagamento: {pagamento.dt_pagamento}, Valor do pagamento: {pagamento.valor_pagamento}, ")
        else:
            print("Não há pagamentos cadastrados.")
    except Exception as e:
        print(f"Erro ao exibir pagamentos: {str(e)}")

# mostrar_pagamentos()

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


#testar a função 
# pagamento_id = 2  
# novo_valor = 2500.0  
# nova_data = "2024-02-15"  


# atualizar_pagamento(pagamento_id, novo_valor, nova_data)