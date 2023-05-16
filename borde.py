import numpy as np
from PIL import Image

img = np.array(Image.open("persona1.jpg"))

mascara = np.array([[-1, -1, -1], 
                    [-1,  8, -1], 
                    [-1, -1, -1]])

#mascara = mascara / 25 #normalización de la mascara

filas,columnas,canales = img.shape# obtención de los tamaños de las imagenes 

mascaraf, mascaraC = mascara.shape
bordeH = int((mascaraf-1)/2)
bordeA = int((mascaraC-1)/2)
matrizF = np.zeros((filas + (mascaraf-1), columnas + (mascaraC-1),canales))#matriz mas grande para eviatar el desbordamiento

matrizF[bordeH:filas+bordeH, bordeA:columnas+bordeA] = img # se copia la imagen 

matrizfinal = np.zeros_like(img)# se genera la matriz en donde se almacenan los datos 

for i in range(bordeH, filas + bordeH):
    for j in range(bordeA, columnas + bordeA):
        matrizfinal[i-bordeH, j-bordeA, 0] = np.sum(mascara * matrizF[i-bordeH:i+bordeH+1, j-bordeA:j+bordeA+1, 0])
        matrizfinal[i-bordeH, j-bordeA, 1] = np.sum(mascara * matrizF[i-bordeH:i+bordeH+1, j-bordeA:j+bordeA+1, 1])
        matrizfinal[i-bordeH, j-bordeA, 2] = np.sum(mascara * matrizF[i-bordeH:i+bordeH+1, j-bordeA:j+bordeA+1, 2])

#se imprime la imagen
Aimg = Image.fromarray(matrizfinal)
Aimg.show()