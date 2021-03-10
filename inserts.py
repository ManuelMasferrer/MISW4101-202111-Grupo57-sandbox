from datetime import date

from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Session, engine, Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    session = Session()


#  Crear actividades y agregarlas a la base de datos con add y commit
    actividad_1 = Actividad("Paseo a la Playa")
    actividad_2 = Actividad("Caminata")
    session.add(actividad_1)
    session.add(actividad_2)
    session.commit()

 # Crear los viajeros y agregarlos a la base de datos con add y commit
    viajero_1 = Viajero("Juan", "Perez")
    viajero_2 = Viajero("Rosa", "Garcia")
    viajero_3 = Viajero("Luis", "Mora")
    viajero_4 = Viajero("Ana", "Zavala")
    session.add(viajero_1)
    session.add(viajero_2)
    session.add(viajero_3)
    session.add(viajero_4)
    session.commit()

# Crear los gastos.  Note que el atributo fecha en este momento es String.

    gasto_1 = Gasto("Transporte", 100, '21-01-2021')
    gasto_2 = Gasto("Comida", 200, '22-01-2021')
    gasto_3 = Gasto("Bebida", 90, '23-01-2021')
    gasto_4 = Gasto("Fiesta",120,'24-01-2021')
    gasto_5 = Gasto("Transporte", 150, '28-01-2021')
    session.add(gasto_1)
    session.add(gasto_2)
    session.add(gasto_3)
    session.add(gasto_4)
    session.add(gasto_5)
    session.commit()

#  Crea las relaciones entre actividad y viajero (cuales son los viajeros asociados a cada actividad)

    actividad_1.viajeros = [viajero_1, viajero_2, viajero_3, viajero_4]
    actividad_2.viajeros = [viajero_2]

# Crea las relaciones entre actividad y gasto *(cuales son los gastos de cada actividad)

    actividad_1.gastos = [gasto_1, gasto_2, gasto_3, gasto_4]
    actividad_2.gastos = [gasto_5]

# Crea las relaciones entre viajero y gastos (que viajero realizo cada gasto)

    viajero_1.gastos = [gasto_1, gasto_3]
    viajero_2.gastos = [gasto_2, gasto_5]
    viajero_3.gastos = [gasto_4]
    viajero_4.gastos = []
    session.commit()

# Cierra la sesion
    session.close()
