
# File:         Clustering.py
# Author:       Ying Zhang
# Email:        yzhang3@umbc.edu
# Course:       CMSC 471
# Date:         5/9/2016
# Description:  Implement K means clustering on a given data set
# Reference:    http://stanford.edu/~cpiech/cs221/handouts/kmeans.html
#               http://www.onmyphd.com/?p=k-means.clustering&ckattempt=1
#               http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
#               http://stackoverflow.com/questions/7827530/array-of-colors-in-python
#--------------------------------------------------------------------------

import sys
import random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.colors as colors

# reads in data from input file
def readFile(filename):
    
    x = []
    y = []

    fin = open(filename, 'r')
    lines = fin.readlines()
    
    for line in lines:
        token = line.split()
        x.append(float(token[0]))
        y.append(float(token[1]))

    return x,y

# initialize cenctroids
def findRandomCentroids(numOfClusters, minX, maxX, minY, maxY):
    
    i = 0
    initCentroidsX = []
    initCentroidsY = []
    
    while (i != numOfClusters):
        tempX = random.uniform(minX, maxX)
        tempY = random.uniform(minY, maxY)
        initCentroidsX.append(tempX)
        initCentroidsY.append(tempY)
        i += 1
        
    return initCentroidsX, initCentroidsY

# label points with nearest centroid
def assignCentroids(allX, allY, centroidsX, centroidsY):

    tempDist = 999999
    label = 0;
    labels= []
    
    for i in range(len(allX)):
        tempDist = 999999
        for j in range(len(centroidsX)):
            # uses distance formula to calculate distance between each point and each centroid
            distX = (centroidsX[j] - allX[i])**2
            distY = (centroidsY[j] - allY[i])**2
            dist = (distX + distY)**(1.0/2.0)   
            # assign appropriate centroids to each point
            if (dist < tempDist):
                tempDist = dist
                label = j
        labels.append(label)
        
    return labels

# calculate centroids based clusters
def findCentroids(numOfClusters, labels, allX, allY):
    
    sumX = 0
    sumY = 0
    counter = 0
    newCentX = []
    newCentY = []

    for i in range(numOfClusters):
        for j in range(len(labels)):
            if (labels[j] == i):
                sumX += allX[j]
                sumY += allY[j]
                counter+=1
        # when the cluster is empty, randomly re-initialize a new value
        if (counter == 0):
            newX = random.uniform(min(allX), max(allX))
            newY = random.uniform(min(allY), max(allY))
        # else use the average of all points in the cluster as the new centroid
        else:
            newX = sumX/counter
            newY = sumY/counter
        newCentX.append(newX)
        newCentY.append(newY)
        sumX = 0
        sumY = 0
        counter = 0

    return newCentX, newCentY

def main():

    allX = []
    allY = []
    centroidsX = []
    centroidsY = []
    cluster = []
    oldCluster = []
    colorArray = []
    stop = False
    maxIteration = 100
    iterations = 0
 
    numOfClusters = int(sys.argv[1])
    filename = str(sys.argv[2])
    

    allX, allY = readFile(filename)
    maxX = max(allX)
    maxY = max(allY)
    minX = min(allX)
    minY = min(allY)

    # initials centroids
    centroidsX, centroidsY = findRandomCentroids(numOfClusters, minX, maxX, minY, maxY)

    # labels each point with appropriate centroid
    cluster = assignCentroids(allX, allY, centroidsX, centroidsY)
    
    # continuously looking for new cluster and new centroids until convergence
    while (stop == False):
        oldCluster = cluster
        centroidsX, centroidsY = findCentroids(numOfClusters, cluster, allX, allY)
        cluster = assignCentroids(allX, allY, centroidsX, centroidsY)
        iterations += 1
        if ((oldCluster == cluster) or (iterations == maxIteration)):
            stop = True

    x = np.asarray(allX)
    y = np.asarray(allY)
    centX = np.asarray(centroidsX)
    centY = np.asarray(centroidsY)


    for i in range(numOfClusters):
        colorArray.append('#'+'%06X' % random.randint(0, 0xFFFFFF))
    
    #plt.scatter(x, y,color=colors.hex2color(colorArray[0]), s=1, alpha=0.5)

    for j in range(len(centX)):
        plt.scatter(centX[j], centY[j], color = colors.hex2color(colorArray[j]))
        for i in range(len(cluster)):
            if (cluster[i] == j):
                plt.scatter(x[i], y[i], color=colors.hex2color(colorArray[j]), s=5, alpha=0.5)

    plt.show()

main()

