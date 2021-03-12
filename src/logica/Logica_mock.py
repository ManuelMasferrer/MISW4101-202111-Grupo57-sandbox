'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from sqlalchemy import inspect

from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import  Base, engine, Table, MetaData


Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

class Logica_mock():

    def __init__(self):
        # if __name__== '__main__':
        Session = sessionmaker(bind=engine)
        session = Session()

        self.actividades = [a.nombre for a in session.query(Actividad.nombre).all()]


        self.viajerosquery = session.query(Viajero).all()
        self.viajerosdict = []
        for viajero in self.viajerosquery:
            self.viajerosdict.append(object_as_dict(viajero))

        self.viajeros = []
        for i in range(len(self.viajerosdict)):
            self.viajeros.append({"Nombre": self.viajerosdict[i]["nombre"],"Apellido": self.viajerosdict[i]["apellido"]})

        self.lista_dict_viajeros_presentes = [{"Nombre": i.nombre, "Apellido": i.apellido, "Presente": False} for i in
                                         session.query(Viajero)] # Ivan
        self.viajeros_en_actividad = self.lista_dict_viajeros_presentes # Ivan

        # self.gastos1 = session.query(Gasto).join(Actividad).filter(Gasto.actividad == ).all()
        # self.gastos = []
        # for gasto in self.gastos1:
        #     self.gastos.append(object_as_dict(gasto))
        # for g in self.gastos:
        #     vid = g.get("viajero")
        #     for viajero in self.viajeros:
        #         if viajero['id'] == vid:
        #             g["Nombre"] = viajero['nombre']
        #             g["Apellido"] = viajero['apellido']

        #Este constructor contiene los datos falsos para probar la interfaz


#        self.actividades = ["Actividad 1", "Actividad 2", "Actividad 3"]
       # self.viajeros = [{"Nombre":"Pepe", "Apellido":"Pérez"}, {"Nombre":"Ana", "Apellido":"Andrade"}]
       # self.gastos = [{"Concepto":"Gasto 1", "Fecha": "12-12-2020", "Valor": 10000, "Nombre": "Pepe", "Apellido": "Pérez"}, {"Concepto":"Gasto 2", "Fecha": "12-12-2020", "Valor": 20000, "Nombre":"Ana", "Apellido":"Andrade"}]
       # self.matriz = [["", "Pepe Pérez", "Ana Andrade", "Pedro Navajas" ],["Pepe Pérez", -1, 1200, 1000],["Ana Andrade", 0, -1, 1000], ["Pedro Navajas", 0, 0, -1]]
        self.gastos_consolidados = [{"Nombre":"Pepe", "Apellido":"Pérez", "Valor":15000}, {"Nombre":"Ana", "Apellido":"Andrade", "Valor":12000},{"Nombre":"Pedro", "Apellido":"Navajas", "Valor":0}]
       # self.viajeros_en_actividad = [{"Nombre": "Pepe Pérez", "Presente":True}, {"Nombre": "Ana Andrade", "Presente":True}, {"Nombre":"Pedro Navajas", "Presente":False}]
        # self.actividades = actividades
        # for actividad in self.actividades_lista:
        #     self.actividades.append(actividad.nombre)





    # def dar_actividades(self):
    #     actividades_lista = session.query(Actividad).all()
    #     self.activities = []
    #     for actividad in actividades_lista:
    #         self.activities.append(actividad.nombre)
    #     return self.activities


#     def dar_actividades():
#         actividades_lista = session.query(Actividad).all()
#     return actividades_lista
#
# print('Las actividades almacenadas son:')
# actividades=dar_actividades()
#
# # print(activities)
# session.close()


#session = Session()
#
#actividades = session.query(Actividad).all()
#
#
#       self.actividades = actividades