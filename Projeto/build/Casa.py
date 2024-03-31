from sqlalchemy.orm import sessionmaker
from Projeto.build.models.models import Casa, Base
from connection import engine
from sqlalchemy import inspect



Session = sessionmaker(bind=engine)
session = Session()


def cadastrar_casa(num_quartos, num_banheiros, metro_quadrado, valor_aluguel_mensal, usuario_id):
    session = Session()
    try:
        inspector = inspect(engine)
        if not inspector.has_table('casas'):
            # Se não existir, cria a tabela
            Base.metadata.create_all(engine)

        # Cria uma instância de Casa com os dados inseridos
        casa = Casa(num_quartos=num_quartos, num_banheiros=num_banheiros, 
                    metro_quadrado=metro_quadrado, valor_aluguel_mensal=valor_aluguel_mensal,
                    usuario_id=usuario_id)

        # Adiciona a casa ao banco de dados
        session.add(casa)
        
        # Confirma a transação
        session.commit()
        
        # Exibe uma mensagem de sucesso
        print("Casa cadastrada com sucesso!")
    finally:
        # print("erro ao cadastrar casa")
        session.close()

# Exemplo de uso da função
cadastrar_casa(num_quartos=3, num_banheiros=2, metro_quadrado=120, valor_aluguel_mensal=1500.00, usuario_id=9)



def excluir_casa(casa_id):
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

# Exemplo de uso da função
# excluir_casa(casa_id=6)



def mostrar_casas():
    try:
        # Consulta todas as casas no banco de dados
        casas = session.query(Casa).all()

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

# Exemplo de uso da função
mostrar_casas()