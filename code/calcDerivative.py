import numpy as np
import math
import cv2

#Loading Peridynamic Mesh Data
GF01 = np.loadtxt('../data/GF01.txt', dtype=float, delimiter=',')
GF10 = np.loadtxt('../data/GF10.txt', dtype=float, delimiter=',')
Family = np.loadtxt('../data/Family.txt', dtype=int, delimiter=',')
frame = cv2.imread('../data/frame0.jpg',0)
height, width = frame.shape

frame_flat = frame.flatten('F') #Flatten in column mayor order
#cv2.imshow('Image', frame)
#cv2.waitKey(0)

#Defining horizon
horizon = 3;

def convertIndxToCoordinates(indx, height):
    x_coordinate = int(indx/height)
    y_coordinate = int(indx%height)    
    return x_coordinate, y_coordinate

def calculateDistance(x_coord_1, y_coord_1, x_coord_2, y_coord_2):
    dist = math.sqrt((x_coord_1-x_coord_2)**2+(y_coord_1-y_coord_2)**2)
    return dist

def calculateDerivative_y(family_members):
    derivative = 0
    for i in range(len(family_members)):
        derivative = derivative + frame_flat[family_members[i]]\
                *GF01[family_members[0]][i]
    return derivative

def calculateDerivative_x(family_members):
    derivative = 0
    for i in range(len(family_members)):
        derivative = derivative + frame_flat[family_members[i]]\
                *GF10[family_members[0]][i]
    return derivative



number_of_nodes, family_members = Family.shape
derivatives_y = []
derivatives_x = []
for nodes in range(number_of_nodes):
    family = Family[nodes]
    current_node_indx = family[0]
    x_coord_current_node, y_coord_current_node = convertIndxToCoordinates(current_node_indx, height)
    family_members_within_horizon = []
    for member in range(family.size):
        x_coord, y_coord = convertIndxToCoordinates(family[member], height)
        dist = calculateDistance(x_coord_current_node, y_coord_current_node, x_coord, y_coord)
        if(dist<=horizon):
            family_members_within_horizon.append(family[member])
    derivatives_y.append(calculateDerivative_y(family_members_within_horizon))
    derivatives_x.append(calculateDerivative_x(family_members_within_horizon))
    #derivatives.append(derivative_at_pixel)
    #print(derivatives)
    #a = input('').split(" ")[0]
    #print(family)
    #a = input('').split(" ")[0]

np.savetxt('../data/derivatives_y_horizon_std.txt', np.array(derivatives_y), fmt='%.6f', delimiter=',')
np.savetxt('../data/derivatives_x_horizon_std.txt', np.array(derivatives_x), fmt='%.6f', delimiter=',')
print(Family)
print(GF01)
