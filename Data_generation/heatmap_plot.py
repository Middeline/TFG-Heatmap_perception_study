import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns

#–----------------------------------------------------------------------------
#plotting or related to it
def plot_heatmap(data, name, points, y, cont):
        # create heatmap
    if cont:
        if reverse:
            cmap = sns.color_palette('viridis_r', as_cmap=True)
        else:
            cmap = sns.color_palette('viridis', as_cmap=True)
    else:
        if reverse:
            cmap = sns.color_palette('viridis_r', 11)
        else:
            cmap = sns.color_palette('viridis', 11)


    plt.subplots(figsize=(6.25, 5), dpi=100) # 6,25 * 5 * 100 pixels
    sns.heatmap(data, cmap = cmap) # palettes: viridis, viridis_r
    if (points):
        plt.scatter(y[0], y[1], s=170, facecolors='none', edgecolors='r')
    plt.yticks(rotation=0)
    plt.title("Bikes per station and time")
    plt.xlabel("Time in a day")
    plt.ylabel("Stations")
    plt.savefig(name, bbox_inches='tight') #(carpeta+name) #remove margins
    #plt.show()

#–----------------------------------------------------------------------------

def init(a, b):
    #read CSV
    carpeta = "data/" + str(a) + "/"
    csv = str(a) + 'data' + str(b) + '.csv'
    global heatmap
    global estacions
    heatmap = np.genfromtxt(carpeta + csv, delimiter=',')
    estacions = len(heatmap[0])

#–----------------------------------------------------------------------------

def point_marker(carpeta, name):
    folder = carpeta + "transformations/"
    for i in range(1):
        x = random.randint(5, estacions-5)
        y = random.randint(5, estacions-5)
        points = [x+0.5, y+0.5]

        value = heatmap_transposed[x][y]
        plot_heatmap(heatmap_transposed, folder + "cont/" + name + "_marker_" + str(int(value)) + "_transposed_" + str(i), 1, points, 1)
        plot_heatmap(heatmap_transposed, folder + "disc/" + name + "_marker_" + str(int(value)) + "_transposed_" + str(i), 1, points, 0)

        value = heatmap[y][x]
        plot_heatmap(heatmap, folder + "cont/" + name + "_marker_" + str(int(value)) + "_" + str(i), 1, points, 1)
        plot_heatmap(heatmap, folder + "disc/" + name + "_marker_" + str(int(value)) + "_" + str(i), 1, points, 0)


    '''
    value = 999
    for i in range(5):
        #----------------------------
        # 0-13
        if (i == 0):
            while (value > 13):
                x = random.randint(5, estacions-5)
                y = random.randint(5, estacions-5)
                points = [x+0.5, y+0.5]
            if transpose:
                value = heatmap[x][y]
                plot_heatmap(heatmap, folder + name + "_marker_" + str(value) + "_transposed", 1, points)
            else:
                value = heatmap[y][x]
                plot_heatmap(heatmap, folder + name + "_marker_" + str(value), 1, points)

        #----------------------------
        # 14-25
        elif (i == 1):
            while (value < 14 or value > 25):
                x = random.randint(5, estacions-5)
                y = random.randint(5, estacions-5)
                points = [x+0.5, y+0.5]
                value = heatmap[y][x]
            plot_heatmap(heatmap, folder + name + "_marker_" + str(value), 1, points)

        #----------------------------
        # 26-38
        elif (i == 2): # 26-38
            while (value < 26 or value > 38):
                x = random.randint(5, estacions-5)
                y = random.randint(5, estacions-5)
                points = [x+0.5, y+0.5]
                value = heatmap[y][x]
            plot_heatmap(heatmap, folder + name + "_marker_" + str(value), 1, points)

        #----------------------------
        # 38-50
        else: # 38-50
            while (value < 39):
                x = random.randint(5, estacions-5)
                y = random.randint(5, estacions-5)
                points = [x+0.5, y+0.5]
                value = heatmap[y][x]
            plot_heatmap(heatmap, folder + name + "_marker_" + str(value), 1, points)
    '''
#–----------------------------------------------------------------------------

def transpose_heatmap(carpeta, plot_name):
    #TRANSPOSE
    global heatmap_transposed
    heatmap_transposed = np.transpose(heatmap)

    plot_name = plot_name + "_transposed"
    plot_heatmap(heatmap_transposed, carpeta + plot_name + "_cont", 0, [], 1)
    plot_heatmap(heatmap_transposed, carpeta + plot_name + "_disc", 0, [], 0)

#–----------------------------------------------------------------------------

reverse = False

for a in range(0, 4):
    for b in range(10):
        init(a, b)
        carpeta = "data/" + str(a) + "/plots/"
        plot_name = str(a) + "heatmap" + str(b)
        plot_heatmap(heatmap, carpeta + plot_name + "_cont", 0, [], 1)
        plot_heatmap(heatmap, carpeta + plot_name + "_disc", 0, [], 0)
        transpose_heatmap(carpeta, plot_name)
        reverse = True
        plot_heatmap(heatmap, carpeta + plot_name + "_RPalette_cont", 0, [], 1)
        plot_heatmap(heatmap, carpeta + plot_name + "_RPalette_disc", 0, [], 0)
        reverse = False


        point_marker(carpeta, plot_name)
        #encercla un valor per cada interval 0-13, 14-25, 26-38, 38-50
