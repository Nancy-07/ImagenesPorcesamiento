from iris import IrisData
import numpy as np

class KnnClassifier( object):
    def __init__(self):
        #privado
        self.__k= 1
        self.___data = []
        self.__label= []

    def fit (self, xtrain, ytrain):
        self.__data = xtrain #data
        self.__label = ytrain #label 
    
    def predict (self,xtest, ytest):
        _train= self.__data
        _label= self.__label
        r= len( xtest) #numero de filas (netrebamiento)
        c= len(xtest[0]) #numero de columnas 

        labels = np.zeros(r)
        distance= self.distEuc(xtest)
        print(distance)
        idx= np.argsort(distance)[:2]
        print(idx)
        distSort= np.sort(distance,axis= 1)
        print( 'Ordenado: \n',distSort)

    def nearest (self, dist):
        distSort = np.sort(dist)

    def distEuc(self, xtest): #ecvalue Euclidean distance
        _train = self.__data 
        _label = self.__label
        rtest = len(xtest) #número de filas (entrenamiento)
        c = len(xtest[0]) #numero de columnas 
        rtrain = len(_train) #número de filas (entrenamiento)
        distance= np.zeros([rtest,rtrain]) #100 x 50

        for i in range (rtest): # 50
            for j in range (rtrain): # i 100
                suma=0.0
                for k in range(c): #for all vector elemennts (col)
                    suma = suma + ((xtest [i,k]- _train[j,k])**2)
                distance [i][j]= np.sqrt(suma)

        return distance
    
    def data(self):
        return self.__data
    
    def label(self):
        return self.__label
    
def split (mat_p, label, _num ):
    r = len (mat_p)#nuero de filas
    c = len(mat_p[0]) #numero de columnas

    num_train = r - _num #Muestra restantes para el test
    x_train = np.zeros([num_train,c]) #training set e.g m(100,4)
    y_train = np.zeros([num_train]) #label
    x_test = np.zeros([_num,c]) #Test set, e.g. m[100]
    y_test = np.zeros([_num])  #label

    for i in range (num_train):
        for j in range (c):
            x_train[i][j] = mat_p[i][j] #data
        y_train[i] = label[i] #label

    ix = i+1    
    for i in range (_num):
        for j in range (c):
            x_test[i,j] = mat_p[i+ix,j] #data
        y_test[i] = label[i] #label

    return x_train, y_train, x_test, y_test

#main
Iris = IrisData()
Iris.load('iris.data')
dataset = Iris.data()
n = 2
mat_p, label = Iris.permutacion(dataset) 
#/*-----------------------------------------------------------
# ytrain and ytest are labels 
xtrain, ytrain, xtest, ytest = split(mat_p,label,n)
knn = KnnClassifier()
knn.fit(xtrain,ytrain)
knn.predict(xtest,ytest)