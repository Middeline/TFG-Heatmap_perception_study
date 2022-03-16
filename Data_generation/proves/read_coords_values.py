import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns


#–----------------------------------------------------------------------------

#plotting or related to it
def plot_heatmap(data, name, points, y):
        # create heatmap
    cmap = sns.color_palette('viridis', 11)
    plt.subplots(figsize=(6.25, 5), dpi=100) # 6,25 * 5 * 100 pixels
    sns.heatmap(data, cmap = cmap) # palettes: viridis, viridis_r
    if (points):
        plt.scatter(y[0], y[1], s=170, facecolors='none', edgecolors='r')
    plt.yticks(rotation=0)
    plt.title("Bikes per station and time")
    plt.xlabel("Time in a day")
    plt.ylabel("Stations")
    #plt.savefig(name, bbox_inches='tight') #(carpeta+name) #remove margins
    plt.show()

#–----------------------------------------------------------------------------

def init():
    #read CSV
    global heatmap
    heatmap = np.genfromtxt('2data8.csv', delimiter=',')
    estacions = len(heatmap[0])

    x = random.randint(5, estacions-5)
    y = random.randint(5, estacions-5)
    points = [x+0.5, y+0.5]
    #plot_heatmap(heatmap, "heatmap", 1, points)

    #TRANSPOSE
    heatmap_transposed = np.transpose(heatmap)
    points_trans = [y+0.5, x+0.5]
    #plot_heatmap(heatmap_transposed, "heatmap_transposed", 1, points_trans)

#–----------------------------------------------------------------------------

def read_coords():
        # importing the module
    import cv2
    from PIL import Image


    def click_event(event, x, y, flags, params):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Pixels ", x, ' ', y) # displaying the coordinates
            rgb_pixel_value = red_image_rgb.getpixel((x, y)) #Get color from (x, y) coordinates
            print("Color", rgb_pixel_value)
            val = read_coords_value(x, y)
            print("Value", val)


    img = cv2.imread("2data8points_14.png", 1)    # reading the image
    red_image = Image.open("2data8points_14.png")    #Create a PIL.Image object
    red_image_rgb = red_image.convert("RGB")    #Convert to RGB colorspace


    cv2.startWindowThread()
    cv2.imshow('img', img)     # displaying the image
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('img', click_event)
    cv2.waitKey()   # wait for a key to be pressed to exit

#–----------------------------------------------------------------------------

def read_coords_value(CoordX, CoordY):
    #57 * 32 of margin
    #flat_list = [item for sublist in t for item in sublist]
    x0 = 57
    y0 = 32

    a = int((CoordX-x0)/13)
    b = int((CoordY-y0)/13)

    Value = heatmap[b][a]
    return(Value)

#–----------------------------------------------------------------------------

init()
read_coords()
