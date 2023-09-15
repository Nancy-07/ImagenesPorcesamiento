import numpy as np
import matplotlib.pyplot as plt
import PIL
from math import floor

'''
Operaciones para el recorte y superposicion de la imagen
'''

def background(images): # (Img_i + img_i+1 + ... + img_n-1 + img_n)/ n
    widthImages = images[0].shape[0]
    heightImages = images[0].shape[1]

    backgroundImg = np.copy(images[0])

    for x in range(widthImages):
        for y in range(heightImages):
            r, g, b = 0, 0, 0
            for i in range(len(images)):
                r += images[i][x][y][0]
                g += images[i][x][y][1]
                b += images[i][x][y][2]
            r = r/len(images)
            g = g/len(images)
            b = b/len(images)
            backgroundImg[x][y][0] = r
            backgroundImg[x][y][1] = g
            backgroundImg[x][y][2] = b
    
    return backgroundImg
    
def difference(M, A): # D = abs(M-A)

    R, G, B = 0, 1, 2

    width_M, height_M, RGBM = M.shape

    width_A, height_A, RGBA = A.shape

    #CHANNELES RGB in M
    R_M = np.zeros(256)
    G_M = np.zeros(256)
    B_M = np.zeros(256)

    for row in range(width_M):
        for column in range(height_M):
            R_M[M[row][column][R]] += 1
            G_M[M[row][column][G]] += 1
            B_M[M[row][column][B]] += 1

    #CHANNELES RGB in A
    R_A = np.zeros(256)
    G_A = np.zeros(256)
    B_A = np.zeros(256)

    for row in range(width_A):
        for column in range(height_A):
            R_A[A[row][column][R]] += 1
            G_A[A[row][column][G]] += 1
            B_A[A[row][column][B]] += 1

    #Diference abs(M-A)
    D = np.zeros((width_A, height_A, 3), dtype=np.uint8)

    for row in range(width_A):
        for column in range(height_A):
            D[row][column][R] = abs(M[row][column][R]-A[row][column][R])
            D[row][column][G] = abs(M[row][column][G]-A[row][column][G]) 
            D[row][column][B] = abs(M[row][column][B]-A[row][column][B]) 

    return D

def gray(img): #Img to gray with 0.21*img[x,y,r]+0.72*img[x,y,g]+0.07*img[x,y,b]
    imgGray = np.copy(img)
    R, G, B = 0, 1, 2
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            r, g, b = img[x][y]
            imgGray[x][y][R] = 0.21*r + 0.72*g + 0.07*b
            imgGray[x][y][G] = 0.21*r + 0.72*g + 0.07*b
            imgGray[x][y][B] = 0.21*r + 0.72*g + 0.07*b
    
    return imgGray

def thresholding(D, threshold): # 0 or 255 since the threshold
    R, G, B = 0, 1, 2

    width_D, height_D, RGBD = D.shape
    thresholdImg = np.copy(D)
    for row in range(width_D):
        for column in range(height_D):
            if(D[row][column][R]>threshold):
                thresholdImg[row][column][R] = 255
            else:
                thresholdImg[row][column][R] = 0
            if(D[row][column][G]>threshold):
                thresholdImg[row][column][G] = 255
            else:
                thresholdImg[row][column][G] = 0
            if(D[row][column][B]>threshold):
                thresholdImg[row][column][B] = 255
            else:
                thresholdImg[row][column][B] = 0
    
    return thresholdImg


def invertedMask(mask):
    widthMask = mask.shape[0]
    heightMask = mask.shape[1]

    invertedMaskImg = np.copy(mask)

    for x in range(widthMask):
        for y in range(heightMask):
            r, g, b = mask[x][y]

            if(r==255 and g==255 and b==255):
                r, g, b = 0, 0, 0
            else:
                r, g, b = 255, 255, 255
            
            invertedMaskImg[x][y][0] = r
            invertedMaskImg[x][y][1] = g
            invertedMaskImg[x][y][2] = b
    
    return invertedMaskImg

def binaryMask(mask):
    widthMask = mask.shape[0]
    heightMask = mask.shape[1]

    binaryMaskArray = np.copy(mask)

    for x in range(widthMask):
        for y in range(heightMask):
            r, g, b = mask[x][y]

            if(r==0 and g==0 and b==0):
                binaryR, binaryG, binaryB = 0, 0, 0
            else:
                binaryR, binaryG, binaryB = 1, 1, 1

            binaryMaskArray[x][y][0] = binaryR
            binaryMaskArray[x][y][1] = binaryG
            binaryMaskArray[x][y][2] = binaryB
    
    return binaryMaskArray

def R(F,U,A):
    Rimg = np.copy(F)
    widthR = Rimg.shape[0]
    heightR = Rimg.shape[1]

    for x in range(widthR):
        for y in range(heightR):
            if(U[x][y][0]==255 and U[x][y][1]==255 and U[x][y][2]==255):
                Rimg[x][y][0] = A[x][y][0]
                Rimg[x][y][1] = A[x][y][1]
                Rimg[x][y][2] = A[x][y][2]
    
    return Rimg

'''
Inician las operaciones morfologicas
'''

