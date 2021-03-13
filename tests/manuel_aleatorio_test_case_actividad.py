from faker import Faker
import unittest
from src.logica.manuel_coleccion_insertar_editar_eliminar_actividad import Coleccion
from src.modelo.declarative_base import Session #Ivan
from src.logica.Logica_mock import * # Ivan
from src.modelo.actividad import Actividad
import random

class ActividadTestCase(unittest.TestCase):

    def tearDown(self):
        '''Abrir la session'''
        self.session = Session()

        '''Consulta todas las actividades'''
        busqueda = self.session.query(Actividad).all()

        '''Borrar todos los albums'''
        for actividad in busqueda:
            self.session.delete(actividad)

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

        '''Genera 5 datos pseudo-aleatorios de actividades'''
        self.data = []
        self.actividades = []

        for i in range(0, 10):
            self.data.append(self.data_factory.unique.name())
            self.actividades.append(
                Actividad(nombre=self.data[-1]))
            self.session.add(self.actividades[-1])

        self.session.commit()

    def test_constructor(self):
        for actividad, dato in zip(self.actividades, self.data):
            self.assertEqual(actividad.nombre, dato)

    def test_insertar_la_actividad(self):
        '''Prueba la adicion de una actividad'''
        self.data.append(self.data_factory.unique.name())
        resultado = self.coleccion.insertar_la_actividad(nombre=self.data[-1])
        self.assertEqual(resultado, True)

    def test_editar_la_actividad(self):
        '''Prueba la edicion de una actividad'''

        self.nombre_repetido = random.choice(self.data)
        self.data.append(self.data_factory.unique.name())
        resultado = self.coleccion.editar_la_actividad(self.nombre_repetido, self.data[-1])
        self.assertEqual(resultado, True)

    def test_eliminar_la_actividad(self):

        '''Prueba la eliminacion de una actividad'''
        self.actividad_repetida = random.choice(self.data)
        resultado = self.coleccion.eliminar_la_actividad(self.actividad_repetida)
        self.assertEqual(resultado, True)
