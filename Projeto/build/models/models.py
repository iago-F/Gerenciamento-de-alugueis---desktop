from sqlalchemy import Column, Integer, String, ForeignKey,Float,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from connection import engine


Base = declarative_base()

class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    sobreNome = Column(String(255), nullable=False)
    cpf = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    senha = Column(String(255),unique=True)
    casa_usuario = relationship("Casa", back_populates="usuario",  overlaps="casa_usuario")

Base.metadata.create_all(engine)


class Casa(Base):
    __tablename__ = 'casas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    num_quartos = Column(Integer, nullable=False)
    num_banheiros = Column(Integer, nullable=False)
    metro_quadrado = Column(Float, nullable=False)
    valor_aluguel_mensal = Column(Float, nullable=False)
    usuario_id = Column(Integer, ForeignKey(User.id), nullable=False)


    usuario = relationship("User", back_populates="casa_usuario")


class Contrato(Base):
    __tablename__ = 'contratos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    casa_id = Column(Integer, ForeignKey('casas.id'))
    usuario = relationship("User", backref="contratos")
    casa = relationship("Casa", backref="contratos")
    dt_inicio = Column(DateTime, nullable=False)
    dt_termino = Column(DateTime, nullable=False)
    valor_total = Column(Float, nullable=False)
    pagamentos = relationship("Pagamento", back_populates="contrato")


class Pagamento(Base):
    __tablename__ = 'pagamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contrato_id = Column(Integer, ForeignKey('contratos.id'), nullable=False)
    contrato = relationship("Contrato", back_populates="pagamentos")
    dt_pagamento = Column(DateTime, nullable=False)
    valor_pagamento = Column(Float, nullable=False)


