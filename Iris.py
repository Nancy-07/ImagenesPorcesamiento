import numpy as np

fichero = open('iris.data')
lineas = fichero.read()
rows = lineas.split('\n')
data_array = []
sepalL = []
sepalW = []
petalL = []
petalW = []
classs = []

for row in rows:
    values = row.split(',')
    if len(values) >= 5:
        data_array.append(values)

data_array = np.array(data_array)
print(data_array.shape)

for data in data_array:
    if data[0]:
        sepalL.append(float(data[0]))
    if data[1]:
        sepalW.append(float(data[1]))
    if data[2]:
        petalL.append(float(data[2]))
    if data[3]:
        petalW.append(float(data[3]))
    if data[4]:
        if data[4] == 'Iris-setosa':
            classs.append(0)
        elif data[4] == 'Iris-versicolor':
            classs.append(1)
        elif data[4] == 'Iris-virginica':
            classs.append(2)
            
print(sepalL, sepalW, petalL, petalW, classs)



#Orientado a objetos 

class Iris:
    def __init__(self, sepalL, sepalW, petalL, petalW, clase):
        self.sepalL = sepalL
        self.sepalW = sepalW
        self.petalL = petalL
        self.petalW = petalW
        self.clase = clase

objetos = []

for data in data_array:
    if len(data) >= 5:
        sepalL = float(data[0]) if data[0] else None
        sepalW = float(data[1]) if data[1] else None
        petalL = float(data[2]) if data[2] else None
        petalW = float(data[3]) if data[3] else None
        clase = data[4] if data[4] else None

        # Asignar valores numéricos a la clase
        if clase == 'Iris-setosa':
            clase = 0
        elif clase == 'Iris-versicolor':
            clase = 1
        elif clase == 'Iris-virginica':
            clase = 2

        # Crear un objeto y agregarlo a la lista
        objeto = Iris(sepalL, sepalW, petalL, petalW, clase)
        objetos.append(objeto)

# Ejemplo de acceso a las propiedades de un objeto
for objeto in objetos:
    print(objeto.sepalL, objeto.sepalW, objeto.petalL, objeto.petalW, objeto.clase)


class Punto:
    def __init__(self, x, y, clase):
        self.x = x
        self.y = y
        self.clase = clase

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def get_clase(self):
        if self.clase == 0:
            return 'Iris-setosa'
        elif self.clase == 1:
            return 'Iris-versicolor'   
        elif self.clase == 2:
            return 'Iris-virginica'

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
    
    def set_clase(self, clase):
        self.clase = clase



class AlgoritmoPuntosCercanos:
    def __init__(self):
        self.puntos = []

    def agregar_punto(self, punto):
        self.puntos.append(punto)

    def encontrar_punto_mas_cercano(self, punto_referencia):
        punto_mas_cercano = None
        distancia_minima = float('inf')

        for punto in self.puntos:
            distancia = self.calcular_distancia(punto, punto_referencia)
            if distancia < distancia_minima:
                distancia_minima = distancia
                punto_mas_cercano = punto

        return punto_mas_cercano

    def calcular_distancia(self, punto1, punto2):
        # Implementa aquí el cálculo de distancia entre dos puntos (puedes utilizar la fórmula de distancia euclidiana)
        distancia = ((punto1.get_x() - punto2.get_x()) ** 2 + (punto1.get_y() - punto2.get_y()) ** 2) ** 0.5
        return distancia
    

import matplotlib.pyplot as plt

# Obtén las listas separadas de las propiedades "x" y "y"
x_valores = [objeto.petalL for objeto in objetos]
y_valores = [objeto.petalW for objeto in objetos]
clase_valores = [objeto.clase for objeto in objetos]

# Graficar los objetos en un gráfico de dispersión, asignando colores basados en la propiedad "clase"
plt.scatter(x_valores, y_valores, c=clase_valores, cmap='viridis' )

# Agregar etiquetas y título al gráfico
plt.xlabel("Propiedad X")
plt.ylabel("Propiedad Y")
plt.title("Gráfico de objetos por propiedades X y Y")

# Mostrar el gráfico
plt.show()

puntos = [Punto(x, y, clase) for x, y, clase in zip(x_valores, y_valores, clase_valores)]

algoritmo = AlgoritmoPuntosCercanos()

for punto in puntos:
    algoritmo.agregar_punto(punto)

punto_referencia = Punto(0, 0, None)
punto_cercano = algoritmo.encontrar_punto_mas_cercano(punto_referencia)
print("El punto más cercano a (0, 0) es: ({}, {}, {})".format(punto_cercano.get_x(), punto_cercano.get_y(), punto_cercano.get_clase()))