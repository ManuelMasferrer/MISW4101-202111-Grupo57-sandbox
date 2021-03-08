# -*- coding: utf-8 -*-

import unittest



from src.logica.Logica_mock import Logica_mock
from src.vista.Vista_lista_actividades import *
from src.logica.cuentas_claras import Listado
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
# from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Session



class ActividadTestCases(unittest.TestCase):

    def setUp(self):
        '''Crea un listado de actividades para hacer las pruebas'''
        self.listado = Listado()

        '''Abre la sesión'''
        self.session = Session()

        '''Crea los objetos'''
        self.actividad1 = Actividad(nombre = 'Actividad 1')
        self.actividad2 = Actividad(nombre = 'Actividad 2')
        self.gasto1 = Gasto(concepto = "Comida", valor = 100 , fecha = 51000, actividad = 'Actividad 1', viajero = 'Juan Perez')
        self.gasto2 = Gasto(concepto = "Transporte", valor = 200 , fecha = 51001, actividad = 'Actividad 2', viajero = 'Rosa Gomez')





        '''Adiciona los objetos a la sesión'''
        self.session.add(self.actividad1)
        self.session.add(self.actividad2)
        self.session.add(self.gasto1)
        self.session.add(self.gasto2)





        '''Persiste los objetos y cierra la sesión'''
        self.session.commit()
        self.session.close()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todas las actividades'''
        busqueda = self.session.query(Actividad).all()

        '''Borra todas las actividades'''
        for actividad in busqueda:
            self.session.delete(actividad)

        self.session.commit()
        self.session.close()

    def test_elemento_en_conjunto(self):
        '''Prueba que un elemento se encuentre en un conjunto'''
        conjunto = [self.actividad1, self.actividad2]
        self.assertIn(self.actividad1, conjunto)
#        self.assertNotIn(self.actividad4, conjunto)



    def test_instancia_clase(self):
        '''Prueba que un elemento sea de una clase'''
        self.assertIsInstance(self.actividad1, Actividad)
        self.assertNotIsInstance(self.listado, Actividad)