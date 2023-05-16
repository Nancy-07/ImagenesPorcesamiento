from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('prueba2.jpg')
imgarr= np.array(img)
height,width,ca = imgarr.shape
gris = np.zeros_like(imgarr)

for h in range(height):
     for w in range(width):
       gris[h][w] = (imgarr[h][w][0] * 0.21) + (imgarr[h][w][1] * 0.72) + (imgarr[h][w][2] * 0.07)


#fondof = Image.fromarray(gris)
#fondof.show()

# esta función presenta fallo, por lo tanto no hacerle caso 
def recoloracion(vr, vg, vb, cc):
  height,width,ca = imgarr.shape
  colores = np.zeros_like(img)
  for c in range(height):
     for k in range(width):
       if gris[c][k][0] < cc:
        colores[c][k][0] = np.round((vr * gris[c][k][0])/cc)
        colores[c][k][1] = np.round((vg * gris[c][k][0])/cc)
        colores[c][k][2] = np.round((vb * gris[c][k][0])/cc)      
       else:
        colores[c][k][0] = vr + np.round((255-vr) * ((gris[c][k][0] - cc)/(255 -cc)))
        colores[c][k][1] = vg + np.round((255-vg) * ((gris[c][k][0] - cc)/(255 -cc)))
        colores[c][k][2] = vb + np.round((255-vb) * ((gris[c][k][0] - cc)/(255 -cc)))
        if (colores[c][k][0]>=255):
          colores[c][k][0] =255
        elif(colores[c][k][1]>=255):
          colores[c][k][1] =255
        elif(colores[c][k][2]>=255):
          colores[c][k][2] =255
        if (colores[c][k][0]<=0):
          colores[c][k][0] = 0
        elif(colores[c][k][1])<=0:
          colores[c][k][1] = 0
        elif(colores[c][k][2])<=0:
          colores[c][k][2] = 0
      

  im = Image.fromarray((colores).astype(np.uint8))
  im.show()    
recoloracion(80,80,50,128)
