from datetime import date

from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Session, engine, Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    session = Session()

    actividad_1 = Actividad("Paseo a la Playa")
    actividad_2 = Actividad("Caminata")
    session.add(actividad_1)
    session.add(actividad_2)
    session.commit()

    viajero_1 = Viajero("Juan Perez")
    viajero_2 = Viajero("Rosa Garcia")
    session.add(viajero_1)
    session.add(viajero_2)
    session.commit()

    gasto_1 = Gasto("Transporte", 100, date(2021, 1, 21))
    gasto_2 = Gasto("Comida", 200, date(2021, 1, 21))
    gasto_3 = Gasto("Transporte", 150, date(2021, 1, 28))
    session.add(gasto_1)
    session.add(gasto_2)
    session.add(gasto_3)
    session.commit()

    actividad_1.viajeros = [viajero_1, viajero_2]
    actividad_2.viajeros = [viajero_1]

    actividad_1.gastos = [gasto_1, gasto_2]
    actividad_2.gastos = [gasto_3]

    viajero_1.gastos = [gasto_1, gasto_3]
    viajero_2.gastos = [gasto_2]

    session.commit()
    session.close()
