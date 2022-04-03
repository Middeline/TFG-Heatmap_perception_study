import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns

#–----------------------------------------------------------------------------
#plotting or related to it
def plot_heatmap(data, name, points, y, cont):
        # create heatmap
    if cont:
        if blues:
            cmap = sns.color_palette('Blues', as_cmap=True)
        else:
            cmap = sns.color_palette('viridis', as_cmap=True)
    else:
        if blues:
            cmap = sns.color_palette('Blues', 11)
        else:
            cmap = sns.color_palette('viridis', 11)


    plt.subplots(figsize=(6.25, 5), dpi=100) # 6,25 * 5 * 100 pixels
    sns.heatmap(data, cmap = cmap) # palettes: viridis, viridis_r
    if (points):
        plt.scatter(y[0], y[1], s=170, facecolors='none', edgecolors='r')
    plt.yticks(rotation=0)
    plt.title("Average Occupancy per Day") #average ocupation per day
    plt.xlabel("Days") #day
    plt.ylabel("Stations id")
    plt.savefig(name, bbox_inches ='tight') #(carpeta+name) #remove margins
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
    x = random.randint(5, estacions-5)
    y = random.randint(5, estacions-5)
    points = [x+0.5, y+0.5]
    points_T = [y+0.5, x+0.5]

    if blues:
        value = heatmap_transposed[x][y]
        plot_heatmap(heatmap_transposed, folder + "cont/" + name + "_Blues_cont_marker_" + str(int(value)) + "_transposed" , 1, points_T, 1)
        plot_heatmap(heatmap_transposed, folder + "disc/" + name + "_Blues_disc_marker_" + str(int(value)) + "_transposed" , 1, points_T, 0)
    else:
        value = heatmap_transposed[x][y]
        plot_heatmap(heatmap_transposed, folder + "cont/" + name + "_Viridis_cont_marker_" + str(int(value)) + "_transposed" , 1, points_T, 1)
        plot_heatmap(heatmap_transposed, folder + "disc/" + name + "_Viridis_disc_marker_" + str(int(value)) + "_transposed" , 1, points_T, 0)
    if blues:
        value = heatmap[y][x]
        plot_heatmap(heatmap, folder + "cont/" + name + "_Blues_cont_marker_" + str(int(value)) , 1, points, 1)
        plot_heatmap(heatmap, folder + "disc/" + name + "_Blues_disc_marker_" + str(int(value))  , 1, points, 0)
    else:
        value = heatmap[y][x]
        plot_heatmap(heatmap, folder + "cont/" + name + "_Viridis_cont_marker_" + str(int(value))  , 1, points, 1)
        plot_heatmap(heatmap, folder + "disc/" + name + "_Viridis_disc_marker_" + str(int(value)) , 1, points, 0)


#–----------------------------------------------------------------------------

def transpose_heatmap(carpeta, plot_name):
    #TRANSPOSE
    global heatmap_transposed
    heatmap_transposed = np.transpose(heatmap)

    plot_name = plot_name + "_transposed"
    plot_heatmap(heatmap_transposed, carpeta + plot_name + "_cont", 0, [], 1)
    plot_heatmap(heatmap_transposed, carpeta + plot_name + "_disc", 0, [], 0)

#–----------------------------------------------------------------------------

for a in range(1, 2):
    for b in ([3, 8]):
        blues = False
        init(a, b)
        carpeta = "data/" + str(a) + "/plots/viridis/"
        plot_name = str(a) + "heatmap" + str(b)
        plot_heatmap(heatmap, carpeta + plot_name + "Viridis_cont", 0, [], 1)
        plot_heatmap(heatmap, carpeta + plot_name + "Viridis_disc", 0, [], 0)
        transpose_heatmap(carpeta, plot_name)
        blues = True
        carpeta = "data/" + str(a) + "/plots/blues/"
        plot_heatmap(heatmap, carpeta + plot_name + "_Blues_cont", 0, [], 1)
        plot_heatmap(heatmap, carpeta + plot_name + "_Blues_disc", 0, [], 0)
        transpose_heatmap(carpeta, plot_name)
        blues = False

        carpeta = "data/" + str(a) + "/plots/viridis/"
        point_marker(carpeta, plot_name)
        blues = True
        carpeta = "data/" + str(a) + "/plots/blues/"
        point_marker(carpeta, plot_name)
        #encercla un valor per cada interval 0-13, 14-25, 26-38, 38-50
