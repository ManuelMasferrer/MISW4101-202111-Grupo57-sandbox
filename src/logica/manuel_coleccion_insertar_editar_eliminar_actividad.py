from src.modelo.declarative_base import Session #Ivan
from src.logica.Logica_mock import * # Ivan

session = Session()
class Coleccion():

    def __init__(self):
        Base.metadata.create_all(engine)


    def insertar_la_actividad(self,nombre):
        busqueda = session.query(Actividad).filter(Actividad.nombre == nombre).all()
        if len(busqueda) ==0:
            actividad = Actividad(nombre=nombre)
            session.add(actividad)
            session.commit()
            return True
        else:
            return False

    def editar_la_actividad(self,nombre_a_cambiar, nombre_alternativo):
        busqueda = session.query(Actividad).filter(Actividad.nombre == nombre_a_cambiar).all()
        if len(busqueda) !=0:
            actividad = session.query(Actividad).filter(Actividad.nombre == nombre_a_cambiar).first()
            actividad.nombre = nombre_alternativo
            session.commit()
            return True
        else:
            return False

    def eliminar_la_actividad(self,nombre):
        busqueda = session.query(Actividad).filter(Actividad.nombre == nombre).all()
        if len(busqueda) !=0:
            session.query(Actividad).filter(Actividad.nombre == nombre).delete()
            session.commit()
            return True
        else:
            return False



