from src.modelo.actividad import Actividad
from src.modelo.declarative_base import engine, Base, session

class Listado():

    def __init__(self):
        Base.metadata.create_all(engine)

    def dar_actividades(self):
        self.lista_actividades = session.query(Actividad).all()





# Agregar actividad
# Ver actividad
# Editar actividad
# Borrar actividad
# Agregar viajero
# Terminar actividad
# Ver viajeros