from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:admin@localhost:3306/gerenciament_aluguel")

