
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Session

#if __name__ == '__main__':
session = Session()
# actividades_lista = session.query(Actividad).all()
# print(actividades_lista)
# activities= []
#
# for actividad in actividades_lista:
#     activities.append(actividad.nombre)

actividades = [a.nombre for a in session.query(Actividad.nombre).all()]
gastos = [session.query(Gasto).asdict()]

# def dar_actividades():
#     actividades_lista = session.query(Actividad.nombre).all()
#     activities = []
#     for actividad in actividades_lista:
#          activities.append(actividad.nombre)
#     return activities

# print('Las actividades almacenadas son:')
# actividades=dar_actividades()
# activities = []
# for actividad in actividades:
#     activities.append(actividad.nombre)
print(actividades)
print(gasto)
session.close()