#general libraries
import numpy as np
import pandas as pd

#cluster detection libraries
from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
import hdbscan
from collections import Counter
from sklearn.cluster import KMeans

#plotting libraries
import matplotlib.pyplot as plt
import seaborn as sns

#random
import random
import time

#perlin noise
import noise

import sys


#------------------------------------------------------------------------------------------------------------

carpeta = "data/"

#FUNCTIONS
#cluster detection algorithms
def cluster_detection(method,data):

    if method == 0: ### DBSCAN
        dbscan = DBSCAN(eps=1, min_samples=20, metric = 'euclidean')
        clustering =  dbscan.fit(data) # METRIC = Euclidean, cosine (mejores)
        # Number of clusters in labels, ignoring noise if present.
        n_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
        #print("DBSCAN - Estimated number of clusters: %d" % n_clusters)


    elif method == 1:  ### HDBSCAN
        Hdbscan = hdbscan.HDBSCAN(min_cluster_size=20, min_samples = 200, metric = 'euclidean').fit(data) # METRIC = Euclidean, cosine (mejores)
        clustering = Hdbscan.fit(data)
        n_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
        #print("HDBSCAN - Estimated number of clusters: %d" % n_clusters)

    elif method == 2: ### K-MEANS
        '''
        ## Per a trobar el millor n_clusters sense fer-ho ja sabent el num"
        rank = range(1, 20)
        kmeans = [KMeans(n_clusters=i) for i in rank]
        print(kmeans)
        score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
        print(score)
        plt.plot(rank,score)
        plt.xlabel('Number of Clusters')
        plt.ylabel('Score')
        plt.title('Elbow Curve')
        plt.show()
        '''
        clustering = KMeans(n_clusters=3).fit(data)
        n_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
        #print("KMEANS - Estimated number of clusters: %d" % n_clusters)

    return clustering.labels_

#plotting or related to it
def plot_heatmap(data, name, points, y):
        # create heatmap
    cmap = sns.color_palette('viridis', 11)
    plt.subplots(figsize=(6.25, 5), dpi=100) # 6,25 * 5 * 100 pixels
    sns.heatmap(data, cmap = cmap) # palettes: viridis, viridis_r
    if (points):
        plt.scatter(y[0], y[1], s=250, facecolors='none', edgecolors='r')
    plt.yticks(rotation=0)
    plt.title("Bikes per station and time")
    plt.xlabel("Time in a day")
    plt.ylabel("Stations")
    plt.savefig(name, bbox_inches='tight') #(carpeta+name) #remove margins
    #plt.tight_layout(pad=0.5)
    #plt.show()



def plot_scatter_3d(X, labels):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection ='3d')

    #colors
    colores=['red','green','blue','purple','yellow','orange','pink']
    asignar=[]
    for row in labels:
        asignar.append(colores[row])

    ax.scatter(X[:, 0], X[:, 1], X[:, 2], marker ='o') #c = asignar
    #ax.scatter(C[:, 0], C[:, 1], C[:, 2], marker ='*', c = colores, s = 1000)
    plt.show()


def build_heatmap(X,labels, max):
    #tambe podriem emplenar amb randoms en comptes de 0
    #passem tots els valors a integers ja que seran hores, estacions o num de bicis
    data = X.astype(int)
    #maxims en les cordenades

    target = np.full((max, max), -1, data.dtype) #els valors buits son 0
    target[data[:, 0], data[:, 1]] = labels #assignar valors que coneixem
    #print(target)
    return target


def triplets_to_array(X, n):
    #passem tots els valors a integers ja que seran hores, estacions o num de bicis
    data = X.astype(int)
    #print(data.shape)

    #maxims en les cordenades
    target = perlin_noise(n)
    #target = np.full((120, 120), 0, data.dtype) #els valors buits son 0
    target[data[:, 0], data[:, 1]] = data[:, 2] #assignar valors que coneixem
    #print(target)
    target = target.astype(int)
    return target


