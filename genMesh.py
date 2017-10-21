from matrix import *
import numpy as np
import time

class Mesh:
    def __init__(self, n):
        self.n = n

    def generateMesh(self):
        n = self.n
        row = n + 1
        col = 2 * n + 1
        nodes = row * col
        branch = 4 * (n ** 2) + 3 * n
        A = createZeros((nodes, branch + 1))
        for i in range(nodes):
            down = row * (col - 1) + i
            up = down - col
            left = (int(i / col)) * (col - 1) + i % col
            right = left - 1

            if (i < col):
                up = -1
            if ((i % col) == 0):
                right = -1
            if ((i % col) == (col - 1)):
                left = -1
            if (i > (nodes - col-1)):
                down = -1
            if (down >= 0):
                A[i][down] = 1
            if (up >= 0):
                A[i][up] = -1
            if (left >= 0):
                A[i][left] = 1
            if (right >= 0):
                A[i][right] = -1
        #take care of the 1 ohm resister and the voltage source
        A[0][branch] = -1
        A[nodes-1][branch] = 1
        A = A[:-1].copy()
        A = np.array(A,dtype=float)
        return A
    def generateE(self):
        n= self.n
        branch = 4 * (n ** 2) + 3 * n
        E = createZeros((branch+1,1))
        E[branch][0] = 1.0

        return E
    def generateJ(self):
        n = self.n
        branch = 4 * (n ** 2) + 3 * n
        J = createZeros((branch + 1, 1))
        return J
    def generateR(self):
        n = self.n
        branch = 4 * (n ** 2) + 3 * n
        R = createZeros((branch + 1, 1))
        for i in range (branch):
            R[i][0] = 1000.0
        R[branch][0] = 1.0
        return R

def sparseStore(matrix):
    row = len(matrix)
    col = len(matrix[0])
    store = []
    for i in range(0,row):
        for j in range(0,col):
            if (matrix[i][j]!=0.0):
                temp = [i,j,matrix[i][j]]
                store.append(temp)
    temp = [row,col]
    #record the orgional matrix dimision
    store.append(temp)
    return store
# a= Mesh(2)
# A = a.generateMesh()
# print(sparseStore(A))

def sparseDot (sMatrix1,sMatrix2):
    result = createZeros((int(sMatrix1[len(sMatrix1)-1][0]),int(sMatrix2[len(sMatrix2)-1][1])))
    for i in range(len(sMatrix1)-1):
        row1 = int(sMatrix1[i][0])
        col1 = int(sMatrix1[i][1])
        val1 = sMatrix1[i][2]
        for j in range(len(sMatrix2)-1):
            row2 = int(sMatrix2[j][0])
            col2 = int(sMatrix2[j][1])
            val2 = sMatrix2[j][2]
            if(col1 == row2):
                result[row1][col2]+= val1*val2

    return result


def solveVoltageSparse(A,E,J,R):
    Y = createZeros((R.shape[0], R.shape[0]))
    for i in range(R.shape[0]):
        Y[i][i] = 1 / R[i]
    As = sparseStore(A)
    At = transpose(A)
    Ys = sparseStore(Y)
    YE = sparseDot(Ys,sparseStore(E))
    b = sparseDot(As, sparseStore(matrixSub(J,YE)))
    AY = sparseDot(As,Ys)
    AYAt = sparseDot(sparseStore(AY), sparseStore(At))
    ans = Matrix(AYAt)
    Vn = ans.solForX(b)
    return Vn

print('use sparse')
for n in range (2,15):

    a = Mesh(n)
    A = a.generateMesh()
    E = a.generateE()
    J = a.generateJ()
    R = a.generateR()
    startTime = time.clock()
    sol = solveVoltageSparse(A,E,J,R)
    endTime = time.clock()
    #voltage at node 0 is the total voltage of the mesh
    Rreq = sol[0] / (1 - sol[0])
    computingTime = endTime - startTime
    print('the equivalent resistance for n = '+str(n)+' is '+str(Rreq[0])+' ohms, computation taking '+' '+str(computingTime))

print('normal')
for n in range (2,15):

    a = Mesh(n)
    A = a.generateMesh()
    E = a.generateE()
    J = a.generateJ()
    R = a.generateR()
    startTime = time.clock()
    sol = solveVoltage(A,E,J,R)
    endTime = time.clock()
    #voltage at node 0 is the total voltage of the mesh
    Rreq = sol[0] / (1 - sol[0])
    computingTime = endTime - startTime
    print('the equivalent resistance for n = '+str(n)+' is '+str(Rreq[0])+' ohms, computation taking '+' '+str(computingTime))




   
