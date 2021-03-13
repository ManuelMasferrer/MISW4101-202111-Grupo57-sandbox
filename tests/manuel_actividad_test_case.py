import unittest
from src.logica.manuel_coleccion_insertar_editar_eliminar_actividad import Coleccion
from src.modelo.declarative_base import Session #Ivan
from src.logica.Logica_mock import * # Ivan


class ActividadTestCase(unittest.TestCase):

    def tearDown(self):
        self.session = Session()

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
        '''Crea una coleccion de funcionalidades sobre las cuales se van hacer los test'''
        self.coleccion = Coleccion()

        '''Abrir la sesion'''
        self.session = Session()

        '''Crear los objetos'''
        self.actividad1 = Actividad(nombre="Ir al mar")
        self.actividad2 = Actividad(nombre='Ir al museo')
        self.actividad3 = Actividad(nombre="Ir al cine")

        '''Adiciona los objetos de la sesion'''
        self.session.add(self.actividad1)
        self.session.add(self.actividad2)
        self.session.add(self.actividad3)

        '''Persistir la informacion y cerrar la sesion'''
        self.session.commit()
        self.session.close()

    def test_insertar_la_actividad(self):
        '''Prueba la adicion de una actividad'''
        resultado = self.coleccion.insertar_la_actividad(nombre="Ir a bailar")
        self.assertEqual(resultado, True)

    def test_editar_la_actividad(self):
        '''Prueba la edicion de una actividad'''
        resultado = self.coleccion.editar_la_actividad("Ir al mar", "Ir al parque de diversiones")
        self.assertEqual(resultado, True)

    def test_eliminar_la_actividad(self):
        resultado = self.coleccion.eliminar_la_actividad("Ir al cine")
        self.assertEqual(resultado, True)
