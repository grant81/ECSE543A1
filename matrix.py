import numpy as np
import math
import random
import csv

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.opMatrix = createZeros(matrix.shape)
        self.cholMat = createZeros(matrix.shape)

    def isSymmetry(self):
        tMatrix = self.matrix
        tMatrixTranspose = transpose(tMatrix)
        return np.array_equal(tMatrix, tMatrixTranspose)

    def isSquare(self):
        matrix = self.matrix.tolist()
        if (isinstance(self.matrix.shape, int)):
            temp = matrix
            matrix = []
            matrix.append(temp)
        elif (len(self.matrix.shape) == 1):
            temp = matrix
            matrix = []
            matrix.append(temp)
        return (len(matrix) == len(matrix[0]))

    def cholesky(self):
        L = createZeros(self.matrix.shape)
        opMatrix = self.matrix
        dim = opMatrix.shape[1]
        if not self.isSquare():
            return "must be a square Matrix"
        elif not self.isSymmetry():
            return "Matrix must be Symmetric"
        else:
            for j in range(0, dim):
                L[j][j] = np.sqrt(opMatrix[j][j])
                for i in range(j + 1, dim):
                    L[i][j] = opMatrix[i][j] / L[j][j]
                    for k in range(j + 1, i + 1):
                        opMatrix[i][k] = opMatrix[i][k] - L[i][j] * L[k][j]
            for q in np.nditer(L):
                if math.isnan(q):
                    return "matrix must be positive defined"
        return L

    def fElimination(self, b):
        L = self.cholMat
        y = createZeros(b.shape)
        length = b.shape[0]
        for i in range(0, length):
            sum = 0
            if (i - 1) >= 0:
                for j in range(0, i):
                    sum = L[i][j] * y[j] + sum
            y[i] = (b[i] - sum) / L[i][i]
        return y

    def bSubstitution(self, y):
        L = self.cholMat
        x = createZeros(y.shape)
        length = y.shape[0]
        for i in range(length-1,-1,-1):
            sum = 0
            for j in range(i+1,length,1):
                sum = sum +L[j][i]*x[j]
            x[i] = (y[i]-sum)/L[i][i]
        return x

    def solForX(self, b):

        self.cholMat = self.cholesky()
        y = self.fElimination(b)
        x = self.bSubstitution(y)
        return x

def createZeros (shape):
    if (isinstance(shape,int)):
        result = [0 for i in range(shape)]
    elif(len(shape)==1):
        result = [0 for i in range(shape[0])]
    elif (len(shape)==2):
        result = [[0 for i in range(shape[1])] for j in range(shape[0])]
    else:
        return 'the matrix dimension is wrong'
    out = np.array(result,dtype=float)
    return out

def dotProduct (a,b):
    matrixA = a.tolist()
    matrixB = b.tolist()
    if(len(a.shape)==1):
        temp = matrixA
        matrixA = []
        matrixA.append(temp)
    if(len(b.shape)==1):
        temp = matrixB
        matrixB = []
        matrixB.append(temp)

    rowA = len(matrixA)
    rowB = len(matrixB)
    colA = len(matrixA[0])
    colB = len(matrixB[0])

    if(colA!= rowB):
        return 'the matrix dimension is wrong'
    result = createZeros((rowA,colB))

    for i in range(rowA):
        for j in range(colB):
                for k in range(rowB):
                    result[i][j] += matrixA[i][k]*matrixB[k][j]

    return result

def transpose(matrix):
    matrixToTranspose = matrix

    if (isinstance(matrix.shape,int)):
        result = createZeros((matrix.shape[0],1))
        for i in range(matrix.shape[0]):
            result [i][0] = matrix[i]
    elif(len(matrix.shape)==1):
        result = createZeros((matrix.shape[0],1))
        for i in range(matrix.shape[0]):
            result [i][0] = matrix[i]
    else:
        rows = matrixToTranspose.shape[0]
        columns = matrixToTranspose.shape[1]
        result = createZeros((columns,rows))
        for i in range(0, rows):
            for j in range(0, columns):
                result[j][i] = matrixToTranspose[i][j]
    # result = matrixToTranspose.transpose()
    return result

