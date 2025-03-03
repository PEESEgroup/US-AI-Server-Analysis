# This file generates the worst practices for AI server water footprint
import numpy as np
import math
import csv

# define scenario numbers
tem_sce_num=5
spt_sce_num=1
typ_sce_num=1

L_1=7
print(L_1)

# Parameter definition
rev2cap=37.6
US_ratio=0.53
#calculate utilization rate based training and inference settings
utilization_level_0=0.3*0.72+0.7*0.25
utilization_level_1=0.3*0.72+0.7*0.25
u_1=0.3*0.74+0.7*0.35
idle_power_rate=0.23
max_power_rate=0.88
DLC_rate_0=0.05
DLC_increase=0

capacity_data=[[12.38452099,12.38452099,12.38452099,12.38452099,12.38452099],
               [25.24151059,25.24151059,25.24151059,25.24151059,24.49468339],
               [45.31383559,45.31383559,45.31383559,45.31383559,44.56700839],
               [64.18503903,64.94884105,68.83140505,69.91355421,79.5840046],
               [76.4008099,78.8836588,89.0288428,93.36924696,121.6582974],
               [82.42292446,87.8425229,103.6748429,115.2113516,161.5394334],
               [80.41621696,89.9042399,111.0747599,130.8812471,194.2004289]]


utilization_level=np.zeros([L_1,1])
DLC_rate=np.zeros([L_1,1])
u_level=np.zeros([L_1,1])
for i1 in range (L_1):
    utilization_level[i1]=(utilization_level_1-utilization_level_0)/L_1*i1+utilization_level_0
    u_level[i1]=(u_1-utilization_level_0)/L_1*i1+utilization_level_0
for i1 in range (L_1):
    if i1==0:
        DLC_rate[i1]=DLC_rate_0
    else:
        DLC_rate[i1]=DLC_rate[i1-1]*(math.pow(1+DLC_increase,1))


# Define power capacity
for i in range (tem_sce_num):
    exec('Capacity_'+repr(i+1)+'=[]')
    for j in range (L_1):
        exec('Capacity_'+repr(i+1)+'.append(capacity_data[j][i]*1e3*u_level[j]/utilization_level[j])')

# spatial allocation scenarios: (1) current data center capacity; (2) uniform allocation
# US ratio
for i in range (tem_sce_num):
    exec('US_Capacity_'+repr(i+1)+'=[]')
    for i1 in range (L_1):
        exec('Maximum_value=Capacity_'+repr(i+1)+'[i1]*US_ratio*max_power_rate')
        exec('Minimum_value=Capacity_'+repr(i+1)+'[i1]*US_ratio*idle_power_rate')
        utilization_level_i=utilization_level[i1]
        exec('US_Capacity_'+repr(i+1)+'.append(((Maximum_value-Minimum_value)*utilization_level_i+Minimum_value))')

print(US_Capacity_1[0])

frozen_data=np.loadtxt(r'D:\2023 Fall\NS R1 Files\Inputs\Spatial Dirstribution\WUE_last25_spatial.txt',delimiter='\t',dtype='float')  
states = ["Alabama", "Arizona","Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", 
          "Georgia", "Idaho","Illinois", "Indiana","Iowa", "Kansas", "Kentucky", "Louisiana","Maine", "Maryland", "Massachusetts", 
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
          "New Jersey", "New Mexico", "New York","North Carolina","North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
          "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
          "Wisconsin", "Wyoming"]

L_2=len(states)
print(L_2)


