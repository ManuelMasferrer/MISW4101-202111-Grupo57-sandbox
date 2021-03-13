import unittest

from datetime import date
from sqlalchemy import inspect, func, Numeric
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero, ActividadViajero
from src.modelo.declarative_base import Session, engine, Base
from src.logica.Logica_mock import object_as_dict


Base.metadata.create_all(engine)



class GastosViajeroTestCase(unittest.TestCase):

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





    def test_gastos_por_viajero(self):
        # Caso 1: actividad sin gastos ni viajeros
        self.session = Session()
        self.actividad_3 = Actividad("Actividad Vacia")
        self.session.add(self.actividad_3)
        self.session.commit()


        self.viajeross = self.session.query(Viajero).all()
        self.viajeros1 = []
        for viajero in self.viajeross:
            self.viajeros1.append(object_as_dict(viajero))

        self.activities = []
        self.actividades1 = self.session.query(Actividad).all()
        for act in self.actividades1:
            self.activities.append(object_as_dict(act))

        # Consultar los viajeros registrados en la actividad

        self.viajeros_actividad = []
        q2 = self.session.query(ActividadViajero).all()
        for q in q2:
            self.viajeros_actividad.append(object_as_dict(q))

        # Determinar los gastos totales por viajero
        self.gastos_viajero_act = []
        self.viajeros_act = []
        for item in self.viajeros_actividad:
            actid = item.get("actividad")
            if actid == 3:
                self.gastos_viajero_act.append([item.get("viajero"),0])
                self.viajeros_act.append(item.get("viajero"))



        # Consolidar los gastos por viajero
        self.gastos_consolidados = []
        self.gastos2 = self.session.query(Gasto.viajero, func.sum(Gasto.valor).label('GastoViajero') ).join(Actividad).filter(Gasto.actividad == 3).group_by(Gasto.viajero).all()

        k=0
        for id in self.viajeros_act:
            for i in range(len(self.gastos2)):
                if id == self.gastos2[i][0]:
                    self.gastos_viajero_act[k][1] = self.gastos2[k][1]
                    k +=1

        for i in range(len(self.viajeros_act)):
            for viajero in self.viajeros1:
                if self.viajeros_act[i] == viajero['id']:
                    self.gastos_consolidados.append({"Nombre":viajero["nombre"], "Apellido":viajero["apellido"]})

        for i in range(len(self.viajeros_act)):
            self.gastos_consolidados[i]['Valor'] = self.gastos_viajero_act[i][1]


        self.lista_gastos = self.gastos_consolidados

        self.assertListEqual(self.gastos_consolidados, [])


    def test_gastos_actividad_sin_gastos(self):
        # Caso 2: actividad sin gastos y un viajero
        self.session = Session()
        self.actividad_4 = Actividad("Actividad sin gastos")
        self.actividad_4.viajeros = [self.viajero_2]
        # self.session.add(self.actividad_4)
        # self.session.add(self.actividad_4.viajeros)
        self.session.commit()

        self.viajeross = self.session.query(Viajero).all()
        self.viajeros1 = []
        for viajero in self.viajeross:
            self.viajeros1.append(object_as_dict(viajero))

        self.activities = []
        self.actividades1 = self.session.query(Actividad).all()
        for act in self.actividades1:
            self.activities.append(object_as_dict(act))

        # Consultar los viajeros registrados en la actividad

        self.viajeros_actividad = []
        q2 = self.session.query(ActividadViajero).all()
        for q in q2:
            self.viajeros_actividad.append(object_as_dict(q))

        # Determinar los gastos totales por viajero
        self.gastos_viajero_act = []
        self.viajeros_act = []
        for item in self.viajeros_actividad:
            actid = item.get("actividad")
            if actid == 4:
                self.gastos_viajero_act.append([item.get("viajero"),0])
                self.viajeros_act.append(item.get("viajero"))

        # Consolidar los gastos por viajero
        self.gastos_consolidados = []
        self.gastos2 = self.session.query(Gasto.viajero, func.sum(Gasto.valor).label('GastoViajero') ).join(Actividad).filter(Gasto.actividad == 4).group_by(Gasto.viajero).all()

        k=0
        for id in self.viajeros_act:
            for i in range(len(self.gastos2)):
                if id == self.gastos2[i][0]:
                    self.gastos_viajero_act[k][1] = self.gastos2[k][1]
                    k +=1

        for i in range(len(self.viajeros_act)):
            for viajero in self.viajeros1:
                if self.viajeros_act[i] == viajero['id']:
                    self.gastos_consolidados.append({"Nombre":viajero["nombre"], "Apellido":viajero["apellido"]})

        for i in range(len(self.viajeros_act)):
            self.gastos_consolidados[i]['Valor'] = self.gastos_viajero_act[i][1]

        self.assertListEqual(self.gastos_consolidados, [])



    def test_gastos_actividad_con_gastos(self):
        # Caso 3: actividad con gastos y un viajero
        self.session = Session()
        self.viajeross = self.session.query(Viajero).all()
        self.viajeros1 = []
        for viajero in self.viajeross:
            self.viajeros1.append(object_as_dict(viajero))

        self.activities = []
        self.actividades1 = self.session.query(Actividad).all()
        for act in self.actividades1:
            self.activities.append(object_as_dict(act))

        # Consultar los viajeros registrados en la actividad

        self.viajeros_actividad = []
        q2 = self.session.query(ActividadViajero).all()
        for q in q2:
            self.viajeros_actividad.append(object_as_dict(q))

        # Determinar los gastos totales por viajero
        self.gastos_viajero_act = []
        self.viajeros_act = []
        for item in self.viajeros_actividad:
            actid = item.get("actividad")
            if actid == 2:
                self.gastos_viajero_act.append([item.get("viajero"),0])
                self.viajeros_act.append(item.get("viajero"))

        # Consolidar los gastos por viajero
        self.gastos_consolidados = []
        self.gastos2 = []
        self.gastos2 = self.session.query(Gasto.viajero, func.sum(Gasto.valor).label('GastoViajero') ).join(Actividad).filter(Gasto.actividad == 2).group_by(Gasto.viajero).all()

        k=0
        for id in self.viajeros_act:
            for i in range(len(self.gastos2)):
                if id == self.gastos2[i][0]:
                    self.gastos_viajero_act[k][1] = self.gastos2[k][1]
                    k +=1

        for i in range(len(self.viajeros_act)):
            for viajero in self.viajeros1:
                if self.viajeros_act[i] == viajero['id']:
                    self.gastos_consolidados.append({"Nombre":viajero["nombre"], "Apellido":viajero["apellido"]})

        for i in range(len(self.viajeros_act)):
            self.gastos_consolidados[i]['Valor'] = self.gastos_viajero_act[i][1]

        self.assertEqual(self.gastos2[0][1], 150)

    def test_gastos_actividad_con_varios_gastos(self):
        # Caso 3: actividad con gastos y un viajero
        self.session = Session()
        self.viajeross = self.session.query(Viajero).all()
        self.viajeros1 = []
        for viajero in self.viajeross:
            self.viajeros1.append(object_as_dict(viajero))

        self.activities = []
        self.actividades1 = self.session.query(Actividad).all()
        for act in self.actividades1:
            self.activities.append(object_as_dict(act))

        # Consultar los viajeros registrados en la actividad

        self.viajeros_actividad = []
        q2 = self.session.query(ActividadViajero).all()
        for q in q2:
            self.viajeros_actividad.append(object_as_dict(q))

        # Determinar los gastos totales por viajero
        self.gastos_viajero_act = []
        self.viajeros_act = []
        for item in self.viajeros_actividad:
            actid = item.get("actividad")
            if actid == 1:
                self.gastos_viajero_act.append([item.get("viajero"),0])
                self.viajeros_act.append(item.get("viajero"))

        # Consolidar los gastos por viajero
        self.gastos_consolidados = []
        self.gastos2 = []
        self.gastos2 = self.session.query(Gasto.viajero, func.sum(Gasto.valor).label('GastoViajero') ).join(Actividad).filter(Gasto.actividad == 1).group_by(Gasto.viajero).all()

        k=0
        for id in self.viajeros_act:
            for i in range(len(self.gastos2)):
                if id == self.gastos2[i][0]:
                    self.gastos_viajero_act[k][1] = self.gastos2[k][1]
                    k +=1

        for i in range(len(self.viajeros_act)):
            for viajero in self.viajeros1:
                if self.viajeros_act[i] == viajero['id']:
                    self.gastos_consolidados.append({"Nombre":viajero["nombre"], "Apellido":viajero["apellido"]})

        for i in range(len(self.viajeros_act)):
            self.gastos_consolidados[i]['Valor'] = self.gastos_viajero_act[i][1]
        print(self.gastos_consolidados)

        self.assertEqual(self.gastos_consolidados[0]['Valor'], 190)
        self.assertEqual(self.gastos_consolidados[1]['Valor'], 200)
        self.assertEqual(self.gastos_consolidados[2]['Valor'], 120)
        self.assertEqual(self.gastos_consolidados[3]['Valor'], 0)


def tearDown(self):
    session = Session()


    session.close()
