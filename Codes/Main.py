# This file contains the main calculation process for supporting our major findings.
import numpy as np
import math
import csv

# define scenarios for this research: temporal scenario number = 8
tem_sce_num=8
spt_sce_num=1
typ_sce_num=1

# import temporal scenarios
# The file containts the increase of the total AI market at each time step
with open(r'FILE PATH\Unit Temporal Scenario.csv', newline='') as csvfile:
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
# Projected period
L_1=len(quarter)-24
# Total Period
LL_1=len(quarter)
print(L_1)

# define key factors for calculation
# rev2cap: revenue data to capacity data
# US_ratio: the ratio of AI server allocation to the U.S.
# Utilization level for AI servers: minimum and maximum values
# DLC: direct liquid cooling adoption
# These definitions can be easily modified for sensitiviy analysis and best/worst case estimations
rev2cap=37.6
US_ratio=0.53
utilization_level_1_0=0.60
utilization_level_1_1=0.75
utilization_level_2_0=0.90
utilization_level_2_1=0.95
idle_power_rate=0.23
max_power_rate=1
DLC_rate_0=0.04710
DLC_increase=0.15

# calculate the utilization level and DLC rate of each time step
utilization_level_1=np.zeros([LL_1,1])
utilization_level_2=np.zeros([LL_1,1])
DLC_rate=np.zeros([L_1,1])
for i1 in range (LL_1):
    if i1<24:
        utilization_level_1[i1]=utilization_level_1_0
        utilization_level_2[i1]=utilization_level_2_0
    else:
        utilization_level_1[i1]=(utilization_level_1_1-utilization_level_1_0)/L_1*i1+utilization_level_1_0
        utilization_level_2[i1]=(utilization_level_2_1-utilization_level_2_0)/L_1*i1+utilization_level_2_0
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

# Calculate the U.S. total capacity
for i in range (tem_sce_num):
    exec('US_Capacity_'+repr(i+1)+'=[]')
    for i1 in range (LL_1):
        exec('Maximum_value=Capacity_'+repr(i+1)+'[i1]*US_ratio*max_power_rate*utilization_level_1_0')
        exec('Minimum_value=Capacity_'+repr(i+1)+'[i1]*US_ratio*idle_power_rate*utilization_level_1_0')
        utilization_level=(utilization_level_2[i1]-utilization_level_1[i1])*np.random.rand()+utilization_level_1[i1]
        exec('US_Capacity_'+repr(i+1)+'.append(((Maximum_value-Minimum_value)*utilization_level+Minimum_value)/utilization_level)')

# import the spatial distribution data
frozen_data=np.loadtxt(r'FILE PATH\states_spatial_scenario_frozen.txt',delimiter='\t',dtype='float')  
region = ['West South Central', 'West North Central', 'South Atlantic', 'Pacific', 'New England', 'Mountain', 'Middle Atlantic', 'East South Central', 'East North Central']
states = ["Alabama", "Arizona","Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", 
          "Georgia", "Idaho","Illinois", "Indiana","Iowa", "Kansas", "Kentucky", "Louisiana","Maine", "Maryland", "Massachusetts", 
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
          "New Jersey", "New Mexico", "New York","North Carolina","North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
          "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
          "Wisconsin", "Wyoming"]
L_2=len(states)


server_cap_save=np.zeros([L_2,tem_sce_num*int(L_1/4)])

