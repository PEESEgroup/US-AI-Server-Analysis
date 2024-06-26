# This file describe how to calculate the top 25%, 50%, and 75% locations

import numpy as np
import math
import csv
import statistics

# Caculation process
with open(r'FILE PATH\PUE_WUE_Density.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    count_num=np.zeros([L_2,1])
    flag=0
    grid_ID=[]
    CUE_value=[]
    WUE_value=[]
    for row in spamreader:
        if flag == 0:
            flag=flag+1
            continue
        else:
            if float(row[4]) > 0.1:
                name=row[1]
                for j1 in range (L_2):
                    if name==states[j1]:
                        break
            if float(row[4])>0.1:
                flag=flag+1
                grid_ID.append(float(row[3]))
                CUE_value.append(sum(emission_data[:,j1])/L_1*float(row[4]))
                WUE_value.append(float(row[8])+sum(water_data[:,j1])/L_1*float(row[4]))
        for j1 in range (L_2):
            if row[1] in states[j1]:
                count_num[j1]=count_num[j1]+1
Grid_N=flag
count_14=int(Grid_N/4)+1
three_quartiles_C = np.quantile(CUE_value, [0.25,0.5,0.75])
three_quartiles_W = np.quantile(WUE_value, [0.25,0.5,0.75])

count_11=0
count_22=0
count_33=0
count_44=0

# Calculate the number of locations with both top 25%, top 50%, and top 75% of WUE and CUE(Carbon Usage Effectivenes)
# To save the location information, use the grid_ID defined before. Example to save top 25%: grid_25.append(grid_ID[z1])
for z1 in range (len(grid_ID)):
    if CUE_value[z1]<=three_quartiles_C[0] and WUE_value[z1]<=three_quartiles_W[0]:
        count_11=count_11+1
    if CUE_value[z1]<=three_quartiles_C[1] and WUE_value[z1]<=three_quartiles_W[1]:
        count_22=count_22+1
    if CUE_value[z1]<=three_quartiles_C[2] and WUE_value[z1]<=three_quartiles_W[2]:
        count_33=count_33+1
    count_44=count_44+1
