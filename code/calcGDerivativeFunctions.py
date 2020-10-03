import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy.spatial import distance_matrix


pd_mesh_type = 'std'
dtype = "float64"

#Loading Peridynamic Mesh Data
CRD = np.loadtxt('../data/uniform_mesh2d_{}.txt'.format(pd_mesh_type), dtype=float, delimiter=',')
HOR = np.loadtxt('../data/uniform_horizon2d_{}.txt'.format(pd_mesh_type), dtype=int, delimiter=',')
XIX = np.loadtxt('../data/uniform_xi2d_x_{}.txt'.format(pd_mesh_type), dtype=float, delimiter=',')
XIY = np.loadtxt('../data/uniform_xi2d_y_{}.txt'.format(pd_mesh_type), dtype=float, delimiter=',')
VOL = np.loadtxt('../data/uniform_area2d_{}.txt'.format(pd_mesh_type), dtype=float, delimiter=',')

num_node = np.sqrt(CRD.shape[0]).astype('int64')
num_feature = HOR.shape[1]
horiz = (np.sqrt(num_feature)-1)/2



def ExpInfFunc(xi, Delta):
    wx = np.exp(-2.0 * (xi[0] / Delta[0])**2)
    wy = np.exp(-2.0 * (xi[1] / Delta[1])**2)
    return wx*wy


def GenAmat(xi, Delta):
    w = ExpInfFunc(xi, Delta)
    Avec = np.array([1.0, xi[0], xi[1], xi[0]**2, xi[0]*xi[1], xi[1]**2])
    Amat = np.outer(Avec, Avec) * w
    return Amat


def InvGFunc(xi, Delta, amat):
    w = ExpInfFunc(xi, Delta)
    Avec = np.array([1.0, xi[0], xi[1], xi[0]**2, xi[0]*xi[1], xi[1]**2])
    GFS = np.matmul(Avec, amat) * w
    return GFS

def simpson(n):
    w=np.zeros(n)
    for i in range(n):
        if i in (0, n-1):
            w[i] = 1.0
        elif i % 2 == 1:
            w[i] = 4.0
        elif i % 2 == 0:
            w[i] = 2.0
    return w / sum(w)

def calcG01G10(num_node, num_feature, horiz):

    bmat = np.eye(6)
    bmat[3, 3] = 2.0
    bmat[5, 5] = 2.0

    for num_nn_feature in [num_feature]:
        horiz = ((np.sqrt(num_nn_feature)-1)/2).astype('int')

        BGF00, BGF10, BGF01, BGF20, BGF11, BGF02 = [], [], [], [], [], []
        for I, crdI in enumerate(CRD):
            horI = HOR[I, :num_nn_feature]
            exiI = np.concatenate((XIX[I, :num_nn_feature].reshape((-1,1)),XIY[I, :num_nn_feature].reshape((-1,1))), axis=1)
            if pd_mesh_type=='ghost':
                raise TypeError('no ghost')
            else:
                deltaI = np.max(np.abs(exiI), axis=0)
            Amat = np.zeros([6, 6])
            for i, xi in enumerate(exiI):
                Amat += GenAmat(xi, deltaI)*VOL[horI[i]]
            amat = np.linalg.solve(Amat, bmat)

            GFMAT = np.zeros([6, len(exiI)])
            for i, xi in enumerate(exiI):
                GFMAT[:, i] = InvGFunc(xi, deltaI, amat)*VOL[horI[i]]
        
        
            BGF00.append(GFMAT[0:1, :])
            BGF10.append(GFMAT[1:2, :])
            BGF01.append(GFMAT[2:3, :])
            BGF20.append(GFMAT[3:4, :])
            BGF11.append(GFMAT[4:5, :])
            BGF02.append(GFMAT[5:6, :])

        BGF00 = np.concatenate(BGF00)
        BGF10 = np.concatenate(BGF10)
        BGF01 = np.concatenate(BGF01)
        BGF20 = np.concatenate(BGF20)
        BGF11 = np.concatenate(BGF11)
        BGF02 = np.concatenate(BGF02)
    
        Famil = HOR[:, :num_nn_feature]
        GF00 = BGF00[:, :num_nn_feature]
        GF10 = BGF10[:, :num_nn_feature]
        GF01 = BGF01[:, :num_nn_feature]
        GF20 = BGF20[:, :num_nn_feature]
        GF11 = BGF11[:, :num_nn_feature]
        GF02 = BGF02[:, :num_nn_feature]
    
    return GF10, GF01, Famil


GF10, GF01, Famil = calcG01G10(num_node, num_feature, horiz)

path = '../data';
if os.path.isfile(path) == False:
    os.mkdir(path)


np.savetxt('../data/GF10.txt', np.array(GF10), fmt='%.6f', delimiter=', ')
np.savetxt('../data/GF01.txt', np.array(GF01), fmt='%.6f', delimiter=', ')
np.savetxt('../data/Family.txt', np.array(Famil), fmt='%6d', delimiter=', ')


#a = input('').split(" ")[0]
#I must fist start by loading an image frame
#frame = cv2.imread('../frame0.jpg',0)
#Finding image dimensions so we can calculate total number of original nodes which should not change
#height, width = frame.shape


#cv2.imshow('Image', frame)


#cv2.waitKey(0)


