import matrix
import math
outerSide = 0.1
coreWidth = 0.04
coreHeight = 0.02
coreVoltage = 15.0
minres = 10**(-5)
def generateMesh(h):
    nodeI = (int)(outerSide/h)
    nodeJ = (int)(outerSide/h)
    mesh = matrix.createZeros((nodeI+1,nodeJ+1))
    for i in range(nodeI+1):
        for j in range(nodeJ+1):
            if(j<=(int(coreWidth/h)-1)and i<= (int(coreHeight/h)-1)):
                mesh[i][j] = coreVoltage
    rateOfXChange = -coreVoltage/((outerSide-coreWidth)/h)
    rateOfYChange = -coreVoltage/((outerSide-coreHeight)/h)
    for i in range(int(coreWidth/h),nodeI):
        mesh[0][i] = mesh[0][i-1] + rateOfXChange
    for j in range(int(coreHeight/h),nodeJ):
        mesh[j][0] = mesh[j-1][0] + rateOfYChange
    # mesh = mesh.tolist()
    return mesh

def SOR(mesh,h,w):
    nodeI = (int)(outerSide / h)
    nodeJ = (int)(outerSide / h)
    for i in range (0,nodeI):
        for j in range(0,nodeJ):
            if (j >=int(coreWidth/h) or i >= int(coreHeight/h)):

                mesh[i][j] = (1-w)*mesh[i][j]+(w/4)*(mesh[i][j-1]+mesh[i-1][j]+mesh[i][j+1]+mesh[i+1][j])
    return mesh
def maxResidual(mesh,h,minRes):
    nodeI = (int)(outerSide/h)
    nodeJ = (int)(outerSide/h)
    max = 0
    for i in range(0,nodeI):
        for j in range(0,nodeJ):
            if (j >= int(coreWidth / h) or i >= int(coreHeight / h)):
                residual = mesh[i][j-1]+mesh[i-1][j]+mesh[i][j+1]+mesh[i+1][j] - 4*mesh[i][j]
                residual = math.fabs(residual)
                if(residual>max):
                    max = residual
    if(max>=minRes):
        return True
    else:
        return False

def SORIter(mesh,h,w,minRes):
    iteration = 0
    while(maxResidual(mesh,h,minRes)):
        mesh = SOR(mesh,h,w)
        iteration+=1
    result = {
        'mesh': mesh,
        'iteration': iteration
    }
    return result


def Jacobian(mesh,h):
    nodeI = (int)(outerSide / h)
    nodeJ = (int)(outerSide / h)
    for i in range (0,nodeI):
        for j in range(0,nodeJ):
            if (i>=(int)(coreWidth/h) or j >= (int)(coreHeight/h)):
                mesh[i][j]=(mesh[i][j-1]+mesh[i-1][j]+mesh[i][j+1]+mesh[i+1][j])/4
    return mesh

def jacIter(mesh,h,minRes):
    iteration = 0
    while(maxResidual(mesh,h,minRes)):
        mesh = Jacobian(mesh,h)
        iteration+=1
    result = {
        'mesh':mesh,
        'iteration':iteration
    }
    return result


def getVoltage(mesh,x,y,h):
    xNode = (int)(x/h)
    yNode = (int)(y/h)
    return mesh[xNode][yNode]

#b
for i in range(0,10):
    w = 1 + 0.1*i
    h = 0.02
    mesh = generateMesh(h)
    result = SORIter(mesh,h,w,minres)
    finMesh = result['mesh']
    voltage = getVoltage(finMesh,0.06,0.04,h)
    finalIter = result['iteration']
    print('for w = '+str(w)+' the voltage is '+str(voltage)+' iteration is '+str(finalIter))