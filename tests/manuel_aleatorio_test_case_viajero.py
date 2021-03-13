from faker import Faker
import unittest
from src.logica.manuel_coleccion_insertar_viajero import Coleccion
from src.modelo.declarative_base import Session #Ivan
from src.logica.Logica_mock import * # Ivan
import random

class ViajeroTestCase(unittest.TestCase):

    def tearDown(self):

        '''Abrir la session'''
        self.session = Session()

        '''Consulta todas las actividades'''
        busqueda = self.session.query(Viajero).all()

        '''Borrar todos los albums'''
        for viajero in busqueda:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()

    def setUp(self):
        '''crear la coleccion de funcionalidades a probar'''
        self.coleccion = Coleccion()

        '''abrir la sesion'''
        self.session = Session()

        '''crea una instancia de la clase Faker'''
        self.data_factory = Faker()

        '''semilla para datos pseudo-aleatorios'''
        Faker.seed(10)

        '''Genera 5 datos pseudo-aleatorios de viajeros'''
        self.data = []
        self.viajeros = []

        for i in range(0, 10):
            self.data.append((self.data_factory.unique.name(), self.data_factory.unique.name()))
            self.viajeros.append(
                Viajero(nombre=self.data[-1][0], apellido=self.data[-1][1]))
            self.session.add(self.viajeros[-1])

        self.session.commit()

    def test_constructor(self):
        for viajero, dato in zip(self.viajeros, self.data):
            self.assertEqual(viajero.nombre, dato[0])
            self.assertEqual(viajero.apellido, dato[1])

    def test_insertar_el_viajero(self):
        '''Prueba la adicion de viajero'''
        self.data.append((self.data_factory.unique.name(), self.data_factory.unique.name()))
        resultado = self.coleccion.insertar_el_viajero(nombre=self.data[-1][0], apellido=self.data[-1][1])
        self.assertEqual(resultado, True)


