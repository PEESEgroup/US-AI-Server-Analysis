# This file is a modified version of an open-source model posted at https://github.com/nuoaleon/Data-Center-Water-footprint, in which the immersion cooling systems are specifically defined.
import numpy as np
import pandas as pd

from scipy.optimize import *
from CoolProp.HumidAirProp import HAPropsSI

import pickle

# COP: based on gp regressor
# for water-cooled chiller
COP_gp = pickle.load(open('COP_2.pkl', 'rb'))
# for DX system
COP_DX_gp = pickle.load(open('COP_DX.pkl', 'rb'))
# for air-cooled chiller
COP_air_gp = pickle.load(open('COP_AC.pkl', 'rb'))


# Other functions #

# (used for HDC_AE_Adiabatic)
def Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air):
    # outside air enthalpy
    H_oa = HAPropsSI('H','T',T_oa+273.15,'P',P_oa,'RH',RH_oa/100)
    # outside air absolute humidity
    d_oa = HAPropsSI('W','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa)
    # outside air dewpoint
    dp_oa = HAPropsSI('Tdp','T',T_oa+273.15,'P',P_oa,'RH',RH_oa/100)-273.15
     
    # # # # (calculations)-------------------------------
    if (T_lw <= T_oa < T_up):
        # absolute humidity range:
        d_up = np.minimum(HAPropsSI('W','T',T_oa+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_oa+273.15,'Tdp',dp_up+273.15,'P',P_oa))
        d_lw = np.maximum(HAPropsSI('W','T',T_oa+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_oa+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
        if (d_lw <= d_oa <= d_up): # *checked*
            AE_use = 1
            HD_use = 0
            Steam_use = 0
            DHD_use = 0
            delta_d = 0
            d_sa = d_oa
            T_cd = T_oa
            H_cd = H_oa
            chiller_energy = 0
            heating_energy = 0
            T_sa = T_oa
            H_sa = H_oa            
        if (d_oa > d_up): # *checked*
            AE_use = 0
            HD_use = 0
            Steam_use = 0
            DHD_use = 1
            d_sa = d_up
            delta_d = d_oa - d_up
            T_cd = dp_up   
            H_cd = HAPropsSI('H','T',dp_up+273.15,'P',P_oa,'W',d_up)
            chiller_energy = H_oa - H_cd
            heating_energy = 0
            T_sa = np.maximum(T_lw, T_cd)   # mix air to low setpoint when required
            H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_up)
        if (d_oa < d_lw): # *checked*
            # if use adiabatic humidification (default)
            AE_use = 1
            HD_use = 1
            Steam_use = 0
            DHD_use = 0
            delta_d = d_lw - d_oa
            d_sa = d_lw
            H_cd = H_oa
            T_cd = HAPropsSI('T','H',H_oa,'W',d_lw,'P',P_oa)-273.15
            chiller_energy = 0
            heating_energy = 0
            T_sa = np.maximum(T_lw, T_cd)   # mix air to low setpoint when required
            H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_lw)
    
    if (T_oa < T_lw):
        # absolute humidity range:
        d_up = np.minimum(HAPropsSI('W','T',T_lw+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_lw+273.15,'Tdp',dp_up+273.15,'P',P_oa))
        d_lw = np.maximum(HAPropsSI('W','T',T_lw+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_lw+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
        if (d_oa < d_lw): # *checked*
            # if use adiabatic humidification (default)
            AE_use = 1
            HD_use = 1
            Steam_use = 0
            DHD_use = 0
            delta_d = d_lw - d_oa
            d_sa = d_lw
            H_cd = H_oa
            T_cd = HAPropsSI('T','H',H_oa,'W',d_lw,'P',P_oa)-273.15
            chiller_energy = 0
            heating_energy = 0
            T_sa = np.maximum(T_lw, T_oa)   # mix air to low setpoint when required
            H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_lw)
        if (d_lw <= d_oa <= d_up): # *checked*
            AE_use = 1
            HD_use = 0
            Steam_use = 0
            DHD_use = 0
            delta_d = 0
            d_sa = d_oa
            T_cd = T_oa 
            H_cd = H_oa
            chiller_energy = 0
            heating_energy = 0
            T_sa = np.maximum(T_lw, T_oa)   # mix air to low setpoint when required
            H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_oa) 
        if (d_oa > d_up): # *checked*
            d_up_at_upsasp = HAPropsSI('W','T',T_up+273.15,'Tdp',dp_up+273.15,'P',P_oa) # absolute humidity at upper bound temperature setpoint
            if (d_oa <= d_up_at_upsasp):
                AE_use = 1
                HD_use = 0
                Steam_use = 0
                DHD_use = 0
                delta_d = 0
                T_cd = T_oa
                d_sa = d_oa
                H_cd = H_oa
                chiller_energy = 0
                heating_energy = 0
                #y = lambda x: HAPropsSI('RH','T',T_oa+273.15+x,'P',P_oa,'W',d_oa) - RH_up/100  # find how mix with hot air could get the required RH
                #T_sa = fsolve(y,0)[0] + T_oa
                T_sa = T_lw
                H_sa = HAPropsSI('H','T',T_lw+273.15,'P',P_oa,'W',d_oa)
            else:  #*checked*
                AE_use = 1
                HD_use = 0
                Steam_use = 0
                DHD_use = 1
                delta_d = d_oa - d_up_at_upsasp
                T_cd = dp_up
                d_sa = d_up_at_upsasp
                H_cd = HAPropsSI('H','T',dp_up + 273.15,'P',P_oa,'W',d_up_at_upsasp)
                chiller_energy = np.maximum(H_cd - H_oa,0)  # a very small portion of time that requires dehumidifcation but enthalpy of air is low, sometimes th
                heating_energy = 0
                T_sa = np.maximum(T_lw, T_cd)   # mix air to low setpoint when required
                H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_up_at_upsasp) 
                
    if (T_oa >= T_up):
        # absolute humidity range:
        d_up = np.minimum(HAPropsSI('W','T',T_up+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_up+273.15,'Tdp',dp_up+273.15,'P',P_oa))
        d_lw = np.maximum(HAPropsSI('W','T',T_up+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_up+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
        # enthalpy threshold for evaporative cooling
        H_threshold_up = HAPropsSI('H','T',T_up+273.15,'P',P_oa,'W',d_up)
        H_threshold_lw = HAPropsSI('H','T',T_up+273.15,'P',P_oa,'W',d_lw)

        #...(new control policy: the old one was commented below because too optimistic)        
        AE_use = 0
        HD_use = 0
        Steam_use = 0
        DHD_use = 0
        T_cd = T_up
        H_cd = HAPropsSI('H','T',T_up+273.15,'P',P_oa,'W',d_up)
        d_sa = d_up #not useful here#
        delta_d = 0

        H_sa = H_cd
        H_ra = H_sa + 1.01*delta_T_air*1000
        
        chiller_energy = H_ra - H_cd
        heating_energy = 0
        T_sa = T_cd
        H_sa = H_cd
        H_oa = H_sa + 1.01*delta_T_air*1000 # treat return air as outside air because DC will use return air

        # if (H_threshold_lw <= H_oa <= H_threshold_up):  # *checked*
        #     AE_use = 1
        #     HD_use = 1
        #     Steam_use = 0
        #     DHD_use = 0
        #     T_cd = T_up
        #     H_cd = H_oa
        #     d_sa = HAPropsSI('W','T',T_up+273.15,'H',H_oa,'P',P_oa)
        #     delta_d = d_sa - d_oa
        #     chiller_energy = 0
        #     heating_energy = 0
        #     T_sa = T_up
        #     H_sa = H_oa
        # if (H_oa < H_threshold_lw): # *checked*
        #     AE_use = 1
        #     HD_use = 1
        #     Steam_use = 0
        #     DHD_use = 0
        #     H_cd = H_oa
        #     d_sa = d_lw
        #     T_cd = HAPropsSI('T','H',H_oa,'P',P_oa,'W',d_lw)-273.15
        #     delta_d = d_lw - d_oa
        #     chiller_energy = 0
        #     heating_energy = 0
        #     H_sa = H_cd
        #     T_sa = T_cd   
        # if (H_oa > H_threshold_up): 
        #     AE_use = 0
        #     if d_oa <= d_up: # *checked*
        #         HD_use = 1
        #         Steam_use = 0
        #         DHD_use = 0
        #         T_cd = dp_up
        #         H_cd = HAPropsSI('H','T',dp_up+273.15,'P',P_oa,'W',d_up)
        #         d_sa = d_up
        #         delta_d = d_up - d_oa
        #         chiller_energy = H_oa - H_cd
        #         heating_energy = 0
        #         T_sa = np.maximum(T_lw, T_cd)   # mix air to low setpoint when required
        #         H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_up)      
        #     if d_oa > d_up:
        #         HD_use = 0
        #         Steam_use = 0
        #         DHD_use = 1
        #         T_cd = dp_up
        #         H_cd = HAPropsSI('H','T',dp_up+273.15,'P',P_oa,'W',d_up)
        #         d_sa = d_up
        #         delta_d = d_oa - d_up
        #         chiller_energy = H_oa - H_cd
        #         heating_energy = 0
        #         T_sa = np.maximum(T_lw, T_cd)   # mix air to low setpoint when required
        #         H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_up)      
     
        #     # constraint (if outside air enthalpy is higher than return air enthalpy, set restriction to use return air)
        #     H_ra = H_sa + 1.0delta_d1*delta_T_air*1000
        #     if H_oa >= H_ra:
        #         AE_use = 0
        #         HD_use = 0
        #         Steam_use = 0
        #         DHD_use = 0
        #         T_cd = T_up
        #         H_cd = HAPropsSI('H','T',T_up+273.15,'P',P_oa,'W',d_up)
        #         d_sa = d_up
        #         delta_d = 0
        #         chiller_energy = H_ra - H_cd
        #         heating_energy = 0
        #         T_sa = T_cd
        #         H_sa = H_cd
        #         H_oa = H_sa + 1.01*delta_T_air*1000 # treat return air as outside air
    
    return AE_use, HD_use, DHD_use, Steam_use, delta_d, T_sa, H_sa, T_cd, H_cd, d_sa, H_oa, chiller_energy, heating_energy 


# (used for Colo_AE)
def Air_side_economizer_colo(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa):
    # outside air enthalpy
    H_oa = HAPropsSI('H','T',T_oa+273.15,'P',P_oa,'RH',RH_oa/100)
    # outside air absolute humidity
    d_oa = HAPropsSI('W','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa)
    # outside air dewpoint
    dp_oa = HAPropsSI('Tdp','T',T_oa+273.15,'P',P_oa,'RH',RH_oa/100)-273.15
    
    ## default supply air temperature:
    T_sa = np.max([T_up,T_lw])
    
    # # # # (calculations)-------------------------------
    if (T_lw <= T_oa <= T_up):
        # absolute humidity range:
        d_up = np.minimum(HAPropsSI('W','T',T_oa+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_oa+273.15,'Tdp',dp_up+273.15,'P',P_oa))
        d_lw = np.maximum(HAPropsSI('W','T',T_oa+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_oa+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
        if (d_lw <= d_oa <= d_up):
            AE_use = 1
            H_cd = H_oa
            T_cd = T_oa
            d_sa = d_oa
            T_sa = T_oa
            H_sa = H_oa
        else: # because no humidification or de-humidification
            AE_use = 0
            T_sa = T_sa
            d_up = np.minimum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_up+273.15,'P',P_oa))
            d_lw = np.maximum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
            # how to select absolute humidity
            d_sa = np.random.uniform(d_up,d_lw,1)[0]
            H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_sa)
            H_cd = H_sa
            T_cd = T_sa
            
    elif (T_oa < T_lw):
        # absolute humidity range:
        d_up = np.minimum(HAPropsSI('W','T',T_lw+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_lw+273.15,'Tdp',dp_up+273.15,'P',P_oa))
        d_lw = np.maximum(HAPropsSI('W','T',T_lw+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_lw+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
        if (d_lw <= d_oa <= d_up): # *checked*
            AE_use = 1
            H_cd = H_oa
            T_cd = T_oa
            d_sa = d_oa
            T_sa = np.maximum(T_lw, T_oa)   # mix air to low setpoint when required
            H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_oa)
        else:
            AE_use = 0
            # how to select temperature: can be changed to random select based on outdoor climate ??(linear)
            T_sa = T_sa
            d_up = np.minimum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_up+273.15,'P',P_oa))
            d_lw = np.maximum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
            # how to select absolute humidity
            d_sa = np.random.uniform(d_up,d_lw,1)[0]
            H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_sa)
            H_cd = H_sa
            T_cd = T_sa      
    else:
        AE_use = 0
        # how to select temperature: can be changed to random select based on outdoor climate ??(linear)
        T_sa = T_sa
        d_up = np.minimum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_up+273.15,'P',P_oa))
        d_lw = np.maximum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
        # how to select absolute humidity
        d_sa = np.random.uniform(d_up,d_lw,1)[0]
        H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_sa)
        H_cd = H_sa
        T_cd = T_sa
    
    return AE_use, d_sa, T_sa, H_sa, T_cd, H_cd


