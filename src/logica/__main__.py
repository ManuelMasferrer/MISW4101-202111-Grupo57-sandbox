
import sys
from PyQt5.QtWidgets import QApplication
from src.vista.Interfaz_CuentasClaras import App_CuentasClaras
from src.logica.Logica_mock import Logica_mock

from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.actividad import Actividad
from src.modelo.declarative_base import Session, engine, Base

if __name__ == '__main__':
    #Punto inicial de la aplicación 

    logica = Logica_mock()



    app = App_CuentasClaras(sys.argv, logica)
    sys.exit(app.exec_())