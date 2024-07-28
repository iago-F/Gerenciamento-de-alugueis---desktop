from sqlalchemy import create_engine
import logging

engine = create_engine("mysql+pymysql://root:admin@localhost:3306/gerenciament_aluguel")

# # Configuração do logger
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)