import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

for i in range(0, 4):
    for j in range (0, 10):
        print (i, j)
        csv = 'data/csv/' + str(i) + 'data' + str(j) + '.csv'
        heatmap = pd.read_csv(csv, header=None)
        heatmap_transposed = np.transpose(heatmap)
        print("len", len(heatmap_transposed))
        print("len", len(heatmap_transposed[0]))
        name =  'data/csv/transposed/' + str(i)+ "data" +str(j)+"_transposed.csv"
        np.savetxt(name, heatmap_transposed, delimiter=',')
