from src.modelo.declarative_base import Session #Ivan
from src.logica.Logica_mock import * # Ivan


if __name__ == "__main__":
    session = Session()
    for i in session.query(Actividad):
        print(i.nombre)
    print("Hello")