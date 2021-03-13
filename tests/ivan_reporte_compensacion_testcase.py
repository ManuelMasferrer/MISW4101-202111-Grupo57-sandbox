import unittest

from datetime import date
from sqlalchemy import inspect, func, Numeric
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero, ActividadViajero
from src.modelo.declarative_base import Session, engine, Base
from src.vista.Interfaz_CuentasClaras import *
from src.logica.Logica_mock import object_as_dict


Base.metadata.create_all(engine)



class MostrarReporteCompensacionTestCase(unittest.TestCase):

    def setUp(self):

        ''' Se puebla la base de datos para las pruebas'''

        self.session = Session()


        busqueda_actividad = self.session.query(Actividad).all()
        for actividad in busqueda_actividad:
            self.session.delete(actividad)

        busqueda_viajero = self.session.query(Viajero).all()
        for viajero in busqueda_viajero:
            self.session.delete(viajero)

        busqueda_gasto = self.session.query(Gasto).all()
        for gasto in busqueda_gasto:
            self.session.delete(gasto)

        busqueda_av = self.session.query(ActividadViajero).all()
        for av in busqueda_av:
            self.session.delete(av)
        self.session.commit()

        #  Crear actividades y agregarlas a la base de datos con add y commit
        self.actividad_1 = Actividad("Paseo a la Playa")
        self.actividad_2 = Actividad("Caminata")
        self.session.add(self.actividad_1)
        self.session.add(self.actividad_2)
        self.session.commit()

        # Crear los viajeros y agregarlos a la base de datos con add y commit
        self.viajero_1 = Viajero("Juan", "Perez")
        self.viajero_2 = Viajero("Rosa", "Garcia")
        self.viajero_3 = Viajero("Luis", "Mora")
        self.viajero_4 = Viajero("Ana", "Zavala")
        self.session.add(self.viajero_1)
        self.session.add(self.viajero_2)
        self.session.add(self.viajero_3)
        self.session.add(self.viajero_4)
        self.session.commit()

        # Crear los gastos.  Note que el atributo fecha en este momento es String.

        self.gasto_1 = Gasto("Transporte", 100, '21-01-2021')
        self.gasto_2 = Gasto("Comida", 200, '22-01-2021')
        self.gasto_3 = Gasto("Bebida", 90, '23-01-2021')
        self.gasto_4 = Gasto("Fiesta",120,'24-01-2021')
        self.gasto_5 = Gasto("Transporte", 150, '28-01-2021')
        self.session.add(self.gasto_1)
        self.session.add(self.gasto_2)
        self.session.add(self.gasto_3)
        self.session.add(self.gasto_4)
        self.session.add(self.gasto_5)
        self.session.commit()

        #  Crea las relaciones entre actividad y viajero (cuales son los viajeros asociados a cada actividad)

        self.actividad_1.viajeros = [self.viajero_1, self.viajero_2, self.viajero_3, self.viajero_4]
        self.actividad_2.viajeros = [self.viajero_2]

        # Crea las relaciones entre actividad y gasto *(cuales son los gastos de cada actividad)

        self.actividad_1.gastos = [self.gasto_1, self.gasto_2, self.gasto_3, self.gasto_4]
        self.actividad_2.gastos = [self.gasto_5]

        # Crea las relaciones entre viajero y gastos (que viajero realizo cada gasto)

        self.viajero_1.gastos = [self.gasto_1, self.gasto_3]
        self.viajero_2.gastos = [self.gasto_2, self.gasto_5]
        self.viajero_3.gastos = [self.gasto_4]
        self.viajero_4.gastos = []
        self.session.commit()

        # Cierra la sesion
        self.session.close()


    def test_mostrar_reporte_compensacion(self):

        self.actividad = 'Paseo a la Playa'
        self.act_id = 1

        self.viajeross = self.session.query(Viajero).all()
        self.viajeros1 = []
        for viajero in self.viajeross:
            self.viajeros1.append(object_as_dict(viajero))

        self.gastos1 = self.session.query(Gasto).join(Actividad).filter(Gasto.actividad == self.act_id).all()
        self.gastos = []
        for gasto in self.gastos1:
            self.gastos.append(object_as_dict(gasto))
        for g in self.gastos:
            vid = g.get("viajero")
            for viajero in self.viajeros1:
                if viajero['id'] == vid:
                    g["Nombre"] = viajero['nombre']
                    g["Apellido"] = viajero['apellido']

        self.gastos_consolidados = []
        self.gastos2 = session.query(Gasto.viajero, func.sum(Gasto.valor).label('GastoViajero') ).join(Actividad).filter(Gasto.actividad == self.act_id).group_by(Gasto.viajero).all()

        self.viajeros_actividad = []
        q2 = session.query(ActividadViajero).all()
        for q in q2:
            self.viajeros_actividad.append(object_as_dict(q))


        self.gastos_viajero_act = []
        self.viajeros_act = []
        for item in self.viajeros_actividad:
            self.actid = item.get("actividad")
            if self.actid == self.act_id:
                self.gastos_viajero_act.append([item.get("viajero"),0])
                self.viajeros_act.append(item.get("viajero"))



        for id in self.viajeros_act:
            for i in range(len(self.gastos2)):
                if id == self.gastos2[i][0]:
                    self.gastos_viajero_act[id-1][1] = self.gastos2[i][1]


        self.total =0
        self.n_viajeros = 0
        for gast in self.gastos_viajero_act:
            self.total += gast[1]
            self.n_viajeros += 1


        for gast in self.gastos_viajero_act:
            self.gastos_consolidados.append(list(gast))
        for g in self.gastos_consolidados:
            if (g[1]-self.total/self.n_viajeros) < 0:
                g.append(self.total/self.n_viajeros-g[1])
                g.append(0)
            else:
                g.append(0)
                g.append(g[1]-self.total/self.n_viajeros)


        self.matriz = []

        for g in self.gastos_consolidados:
            self.matriz.append([])
        for j in range(len(self.gastos_consolidados)):
            for row in self.gastos_consolidados:
                i=1
                if j+1==row[0]:
                    self.matriz[j].append(-1)
                elif row[3] == 0:
                    self.matriz[j].append(0)
                elif row[3] >0:
                    if row[3] > self.gastos_consolidados[j][2]:
                        self.matriz[j].append(self.gastos_consolidados[j][2])
                        row[3] = row[3] - self.gastos_consolidados[j][2]
                        self.gastos_consolidados[j][2] = 0
                    elif row[3] <= self.gastos_consolidados[j][2]:
                        self.matriz[j].append(row[3])
                        self.gastos_consolidados[j][2] = self.gastos_consolidados[j][2] - row[3]
                        row[3] = 0
                i+=1

        self.viajeros_en_actividad = []
        for viajero in self.viajeros1:
            if viajero['id'] not in self.viajeros_act:
                self.viajerodict = {"Nombre": viajero['nombre']+' '+viajero['apellido'], "Presente":False}
                self.viajeros_en_actividad.append(self.viajerodict)
            else:
                self.viajerodict = {"Nombre": viajero['nombre']+' '+viajero['apellido'], "Presente":True}
                self.viajeros_en_actividad.append(self.viajerodict)


        self.matriz_header=[[""]]
        for viajero in self.viajeros_en_actividad:
            self.matriz_header[0].append(viajero['Nombre'])
        for i in range(len(self.matriz)):
            self.matriz[i].insert(0, self.matriz_header[0][i+1])
        self.matriz.insert(0, self.matriz_header[0])

        self.reporte = [['', 'Juan Perez', 'Rosa Garcia', 'Luis Mora', 'Ana Zavala'], ['Juan Perez', -1, 0, 0, 0], ['Rosa Garcia', 0, -1, 0, 0], ['Luis Mora', 7.5, 0, -1, 0], ['Ana Zavala', 55.0, 72.5, 0, -1]]

        self.assertEqual(self.reporte, self.matriz)


    def tearDown(self):
        session = Session()

        session.close()