import unittest

from datetime import date
from sqlalchemy import inspect, func, Numeric
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero, ActividadViajero
from src.modelo.declarative_base import Session, engine, Base
from src.logica.Logica_mock import object_as_dict


Base.metadata.create_all(engine)



class MostrarGastosActividadTestCase(unittest.TestCase):

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


    def test_mostrar_gastos_actividad(self):
        self.session = Session()
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


        # Mostrar que la lista en la base de datos es la misma que fue insertada

        self.lista_gastos = [{'id': 1, 'concepto': 'Transporte', 'valor': 100, 'fecha': '21-01-2021', 'actividad': 1, 'viajero': 1, 'Nombre': 'Juan', 'Apellido': 'Perez'}, {'id': 2, 'concepto': 'Comida', 'valor': 200, 'fecha': '22-01-2021', 'actividad': 1, 'viajero': 2, 'Nombre': 'Rosa', 'Apellido': 'Garcia'}, {'id': 3, 'concepto': 'Bebida', 'valor': 90, 'fecha': '23-01-2021', 'actividad': 1, 'viajero': 1, 'Nombre': 'Juan', 'Apellido': 'Perez'}, {'id': 4, 'concepto': 'Fiesta', 'valor': 120, 'fecha': '24-01-2021', 'actividad': 1, 'viajero': 3, 'Nombre': 'Luis', 'Apellido': 'Mora'}]
        self.assertListEqual(self.lista_gastos, self.gastos)



    def tearDown(self):
        session = Session()

        session.close()