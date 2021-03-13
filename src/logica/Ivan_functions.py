from src.modelo.declarative_base import Session #Ivan
from src.logica.Logica_mock import * # Ivan
from src.logica.manuel_coleccion_insertar_editar_eliminar_actividad import Coleccion



if __name__ == "__main__":
    session = Session()
    for i in session.query(Actividad):
        print(i.nombre)

    lista_dict_viajeros_presentes = [{"Nombre":i.nombre, "Apellido":i.apellido, "Presente":False} for i in session.query(Viajero)]
    print(lista_dict_viajeros_presentes)
    for i in session.query(Viajero):
        print(i.apellido)
    print("Hello")

    lista_dict_viajero = list()
    for viajero in session.query(Viajero).all():
        print(object_as_dict(viajero))

    print(" ")

    for actividad in session.query(Actividad).all():
        print(object_as_dict(actividad))

    for i in session.query(Gasto).join(Actividad).filter(Gasto.actividad == 1).all():
        print(i.concepto)

    first_actividad = session.query(Actividad).filter(Actividad.id ==1).all()
    for i in first_actividad:
        print(i.nombre)
    print("")
    a = session.query(Actividad).filter(Actividad.id ==1).all()
    for i in a:
        print(i.nombre)
    second_actividad = session.query(Actividad).filter(Actividad.nombre == "actividad 15").all()
    print(len(second_actividad), type(second_actividad), second_actividad)
    for i in second_actividad:
        print(i.nombre)

    clase_insertar = Coleccion()
    print("******")

    print(clase_insertar.insertar_la_actividad("Ir a venecia"))

    def insertar_la_actividad(nombre):
        busqueda = session.query(Actividad).filter(Actividad.nombre == nombre).all()
        if len(busqueda) ==0:
            actividad = Actividad(nombre=nombre)
            session.add(actividad)
            session.commit()
            return True
        else:
            return False

    print(insertar_la_actividad("Ir a Hong Kong"), "Hello")

    def insertar_el_viajero(nombre, apellido):
        busqueda = session.query(Viajero).filter(Viajero.nombre == nombre and Viajero.apellido == apellido).all()
        if len(busqueda) ==0:
            viajero = Viajero(nombre = nombre, apellido = apellido)
            session.add(viajero)
            session.commit()
            return True
        else:
            return False
    print("******")
    print(insertar_el_viajero(nombre="Samuel",apellido="Rodriguez"))
    print("********")
