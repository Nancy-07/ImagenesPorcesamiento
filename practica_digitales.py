from PIL import Image

# cargar la imagen y convertirla a escala de grises
img = Image.open('salida.jpg').convert('L')

# obtener los valores de intensidad de los píxeles
pixels = img.getdata()

# aplicar el umbral a cada pixel
threshold_value = 127
binary_pixels = []
for pixel in pixels:
    if pixel > threshold_value:
        binary_pixels.append(255)
    else:
        binary_pixels.append(0)

# crear la imagen binaria a partir de los píxeles umbralizados
binary_img = Image.new('L', img.size)
binary_img.putdata(binary_pixels)

# mostrar la imagen original y la imagen binaria
img.show()
binary_img.show()