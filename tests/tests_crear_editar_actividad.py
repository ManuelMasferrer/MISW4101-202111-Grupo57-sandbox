import unittest

from datetime import date
from sqlalchemy import inspect, func, Numeric
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero, ActividadViajero
from src.modelo.declarative_base import Session, engine, Base
from src.logica.Logica_mock import object_as_dict


Base.metadata.create_all(engine)



class ModificarActividadesTestCase(unittest.TestCase):

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





    def test_crear_actividad(self):

        # Caso 1: actividad con nombre en blanco
        self.session = Session()
        self.actividad_3 = Actividad("Actividad 3")
        self.session.add(self.actividad_3)
        self.session.commit()

        self.actividades = [a.nombre for a in self.session.query(Actividad.nombre).all()]
        self.assertIn("Actividad 3", self.actividades)
        self.assertEqual(3, len(self.actividades))


    def test_editar_actividad(self):
        self.session = Session()
        self.session.query(Actividad).filter(Actividad.nombre == "Caminata").update({'nombre': 'Hiking'})

        self.actividades = [a.nombre for a in self.session.query(Actividad.nombre).all()]
        self.assertIn('Hiking', self.actividades)
        self.assertEqual(2, len(self.actividades))

    def test_eliminar_actividad(self):
        self.session = Session()
        self.session.query(Actividad).filter(Actividad.nombre == "Caminata").delete()

        self.actividades = [a.nombre for a in self.session.query(Actividad.nombre).all()]
        # self.assertNotIn('Caminata', self.actividades)
        # self.assertEqual(1, len(self.actividades))

def tearDown(self):
    session = Session()


    session.close()