def matrixSub(a,b):

    if (a.shape!=b.shape):
        return "matrix dimension not equal"
    result = createZeros(a.shape)
    if len(a.shape) == 1:
        for i in range(0,a.shape[0]):
            result[i] = a[i] - b[i]
    else:
        for i in range(0,a.shape[0]):
            for j in range(0,a.shape[1]):
                result[i][j] = a[i][j]-b[i][j]
    return result


def genMatrix(length):
    randomMatrix = createZeros((length, length))
    for i in range(0, length):
        for j in range(0, i + 1):
            randomMatrix[i][j] = random.randint(1, 30)
    ranTan = transpose(randomMatrix)
    A = dotProduct(randomMatrix, ranTan)
    return A
def readFile(cirNum):
    with open('CircuitQ1.csv','r')as data:
        reader = csv.reader(data)
        out = list (reader)
    data.close()
    dataToProcess = out[cirNum-1]
    output={
        'A' : [],
        'E' : [],
        'J' : [],
        'R' : []
    }
    i = 1
    end = len(dataToProcess)
    rowsA = []
    while (dataToProcess[i]!= 'E' and i<end):
        if (dataToProcess[i]==','):
            output['A'].append(rowsA)
            i +=1
            rowsA = []
        rowsA.append(float(dataToProcess[i]))
        i += 1
    output['A'].append(rowsA)
    i +=1
    while (dataToProcess[i]!='J' and i<end):
        output['E'].append(float(dataToProcess[i]))
        i += 1
    i+=1
    while (dataToProcess[i]!='R' and i<end):
        output['J'].append(float(dataToProcess[i]))
        i += 1
    i+=1
    while (dataToProcess[i]!='' and i<end):
        output['R'].append(float(dataToProcess[i]))
        i += 1
        if(i==end):
            break
    output['E'] = transpose(np.array(output['E']))
    output['J'] = transpose(np.array(output['J']))
    output['R'] = transpose(np.array(output['R']))
    return output

def solveCircuit(cirNum):
    cirInfo = readFile(cirNum)
    A = np.array(cirInfo['A'])
    E = np.array(cirInfo['E'])
    J = np.array(cirInfo['J'])
    R = np.array(cirInfo['R'])
    #(AYA^t)Vn = A(j-YE)
    Y = createZeros((R.shape[0],R.shape[0]))
    for i in range(R.shape[0]):
        Y[i][i] = 1/R[i]

    YE = dotProduct(Y,E)
    b = dotProduct(A,matrixSub(J,YE))
    AY = dotProduct(A,Y)
    AYAt = dotProduct(AY,A.transpose())
    ans = Matrix(AYAt)
    Vn = ans.solForX(b)
    print ("the voltage for circuit "+str(cirNum)+" is: \n"+str(Vn)+" V")
    return Vn

def solveVoltage(A,E,J,R):

    # (AYA^t)Vn = A(j-YE)
    Y = createZeros((R.shape[0], R.shape[0]))
    for i in range(R.shape[0]):
        Y[i][i] = 1 / R[i]
    YE = dotProduct(Y, E)
    b = dotProduct(A, matrixSub(J, YE))
    AY = dotProduct(A, Y)
    AYAt = dotProduct(AY, transpose(A))
    ans = Matrix(AYAt)
    Vn = ans.solForX(b)
    return Vn
   # print(Vn)

# #
#
# for i in range(1,6):
#      solveCircuit(i)
#
# # t2 = t1
# # t1 = []
# # t1.append(t2)
# t3 = np.array(t1)
# t4 = t3.tolist()
# print(transpose(t3))
# print(t1[0][0])
# print(len(t1[0]))
# print(len(t4[0]))
# a1 = np.array([[1,2,3],[]])
# a2 = np.array([[2,4,5]])
# print(readFile(2))
# print(dotProduct(a1,a2))
# print(np.dot(a1,a2))