def convolucionErosion(img, kernel):
    kernelint = floor(kernel.shape[0]/2)
    R, G, B = 0, 1, 2
    img = binaryMask(img)
    matrizExtendida =  np.zeros((img.shape[0]+kernelint*2, img.shape[1]+ kernelint*2, 3))
    for i in range(kernelint, matrizExtendida.shape[0] - kernelint):
        for j in range(kernelint, matrizExtendida.shape[1] - kernelint):
            matrizExtendida[i][j][R] = img[i-kernelint][j-kernelint][R]
            matrizExtendida[i][j][G] = img[i-kernelint][j-kernelint][G]
            matrizExtendida[i][j][B] = img[i-kernelint][j-kernelint][B]
            
    matrixRes = np.zeros((img.shape[0], img.shape[1], img.shape[2]))
    
    Elementval=kernel.shape[0]* kernel.shape[1]
    for i in range(kernelint, matrizExtendida.shape[0] - kernelint):
        for j in range(kernelint, matrizExtendida.shape[1] - kernelint):
            veriR, veriG, veriB = 0, 0, 0
            for m in range(kernel.shape[0]):
                for n in range(kernel.shape[1]):
                    if (kernel[m][n] == matrizExtendida[i-kernelint+m][j-kernelint+n][R]):
                        veriR =  veriR + 1
                    if (kernel[m][n] == matrizExtendida[i-kernelint+m][j-kernelint+n][G]):
                        veriG =  veriG + 1
                    if (kernel[m][n] == matrizExtendida[i-kernelint+m][j-kernelint+n][B]):
                        veriB =  veriB + 1
            if (veriR == Elementval):
                matrixRes[i-kernelint][j-kernelint][R] = 255
            if (veriR == Elementval):
                matrixRes[i-kernelint][j-kernelint][G] = 255
            if (veriR == Elementval):
                matrixRes[i-kernelint][j-kernelint][B] = 255
    return matrixRes.astype(np.uint8)

def convolucionDilatacion(img, kernel):
    kernelint = floor(kernel.shape[0]/2)
    R, G, B = 0, 1, 2
    matrizExtendida =  np.zeros((img.shape[0]+kernelint*2, img.shape[1]+ kernelint*2, 3))
    for i in range(kernelint, matrizExtendida.shape[0] - kernelint):
        for j in range(kernelint, matrizExtendida.shape[1] - kernelint):
            matrizExtendida[i][j][R] = img[i-kernelint][j-kernelint][R]
            matrizExtendida[i][j][G] = img[i-kernelint][j-kernelint][G]
            matrizExtendida[i][j][B] = img[i-kernelint][j-kernelint][B]
            
    matrixRes = np.zeros((img.shape[0], img.shape[1], img.shape[2]))
    
    for i in range(kernelint, matrizExtendida.shape[0] - kernelint):
        for j in range(kernelint, matrizExtendida.shape[1] - kernelint):
            veriR, veriG, veriB = 0, 0, 0
            for m in range(kernel.shape[0]):
                for n in range(kernel.shape[1]):
                    if (kernel[m][n] == 1  and (matrizExtendida[i-kernelint+m][j-kernelint+n][R] == 1 or matrizExtendida[i-kernelint+m][j-kernelint+n][R] == 255)):
                        veriR =  veriR + 1
                    if (kernel[m][n] == 1  and (matrizExtendida[i-kernelint+m][j-kernelint+n][G] == 1 or matrizExtendida[i-kernelint+m][j-kernelint+n][G] == 255)):
                        veriG =  veriG + 1
                    if (kernel[m][n] == 1  and (matrizExtendida[i-kernelint+m][j-kernelint+n][B] == 1 or matrizExtendida[i-kernelint+m][j-kernelint+n][R] == 255)):
                        veriB =  veriB + 1
            if (veriR > 1):
                matrixRes[i-kernelint][j-kernelint][R] = 255
            if (veriR > 1):
                matrixRes[i-kernelint][j-kernelint][G] = 255
            if (veriR > 1):
                matrixRes[i-kernelint][j-kernelint][B] = 255
    return matrixRes.astype(np.uint8)

#Elemento estructurante
struct = np.ones((5,5))

#Se hace el recorte de la mascara inicial
A = np.array(PIL.Image.open("daphne.jpg"))
F = np.resize(np.array(PIL.Image.open("paris.jpg")), (A.shape[0], A.shape[1], 3))
images = [np.array(PIL.Image.open("2.jpg")),np.array(PIL.Image.open("3.jpg")),np.array(PIL.Image.open("4.jpg"))]
M = background(images)
D = gray(difference(M, A))
mask = thresholding(D, 200)
U = invertedMask(mask)
binary_Mask = binaryMask(U)

'''
Aplicación de las funciones
'''
#Erosion 
Erosion = convolucionErosion(binary_Mask, struct)
#Dilatacion
#Dis = convolucionDilatacion(binary_mask, struct)

#Combinación de las funcipnes
#EroDis = convolucionDilatacion(Erosion, struct)
#DisEro = convolucionErosion(Dis, struct) 

'''
Mostrar los resultados
'''

fig, axs = plt.subplots(1,4,figsize=(15, 4))
axs[0].imshow(Erosion)
axs[0].set_title("Erosion")
axs[1].imshow(U)
axs[1].set_title("Mask")
axs[2].imshow(R(F, Erosion, A))
axs[2].set_title("Result")
axs[3].imshow(F)
axs[3].set_title("Fondo real")
plt.show()