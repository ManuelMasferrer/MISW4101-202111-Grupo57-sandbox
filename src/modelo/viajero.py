from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .declarative_base import Base

#viajero_gasto = Table(
#    'viajero_gasto', Base.metadata,
#    Column('viajero_id', Integer, ForeignKey('viajero.id')),
#    Column('gasto_id', Integer, ForeignKey('gasto.id'))
#)

class ActividadViajero(Base):
    __tablename__ = 'actividad_viajero'

    actividad = Column(Integer, ForeignKey('actividad.id'), primary_key=True)
    viajero = Column(Integer, ForeignKey('viajero.id'), primary_key=True)



class Viajero(Base):
    __tablename__ = 'viajero'

    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    actividades = relationship('Actividad', secondary = 'actividad_viajero')
    gastos = relationship('Gasto')


    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
