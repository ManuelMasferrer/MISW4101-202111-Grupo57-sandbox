from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget


from sqlalchemy.orm import sessionmaker
from src.modelo.declarative_base import  Base, engine
from src.logica.Logica_mock import object_as_dict
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero, ActividadViajero
from src.modelo.gasto import Gasto
from sqlalchemy import inspect, func

Base.metadata.create_all(engine)

from functools import partial

class Vista_reporte_gastos_viajero(QWidget):
    #Ventana que muestra el reporte de gastos consolidados

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        # Se establecen las características de la ventana
        self.titulo = 'Cuentas Claras - Reporte de gastos por viajero'
        self.left = 80
        self.top = 80
        self.width = 720
        self.height = 560

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.interfaz = interfaz

        self.inicializar_GUI()
        self.show()

    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))

        self.distribuidor_base = QVBoxLayout(self)

        # Creación de la tabla en dónde se hará el reporte
        self.tabla_reporte = QScrollArea(self)
        self.tabla_reporte.setWidgetResizable(True)
        self.widget_tabla_reporte = QWidget()
        self.distribuidor_tabla_reporte = QGridLayout(self.widget_tabla_reporte)
        self.tabla_reporte.setWidget(self.widget_tabla_reporte)
        self.distribuidor_base.addWidget(self.tabla_reporte)

        self.distribuidor_tabla_reporte.setColumnStretch(0, 1)
        self.distribuidor_tabla_reporte.setColumnStretch(1, 1)
        self.distribuidor_tabla_reporte.setColumnStretch(2, 0)
        self.distribuidor_tabla_reporte.setColumnStretch(3, 0)

        # Creación de las etiquetas con los encabezados
        etiqueta_viajero = QLabel("Viajero")
        etiqueta_viajero.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_reporte.addWidget(etiqueta_viajero, 0, 0, Qt.AlignLeft)

        etiqueta_concepto = QLabel("Concepto")
        etiqueta_concepto.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_reporte.addWidget(etiqueta_concepto, 0, 1, Qt.AlignLeft)

        etiqueta_total = QLabel("Total")
        etiqueta_total.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_reporte.addWidget(etiqueta_total, 0, 2, 1, 2, Qt.AlignLeft)

        #Creación de los botones de funciones de la ventana
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Añadir Actividad")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.setIconSize(QSize(120, 120))
        self.btn_volver.clicked.connect(self.volver)
        self.distribuidor_base.addWidget(self.btn_volver)
        self.distribuidor_base.setAlignment(self.btn_volver, Qt.AlignCenter)


    def mostar_reporte_gastos(self, actividad):
        """
        Esta función puebla el reporte de gastos con la información en la lista
        """
        self.actividad = actividad

        Session = sessionmaker(bind=engine)
        session = Session()

        self.viajeross = session.query(Viajero).all()
        self.viajeros1 = []
        for viajero in self.viajeross:
            self.viajeros1.append(object_as_dict(viajero))

        self.activities = []
        self.actividades1 = session.query(Actividad).all()
        for act in self.actividades1:
            self.activities.append(object_as_dict(act))

    # Funcionalidad para encontrar id de la actividad actual
        for act in self.activities:
            self.actnom = act.get("nombre")
            if self.actnom == actividad:
                act_id = act.get("id")

    # Consultar los viajeros registrados en la actividad

        self.viajeros_actividad = []
        q2 = session.query(ActividadViajero).all()
        for q in q2:
            self.viajeros_actividad.append(object_as_dict(q))

    # Determinar los gastos totales por viajero
        self.gastos_viajero_act = []
        self.viajeros_act = []
        for item in self.viajeros_actividad:
            actid = item.get("actividad")
            if actid == act_id:
                self.gastos_viajero_act.append([item.get("viajero"),0])
                self.viajeros_act.append(item.get("viajero"))



    # Consolidar los gastos por viajero
        self.gastos_consolidados = []
        self.gastos2 = session.query(Gasto.viajero, func.sum(Gasto.valor).label('GastoViajero') ).join(Actividad).filter(Gasto.actividad == act_id).group_by(Gasto.viajero).all()

    #
    # for id in self.viajeros1:
    #     self.gastos_consolidados.append({self.viajeros1[id].nombre, self.viajeros1[id].apellido, self.gastos2[id][1]})




        k=0
        for id in self.viajeros_act:
            for i in range(len(self.gastos2)):
                if id == self.gastos2[i][0]:
                    self.gastos_viajero_act[k][1] = self.gastos2[k][1]
                    k +=1



        for i in range(len(self.viajeros_act)):
            for viajero in self.viajeros1:
                if self.viajeros_act[i] == viajero['id']:
                    self.gastos_consolidados.append({"Nombre":viajero["nombre"], "Apellido":viajero["apellido"]})

        for i in range(len(self.viajeros_act)):
            self.gastos_consolidados[i]['Valor'] = self.gastos_viajero_act[i][1]


        self.lista_gastos = self.gastos_consolidados

    #Por cada iteración, llenamos con el nombre del viajero y sus gastos consolidados para la actividad
        numero_fila = 1
        for gasto in self.lista_gastos:

            etiqueta_viajero = QLabel(gasto["Nombre"] + ' ' + gasto["Apellido"])
            etiqueta_viajero.setWordWrap(True)
            self.distribuidor_tabla_reporte.addWidget(etiqueta_viajero, numero_fila, 0, Qt.AlignLeft)

            etiqueta_concepto = QLabel('Gastos consolidados')
            etiqueta_concepto.setWordWrap(True)
            self.distribuidor_tabla_reporte.addWidget(etiqueta_concepto, numero_fila, 1, Qt.AlignLeft)

            etiqueta_total = QLabel("${:,.2f}".format(gasto["Valor"]))
            etiqueta_total.setWordWrap(True)
            self.distribuidor_tabla_reporte.addWidget(etiqueta_total, numero_fila, 2, Qt.AlignLeft)

            numero_fila = numero_fila+1

        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_reporte.layout().setRowStretch(numero_fila+1, 1)

    def volver(self):
        """
        Esta función permite volver a la ventana de la actividad
        """   
        self.hide()
        self.interfaz.mostrar_actividad()
