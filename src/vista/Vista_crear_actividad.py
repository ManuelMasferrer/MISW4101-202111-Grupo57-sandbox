from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial
from src.logica.Logica_mock import * # Ivan


class Dialogo_crear_actividad(QDialog):
    #Diálogo para crear una actividad

    def __init__(self,actividad):
        """
        Constructor del diálogo
        """    
        super().__init__()

        self.actividad = actividad # Ivan semana 07

        self.setFixedSize(300,110)
        
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #El título del diálogo varía si se usa para crear o editar una actividad

        titulo=""
        if actividad is None:
            titulo="Nueva Actividad"
        else:
            titulo="Editar Actividad"
        self.setWindowTitle(titulo)
        
        #Creación de las etiquetas

        etiqueta_nombre=QLabel("Nombre")
        distribuidor_dialogo.addWidget(etiqueta_nombre,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.texto_nombre=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_nombre,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        #Creación de los botones
        
        self.btn_guardar = QPushButton("Guardar")
        distribuidor_dialogo.addWidget(self.btn_guardar ,numero_fila,1)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        distribuidor_dialogo.addWidget(self.btn_cancelar ,numero_fila,2)
        self.btn_cancelar.clicked.connect(self.cancelar)

        #Si el diálogo se usa para editar, se debe mostrar el nombre de la actividad a editar
        
        if (actividad!=None):
            self.texto_nombre.setText(actividad)

    def guardar(self):
        """
        Esta función envía la información de que se han guardado los cambios
        """
        self.logica = Logica_mock() # Ivan semana 07
        lista_no_opciones = [x for x in self.logica.actividades if x != self.actividad ] # Ivan
        if self.texto_nombre.text() != "" and self.texto_nombre.text() not in lista_no_opciones:  # Ivan
            self.resultado = 1  # Ivan semana 07
            self.logica = Logica_mock()
            print(self.logica.actividades)
            self.close()  # Ivan semana 07
        else:  # Ivan semana 07
            self.resultado = 0  # Ivan semana 07
            self.close()  # Ivan semana 07
        return self.resultado  # Ivan semana 07


    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """ 
        self.resultado=0
        self.close()
        return self.resultado


