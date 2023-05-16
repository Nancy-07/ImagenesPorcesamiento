import numpy as np
import cv2 
from PIL import Image
# cargar la imagen en escala de grises
img = cv2.imread('salida.jpg', cv2.IMREAD_GRAYSCALE)
img1 = Image.open('salida.jpg').convert('L')
columnas, alto = img1.size
img1.show()

threshold_value, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
imgfinal = Image.fromarray(binary)
imgfinal.show()
print(threshold_value)

# Crear la lista de tamaño 256 para el histograma
hist = [0]*256

# Recorrer la imagen píxel por píxel y contar las intensidades de gris
for x in range(columnas):
    for y in range(alto):
         gris = img1.getpixel((x, y))
         hist[gris] += 1


# calcular la probabilidad de ocurrencia de cada nivel de gris
prob = hist / np.sum(hist)

# calcular la probabilidad acumulada de cada nivel de gris
prob_acum = np.cumsum(prob)

# calcular la media global de la imagen
media_global = np.sum(np.multiply(prob, np.arange(256)))

# inicializar la varianza máxima y el umbral óptimo
varianza_max = 0
umbral_optimo = 0

# recorrer todos los niveles de gris para encontrar el umbral óptimo
for umbral in range(1, 256):
    # calcular la probabilidad de ocurrencia de los píxeles por debajo del umbral
    prob_fondo = prob_acum[umbral]
    # calcular la probabilidad de ocurrencia de los píxeles por encima del umbral
    prob_objeto = 1 - prob_fondo

    # calcular la media del fondo y del objeto
    media_fondo = np.sum(np.multiply(prob[:umbral], np.arange(umbral)))
    media_objeto = np.sum(np.multiply(prob[umbral:], np.arange(umbral, 256)))

    # calcular la varianza entre clases
    varianza_entre = prob_fondo * prob_objeto * ((media_fondo - media_objeto) ** 2)

    # actualizar la varianza máxima y el umbral óptimo si se encuentra una varianza más alta
    if varianza_entre >= varianza_max:
        varianza_max = varianza_entre
        umbral_optimo = umbral

# aplicar el umbral óptimo a la imagen original para obtener la imagen binaria
binary_img = np.zeros_like(img)
binary_img[img > umbral_optimo] = 255

imgfinal = Image.fromarray(binary_img)
imgfinal.show()
print(imgfinal.size)