# (used for HDC_AE_Adiabatic, HDC_WE, Colo_AE, Colo_WE, Colo_Chiller)
def Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,Q,delta_T_CT,Windage_p,CC,LGRatio):
    # Enthalpy of outside air
    h_oa = HAPropsSI('H','T',T_oa+273.15,'P',P_oa,'R',RH_oa/100)
    # wetbulb temperature of outside air
    T_wb_oa = HAPropsSI('Twb','H',h_oa,'T',T_oa+273.15,'P',P_oa)-273.15
    # absolute humidity of outside air
    d_oa = HAPropsSI('W','H',h_oa,'R',RH_oa/100,'P',P_oa)
    # absolute humidity of outlet cooling tower air: saturated
    d_oasa = HAPropsSI('W','H',h_oa,'R',1,'P',P_oa)
    # fun: Latent heat of water
    Latent_heat_vaporization = lambda T_water: -0.0013*(T_water)**(2)-2.3097*(T_water)+2500.5
    # Mass flow rate of cooling tower water: m_CT, kg/s
    m_CT = Q/(4.184*delta_T_CT)
    # Average temperature of cooling tower water: 
    T_CT = T_wb_oa + AT_CT + delta_T_CT/2
    # Evaporated water:
    Water_CT_evaporated = Q/Latent_heat_vaporization(T_CT)
    # Mass-flow of cooling tower air
    #m_air = Water_CT_evaporated/(d_oasa-d_oa)
    m_air = Water_CT_evaporated/LGRatio
    # Drift loss water: 
    Water_CT_windage =  m_CT*Windage_p
    # Drain-off water:
    Water_CT_DF = np.maximum(Water_CT_evaporated/(CC-1)-Water_CT_windage, 0)
    WUE = (Water_CT_evaporated +  Water_CT_windage + Water_CT_DF)*3600/Power_IT
    return WUE, m_air, m_CT/m_air, Water_CT_evaporated, Water_CT_windage, Water_CT_DF

