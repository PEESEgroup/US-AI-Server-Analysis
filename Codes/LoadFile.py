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
L5=8

frozen_data=np.loadtxt(r'E:\ReEDS-2.0-main\inputs\loaddata\states_spatial_scenario_frozen.txt',delimiter='\t',dtype='float') 

load_data=np.array([[2.1473,2.2276,2.2676,2.2874,2.2913,2.2730,2.2327,2.1027],
                    [3.5496,4.2520,4.7132,4.9808,5.0366,4.8903,4.5209,4.0114],
                    [4.5898,6.5960,8.4797,9.9043,10.2433,9.7898,8.3494,6.9126],
                    [5.1094,8.4457,12.7547,17.2065,18.4824,17.8975,14.1337,11.0181],
                    [5.3170,9.5095,16.2245,25.3222,28.4799,29.1958,21.9450,16.3384],
                    [5.3922,10.0106,18.3453,31.9103,37.3706,41.9044,31.2514,22.2717],
                    [5.4185,10.2239,19.4205,36.0127,43.3305,53.3215,40.9739,28.3817]])

for i in range (L1):
    for j in range (L5):
        load_data[i][j]=load_data[i][j]*1e3

for scenarios in range (L5):
    name="std"+repr(scenarios+1)+"_load_hourly.h5"
    filename = r"E:\ReEDS-2.0-main\inputs\loaddata\Baseline_"+name
    f1 = h5py.File(filename, 'r+')
    data = f1['2030']
    print(data[0][0])
    
    states_demand=np.zeros([L1,L2])
    for i in range (L1):
        for j in range (L2):
            states_demand[i][j]=frozen_data[j][i]*load_data[i][scenarios]

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

# edit h5 load files for location matters section
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
L5=8

def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

BA_number=134
year=7

frozen_data=np.loadtxt(r'E:\ReEDS-2.0-main\inputs\loaddata\states_spatial_scenario_frozen.txt',delimiter='\t',dtype='float') 

PUE=[1.1940,1.1656,1.1870,1.1477,1.1490,1.1617,1.1733,1.1800,1.2047,1.1856,1.1373,1.1686,1.1668,1.1607,1.1716,1.1755,
    1.1917,1.1374,1.1693,1.1564,1.1439,1.1429,1.1923,1.1766,1.1368,1.1606,1.1468,1.1437,1.1687,1.1565,1.1507,1.1859,
    1.1431,1.1632,1.1852,1.1314,1.1571,1.1873,1.1509,1.1804,1.1880,1.1450,1.1438,1.1732,1.1297,1.1688,1.1486,1.1417]

WUE=[4.63E-01,4.11E-01,6.97E-01,8.66E-01,1.03E+00,2.12E+00,1.53E+00,3.41E-01,7.86E-01,7.70E-01,6.57E-01,8.14E-01,
     8.98E-01,1.93E+00,3.60E-01,8.23E-01,6.15E-01,4.38E-01,4.22E-01,1.49E+00,8.90E-01,3.26E-01,6.23E-01,5.34E-01,
     4.60E-01,7.99E-01,5.16E-01,5.43E-01,1.03E+00,4.02E-01,7.09E-01,1.01E+00,2.76E-01,6.24E-01,1.38E+00,4.94E-01,
     9.66E-01,1.39E+00,4.76E-01,4.64E-01,8.44E-01,2.15E-01,7.79E-01,4.78E-01,3.91E-01]


load_data=np.array([[2.1473,2.2276,2.2676,2.2874,2.2913,2.2730,2.2327,2.1027],
                    [3.5496,4.2520,4.7132,4.9808,5.0366,4.8903,4.5209,4.0114],
                    [4.5898,6.5960,8.4797,9.9043,10.2433,9.7898,8.3494,6.9126],
                    [5.1094,8.4457,12.7547,17.2065,18.4824,17.8975,14.1337,11.0181],
                    [5.3170,9.5095,16.2245,25.3222,28.4799,29.1958,21.9450,16.3384],
                    [5.3922,10.0106,18.3453,31.9103,37.3706,41.9044,31.2514,22.2717],
                    [5.4185,10.2239,19.4205,36.0127,43.3305,53.3215,40.9739,28.3817]])

