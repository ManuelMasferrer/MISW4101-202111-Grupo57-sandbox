# -*- coding: utf-8 -*-

import unittest

__author__ = "Ricardo"
__copyright__ = "Ricardo"
__license__ = "mit"


from src.logica.Logica_mock import Logica_mock
from src.vista.Vista_lista_actividades import *






class ActividadTestCase(unittest.TestCase):

    def setUp(self):
        self.actividades = ["Actividad 1", "Actividad 2","Actividad 3", "Actividad 4"]

    def tearDown(self):
        self.actividades = ["Actividad 1", "Actividad 2","Actividad 3"]


    def test_jenkinsfile(self):
        self.assertEqual(0, 0)




    def test_agregar_actividad(self):

        self.assertEqual(len(self.actividades), 4)