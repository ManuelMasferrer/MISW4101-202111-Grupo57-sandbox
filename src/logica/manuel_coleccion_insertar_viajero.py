from src.modelo.declarative_base import Session #Ivan
from src.logica.Logica_mock import * # Ivan

session = Session()
class Coleccion():

    def __init__(self):
        Base.metadata.create_all(engine)

    def insertar_el_viajero(self,nombre, apellido):
        busqueda = session.query(Viajero).filter(Viajero.nombre == nombre and Viajero.apellido == apellido).all()
        if len(busqueda) ==0:
            viajero = Viajero(nombre = nombre, apellido = apellido)
            session.add(viajero)
            session.commit()
            return True
        else:
            return False
