

from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Session

session = Session()

actividades = session.query(Actividad).all()


'''Borra todos las actividades'''
viajeros = session.query(Viajero).all()

for viajero in viajeros:
    session.delete(viajero)


gastos = session.query(Gasto).all()

for gasto  in gastos:
    session.delete(gasto)

for actividad in actividades:
    session.delete(actividad)



session.commit()
session.close()

