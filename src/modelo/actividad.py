
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True, autoincrement="auto")
    nombre = Column(String, unique=True, nullable= False)
#    activa = Column(Boolean)
    gastos = relationship("Gasto", cascade='all, delete, delete-orphan')
    viajeros = relationship('Viajero', secondary = 'actividad_viajero')

    def __init__(self, nombre):
        self.nombre = nombre
# #        self.activa = activa
#
#     def __repr__(self):
#         return "<Actividad(nombre='{}')>" \
#             .format(self.nombre)
#
#
