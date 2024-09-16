# This file contains the main calculation process for generating the Base scenarios.
import numpy as np
import math
import csv

# define scenario numbers
tem_sce_num=8
spt_sce_num=1
typ_sce_num=1

# import temporal scenarios
with open(r'D:\2023 Fall\Github Data\Unit Temporal Scenario.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    flag=0
    quarter=[]
    real_values=[]
    for i in range (tem_sce_num):
        exec('temporal_scenario_'+repr(i+1)+'=[]')
    for row in spamreader:
        if flag == 0:
            flag=flag+1
            continue
        else:
            flag=flag+1
            quarter.append(float(row[0]))
            if row[2]!="" :
                real_values.append(float(row[2]))
            for i in range (tem_sce_num):
                exec('temporal_scenario_'+repr(i+1)+'.append(float(row[3+i]))')

L_1=len(quarter)-24
LL_1=len(quarter)

# define parameters for the analysis
rev2cap=37.6
US_ratio=0.53
utilization_level_0=0.6
utilization_level_1=0.65
idle_power_rate=0.23
max_power_rate=0.88
DLC_rate_0=0.05
DLC_increase=0.2

utilization_level=np.zeros([LL_1,1])
DLC_rate=np.zeros([L_1,1])
for i1 in range (LL_1):
    if i1<24:
        utilization_level[i1]=utilization_level_0
    else:
        utilization_level[i1]=(utilization_level_1-utilization_level_0)/L_1*i1+utilization_level_0
for i1 in range (L_1):
    if i1==0:
        DLC_rate[i1]=DLC_rate_0
    else:
        DLC_rate[i1]=DLC_rate[i1-1]*(math.pow(1+DLC_increase,1/4))


# transfer revenue to power capacity
for i in range (tem_sce_num):
    exec('Capacity_'+repr(i+1)+'=[]')
    for j in range (LL_1):
        exec('Capacity_'+repr(i+1)+'.append(temporal_scenario_'+repr(i+1)+'[j'+']*rev2cap)')

# define US AI server capacity
for i in range (tem_sce_num):
    exec('US_Capacity_'+repr(i+1)+'=[]')
    for i1 in range (LL_1):
        exec('Maximum_value=Capacity_'+repr(i+1)+'[i1]*US_ratio*max_power_rate*utilization_level_0')
        exec('Minimum_value=Capacity_'+repr(i+1)+'[i1]*US_ratio*idle_power_rate*utilization_level_0')
        utilization_level_i=utilization_level[i1]
        exec('US_Capacity_'+repr(i+1)+'.append(((Maximum_value-Minimum_value)*utilization_level_i+Minimum_value)/utilization_level_i)')

# Import US allocation scenario
frozen_data=np.loadtxt(r'D:\2023 Fall\Github Data\states_spatial_scenario_frozen.txt',delimiter='\t',dtype='float')  
states = ["Alabama", "Arizona","Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", 
          "Georgia", "Idaho","Illinois", "Indiana","Iowa", "Kansas", "Kentucky", "Louisiana","Maine", "Maryland", "Massachusetts", 
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
          "New Jersey", "New Mexico", "New York","North Carolina","North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
          "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
          "Wisconsin", "Wyoming"]
L_2=len(states)
for i in range (tem_sce_num):
    for j in range (spt_sce_num):
        exec('Specific_Capacity_'+repr(i+1)+'_'+repr(j+1)+'=np.zeros([L_1,L_2])')
        flag=0
        flag_1=0
        for i1 in range (L_1):
            flag=flag+1
            for j1 in range (L_2):
                exec('Specific_Capacity_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]=sum(US_Capacity_'+repr(i+1)+'[ii1]*frozen_data[j1][0] for ii1 in range (0,i1+24+1))')
                # transfer MW to MWh in one quarter
                exec('Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'=Specific_Capacity_'+repr(i+1)+'_'+repr(j+1)+'*8760/4')
            if flag==4:
                flag=0
                flag_1=flag_1+1
                

# Caculation process
with open(r'D:\2023 Fall\Github Data\Density.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    count_num=np.zeros([L_2,1])
    flag=0
    grid_ID=[]
    for row in spamreader:
        if flag == 0:
            flag=flag+1
            continue
        else:
            flag=flag+1
            grid_ID.append(float(row[3]))
        for j1 in range (L_2):
            if row[1] in states[j1]:
                count_num[j1]=count_num[j1]+1
Grid_N=flag
for i in range (tem_sce_num):
    for j in range (spt_sce_num):
        for k in range (typ_sce_num):
            # import unit emission & water data
            name=r'D:\2023 Fall\Github Data\cases_std_'+repr(i+1)+'_CF.txt'
            e_data=np.loadtxt(name,delimiter=' ',dtype='float')
            name=r'D:\2023 Fall\Github Data\cases_std_'+repr(i+1)+'_WF.txt'
            w_data=np.loadtxt(name,delimiter=' ',dtype='float')
            emission_data=np.zeros([L_1,L_2])
            water_data=np.zeros([L_1,L_2])
            if i == 0:
                e_save=e_data/tem_sce_num
                w_save=w_data/tem_sce_num
            else:
                e_save=e_save+e_data/tem_sce_num
                w_save=w_save+w_data/tem_sce_num
            flag=0
            flag_1=0
            for i1 in range (L_1):
                flag=flag+1
                for j1 in range (L_2):
                    emission_data[i1][j1]=e_data[j1][flag_1]
                    water_data[i1][j1]=w_data[j1][flag_1]
                if flag==4:
                    flag=0
                    flag_1=flag_1+1
                  
            PowerUsage=np.zeros([L_1,L_2])
            WaterUsage=np.zeros([L_1,L_2])
            WaterUsage_D=np.zeros([L_1,L_2])
            CarbonEmission=np.zeros([L_1,L_2])
            # import PUE & WUE data
            with open(r'D:\2023 Fall\Github Data\Density.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if flag ==0:
                        flag=flag+1
                        continue
                    # chosse either airside or waterside economizer
                    else:
                        for i1 in range (L_1):
                            rand_num=np.random.rand()
                            if rand_num> DLC_rate[i1] :
                                if float(row[12]) < 70:
                                    n_count=4
                                else:
                                    n_count=5
                            else:
                                if float(row[12]) < 70:
                                    n_count=6
                                else:
                                    n_count=7  
                            PUE=float(row[n_count])
                            WUE=float(row[n_count+4])
                            for j1 in range (L_2):
                                if row[1] in states[j1]:
                                    exec('PowerUsage[i1][j1]=PowerUsage[i1][j1]+PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]/count_num[j1]')
                                    exec('WaterUsage[i1][j1]=WaterUsage[i1][j1]+WUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]/count_num[j1]+water_data[i1][j1]*PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]/count_num[j1]')
                                    exec('WaterUsage_D[i1][j1]=WaterUsage_D[i1][j1]+WUE*PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]/count_num[j1]')
                                    exec('CarbonEmission[i1][j1]=CarbonEmission[i1][j1]+emission_data[i1][j1]*PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]/count_num[j1]')
            

            # 7 years and million unit = 7e6
            # print annual results of each scenario
            if i <7:
                sce='scenario Peak '+repr(2024+i)+':'
            else:
                sce='scenario Peak 2030+'
            print(sce)
            print('Aunnal Energy Consumption: ',sum(sum(PowerUsage))/7e6)
            print('Accumulative Energy Consumption: ',sum(sum(PowerUsage))/1e6)
            print('Aunnal Water Footprint: ',sum(sum(WaterUsage))/7e6)
            print('Accumulative Water Footprint: ',sum(sum(WaterUsage))/1e6)
            print('Aunnal Carbon Emission: ',sum(sum(CarbonEmission))/7e6)
            print('Accumulative Carbon Emission: ',sum(sum(CarbonEmission))/1e6)
          
# The results saving process is quite flexible, which means any intermediate results during the calculation can be saved if needed.