# (used for HDC_WE, Colo_WE)
def waterside_economizer(T_sfw,T_rfw,Twb_oa,AT_CT,AT_HE,Cooling_required):
    if (Twb_oa + AT_CT + AT_HE) <= T_sfw:
        use = 1
        WE_heat_removed = Cooling_required
    elif (Twb_oa + AT_CT + AT_HE) > T_sfw and (Twb_oa + AT_CT + AT_HE) < T_rfw:
        use = 1
        WE_heat_removed = Cooling_required*((T_rfw-(Twb_oa + AT_CT + AT_HE))/(T_rfw-T_sfw))
    else:
        use = 0
        WE_heat_removed = 0
    return use, WE_heat_removed

# (used for HDC_WE, Colo_WE)
def Chiller_system(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air):
    # how to select temperature: can be changed to random select based on outdoor climate (linear)
    T_sa = np.max([T_up,T_lw])
    #T_sa = np.random.uniform(T_up,T_lw,1)[0] 
    d_up = np.minimum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_up+273.15,'P',P_oa))
    d_lw = np.maximum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
    # how to select absolute humidity
    #d_sa = np.mean([d_up,d_lw])
    d_sa = np.random.uniform(d_up,d_lw,1)[0]
    H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_sa)
    return T_sa,d_sa,H_sa

# (used for DX)
def Chiller_system_DX(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa):        
    # how to select temperature: can be changed to random select based on outdoor climate (linear)
    T_sa = np.mean([T_up,T_lw])
    #T_sa = np.random.uniform(T_up,T_lw,1)[0]
    d_up = np.minimum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_up/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_up+273.15,'P',P_oa))
    d_lw = np.maximum(HAPropsSI('W','T',T_sa+273.15,'RH',RH_lw/100,'P',P_oa),HAPropsSI('W','T',T_sa+273.15,'Tdp',dp_lw+273.15,'P',P_oa))
    d_sa = np.random.uniform(d_up,d_lw,1)[0]
    H_sa = HAPropsSI('H','T',T_sa+273.15,'P',P_oa,'W',d_sa)
    return T_sa,d_sa,H_sa



