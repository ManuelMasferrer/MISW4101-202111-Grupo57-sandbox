from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from functools import partial
from PyQt5.QtWidgets import QWidget

from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import  Base, engine
from src.logica.Logica_mock import object_as_dict
from src.modelo.viajero import Viajero, ActividadViajero


from sqlalchemy import inspect, func
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)

class Vista_reporte_compensacion(QWidget):
    #Ventana que muestra el reporte de compensación

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        # Se establecen las características de la ventana
        self.titulo = 'Cuentas Claras - Reporte de compensación'
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

        self.tabla_compensacion = QScrollArea(self)
        self.tabla_compensacion.setWidgetResizable(True)
        self.widget_tabla_compensacion = QWidget()
        self.distribuidor_tabla_compensacion = QGridLayout(
            self.widget_tabla_compensacion)
        self.tabla_compensacion.setWidget(self.widget_tabla_compensacion)
        self.distribuidor_base.addWidget(self.tabla_compensacion)

        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Añadir Actividad")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.clicked.connect(self.volver)

        self.distribuidor_base.addWidget(self.btn_volver)
        self.distribuidor_base.setAlignment(self.btn_volver, Qt.AlignCenter)

    def mostrar_reporte_compensacion(self, actividad):
        """
        Esta función construye el reporte de compensación a partir de una matriz
        """        

        #self.matriz = matriz_compensacion
        self.actividad = actividad

        Session = sessionmaker(bind=engine)
        session = Session()

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

        for id in self.viajeros_act:
            for i in range(len(self.gastos2)):
                if id == self.gastos2[i][0]:
                    self.gastos_viajero_act[id-1][1] = self.gastos2[i][1]

        total =0
        n_viajeros = 0
        for gast in self.gastos_viajero_act:
            total += gast[1]
            n_viajeros += 1

        for gast in self.gastos_viajero_act:
            self.gastos_consolidados.append(list(gast))
        for g in self.gastos_consolidados:
            if (g[1]-total/n_viajeros) < 0:
                g.append(total/n_viajeros-g[1])
                g.append(0)
            else:
                g.append(0)
                g.append(g[1]-total/n_viajeros)


        self.matriz = []

        for g in self.gastos_consolidados:
            self.matriz.append([])
        for j in range(len(self.gastos_consolidados)):
            for row in self.gastos_consolidados:
                i=1
                if j+1==row[0]:
                    self.matriz[j].append(-1)
                elif row[3] == 0:
                    self.matriz[j].append(0)
                elif row[3] >0:
                    if row[3] > self.gastos_consolidados[j][2]:
                        self.matriz[j].append(self.gastos_consolidados[j][2])
                        row[3] = row[3] - self.gastos_consolidados[j][2]
                        self.gastos_consolidados[j][2] = 0
                    elif row[3] <= self.gastos_consolidados[j][2]:
                        self.matriz[j].append(row[3])
                        self.gastos_consolidados[j][2] = self.gastos_consolidados[j][2] - row[3]
                        row[3] = 0
                i+=1
        self.viajeross = session.query(Viajero).all()
        self.viajeros1 = []
        for viajero in self.viajeross:
            self.viajeros1.append(object_as_dict(viajero))

        self.viajeros_en_act = []
        for id in self.viajeros_act:
            for viajero in self.viajeros1:
                if id == viajero["id"]:
                    self.viajeros_en_act.append(viajero["nombre"])
                    self.viajeros_en_act[id-1] = self.viajeros_en_act[id-1]+ ' ' +viajero['apellido']

        self.viajeros_en_actividad = []
        for viajero in self.viajeros1:
            if viajero['id'] not in self.viajeros_act:
                self.viajerodict = {"Nombre": viajero['nombre']+' '+viajero['apellido'], "Presente":False}
                self.viajeros_en_actividad.append(self.viajerodict)
            else:
                self.viajerodict = {"Nombre": viajero['nombre']+' '+viajero['apellido'], "Presente":True}
                self.viajeros_en_actividad.append(self.viajerodict)

        self.matriz_header=[[""]]
        for viajero in self.viajeros_en_actividad:
            self.matriz_header[0].append(viajero['Nombre'])
        for i in range(len(self.matriz)):
            self.matriz[i].insert(0,self.matriz_header[0][i+1])
        self.matriz.insert(0, self.matriz_header[0])



        for i in range(0, len(self.matriz)):
            for j in range(0, len(self.matriz)):
                
                if i == j:
                    #La etiqueta 0,0 debe estar vacía. Las etiquetas diagonales deben estar en negro
                    etiqueta_valor = QLabel("")
                    if i != 0:
                        etiqueta_valor = QLabel("")
                        etiqueta_valor.setStyleSheet(
                            "QLabel { background-color : #000; }")
                elif i == 0 or j == 0:
                    #Las etiquetas de la primera fila y la primera columna son nombres
                    etiqueta_valor = QLabel("{}".format(self.matriz[i][j]))
                    etiqueta_valor.setWordWrap(True)
                    etiqueta_valor.setFont(QFont("Times", weight=QFont.Bold))
                else:
                    #Las etiquetas restantes deben ser los montos de dinero
                    etiqueta_valor = QLabel(
                        "${:,.2f}".format(self.matriz[i][j]))
                    etiqueta_valor.setWordWrap(True)
                    etiqueta_valor.setToolTip(
                        self.matriz[0][i] + " debe " + "${:,.2f}".format(self.matriz[i][j]) + " a " + self.matriz[0][j])
                etiqueta_valor.setFixedSize(100, 40)
                self.distribuidor_tabla_compensacion.addWidget(
                    etiqueta_valor, i, j, Qt.AlignHCenter)

        #Elementos de espacio para ajustar las dimensiones de la tabla
        self.distribuidor_tabla_compensacion.layout().setRowStretch(len(self.matriz), 1)
        self.distribuidor_tabla_compensacion.layout().setColumnStretch(len(self.matriz), 1)


    def volver(self):
        """
        Esta función permite volver a la ventana de la actividad
        """   
        self.hide()
        self.interfaz.mostrar_actividad()
