from sqlalchemy import inspect, func, Numeric

from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero, ActividadViajero
from src.modelo.declarative_base import Session

#if __name__ == '__main__':
session = Session()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

# Esta es la linea para generar una lista con el nombre de las actividades registradas:
# actividades = [a.nombre for a in session.query(Actividad.nombre).all()]

actividades = []
actividades1 = session.query(Actividad).all()
for act in actividades1:
    actividades.append(object_as_dict(act))

print("Las actividades registradas son:")
print(actividades)

viajeross = session.query(Viajero).all()
viajeros1 = []
for viajero in viajeross:
    viajeros1.append(object_as_dict(viajero))

print(viajeros1)
print(type(viajeros1[1]))

print("Los viajeros registrados son:")
viajeros = []
for i in range(len(viajeros1)):
    viajeros.append({"Nombre": viajeros1[i]["nombre"],"Apellido":viajeros1[i]["apellido"]})
print(viajeros)







activities = []
actividades1 = session.query(Actividad).all()
for act in actividades1:
    activities.append(object_as_dict(act))

actividad = "Paseo a la Playa"
for act in activities:
    actnom = act.get("nombre")
    if actnom == actividad:
        act_id = act.get("id")
print('el id de actividad es:')
print(act_id)


#
gastos1 = session.query(Gasto).join(Actividad).filter(Gasto.actividad == act_id).all()
gastos = []
for gasto in gastos1:
    gastos.append(object_as_dict(gasto))
for g in gastos:
    vid = g.get("viajero")
    for viajero in viajeros1:
        if viajero['id'] == vid:
            g["Nombre"] = viajero['nombre']
            g["Apellido"] = viajero['apellido']

print("Los gastos registrados en la actividad " + actividad + " son:")
print(gastos)

# Funcionalidad para encontrar id de la actividad actual
for act in activities:
    actnom = act.get("nombre")
    if actnom == actividad:
        act_id = act.get("id")


# Funcionalidad para consultar los viajeros en actividad
# viajeros_act = session.query(Actividad).filter(if act_id in Actividad.viajeros).join(Actividad).order_by(Viajero.id)

viajeros_actividad = []
q2 = session.query(ActividadViajero).all()
for q in q2:
    viajeros_actividad.append(object_as_dict(q))
print(viajeros_actividad)

gastos_viajero_act = []
viajeros_act = []
for item in viajeros_actividad:
    actid = item.get("actividad")
    if actid == act_id:
        gastos_viajero_act.append([item.get("viajero"),0])
        viajeros_act.append(item.get("viajero"))
print("Los viajeros registrados en la actividad "  + actividad + " son:")
print(viajeros_act)
print(gastos_viajero_act)
# for viajero in viajeros:



gastos_consolidados = []
gastos2 = session.query(Gasto.viajero, func.sum(Gasto.valor).label('GastoViajero') ).join(Actividad).filter(Gasto.actividad == act_id).group_by(Gasto.viajero).all()
print("Los gastos de cada viajero en la actividad " + actividad + " son:")
#print(gastos2)



for id in viajeros_act:
    for i in range(len(gastos2)):
        if id == gastos2[i][0]:
            gastos_viajero_act[id-1][1] = gastos2[i][1]

print(gastos_viajero_act)

total =0
n_viajeros = 0
for gast in gastos_viajero_act:
    total += gast[1]
    n_viajeros += 1
print("El gasto promedio en la actividad " + actividad + " es:")
print(total/n_viajeros)

for gast in gastos_viajero_act:
    gastos_consolidados.append(list(gast))
for g in gastos_consolidados:
    if (g[1]-total/n_viajeros) < 0:
        g.append(total/n_viajeros-g[1])
        g.append(0)
    else:
        g.append(0)
        g.append(g[1]-total/n_viajeros)
    print(g)

gastos_act = gastos_consolidados
print("Los gastos y deudas por viajero en la actividad "+ actividad + " son:")
print(gastos_consolidados)
print(type(gastos_consolidados))
print(type(gastos_consolidados[0]))
print(len(gastos_consolidados))

matriz = []

for g in gastos_consolidados:
    matriz.append([])
for j in range(len(gastos_consolidados)):
    for row in gastos_consolidados:
       i=1
       if j+1==row[0]:
           matriz[j].append(-1)
       elif row[3] == 0:
           matriz[j].append(0)
       elif row[3] >0:
           if row[3] > gastos_consolidados[j][2]:
            matriz[j].append(gastos_consolidados[j][2])
            row[3] = row[3] - gastos_consolidados[j][2]
            gastos_consolidados[j][2] = 0
           elif row[3] <= gastos_consolidados[j][2]:
            matriz[j].append(row[3])
            gastos_consolidados[j][2] = gastos_consolidados[j][2] - row[3]
            row[3] = 0
       i+=1


#print(gastos_consolidados)
print("La matriz de compensacion es:")
print(matriz)

# gastos_act = []
# for gast in gastos2:
#     gastos_act.append(object_as_dict(gast))
# print(gastos_act)
# for g in gastos_act:
#     vid = g.get("viajero")
#     for viajero in viajeros:
#         if viajero['id'] == vid:
#             g["Nombre"] = viajero['nombre']
#             g["Apellido"] = viajero['apellido']


viajeros_en_act = []
for id in viajeros_act:
    for viajero in viajeros1:
        if id == viajero["id"]:
            viajeros_en_act.append(viajero["nombre"])
            viajeros_en_act[id-1] = viajeros_en_act[id-1]+ ' ' +viajero['apellido']

#     for viajero in
#     viajnom = session.query(Viajero).filter(Viajero.id == id)
#     print(type(object_as_dict(viajnom)))
#    viajeros_en_actividad.append(Viajero.nombre)
print(viajeros_en_act)

# Construimos la lista de viajeros en la actividad, con formato de lista de diccionarios
viajeros_en_actividad = []
for viajero in viajeros1:
    if viajero['id'] not in viajeros_act:
        viajerodict = {"Nombre": viajero['nombre']+' '+viajero['apellido'], "Presente":False}
        viajeros_en_actividad.append(viajerodict)
    else:
        viajerodict = {"Nombre": viajero['nombre']+' '+viajero['apellido'], "Presente":True}
        viajeros_en_actividad.append(viajerodict)
print("La lista de viajeros en la actividad " + actividad + ' es:')
print(viajeros_en_actividad)


# Finalmente construimos la matriz de compensacion a desplegar
# matriz_header=[[""]]
# for viajero in viajeros_en_actividad:
#     matriz_header[0].append(viajero['Nombre'])
# for i in range(len(matriz)):
#     matriz[i].insert(0,matriz_header[0][i+1])

matriz_header=[[""]]
for viajero in viajeros_en_actividad:
    matriz_header[0].append(viajero['Nombre'])
for i in range(len(matriz)):
    matriz[i].insert(0,matriz_header[0][i+1])
matriz.insert(0, matriz_header[0])
print(matriz_header)
print(matriz)









# print(type(gastoss))
# print(object_as_dict(gastoss[0]))




# def dar_actividades():
#     actividades_lista = session.query(Actividad.nombre).all()
#     activities = []
#     for actividad in actividades_lista:
#          activities.append(actividad.nombre)
#     return activities

# print('Las actividades almacenadas son:')
# actividades=dar_actividades()
# activities = []
# for actividad in actividades:
#     activities.append(actividad.nombre)


session.close()