###############################
###### PUE&WUE functions ######
###############################

# PUE & WUE for Data Center with Airside Economizer***
def PUE_WUE_AE_Chiller(w):
    Power_IT = 1 #
    T_oa = w[0] #
    RH_oa = w[1] #
    P_oa = w[2] #
    UPS_e = w[3] #
    PD_lr = w[4] #
    L_percentage = w[5] #
    delta_T_air = w[6] #
    Fan_Pressure_CRAC = w[7] #
    Fan_e_CRAC = w[8] #
    Pump_Pressure_HD = w[9] #
    Pump_e_HD = w[10] #
    AT_CT = w[11] #
    Chiller_load = w[12] # 
    delta_T_water = w[13] #
    Pump_Pressure_CW = w[14] #
    Pump_e_CW = w[15] #
    delta_T_CT = w[16] #
    Pump_Pressure_CT = w[17] #
    Pump_e_CT = w[18] #
    Windage_p = w[19] #
    CC = w[20] #
    Fan_Pressure_CT = w[21] #
    Fan_e_CT = w[22] #
    SHR = w[23] #
    LGRatio = w[24] #
    T_up = w[25] #
    T_lw = w[26] #
    dp_up = w[27] #
    dp_lw = w[28] #
    RH_up = w[29] #
    RH_lw = w[30] #
    w_eff = 1
    pcop = w[31] #
    
    # functions````````
    Fan_Power = lambda mass_flow_rate,air_density,Fan_Pressure,Fan_e: mass_flow_rate/air_density*Fan_Pressure/Fan_e/1000
    Pump_Power = lambda mass_flow_rate,Pump_Pressure,Pump_e,liquid_density: Pump_Pressure*mass_flow_rate/(1000*Pump_e*liquid_density)
    # ``````````````````
    
    # cooling requirement: --IT --UPS loss --power distribution loss --lighting power
    Q = Power_IT + (Power_IT/UPS_e - Power_IT) + (Power_IT/(1-PD_lr) - Power_IT) + (Power_IT*L_percentage)
    # supply air temp
    T_sa = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[2]
    # return air temp
    T_ra = T_sa + delta_T_air
    # usage scenario of --AE, --HD, --DHD
    AE_use = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[0]  
    # enthalpy of --conditioned air and --supply air --return air --outside air: kJ/kg
    H_cd = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[5]/1000
    H_sa = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[3]/1000
    H_ra = H_sa + 1.01*delta_T_air
    H_oa = HAPropsSI('H','T',T_oa+273.15,'P',P_oa,'RH',RH_oa/100)/1000
    # mass flow of supply air
    m_sa = Q/(H_ra-H_sa)
    # mass flow of conditioned air (because there is air mix with return air to get supply air)
    m_cd = m_sa*(H_sa-H_ra)/(H_cd-H_ra)
    # supply air absolute humidity
    d_sa = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[1]
    # mass flow of conditional dry air (no water sink and source inside DC, d_sa=d_ra=d_cd)
    m_cd_dry =  m_cd/(1 + d_sa)
    m_sa_dry =  m_sa/(1 + d_sa)
    # heat removed by AE
    heat = AE_use*m_cd*(H_ra-H_cd)
    # supply air --density
    density_sa = 1/HAPropsSI('Vha','T',T_sa+273.15,'W',d_sa,'P',P_oa)
    #p# (power)---CRAC Fan Power
    Power_Fan_CRAC = Fan_Power(m_sa,density_sa,Fan_Pressure_CRAC,Fan_e_CRAC)
    #w# (water)---Humidification amount (***)
    HD_use = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[1]
    delta_d = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[4]
    hd_amount_ae = np.maximum(HD_use * m_cd_dry * delta_d,0)
    
    # heat removed by chiller
    Chiller_heat_removed = Q - heat
    if Chiller_heat_removed !=0:
        Q_heat_latent = Chiller_heat_removed/SHR - Chiller_heat_removed
        Chiller_heat_removed = Q_heat_latent + Chiller_heat_removed
        d_ra_chiller = Q_heat_latent/2266
        #w# (water)---Humidification amount
        #hd_amount = np.maximum(m_sa_dry * (d_ra_chiller),0)
        hd_amount = np.maximum((d_ra_chiller),0)
    else:
        Q_heat_latent = 0
        Chiller_heat_removed = Q_heat_latent + Chiller_heat_removed
        hd_amount = 0
    #p# (power)---Humidification Pump Power  ？？？？change input
    Power_Pump_hd = Pump_Power(hd_amount,Pump_Pressure_HD,Pump_e_HD,1000)
    # ---wetbulb of outside air
    Twb_oa = HAPropsSI('Twb','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa) - 273.15
    # Approach temperature
    AT_CT = AT_CT
    # COP of chiller: using GP model
    COP_chiller = COP_gp.predict(np.array([Twb_oa+AT_CT,Chiller_load]).reshape(1,2))[0]*(1+pcop)
    #p# (power)---Chiller power
    Power_Chiller = Chiller_heat_removed/COP_chiller
    # mass flow rate of chilled water
    m_sw = Chiller_heat_removed/(4.184*(delta_T_water))
    #p# (power)---Chilled water pump
    Power_Pump_CW = Pump_Power(m_sw,Pump_Pressure_CW,Pump_e_CW,1000)
    # Heat removed by cooing tower
    CT_heat_removed = Chiller_heat_removed + Power_Chiller
    # Mass flow rate of cooling tower water
    m_CT = CT_heat_removed/(4.184*delta_T_CT)
    #p# (power)---Cooling tower water pump
    Power_Pump_CT = Pump_Power(m_CT,Pump_Pressure_CT,Pump_e_CT,1000)
    # Mass flow rate of cooling tower air
    m_CT_air = Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,CT_heat_removed,delta_T_CT,Windage_p,CC,LGRatio)[1]
    #p# (power)---Cooling tower fan
    density_oa = 1/HAPropsSI('Vha','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa)
    Power_Fan_CT = Fan_Power(m_CT_air,density_oa,Fan_Pressure_CT,Fan_e_CT)
    #****# PUE
    Power_comp = np.array([Power_IT, (Power_IT/UPS_e - Power_IT), (Power_IT/(1-PD_lr) - Power_IT), Power_IT*L_percentage, Power_Fan_CRAC, Power_Pump_hd, Power_Chiller, Power_Pump_CW, Power_Pump_CT, Power_Fan_CT])
    PUE = np.sum(Power_comp)/Power_IT
    #****# WUE
    Water_comp = np.concatenate(([(hd_amount+hd_amount_ae)/w_eff],np.maximum([0,0,0],Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,CT_heat_removed,delta_T_CT,Windage_p,CC,LGRatio)[3:6])))
    WUE = np.sum(Water_comp)*3600/Power_IT
    return PUE, WUE


