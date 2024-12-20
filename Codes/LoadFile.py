# edit h5 load files for base scenarios
import h5py
import numpy as np
import csv

states = ["Alabama", "Arizona","Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", 
          "Georgia", "Idaho","Illinois", "Indiana","Iowa", "Kansas", "Kentucky", "Louisiana","Maine", "Maryland", "Massachusetts", 
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
          "New Jersey", "New Mexico", "New York","North Carolina","North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
          "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
          "Wisconsin", "Wyoming"]
L1=7
L2=len(states)
L3=134
L4=8760
L5=3

frozen_data=np.loadtxt(r'E:\ReEDS-2.0-main\Calculated_Data\R2_spatial.txt',delimiter='\t',dtype='float') 

load_data=np.array([[11.73527636,23.89338596,43.19965448,57.51826928,62.5129203,61.92256746,62.43625529],
                    [11.73527636,23.89338596,43.19965448,62.1646353,75.1409532,81.6980179,84.7748392],
                    [11.73527636,23.14655876,42.45282728,69.86274285,100.808093,127.5729379,143.218128]])




for i in range (L1):
    for j in range (L5):
        load_data[j][i]=load_data[j][i]*1e3

for scenarios in range (L5):
    name="std"+repr(scenarios+1)+"_load_hourly.h5"
    filename = r"E:\ReEDS-2.0-main\inputs\loaddata\EER_IRAlow_"+name
    f1 = h5py.File(filename, 'r+')
    data = f1['2030']
    print(data[0][0])
    
    states_demand=np.zeros([L1,L2])
    for i in range (L1):
        for j in range (L2):
            states_demand[i][j]=frozen_data[j]*load_data[scenarios][i]

    with open(r'E:\ReEDS-2.0-main\inputs\loaddata\BA_area_1.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        states_area=np.zeros([L2,1])
        BA_stateID=[]
        for row in reader:
            i=0
            for ID in states:
                if row[1] == ID:
                    states_area[i]=states_area[i]+float(row[2])
                    BA_stateID.append(i)
                i=i+1
            if row [1] not in states:
                BA_stateID.append(-1)

    with open(r'E:\ReEDS-2.0-main\inputs\loaddata\BA_area_1.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        BA_demand=np.zeros([L3,L1])
        i=0
        for row in reader:
            if BA_stateID[i]>0:
                area=states_area[BA_stateID[i]]
                area_BA=float(row[2])
                for year in range (L1):
                    BA_demand[i,year]=states_demand[year][BA_stateID[i]]*area_BA/area
            i=i+1

    year=[]
    for i in range (7):
        year=repr(i+2024)
        data=f1[year]
        for k in range (L3):
            data[:,k] = data[:,k] + BA_demand[k,i]

    data = f1['2030']
    print(data[0][0])

    f1.close()