s_name=['std']
for scenario in range (1):
    BA=[]
    s_name_1=s_name[scenario]
    for i in range (BA_number):
        BA.append('p'+repr(i+1))

    #Metric Tons
    BA_emit=np.zeros([BA_number,year])
    
    name = r'E:\ReEDS-2.0-main\runs\cases_base_'+s_name_1+r'\outputs\emit_r.csv'
    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        for row in reader:
            if row[0]=='CO2e' and int(row[2]) > 2023:
                r=int(row[1].replace('p', ''))
                t=int(row[2])
                BA_emit[r-1][t-2024]=float(row[3])

    #MWh
    BA_en=np.zeros([BA_number,year])
    #m3
    BA_wa=np.zeros([BA_number,year]) 
    
    name = r'E:\ReEDS-2.0-main\runs\cases_base_'+s_name_1+r'\outputs\gen_ann.csv'
    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        for row in reader:
            if float(row[3]) > 0 and int(row[2]) > 2023:
                r=int(row[1].replace('p', ''))
                t=int(row[2])
                BA_en[r-1][t-2024]=BA_en[r-1][t-2024]+float(row[3])

                #calculate water usage of each energy resource
                water_tf=3.78541
                water_f=0
                if 'bio' in row[0] or 'Bio' in row[0]:
                    water_f=water_tf*0.58
                elif 'coal' in row[0] or 'Coal' in row[0]:
                    water_f=water_tf*0.48
                elif 'Gas' in row[0] or 'gas' in row[0]:
                    water_f=water_tf*0.21
                elif 'Nuclear' in row[0] or 'nuclear' in row[0]:
                    water_f=water_tf*0.61
                elif 'pv' in row[0] or 'Pv' in row[0]:
                    water_f=water_tf*0
                elif 'wind' in row[0] or 'Wind' in row[0]:
                    water_f=water_tf*0
                elif 'hyd' in row[0] or 'Hyd' in row[0]:
                    water_f=water_tf*5.99
                elif 'geo' in row[0] or 'Geo' in row[0]:
                    water_f=water_tf*1.89
                else:
                    water_f=0
                BA_wa[r-1][t-2024]=BA_wa[r-1][t-2024]+float(row[3])*water_f


    #Calculate BA-based Carbon Rate
    BA_carbon_rate=BA_emit*1000/BA_en
    #Calculate BA-based Water Rate
    BA_water_rate=BA_wa*1000/BA_en
    
    total_area=817.859
    with open(r'E:\ReEDS-2.0-main\inputs\loaddata\BA_area_1.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        BA_id=[]
        BA_state=[]
        BA_area=[]
        for row in reader:
            BA_id.append(row[0])
            BA_state.append(row[1])
            BA_area.append(row[2])
            r=int(row[0].replace('p', ''))
    BA_carbon_rate_cc=np.zeros([BA_number])
    BA_water_rate_cc=np.zeros([BA_number])
    BA_carbon_rate_1=np.zeros([BA_number])
    BA_water_rate_1=np.zeros([BA_number])
    for BA_n in range (BA_number):
        BA_carbon_rate_1[BA_n]=np.mean(BA_carbon_rate[BA_n,:])
        BA_water_rate_1[BA_n]=np.mean(BA_water_rate[BA_n,:])
    BA_carbon_rate_1[BA_carbon_rate_1==0] = 1e12
    BA_water_rate_1[BA_carbon_rate_1==0] = 1e12
    WUE_25=[]
    WUE_50=[]
    WUE_75=[]
    CUE_25=[]
    CUE_50=[]
    CUE_75=[]
    WUE_last25=[]
    CUE_last25=[]
    WUECUE_25=[]
    WUECUE_50=[]
    WUECUE_75=[]
    WUE_25_state_area=np.zeros([L2])
    WUE_50_state_area=np.zeros([L2])
    WUE_75_state_area=np.zeros([L2])
    CUE_25_state_area=np.zeros([L2])
    CUE_50_state_area=np.zeros([L2])
    CUE_75_state_area=np.zeros([L2])
    WUE_last25_state_area=np.zeros([L2])
    CUE_last25_state_area=np.zeros([L2])
    WUECUE_25_state_area=np.zeros([L2])
    WUECUE_50_state_area=np.zeros([L2])
    WUECUE_75_state_area=np.zeros([L2])
    WUE_25_total_area=0
    WUE_50_total_area=0
    WUE_75_total_area=0
    CUE_25_total_area=0
    CUE_50_total_area=0
    CUE_75_total_area=0
    WUE_last25_total_area=0
    CUE_last25_total_area=0
    WUECUE_25_total_area=0
    WUECUE_50_total_area=0
    WUECUE_75_total_area=0
    c_carbon=0
    c_water=0
    c_area_carbon=0
    c_area_water=0
    cc_h=[]
    ww_h=[]
    for BA_n in range (BA_number):
        cc=np.where(BA_carbon_rate_1 == BA_carbon_rate_1.min())[0]
        for item in cc:
            if item not in cc_h:
                cc=cc[0]
                break
        cc_h.append(cc)
        c_area_carbon=c_area_carbon+float(BA_area[cc])
        ww=np.where(BA_water_rate_1 == BA_water_rate_1.min())[0]

        for item in ww:
            if item not in ww_h:
                ww=ww[0]
                break
        ww_h.append(ww)
        c_area_water=c_area_water+float(BA_area[ww])
        
        # last 25% CUE locations
        if c_area_carbon <= total_area*1 and c_area_carbon > total_area*0.75:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                CUE_last25.append(BA_id[cc])
                state_num=indices(states, BA_state[cc])[0]
                CUE_last25_state_area[state_num]=CUE_last25_state_area[state_num]+float(BA_area[cc])
                CUE_last25_total_area=CUE_last25_total_area+float(BA_area[cc])
        
        # 75% CUE locations
        if c_area_carbon <= total_area*0.75:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                CUE_75.append(BA_id[cc])
                state_num=indices(states, BA_state[cc])[0]
                CUE_75_state_area[state_num]=CUE_75_state_area[state_num]+float(BA_area[cc])
                CUE_75_total_area=CUE_75_total_area+float(BA_area[cc])

        # 50% CUE locations
        if c_area_carbon <= total_area*0.50:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                CUE_50.append(BA_id[cc])
                state_num=indices(states, BA_state[cc])[0]
                CUE_50_state_area[state_num]=CUE_50_state_area[state_num]+float(BA_area[cc])
                CUE_50_total_area=CUE_50_total_area+float(BA_area[cc])
        
        # 25% CUE locations
        if c_area_carbon <= total_area*0.25:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                CUE_25.append(BA_id[cc])
                state_num=indices(states, BA_state[cc])[0]
                CUE_25_state_area[state_num]=CUE_25_state_area[state_num]+float(BA_area[cc])
                CUE_25_total_area=CUE_25_total_area+float(BA_area[cc])
    
        # last 25% WUE locations
        if c_area_water <= total_area*1 and c_area_water > total_area*0.75:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                WUE_last25.append(BA_id[ww])
                state_num=indices(states, BA_state[cc])[0]
                WUE_last25_state_area[state_num]=WUE_last25_state_area[state_num]+float(BA_area[ww])
                WUE_last25_total_area=WUE_last25_total_area+float(BA_area[ww])
        
        # 75% WUE locations
        if c_area_water <= total_area*0.75:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                WUE_75.append(BA_id[ww])
                state_num=indices(states, BA_state[cc])[0]
                WUE_75_state_area[state_num]=WUE_75_state_area[state_num]+float(BA_area[ww])
                WUE_75_total_area=WUE_75_total_area+float(BA_area[ww])
                
        # 50% WUE locations
        if c_area_water <= total_area*0.50:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                WUE_50.append(BA_id[ww])
                state_num=indices(states, BA_state[cc])[0]
                WUE_50_state_area[state_num]=WUE_50_state_area[state_num]+float(BA_area[ww])
                WUE_50_total_area=WUE_50_total_area+float(BA_area[ww])
        
        # 25% WUE locations
        if c_area_water <= total_area*0.25:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                WUE_25.append(BA_id[ww])
                state_num=indices(states, BA_state[cc])[0]
                WUE_25_state_area[state_num]=WUE_25_state_area[state_num]+float(BA_area[ww])
                WUE_25_total_area=WUE_25_total_area+float(BA_area[ww])

        BA_carbon_rate_1[cc]=1e15
        BA_water_rate_1[ww]=1e15
    
    ii=0
    for enum in BA_id:
        # 25% WUE & CUE locations
        if enum in WUE_25 and enum in CUE_25:
            WUECUE_25.append(enum)
            state_num=indices(states, BA_state[ii])[0]
            WUECUE_25_state_area[state_num]=WUECUE_25_state_area[state_num]+float(BA_area[ii])
            WUECUE_25_total_area=WUECUE_25_total_area+float(BA_area[ii])
        
        # 50% WUE & CUE locations
        if enum in WUE_50 and enum in CUE_50:
            WUECUE_50.append(enum)
            state_num=indices(states, BA_state[ii])[0]
            WUECUE_50_state_area[state_num]=WUECUE_50_state_area[state_num]+float(BA_area[ii])
            WUECUE_50_total_area=WUECUE_50_total_area+float(BA_area[ii])
        
        # 75% WUE & CUE locations
        if enum in WUE_75 and enum in CUE_75:
            WUECUE_75.append(enum)
            state_num=indices(states, BA_state[ii])[0]
            WUECUE_75_state_area[state_num]=WUECUE_75_state_area[state_num]+float(BA_area[ii])
            WUECUE_75_total_area=WUECUE_75_total_area+float(BA_area[ii])
        ii=ii+1
            
    #edit h5 file based on the allocation data
    
    for i in range (L1):
        for j in range (L5):
            load_data[i][j]=load_data[i][j]*1e3
    
    alc_name=['_WUE_25','_WUE_50','_WUE_75','_CUE_25','_CUE_50','_CUE_75','_WUECUE_25','_WUECUE_50','_WUECUE_75']
    alc_data=np.zeros([9,L2,L1])
    alc_data_raw_1=[WUE_25_state_area,WUE_50_state_area,WUE_75_state_area,
                   CUE_25_state_area,CUE_50_state_area,CUE_75_state_area,
                   WUECUE_25_state_area,WUECUE_50_state_area,WUECUE_75_state_area]
    alc_data_raw_2=[WUE_25_total_area,WUE_50_total_area,WUE_75_total_area,
               CUE_25_total_area,CUE_50_total_area,CUE_75_total_area,
               WUECUE_25_total_area,WUECUE_50_total_area,WUECUE_75_total_area]
    for i in range (9):
        for j in range (L2):
            for k in range (L1):
                alc_data[i][j][k]=(alc_data_raw_1[i]/alc_data_raw_2[i])[j]
    
    for scenarios in range (9):
        name="std"+repr(6)+alc_name[scenarios]+"_load_hourly.h5"
        filename = r"E:\ReEDS-2.0-main\inputs\loaddata\Baseline_"+name
        print(filename)
        f1 = h5py.File(filename, 'r+')
        data = f1['2030']
        print(data[0][0])

        states_demand=np.zeros([L1,L2])
        for i in range (L1):
            for j in range (L2):
                states_demand[i][j]=alc_data[scenarios][j][i]*load_data[i][5]

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

# edit h5 load files for net-zero pathway section
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
L5=8

def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

BA_number=134
year=7

frozen_data=np.loadtxt(r'E:\ReEDS-2.0-main\inputs\loaddata\states_spatial_scenario_frozen.txt',delimiter='\t',dtype='float') 

PUE=[1.1940,1.1656,1.1870,1.1477,1.1490,1.1617,1.1733,1.1800,1.2047,1.1856,1.1373,1.1686,1.1668,1.1607,1.1716,1.1755,
    1.1917,1.1374,1.1693,1.1564,1.1439,1.1429,1.1923,1.1766,1.1368,1.1606,1.1468,1.1437,1.1687,1.1565,1.1507,1.1859,
    1.1431,1.1632,1.1852,1.1314,1.1571,1.1873,1.1509,1.1804,1.1880,1.1450,1.1438,1.1732,1.1297,1.1688,1.1486,1.1417]

WUE=[4.63E-01,4.11E-01,6.97E-01,8.66E-01,1.03E+00,2.12E+00,1.53E+00,3.41E-01,7.86E-01,7.70E-01,6.57E-01,8.14E-01,
     8.98E-01,1.93E+00,3.60E-01,8.23E-01,6.15E-01,4.38E-01,4.22E-01,1.49E+00,8.90E-01,3.26E-01,6.23E-01,5.34E-01,
     4.60E-01,7.99E-01,5.16E-01,5.43E-01,1.03E+00,4.02E-01,7.09E-01,1.01E+00,2.76E-01,6.24E-01,1.38E+00,4.94E-01,
     9.66E-01,1.39E+00,4.76E-01,4.64E-01,8.44E-01,2.15E-01,7.79E-01,4.78E-01,3.91E-01]


load_data=np.array([[2.1473,2.2276,2.2676,2.2874,2.2913,2.2730,2.2327,2.1027],
                    [3.5496,4.2520,4.7132,4.9808,5.0366,4.8903,4.5209,4.0114],
                    [4.5898,6.5960,8.4797,9.9043,10.2433,9.7898,8.3494,6.9126],
                    [5.1094,8.4457,12.7547,17.2065,18.4824,17.8975,14.1337,11.0181],
                    [5.3170,9.5095,16.2245,25.3222,28.4799,29.1958,21.9450,16.3384],
                    [5.3922,10.0106,18.3453,31.9103,37.3706,41.9044,31.2514,22.2717],
                    [5.4185,10.2239,19.4205,36.0127,43.3305,53.3215,40.9739,28.3817]])

s_name=['std']
for scenario in range (1):
    BA=[]
    s_name_1=s_name[scenario]
    for i in range (BA_number):
        BA.append('p'+repr(i+1))

    #Metric Tons
    BA_emit=np.zeros([BA_number,year])
    
    name = r'E:\ReEDS-2.0-main\runs\cases_base_'+s_name_1+r'\outputs\emit_r.csv'
    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        for row in reader:
            if row[0]=='CO2e' and int(row[2]) > 2023:
                r=int(row[1].replace('p', ''))
                t=int(row[2])
                BA_emit[r-1][t-2024]=float(row[3])

    #MWh
    BA_en=np.zeros([BA_number,year])
    #m3
    BA_wa=np.zeros([BA_number,year]) 
    
    name = r'E:\ReEDS-2.0-main\runs\cases_base_'+s_name_1+r'\outputs\gen_ann.csv'
    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        for row in reader:
            if float(row[3]) > 0 and int(row[2]) > 2023:
                r=int(row[1].replace('p', ''))
                t=int(row[2])
                BA_en[r-1][t-2024]=BA_en[r-1][t-2024]+float(row[3])

                #calculate water usage of each energy resource
                water_tf=3.78541
                water_f=0
                if 'bio' in row[0] or 'Bio' in row[0]:
                    water_f=water_tf*0.58
                elif 'coal' in row[0] or 'Coal' in row[0]:
                    water_f=water_tf*0.48
                elif 'Gas' in row[0] or 'gas' in row[0]:
                    water_f=water_tf*0.21
                elif 'Nuclear' in row[0] or 'nuclear' in row[0]:
                    water_f=water_tf*0.61
                elif 'pv' in row[0] or 'Pv' in row[0]:
                    water_f=water_tf*0
                elif 'wind' in row[0] or 'Wind' in row[0]:
                    water_f=water_tf*0
                elif 'hyd' in row[0] or 'Hyd' in row[0]:
                    water_f=water_tf*5.99
                elif 'geo' in row[0] or 'Geo' in row[0]:
                    water_f=water_tf*1.89
                else:
                    water_f=0
                BA_wa[r-1][t-2024]=BA_wa[r-1][t-2024]+float(row[3])*water_f


    #Calculate BA-based Carbon Rate
    BA_carbon_rate=BA_emit*1000/BA_en
    #Calculate BA-based Water Rate
    BA_water_rate=BA_wa*1000/BA_en
    
    total_area=817.859
    with open(r'E:\ReEDS-2.0-main\inputs\loaddata\BA_area_1.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        BA_id=[]
        BA_state=[]
        BA_area=[]
        for row in reader:
            BA_id.append(row[0])
            BA_state.append(row[1])
            BA_area.append(row[2])
            r=int(row[0].replace('p', ''))
    BA_carbon_rate_cc=np.zeros([BA_number])
    BA_water_rate_cc=np.zeros([BA_number])
    BA_carbon_rate_1=np.zeros([BA_number])
    BA_water_rate_1=np.zeros([BA_number])
    for BA_n in range (BA_number):
        BA_carbon_rate_1[BA_n]=np.mean(BA_carbon_rate[BA_n,:])
        BA_water_rate_1[BA_n]=np.mean(BA_water_rate[BA_n,:])
    BA_carbon_rate_1[BA_carbon_rate_1==0] = 1e12
    BA_water_rate_1[BA_carbon_rate_1==0] = 1e12
    WUE_25=[]
    WUE_50=[]
    WUE_75=[]
    CUE_25=[]
    CUE_50=[]
    CUE_75=[]
    WUE_last25=[]
    CUE_last25=[]
    WUECUE_25=[]
    WUECUE_50=[]
    WUECUE_75=[]
    WUE_25_state_area=np.zeros([L2])
    WUE_50_state_area=np.zeros([L2])
    WUE_75_state_area=np.zeros([L2])
    CUE_25_state_area=np.zeros([L2])
    CUE_50_state_area=np.zeros([L2])
    CUE_75_state_area=np.zeros([L2])
    WUE_last25_state_area=np.zeros([L2])
    CUE_last25_state_area=np.zeros([L2])
    WUECUE_25_state_area=np.zeros([L2])
    WUECUE_50_state_area=np.zeros([L2])
    WUECUE_75_state_area=np.zeros([L2])
    WUE_25_total_area=0
    WUE_50_total_area=0
    WUE_75_total_area=0
    CUE_25_total_area=0
    CUE_50_total_area=0
    CUE_75_total_area=0
    WUE_last25_total_area=0
    CUE_last25_total_area=0
    WUECUE_25_total_area=0
    WUECUE_50_total_area=0
    WUECUE_75_total_area=0
    c_carbon=0
    c_water=0
    c_area_carbon=0
    c_area_water=0
    cc_h=[]
    ww_h=[]
    for BA_n in range (BA_number):
        cc=np.where(BA_carbon_rate_1 == BA_carbon_rate_1.min())[0]
        for item in cc:
            if item not in cc_h:
                cc=cc[0]
                break
        cc_h.append(cc)
        c_area_carbon=c_area_carbon+float(BA_area[cc])
        ww=np.where(BA_water_rate_1 == BA_water_rate_1.min())[0]

        for item in ww:
            if item not in ww_h:
                ww=ww[0]
                break
        ww_h.append(ww)
        c_area_water=c_area_water+float(BA_area[ww])
        
        # last 25% CUE locations
        if c_area_carbon <= total_area*1 and c_area_carbon > total_area*0.75:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                CUE_last25.append(BA_id[cc])
                state_num=indices(states, BA_state[cc])[0]
                CUE_last25_state_area[state_num]=CUE_last25_state_area[state_num]+float(BA_area[cc])
                CUE_last25_total_area=CUE_last25_total_area+float(BA_area[cc])
        
        # 75% CUE locations
        if c_area_carbon <= total_area*0.75:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                CUE_75.append(BA_id[cc])
                state_num=indices(states, BA_state[cc])[0]
                CUE_75_state_area[state_num]=CUE_75_state_area[state_num]+float(BA_area[cc])
                CUE_75_total_area=CUE_75_total_area+float(BA_area[cc])

        # 50% CUE locations
        if c_area_carbon <= total_area*0.50:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                CUE_50.append(BA_id[cc])
                state_num=indices(states, BA_state[cc])[0]
                CUE_50_state_area[state_num]=CUE_50_state_area[state_num]+float(BA_area[cc])
                CUE_50_total_area=CUE_50_total_area+float(BA_area[cc])
        
        # 25% CUE locations
        if c_area_carbon <= total_area*0.25:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                CUE_25.append(BA_id[cc])
                state_num=indices(states, BA_state[cc])[0]
                CUE_25_state_area[state_num]=CUE_25_state_area[state_num]+float(BA_area[cc])
                CUE_25_total_area=CUE_25_total_area+float(BA_area[cc])
    
        # last 25% WUE locations
        if c_area_water <= total_area*1 and c_area_water > total_area*0.75:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                WUE_last25.append(BA_id[ww])
                state_num=indices(states, BA_state[cc])[0]
                WUE_last25_state_area[state_num]=WUE_last25_state_area[state_num]+float(BA_area[ww])
                WUE_last25_total_area=WUE_last25_total_area+float(BA_area[ww])
        
        # 75% WUE locations
        if c_area_water <= total_area*0.75:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                WUE_75.append(BA_id[ww])
                state_num=indices(states, BA_state[cc])[0]
                WUE_75_state_area[state_num]=WUE_75_state_area[state_num]+float(BA_area[ww])
                WUE_75_total_area=WUE_75_total_area+float(BA_area[ww])
                
        # 50% WUE locations
        if c_area_water <= total_area*0.50:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                WUE_50.append(BA_id[ww])
                state_num=indices(states, BA_state[cc])[0]
                WUE_50_state_area[state_num]=WUE_50_state_area[state_num]+float(BA_area[ww])
                WUE_50_total_area=WUE_50_total_area+float(BA_area[ww])
        
        # 25% WUE locations
        if c_area_water <= total_area*0.25:
            if indices(states, BA_state[cc])==[]:
                aaa=1
            else:
                WUE_25.append(BA_id[ww])
                state_num=indices(states, BA_state[cc])[0]
                WUE_25_state_area[state_num]=WUE_25_state_area[state_num]+float(BA_area[ww])
                WUE_25_total_area=WUE_25_total_area+float(BA_area[ww])

        BA_carbon_rate_1[cc]=1e15
        BA_water_rate_1[ww]=1e15
    
    ii=0
    for enum in BA_id:
        # 25% WUE & CUE locations
        if enum in WUE_25 and enum in CUE_25:
            WUECUE_25.append(enum)
            state_num=indices(states, BA_state[ii])[0]
            WUECUE_25_state_area[state_num]=WUECUE_25_state_area[state_num]+float(BA_area[ii])
            WUECUE_25_total_area=WUECUE_25_total_area+float(BA_area[ii])
        
        # 50% WUE & CUE locations
        if enum in WUE_50 and enum in CUE_50:
            WUECUE_50.append(enum)
            state_num=indices(states, BA_state[ii])[0]
            WUECUE_50_state_area[state_num]=WUECUE_50_state_area[state_num]+float(BA_area[ii])
            WUECUE_50_total_area=WUECUE_50_total_area+float(BA_area[ii])
        
        # 75% WUE & CUE locations
        if enum in WUE_75 and enum in CUE_75:
            WUECUE_75.append(enum)
            state_num=indices(states, BA_state[ii])[0]
            WUECUE_75_state_area[state_num]=WUECUE_75_state_area[state_num]+float(BA_area[ii])
            WUECUE_75_total_area=WUECUE_75_total_area+float(BA_area[ii])
        ii=ii+1
            
    #edit h5 file based on the allocation data
    for i in range (L1):
        for j in range (L5):
            load_data[i][j]=load_data[i][j]*1e3
    
    alc_name=['_WUE_25','_CUE_25','_WUE_last25','_CUE_last25']
    alc_data=np.zeros([4,L2,L1])
    alc_data_raw_1=[WUE_25_state_area,CUE_25_state_area,
                   WUE_last25_state_area,CUE_last25_state_area]
    alc_data_raw_2=[WUE_25_total_area,CUE_25_total_area,
                   WUE_last25_total_area,CUE_last25_total_area]
    for i in range (4):
        for j in range (L2):
            for k in range (L1):
                alc_data[i][j][k]=(alc_data_raw_1[i]/alc_data_raw_2[i])[j]
    
    for scenarios in range (4):
        for projections in range (L5):
            if scenarios <2 and projections ==5:
                bbb=1
            else:
                name="std"+repr(projections+1)+alc_name[scenarios]+"_load_hourly.h5"
                filename = r"E:\ReEDS-2.0-main\inputs\loaddata\Baseline_"+name
                print(filename)
                f1 = h5py.File(filename, 'r+')
                data = f1['2030']
                print(data[0][0])

                states_demand=np.zeros([L1,L2])
                for i in range (L1):
                    for j in range (L2):
                        states_demand[i][j]=alc_data[scenarios][j][i]*load_data[i][projections]

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