# PUE & WUE for Data Center with Waterside Economizer***
def PUE_WUE_Chiller_Watereconomier(w):    
    Power_IT = 1 #
    T_oa = w[0] #
    RH_oa = w[1] #
    P_oa = w[2] #
    UPS_e = w[3] #
    PD_lr = w[4] #
    L_percentage = w[5] #
    delta_T_air = w[6] #
    Fan_Pressure_CRAC = w[7] #
    Fan_e_CRAC = w[8] #
    Pump_Pressure_HD = w[9] #
    Pump_e_HD = w[10] #
    AT_CT = w[11] #
    Chiller_load = w[12] #
    delta_T_water = w[13] #
    Pump_Pressure_CW = w[14] #
    Pump_e_CW = w[15] #
    delta_T_CT = w[16] #
    Pump_Pressure_CT = w[17] #
    Pump_e_CT = w[18] #
    Windage_p = w[19] #
    CC = w[20]
    Fan_Pressure_CT = w[21]
    Fan_e_CT = w[22]
    SHR = w[23] #
    LGRatio = w[24]
    T_up = w[25]
    T_lw = w[26]
    dp_up = w[27]
    dp_lw = w[28]
    RH_up = w[29]
    RH_lw = w[30]
    pcop = w[31]
    HTE = w[32] #
    AT_HE = w[33] #
    Pump_Pressure_WE = w[34] #
    Pump_e_WE = w[35] #
    w_eff = 1

    # functions````````
    Fan_Power = lambda mass_flow_rate,air_density,Fan_Pressure,Fan_e: mass_flow_rate/air_density*Fan_Pressure/Fan_e/1000
    Pump_Power = lambda mass_flow_rate,Pump_Pressure,Pump_e,liquid_density: Pump_Pressure*mass_flow_rate/(1000*Pump_e*liquid_density)
    # ``````````````````
    
    # ---wetbulb of outside air
    Twb_oa = HAPropsSI('Twb','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa) - 273.15
    # cooling requirement: --IT --UPS loss --power distribution loss --lighting power
    Q = Power_IT + (Power_IT/UPS_e - Power_IT) + (Power_IT/(1-PD_lr) - Power_IT) + (Power_IT*L_percentage)
    # latent heat
    Q_heat_latent = Q/SHR - Q
    # supply --air temp --abosolute humidity --enthalpy
    T_sa = Chiller_system(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[0]
    d_sa = Chiller_system(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[1]
    H_sa = Chiller_system(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[2]/1000
    # return air temp
    T_ra = T_sa + delta_T_air
    # mass flow of --supply air --supply dry air
    m_sa = Q/(1.01 * delta_T_air)
    m_sa_dry =  m_sa/(1 + d_sa)
    # supply air density
    density_sa = 1/HAPropsSI('Vha','T',T_sa+273.15,'W',d_sa,'P',P_oa) 
    #p# (power)---CRAC Fan Power
    Power_Fan_CRAC = Fan_Power(m_sa,density_sa,Fan_Pressure_CRAC,Fan_e_CRAC) 
    # return --air enthalpy --absolute humidity
    H_ra = (Q_heat_latent + Q)/m_sa + H_sa
    d_ra = HAPropsSI('W','H',H_ra*1000,'T',T_ra+273.15,'P',P_oa)
    d_ra_chiller = Q_heat_latent/2266
    #w# (water)---Humidification amount
    hd_amount = np.maximum((d_ra_chiller),0)
    #p# (power)---Humidification Pump Power  ？？？？change input
    Power_Pump_hd = Pump_Power(hd_amount,Pump_Pressure_HD,Pump_e_HD,1000)
    # Cooling required: Cooling_required
    Cooling_required = Q + Q_heat_latent
    # Supply facility water temperature
    T_sfw = T_ra - (T_ra - T_sa)/HTE
    # Return facility water temperature
    T_rfw = T_sfw + delta_T_water
    # Usage scenario of waterside economizer
    WE_use = waterside_economizer(T_sfw,T_rfw,Twb_oa,AT_CT,AT_HE,Cooling_required)[0]
    # The heat removed by waterside economizer
    WE_heat_removed = waterside_economizer(T_sfw,T_rfw,Twb_oa,AT_CT,AT_HE,Cooling_required)[1]
    # Mass flow of facility water
    m_sfw = WE_heat_removed/(4.2*delta_T_water)
    #p# (power)---Waterside economizer pump
    Power_Pump_WE = Pump_Power(m_sfw,Pump_Pressure_WE,Pump_e_WE,1000)
    #Additional cooling by chiller: Chiller_heat_removed
    Chiller_heat_removed = Cooling_required - WE_heat_removed
    # Mass flow of chilled water
    m_sw = Chiller_heat_removed/(4.2*delta_T_water)
    #p# (power) --- Chilled water pump
    Power_Pump_CW = Pump_Power(m_sw,Pump_Pressure_CW,Pump_e_CW,1000)
    # COP of chiller: using GP model
    COP_chiller = COP_gp.predict(np.array([Twb_oa+AT_CT,Chiller_load]).reshape(1,2))[0]*(1+pcop)
    #p# (power)---Chiller power
    Power_Chiller = Chiller_heat_removed/COP_chiller
    # Heat removed by cooing tower
    CT_heat_removed = Cooling_required + Power_Chiller
    # Mass flow rate of cooling tower water
    m_CT = CT_heat_removed/(4.184*delta_T_CT)
    #p# (power)---Cooling tower water pump
    Power_Pump_CT = Pump_Power(m_CT,Pump_Pressure_CT,Pump_e_CT,1000)
    # Mass flow rate of cooling tower air
    m_CT_air = Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,Q,delta_T_CT,Windage_p,CC,LGRatio)[1]
    #p# (power)---Cooling tower fan
    density_oa = 1/HAPropsSI('Vha','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa)
    Power_Fan_CT = Fan_Power(m_CT_air,density_oa,Fan_Pressure_CT,Fan_e_CT)
    #****# PUE
    Power_comp = np.array([Power_IT, (Power_IT/UPS_e - Power_IT), (Power_IT/(1-PD_lr) - Power_IT), Power_IT*L_percentage, Power_Fan_CRAC, Power_Pump_hd, Power_Pump_WE, Power_Chiller, Power_Pump_CW, Power_Pump_CT, Power_Fan_CT])
    PUE = np.sum(Power_comp)/Power_IT
    #****# WUE
    Water_comp = np.concatenate(([hd_amount/w_eff],Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,Q,delta_T_CT,Windage_p,CC,LGRatio)[3:6]))
    WUE = np.sum(Water_comp)*3600/Power_IT
    return PUE, WUE
    
# PUE & WUE for Data Center with Airside Economizer and immersion cooling***
def PUE_WUE_AE_Immersion_Chiller(w):
    Power_IT = 1 #
    T_oa = w[0] #
    RH_oa = w[1] #
    P_oa = w[2] #
    UPS_e = w[3] #
    PD_lr = w[4] #
    L_percentage = w[5] #
    delta_T_air = w[6] #
    Fan_Pressure_CRAC = w[7] #
    Fan_e_CRAC = w[8] #
    Pump_Pressure_HD = w[9] #
    Pump_e_HD = w[10] #
    AT_CT = w[11] #
    Chiller_load = w[12] # 
    delta_T_water = w[13] #
    Pump_Pressure_CW = w[14] #
    Pump_e_CW = w[15] #
    delta_T_CT = w[16] #
    Pump_Pressure_CT = w[17] #
    Pump_e_CT = w[18] #
    Windage_p = w[19] #
    CC = w[20] #
    Fan_Pressure_CT = w[21] #
    Fan_e_CT = w[22] #
    SHR = w[23] #
    LGRatio = w[24] #
    T_up = w[25] #
    T_lw = w[26] #
    dp_up = w[27] #
    dp_lw = w[28] #
    RH_up = w[29] #
    RH_lw = w[30] #
    w_eff = 1
    pcop = w[31] #
    rho_CL=w[32]
    f_CL=w[33]
    m_CL=f_CL*rho_CL/(1000*60)
    Pump_Pressure_CL=w[34]
    Pump_e_CL=w[35]
    
    # functions````````
    Fan_Power = lambda mass_flow_rate,air_density,Fan_Pressure,Fan_e: mass_flow_rate/air_density*Fan_Pressure/Fan_e/1000
    Pump_Power = lambda mass_flow_rate,Pump_Pressure,Pump_e,liquid_density: Pump_Pressure*mass_flow_rate/(1000*Pump_e*liquid_density)
    # ``````````````````
    
    # cooling requirement: --IT --UPS loss --power distribution loss --lighting power
    Q = Power_IT + (Power_IT/(1-PD_lr) - Power_IT)
    # supply air temp
    T_sa = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[2]
    # return air temp
    T_ra = T_sa + delta_T_air
    # usage scenario of --AE, --HD, --DHD
    AE_use = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[0]  
    # enthalpy of --conditioned air and --supply air --return air --outside air: kJ/kg
    H_cd = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[5]/1000
    H_sa = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[3]/1000
    H_ra = H_sa + 1.01*delta_T_air
    H_oa = HAPropsSI('H','T',T_oa+273.15,'P',P_oa,'RH',RH_oa/100)/1000
    # mass flow of supply air
    m_sa = Q/(H_ra-H_sa)
    # mass flow of conditioned air (because there is air mix with return air to get supply air)
    m_cd = m_sa*(H_sa-H_ra)/(H_cd-H_ra)
    # supply air absolute humidity
    d_sa = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[1]
    # mass flow of conditional dry air (no water sink and source inside DC, d_sa=d_ra=d_cd)
    m_cd_dry =  m_cd/(1 + d_sa)
    m_sa_dry =  m_sa/(1 + d_sa)
    # heat removed by AE
    heat = AE_use*m_cd*(H_ra-H_cd)
    # supply air --density
    density_sa = 1/HAPropsSI('Vha','T',T_sa+273.15,'W',d_sa,'P',P_oa)
    #p# (power)---CRAC Fan Power
    Power_Fan_CRAC = Fan_Power(m_sa,density_sa,Fan_Pressure_CRAC,Fan_e_CRAC)
    #w# (water)---Humidification amount (***)
    HD_use = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[1]
    delta_d = Air_side_economizer(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[4]
    hd_amount_ae = np.maximum(HD_use * m_cd_dry * delta_d,0)
    
    # heat removed by chiller
    Chiller_heat_removed = Q - heat
    if Chiller_heat_removed !=0:
        Q_heat_latent = Chiller_heat_removed/SHR - Chiller_heat_removed
        Chiller_heat_removed = Q_heat_latent + Chiller_heat_removed
        d_ra_chiller = Q_heat_latent/2266
        #w# (water)---Humidification amount
        #hd_amount = np.maximum(m_sa_dry * (d_ra_chiller),0)
        hd_amount = np.maximum((d_ra_chiller),0)
    else:
        Q_heat_latent = 0
        Chiller_heat_removed = Q_heat_latent + Chiller_heat_removed
        hd_amount = 0
    #p# (power)---Humidification Pump Power  ？？？？change input
    Power_Pump_hd = Pump_Power(hd_amount,Pump_Pressure_HD,Pump_e_HD,1000)
    # ---wetbulb of outside air
    Twb_oa = HAPropsSI('Twb','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa) - 273.15
    # Approach temperature
    AT_CT = AT_CT
    # COP of chiller: using GP model
    COP_chiller = COP_gp.predict(np.array([Twb_oa+AT_CT,Chiller_load]).reshape(1,2))[0]*(1+pcop)
    #p# (power)---Chiller power
    Power_Chiller = Chiller_heat_removed/COP_chiller
    # mass flow rate of chilled water
    m_sw = Chiller_heat_removed/(4.184*(delta_T_water))
    #p# (power)---Chilled water pump
    Power_Pump_CW = Pump_Power(m_sw,Pump_Pressure_CW,Pump_e_CW,1000)
    # Heat removed by cooing tower
    CT_heat_removed = Chiller_heat_removed + Power_Chiller
    # Mass flow rate of cooling tower water
    m_CT = CT_heat_removed/(4.184*delta_T_CT)
    #p# (power)---Cooling tower water pump
    Power_Pump_CT = Pump_Power(m_CT,Pump_Pressure_CT,Pump_e_CT,1000)
    # Mass flow rate of cooling tower air
    m_CT_air = Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,CT_heat_removed,delta_T_CT,Windage_p,CC,LGRatio)[1]
    #p# (power)---Cooling tower fan
    density_oa = 1/HAPropsSI('Vha','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa)
    Power_Fan_CT = Fan_Power(m_CT_air,density_oa,Fan_Pressure_CT,Fan_e_CT)
    #p# (power)---Immersion cooling water pump
    Power_Pump_CL = Pump_Power(m_CL,Pump_Pressure_CL,Pump_e_CL,rho_CL)
    #****# PUE
    Power_comp_single = np.array([Power_IT,(Power_IT/UPS_e - Power_IT),(Power_IT/(1-PD_lr) - Power_IT),Power_IT*L_percentage, Power_Pump_hd, Power_Chiller, Power_Pump_CW, Power_Pump_CT, Power_Fan_CT,Power_Pump_CL])
    Power_comp_two = np.array([Power_IT, (Power_IT/UPS_e - Power_IT), (Power_IT/(1-PD_lr) - Power_IT), Power_IT*L_percentage, Power_Pump_hd, Power_Chiller, Power_Pump_CW, Power_Pump_CT, Power_Fan_CT])
    PUE_single = np.sum(Power_comp_single)/Power_IT
    PUE_two = np.sum(Power_comp_two)/Power_IT
    #****# WUE
    Water_comp = np.concatenate(([(hd_amount+hd_amount_ae)/w_eff],np.maximum([0,0,0],Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,CT_heat_removed,delta_T_CT,Windage_p,CC,LGRatio)[3:6])))
    WUE_single = np.sum(Water_comp)*3600/Power_IT
    WUE_two = np.sum(Water_comp)*3600/Power_IT
    return PUE_single, PUE_two, WUE_single, WUE_two    

# PUE & WUE for Data Center with Waterside Economizer and immersion cooling***
def PUE_WUE_Immersion_Chiller_Watereconomier(w):    
    Power_IT = 1 #
    T_oa = w[0] #
    RH_oa = w[1] #
    P_oa = w[2] #
    UPS_e = w[3] #
    PD_lr = w[4] #
    L_percentage = w[5] #
    delta_T_air = w[6] #
    Fan_Pressure_CRAC = w[7] #
    Fan_e_CRAC = w[8] #
    Pump_Pressure_HD = w[9] #
    Pump_e_HD = w[10] #
    AT_CT = w[11] #
    Chiller_load = w[12] #
    delta_T_water = w[13] #
    Pump_Pressure_CW = w[14] #
    Pump_e_CW = w[15] #
    delta_T_CT = w[16] #
    Pump_Pressure_CT = w[17] #
    Pump_e_CT = w[18] #
    Windage_p = w[19] #
    CC = w[20]
    Fan_Pressure_CT = w[21]
    Fan_e_CT = w[22]
    SHR = w[23] #
    LGRatio = w[24]
    T_up = w[25]
    T_lw = w[26]
    dp_up = w[27]
    dp_lw = w[28]
    RH_up = w[29]
    RH_lw = w[30]
    pcop = w[31]
    HTE = w[32] #
    AT_HE = w[33] #
    Pump_Pressure_WE = w[34] #
    Pump_e_WE = w[35] #
    w_eff = 1
    rho_CL=w[36]
    f_CL=w[37]
    m_CL=f_CL*rho_CL/(1000*60)
    Pump_Pressure_CL=w[38]
    Pump_e_CL=w[39]

    # functions````````
    Fan_Power = lambda mass_flow_rate,air_density,Fan_Pressure,Fan_e: mass_flow_rate/air_density*Fan_Pressure/Fan_e/1000
    Pump_Power = lambda mass_flow_rate,Pump_Pressure,Pump_e,liquid_density: Pump_Pressure*mass_flow_rate/(1000*Pump_e*liquid_density)
    # ``````````````````
    
    # ---wetbulb of outside air
    Twb_oa = HAPropsSI('Twb','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa) - 273.15
    # cooling requirement: --IT --UPS loss --power distribution loss --lighting power
    Q = Power_IT + (Power_IT/(1-PD_lr) - Power_IT)
    # latent heat
    Q_heat_latent = Q/SHR - Q
    # supply --air temp --abosolute humidity --enthalpy
    T_sa = Chiller_system(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[0]
    d_sa = Chiller_system(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[1]
    H_sa = Chiller_system(T_up,T_lw,dp_up,dp_lw,RH_up,RH_lw,T_oa,RH_oa,P_oa,delta_T_air)[2]/1000
    # return air temp
    T_ra = T_sa + delta_T_air
    # mass flow of --supply air --supply dry air
    m_sa = Q/(1.01 * delta_T_air)
    m_sa_dry =  m_sa/(1 + d_sa)
    # supply air density
    density_sa = 1/HAPropsSI('Vha','T',T_sa+273.15,'W',d_sa,'P',P_oa) 
    #p# (power)---CRAC Fan Power
    Power_Fan_CRAC = Fan_Power(m_sa,density_sa,Fan_Pressure_CRAC,Fan_e_CRAC) 
    # return --air enthalpy --absolute humidity
    H_ra = (Q_heat_latent + Q)/m_sa + H_sa
    d_ra = HAPropsSI('W','H',H_ra*1000,'T',T_ra+273.15,'P',P_oa)
    d_ra_chiller = Q_heat_latent/2266
    #w# (water)---Humidification amount
    hd_amount = np.maximum((d_ra_chiller),0)
    #p# (power)---Humidification Pump Power  ？？？？change input
    Power_Pump_hd = Pump_Power(hd_amount,Pump_Pressure_HD,Pump_e_HD,1000)
    # Cooling required: Cooling_required
    Cooling_required = Q + Q_heat_latent
    # Supply facility water temperature
    T_sfw = T_ra - (T_ra - T_sa)/HTE
    # Return facility water temperature
    T_rfw = T_sfw + delta_T_water
    # Usage scenario of waterside economizer
    WE_use = waterside_economizer(T_sfw,T_rfw,Twb_oa,AT_CT,AT_HE,Cooling_required)[0]
    # The heat removed by waterside economizer
    WE_heat_removed = waterside_economizer(T_sfw,T_rfw,Twb_oa,AT_CT,AT_HE,Cooling_required)[1]
    # Mass flow of facility water
    m_sfw = WE_heat_removed/(4.2*delta_T_water)
    #p# (power)---Waterside economizer pump
    Power_Pump_WE = Pump_Power(m_sfw,Pump_Pressure_WE,Pump_e_WE,1000)
    #Additional cooling by chiller: Chiller_heat_removed
    Chiller_heat_removed = Cooling_required - WE_heat_removed
    # Mass flow of chilled water
    m_sw = Chiller_heat_removed/(4.2*delta_T_water)
    #p# (power) --- Chilled water pump
    Power_Pump_CW = Pump_Power(m_sw,Pump_Pressure_CW,Pump_e_CW,1000)
    # COP of chiller: using GP model
    COP_chiller = COP_gp.predict(np.array([Twb_oa+AT_CT,Chiller_load]).reshape(1,2))[0]*(1+pcop)
    #p# (power)---Chiller power
    Power_Chiller = Chiller_heat_removed/COP_chiller
    # Heat removed by cooing tower
    CT_heat_removed = Cooling_required + Power_Chiller
    # Mass flow rate of cooling tower water
    m_CT = CT_heat_removed/(4.184*delta_T_CT)
    #p# (power)---Cooling tower water pump
    Power_Pump_CT = Pump_Power(m_CT,Pump_Pressure_CT,Pump_e_CT,1000)
    # Mass flow rate of cooling tower air
    m_CT_air = Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,Q,delta_T_CT,Windage_p,CC,LGRatio)[1]
    #p# (power)---Cooling tower fan
    density_oa = 1/HAPropsSI('Vha','T',T_oa+273.15,'RH',RH_oa/100,'P',P_oa)
    Power_Fan_CT = Fan_Power(m_CT_air,density_oa,Fan_Pressure_CT,Fan_e_CT)
    #p# (power)---Immersion cooling water pump
    Power_Pump_CL = Pump_Power(m_CL,Pump_Pressure_CL,Pump_e_CL,rho_CL)
    #****# PUE
    Power_comp_single = np.array([Power_IT, (Power_IT/UPS_e - Power_IT), (Power_IT/(1-PD_lr) - Power_IT), Power_IT*L_percentage, Power_Pump_hd, Power_Pump_WE, Power_Chiller, Power_Pump_CW, Power_Pump_CT, Power_Fan_CT, Power_Pump_CL])
    Power_comp_two = np.array([Power_IT, (Power_IT/UPS_e - Power_IT), (Power_IT/(1-PD_lr) - Power_IT), Power_IT*L_percentage, Power_Pump_hd, Power_Pump_WE, Power_Chiller, Power_Pump_CW, Power_Pump_CT, Power_Fan_CT])
    PUE_single = np.sum(Power_comp_single)/Power_IT
    PUE_two = np.sum(Power_comp_two)/Power_IT
    #****# WUE
    Water_comp = np.concatenate(([hd_amount/w_eff],Cooling_Tower(T_oa,RH_oa,P_oa,AT_CT,Power_IT,Q,delta_T_CT,Windage_p,CC,LGRatio)[3:6]))
    WUE_single = np.sum(Water_comp)*3600/Power_IT
    WUE_two = np.sum(Water_comp)*3600/Power_IT
    return PUE_single, PUE_two, WUE_single, WUE_two
