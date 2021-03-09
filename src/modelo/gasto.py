from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, backref

from .declarative_base import Base

class Gasto(Base):
    __tablename__ = 'gasto'

    id = Column(Integer, primary_key=True)
    concepto = Column(String)
    valor = Column(Integer)
    fecha = Column(String)
    actividad = Column(Integer, ForeignKey('actividad.id'))
    viajero = Column(Integer, ForeignKey('viajero.id'))

    def __init__(self, concepto, valor, fecha):
        self.concepto = concepto
        self.valor = valor
        self.fecha = fecha


