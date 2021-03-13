import unittest
from src.logica.manuel_coleccion_insertar_viajero import Coleccion
from src.modelo.declarative_base import Session #Ivan
from src.logica.Logica_mock import * # Ivan


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
        '''Crea una coleccion de funcionalidades sobre las cuales se van hacer los test'''
        self.coleccion = Coleccion()

        '''Abrir la sesion'''
        self.session = Session()

        '''Crear los objetos'''
        self.viajero1 = Viajero(nombre="Juan", apellido="Gutierrez")
        self.viajero2 = Viajero(nombre='Natalia', apellido="Camargo")
        self.viajero3 = Viajero(nombre="Fabian", apellido="Gonzalez")

        '''Adiciona los objetos de la sesion'''
        self.session.add(self.viajero1)
        self.session.add(self.viajero2)
        self.session.add(self.viajero3)

        '''Persistir la informacion y cerrar la sesion'''
        self.session.commit()
        self.session.close()


    def test_insertar_el_viajero(self, nombre = "Gloria", apellido = "Cardenas"):
        '''Prueba la adicion del viajero'''
        resultado = self.coleccion.insertar_el_viajero(nombre=nombre, apellido=apellido)
        self.assertEqual(resultado, True)