#data creation & noise
def generar_data(n_clus, estacions):
    #CREATE DATA
    # We will be using the make_blobs method, in order to generate our own data


    clusters = []
    for i in range(n_clus):
        fuera_de_rango = True

        #comprobar que no esten en los extremos para que no se corten
        while fuera_de_rango:
            clus = random.sample(range(estacions), 3) #(np.random.randint(estacions, size=(1, 3)))
            if clus[0] > 3 and clus[0] < estacions-3 and clus[1] > 10 and clus[1] < estacions-3:
                fuera_de_rango = False
                clusters.append(clus)

    print(clusters)

    for dim in clusters:
        #poso el 3r valor com a màxim 50 (bicis per estació)
        #dim[2] = random.randint(10,40)

        min_o_max = random.randint(1, 2)
        if (min_o_max == 1):
            dim[2] = random.randint(5, 15) #minims
        else:
            dim[2] = random.randint(35, 45) #maxims
        #random.randint(0,15) or random.randint(25,40)

    #generate clusters
    X, _ = make_blobs(n_samples = estacions*estacions, centers = clusters, cluster_std = 1)
    # random_state, RandomState instance or None, default=None
    # cluster_std, float or array-like of float, default=1.0

    for dim in X:
        #poso el 3r valor com a màxim 50 (bicis per estació)
        dim[2] += random.randint(-2,2)

        if dim[2] < 0:
            dim[2] = 0


    #afegir soroll
    '''noise = (np.random.randint(estacions, size=(n, 3)))
    for dim in noise:
        #poso el 3r valor com a màxim 40 (bicis per estació)
        dim[2] = random.randint(0, 40)

    data1 = np.append(noise, X, axis = 0) '''

    #plot_heatmap(data_r, "Bikes per hour and station", "Hours", "Stations", name )
    return X

def gaussian (data):
    import scipy as sp
    result = sp.ndimage.filters.gaussian_filter(data, 1)
    return result
    #for d in data:
        #for point in d:

def perlin_noise(n):
    shape = (n,n)
    scale = 3.5
    octaves = 5 #number of levels of detail you want you perlin noise to have
    persistence = 0.6 #0.6 #number that determines how much each octave contributes to the overall shape (adjusts amplitude).
    lacunarity =  9 #9.0 #number that determines how much detail is added or removed at each octave (adjusts frequency)

    lol = random.randint(0, 1000)
    arrel = lol

    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = 20 + 100 * noise.pnoise2(i/scale,
                                        j/scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=n,
                                        repeaty=n,
                                        base= arrel)
            if (world[i][j] < 0):
                world[i][j] = 0
            elif (world[i][j] > 50):
                world[i][j] = 50

    return world
    #cl = sns.heatmap(world, cmap= 'viridis') # palettes: viridis, viridis_r
    #plt.show()

#--------------------------------------------------------------------------------------------------------

##### START #####

random.seed(time.time())

i = int(sys.argv[1]) #per iteracio

num_clusters = 0
estacions = 30 #num d'estacions

if (num_clusters == 0):
    heatmap = perlin_noise(estacions)
    heatmap = heatmap.astype(int)
else:
    data = generar_data(num_clusters, estacions)
    #blurred = gaussian(data)
    heatmap = triplets_to_array(data, estacions)

name =  carpeta + str(num_clusters)+ "data" +str(i)+".csv"
np.savetxt(name, heatmap, delimiter=',')

heatmap_blurred = []
for d in heatmap:
     heatmap_blurred.append(gaussian(d))

'''
array3d = []
for i in range(120):
    for j in range(120):
            array3d.append([i, j, heatmap[i][j]])

array3d = np.array(array3d)
print(array3d)
'''

name = str(num_clusters)+ "data" +str(i)
plot_heatmap(heatmap, carpeta+name, 0, [])
#plot_heatmap(heatmap_blurred, "Bikes per hour and station", "Horas", "Stations", name)

x = random.randint(5, estacions-5) + 0.5
print(x)
y = random.randint(5, estacions-5) +0.5
print(y)

name2 = name+"points_" + str(int(x)) + "-" + str(int(y))

plot_heatmap(heatmap, carpeta+name2, 1, [x, y])


#CLUSTER DETECTION
'''
labels = cluster_detection(0, data)
print(Counter(labels).keys()) # equals to list(set(words))

heatmap_clusters = build_heatmap(data, labels, estacions)
heatmap_noise_clus = build_heatmap(array3d, labels2, estacions)
'''


#---------KERNEL SCRIPT -------------
'''
for ((a = 0; a < 10; a++)); do
    python3 data.py $a;
done;
'''