for i in range (tem_sce_num):
    for j in range (spt_sce_num):
        exec('Specific_Capacity_'+repr(i+1)+'_'+repr(j+1)+'=np.zeros([L_1,L_2])')
        for i1 in range (L_1):
            for j1 in range (L_2):
                exec('Specific_Capacity_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]=US_Capacity_'+repr(i+1)+'[i1]*frozen_data[j1]')
                # transfer MW to MWh in one year
                exec('Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'=Specific_Capacity_'+repr(i+1)+'_'+repr(j+1)+'*8760')
                
# create matrices for save
Power_results=np.zeros([tem_sce_num,spt_sce_num,typ_sce_num])
Water_results=np.zeros([tem_sce_num,spt_sce_num,typ_sce_num])
Carbon_results=np.zeros([tem_sce_num,spt_sce_num,typ_sce_num])

PowerUsage_2=np.zeros([L_1,tem_sce_num*spt_sce_num*typ_sce_num])
WaterUsage_2=np.zeros([L_1,tem_sce_num*spt_sce_num*typ_sce_num])
WaterUsage_D_2=np.zeros([L_1,tem_sce_num*spt_sce_num*typ_sce_num])
CarbonEmission_2=np.zeros([L_1,tem_sce_num*spt_sce_num*typ_sce_num])
sce_flag=0

for i in range (tem_sce_num):
    for j in range (spt_sce_num):
        for k in range (typ_sce_num):
            # import unit emission & water data
            name=r'D:\2023 Fall\NS R1 Files\Inputs\Grid Factor\cases_REcon_'+repr(i+1)+'_WUE_last25_CF.txt'
            e_data=np.loadtxt(name,delimiter=' ',dtype='float')
            name=r'D:\2023 Fall\NS R1 Files\Inputs\Grid Factor\cases_REcon_'+repr(i+1)+'_WUE_last25_WF.txt'
            w_data=np.loadtxt(name,delimiter=' ',dtype='float')
            emission_data=np.zeros([L_1,L_2])
            water_data=np.zeros([L_1,L_2])
            if i == 0:
                e_save=e_data/tem_sce_num
                w_save=w_data/tem_sce_num
            else:
                e_save=e_save+e_data/tem_sce_num
                w_save=w_save+w_data/tem_sce_num
            
            for i1 in range (L_1):
                for j1 in range (L_2):
                    emission_data[i1][j1]=e_data[j1][i1]
                    water_data[i1][j1]=w_data[j1][i1]

            sce_flag=sce_flag+1
            PowerUsage=np.zeros([L_1,L_2])
            WaterUsage=np.zeros([L_1,L_2])
            WaterUsage_D=np.zeros([L_1,L_2])
            CarbonEmission=np.zeros([L_1,L_2])
            flag=0
            with open(r'D:\2023 Fall\NS R1 Files\Inputs\Worst_WUE.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if flag ==0:
                        flag=flag+1
                        continue
                    # chosse either airside or waterside economizer
                    else:
                        for i1 in range (L_1):
                            if row[3]>row[4]:
                                n_count=1
                            else:
                                n_count=2
                            PUE=float(row[n_count])*(1-DLC_rate[i1])+float(row[n_count+4])*(DLC_rate[i1])
                            WUE=float(row[n_count+2])*(1-DLC_rate[i1])+float(row[n_count+4+2])*(DLC_rate[i1])
                            for j1 in range (L_2):
                                if row[0] in states[j1]:
                                    exec('PowerUsage[i1][j1]=PowerUsage[i1][j1]+PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]')
                                    exec('WaterUsage[i1][j1]=WaterUsage[i1][j1]+WUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]+water_data[i1][j1]*PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]')
                                    exec('WaterUsage_D[i1][j1]=WaterUsage_D[i1][j1]+WUE*PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]')
                                    # emission unit should be tons
                                    exec('CarbonEmission[i1][j1]=CarbonEmission[i1][j1]+emission_data[i1][j1]*PUE*Specific_Power_'+repr(i+1)+'_'+repr(j+1)+'[i1][j1]')
                        flag=flag+1
            
            for i1 in range (L_1):
                PowerUsage_2[i1,sce_flag-1]=sum(sum(PowerUsage[i1:(i1+1),:]))/1e6
                WaterUsage_2[i1,sce_flag-1]=sum(sum(WaterUsage[i1:(i1+1),:]))/1e6
                WaterUsage_D_2[i1,sce_flag-1]=sum(sum(WaterUsage_D[i1:(i1+1),:]))/1e6
                CarbonEmission_2[i1,sce_flag-1]=sum(sum(CarbonEmission[i1:(i1+1),:]))/1e6
                
            PowerUsage_1=np.zeros([L_1,L_2])
            WaterUsage_1=np.zeros([L_1,L_2])
            CarbonEmission_1=np.zeros([L_1,L_2])
            for i1 in range (L_1):
                for j1 in range (L_2):
                    PowerUsage_1[i1][j1]=sum(sum(PowerUsage[i1:(i1+1),j1:j1+1]))/1e6
                    WaterUsage_1[i1][j1]=sum(sum(WaterUsage[i1:(i1+1),j1:j1+1]))/1e6
                    CarbonEmission_1[i1][j1]=sum(sum(CarbonEmission[i1:(i1+1),j1:j1+1]))/1e6
            

            # 7 years and million unit = 7e6
            Power_results[i][j][k]=sum(sum(PowerUsage))/7e6
            Water_results[i][j][k]=sum(sum(WaterUsage))/7e6
            Carbon_results[i][j][k]=sum(sum(CarbonEmission))/7e6
            print(sum(sum(PowerUsage))/7e6)
            print(sum(sum(WaterUsage))/7e6)
            print(sum(sum(CarbonEmission))/7e6)
