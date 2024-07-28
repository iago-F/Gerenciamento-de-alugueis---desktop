from sqlalchemy.orm import sessionmaker
from connection import engine
from Projeto.build.models.models import User

Session = sessionmaker(bind=engine)
session = Session()

authenticated_user = None

def authenticate_user(nome, senha):
    global authenticated_user
    user = session.query(User).filter_by(nome=nome, senha=senha).first()
    if user:
        authenticated_user = user
        return True, user
    else:
        return False, None


def get_authenticated_user():
    return authenticated_user