# import data of emission & water per unit of electricity generation
# The best/worst grid decarbonization case will lead to different values. Therefore, the worst and best values are also included in our data folder.
e_data=np.loadtxt(r'D:\2023 Fall\temporal scenario\Unit Emission.txt',delimiter='\t',dtype='float')
emission_data=np.zeros([L_1,L_2])
w_data=np.loadtxt(r'D:\2023 Fall\temporal scenario\Unit Water.txt',delimiter='\t',dtype='float')
water_data=np.zeros([L_1,L_2])
flag=0
flag_1=2
flag_2=0
for i1 in range (L_1):
    flag=flag+1
    for j1 in range (L_2):
        if states [j1] in ['Arkansas', 'Louisiana', 'Oklahoma', 'Texas']:
            j_flag=0
        if states [j1] in ['Iowa', 'Kansas', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota']:
            j_flag=1
        if states [j1] in ['Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 'Virginia', 'West Virginia']:
            j_flag=2
        if states [j1] in ['California', 'Oregon', 'Washington']:
            j_flag=3
        if states [j1] in ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Vermont']:
            j_flag=4
        if states [j1] in ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada', 'New Mexico', 'Utah', 'Wyoming']:
            j_flag=5
        if states [j1] in ['New York', 'New Jersey', 'Pennsylvania']:
            j_flag=6
        if states [j1] in ['Alabama', 'Kentucky', 'Mississippi', 'Tennessee']:
            j_flag=7
        if states [j1] in ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin']:
            j_flag=8
        emission_data[i1][j1]=e_data[j_flag][flag_1]
        water_data[i1][j1]=w_data[j_flag][flag_2]
    if flag==4:
        flag=0
        flag_1=flag_1+1
        flag_2=flag_2+1

        
# Calculate the AI server capacity in each grid cell.
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
                
for i in range (tem_sce_num):
    for j in range (spt_sce_num):
        for i1 in range (int(L_1/4)):
            for j1 in range (L_2):
                exec('server_cap_save[j1,tem_sce_num*i1+i]=sum(Specific_Capacity_'+repr(i+1)+'_'+repr(j+1)+'[i1*4:(i1+1)*4,j1])')
                
# create matrices for save Energy/Water/Carbon results
Power_results=np.zeros([tem_sce_num,spt_sce_num,typ_sce_num])
Water_results=np.zeros([tem_sce_num,spt_sce_num,typ_sce_num])
Carbon_results=np.zeros([tem_sce_num,spt_sce_num,typ_sce_num])

# Caculation process
# Import the PUE and WUE values of each grid cell
# The best/worst PUE and WUE values are calculated in our Best&Worst PUE and WUE.py file. The calculated results for each grid cell is included in our data folder.
# For using the best/worst results of PUE and WUE values, simply replace the csv file with the corresponding one.
with open(r'FILE PATH\PUE_WUE_Density.csv', newline='') as csvfile:
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

for i in range (tem_sce_num):
    for j in range (spt_sce_num):
        for k in range (typ_sce_num):
            PowerUsage=np.zeros([L_1,L_2])
            WaterUsage=np.zeros([L_1,L_2])
            WaterUsage_D=np.zeros([L_1,L_2])
            CarbonEmission=np.zeros([L_1,L_2])
            flag=0
            with open(r'FILE PATH\PUE_WUE_Density.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if flag ==0:
                        flag=flag+1
                        continue
                    else:
                        for i1 in range (L_1):
                            rand_num=np.random.rand()
                            # Determine if DLC is adopted
                            if rand_num> DLC_rate[i1] :
                                # Chosse either airside or waterside economizer
                                if float(row[12]) < 70:
                                    n_count=4
                                else:
                                    n_count=5
                            else:
                                # Chosse either airside or waterside economizer
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
                                    # Emission unit should be tons
                                    exec('CarbonEmission[i1][j1]=CarbonEmission[i1][j1]+emission_data[i1][j1]*PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]/count_num[j1]')
                        flag=flag+1
          # Save results  
          # 7 years and the million unit = 7e6
          # Energy Unit: TWh, Water Unit: Million m3, Carbon Emission Unit: Million tons
            Power_results[i][j][k]=sum(sum(PowerUsage))/7e6
            Water_results[i][j][k]=sum(sum(WaterUsage))/7e6
            Carbon_results[i][j][k]=sum(sum(CarbonEmission))/7e6
            print(sum(sum(PowerUsage))/7e6)
            print(sum(sum(WaterUsage))/7e6)
            print(sum(sum(CarbonEmission))/7e6)
          
# The results saving process is quite flexible, which means any intermediate results during the calculation can be saved if needed.
