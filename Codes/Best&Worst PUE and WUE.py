# import packages
from simulation_funs_DC_i import PUE_WUE_AE_Chiller,PUE_WUE_Chiller_Watereconomier,PUE_WUE_AE_Immersion_Chiller, PUE_WUE_Immersion_Chiller_Watereconomier
import numpy as np
from os import listdir
from os.path import isfile, join
import warnings
warnings.filterwarnings('ignore')
import re
import time
import cyipopt
from cyipopt import minimize_ipopt
import csv
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from torch.autograd import Variable
import math
import time

# Specify model inputs
x = [ 9,  10, 101325,  8.94746094e-01,
        2.84082031e-02,  4.72167969e-02,  9.51835937e-01,  9.49707031e+00,
        6.50488281e+02,  6.13867188e-01,  6.41894531e+06,  6.50976563e-01,
        6.90283203e-01,  6.91894531e+00,  3.35986328e+00,  2.10712891e+00,
        1.56284191e+05,  6.68945312e-01,  1.71884552e+05,  7.45117188e-01,
        3.08984375e-01,  5.09960938e+00,  2.46235102e+05,  7.08007812e-01,
        2.93588867e-03,  1.11650391e+01,  2.72070313e-01,  3.95898438e+02,
        6.11914063e-01,  2.87041016e+01,  1.54423828e+01,  1.67460938e+01,
       -1.11123047e+01,  7.18554688e+01,  2.60351562e+01, -9.17968750e-02]
LB_AE=[-10,10,101325,0.90,0,0,13.9,300,0.65,6300,0.60,2.8,0.2,5,114.9,0.60,4,166.9,0.60,0.005/100,
       3,100,0.65,0.95,0.2,27,10,15,-12,95,60,-0.11]
UB_AE=[+35,100,101325,0.99,0.02,0.002,19.4,1000,0.90,7700,0.90,6.7,0.8,10,172.4,0.80,6,250.4,0.80,0.5/100,
       15,400,0.90,0.99,4,35,18,27,-9,99,95,0.11]
LB_WE=[-10,10,101325,0.90,0,0,13.9,300,0.65,6300,0.60,2.8,0.2,5,114.9,0.60,4,166.9,0.60,0.005/100,
       3,100,0.65,0.95,0.2,27,10,15,-12,95,60,-0.11,0.7,1.7,114.9,0.60]
UB_WE=[+35,100,101325,0.99,0.02,0.002,19.4,700,0.90,7700,0.90,6.7,0.8,10,172.4,0.80,6,250.4,0.80,0.5/100,
       15,400,0.90,0.99,4,35,18,27,-9,99,90,0.11,0.9,2.8,172.4,0.80]
LB_i=[1400,0.5,114.9,60]
UB_i=[1855,2.5,172.4,80]
for index in [4, 5, 19]:
    LB_AE[index]=UB_AE[index]
    LB_WE[index]=UB_WE[index]
for index in [3, 8, 10, 12, 15, 18, 22]:
    UB_AE[index]=LB_AE[index]
    UB_WE[index]=LB_WE[index]
for index in [32, 35]:
    UB_WE[index]=LB_WE[index]
for index in [3]:
    UB_i[index]=LB_i[index]
LB_AE_i=LB_AE+LB_i
UB_AE_i=UB_AE+UB_i
LB_WE_i=LB_WE+LB_i
UB_WE_i=UB_WE+UB_i
L_AE=len(LB_AE)
L_WE=len(LB_WE)
L_i=4


# define corresponding objectives for different data center types and operation goals
def Optobj_1 (inputs):
    [PUE,WUE]=PUE_WUE_AE_Chiller(inputs)
    return -PUE
def Optobj_2 (inputs):
    [PUE,WUE]=PUE_WUE_AE_Chiller(inputs)
    return -WUE
def Optobj_3 (inputs):
    [PUE,WUE]=PUE_WUE_Chiller_Watereconomier(inputs)
    return -PUE
def Optobj_4 (inputs):
    [PUE,WUE]=PUE_WUE_Chiller_Watereconomier(inputs)
    return -WUE
def Optobj_5 (inputs):
    [PUE,PUE1,WUE,WUE1]=PUE_WUE_AE_Immersion_Chiller(inputs)
    return -PUE
def Optobj_6 (inputs):
    [PUE,PUE1,WUE,WUE1]=PUE_WUE_AE_Immersion_Chiller(inputs)
    return -WUE
def Optobj_7 (inputs):
    [PUE,PUE1,WUE,WUE1]=PUE_WUE_Immersion_Chiller_Watereconomier(inputs)
    return -PUE
def Optobj_8 (inputs):
    [PUE,PUE1,WUE,WUE1]=PUE_WUE_Immersion_Chiller_Watereconomier(inputs)
    return -WUE
def Optobj_9 (inputs):
    [PUE,WUE]=PUE_WUE_AE_Chiller(inputs)
    return PUE
def Optobj_10 (inputs):
    [PUE,WUE]=PUE_WUE_AE_Chiller(inputs)
    return WUE
def Optobj_11 (inputs):
    [PUE,WUE]=PUE_WUE_Chiller_Watereconomier(inputs)
    return PUE
def Optobj_12 (inputs):
    [PUE,WUE]=PUE_WUE_Chiller_Watereconomier(inputs)
    return WUE
def Optobj_13 (inputs):
    [PUE,PUE1,WUE,WUE1]=PUE_WUE_AE_Immersion_Chiller(inputs)
    return PUE
def Optobj_14 (inputs):
    [PUE,PUE1,WUE,WUE1]=PUE_WUE_AE_Immersion_Chiller(inputs)
    return WUE
def Optobj_15 (inputs):
    [PUE,PUE1,WUE,WUE1]=PUE_WUE_Immersion_Chiller_Watereconomier(inputs)
    return PUE
def Optobj_16 (inputs):
    [PUE,PUE1,WUE,WUE1]=PUE_WUE_Immersion_Chiller_Watereconomier(inputs)
    return WUE



#Optimization Solver
def Optimization_ipopt(s_number,LB,UB,inputs):
    T_rand =int(time.perf_counter())
    
    # boundary difinition
    bnds = [(0,1) for _ in range(len(LB))]
    for i in range (len(LB)):
        max_value=UB[i]
        min_value=LB[i]
        bnds[i]=(min_value,max_value)
    
    T1 = time.perf_counter()
    # use one objective function to sovle this problem
    solution= minimize_ipopt(Optobj_1, x0=inputs,bounds=bnds,options={'tol':0.01,'dual_inf_tol':0.1,'constr_viol_tol':0.1,'compl_inf_tol':0.1,'acceptable_tol':0.1,'disp': 1,'maxiter':5000,'nlp_scaling_method':'none'})
    return solution

input_AE=np.array([UB_AE,LB_AE])
input_AE=np.average(input_AE, axis=0).tolist()
input_WE=np.array([UB_WE,LB_WE])
input_WE=np.average(input_WE, axis=0).tolist()
input_i=np.array([UB_i,LB_i])
input_i=np.average(input_i, axis=0).tolist()

input_AE_i=input_AE+input_i
input_WE_i=input_WE+input_i

# Airside Economizer data center
solution=Optimization_ipopt(1,LB_AE,UB_AE,input_AE)
input_AE_PUE=solution.x.tolist()
print('input_AE_PUE = ',input_AE_PUE)
print('value = ',-solution.fun)
solution=Optimization_ipopt(2,LB_AE,UB_AE,input_AE)
input_AE_WUE=solution.x.tolist()
print('input_AE_WUE = ',input_AE_WUE)
print('value = ',-solution.fun)

# Waterside Economizer data center
solution=Optimization_ipopt(3,LB_WE,UB_WE,input_WE)
input_WE_PUE=solution.x.tolist()
print('input_WE_PUE = ',input_WE_PUE)
print('value = ',-solution.fun)
solution=Optimization_ipopt(4,LB_WE,UB_WE,input_WE)
input_WE_WUE=solution.x.tolist()
print('input_WE_WUE = ',input_WE_WUE)
print('value = ',-solution.fun)

# Airside Economizer data center with immersion cooling
solution=Optimization_ipopt(5,LB_AE_i,UB_AE_i,input_AE_i)
input_AE_PUE_i=solution.x.tolist()
print('input_AE_PUE_i = ',input_AE_PUE_i)
print('value = ',-solution.fun)
solution=Optimization_ipopt(6,LB_AE_i,UB_AE_i,input_AE_i)
input_AE_WUE_i=solution.x.tolist()
print('input_AE_WUE_i = ',input_AE_WUE_i)
print('value = ',-solution.fun)

# Waterside Economizer data center with immersion cooling
solution=Optimization_ipopt(7,LB_WE_i,UB_WE_i,input_WE_i)
input_WE_PUE_i=solution.x.tolist()
print('input_WE_PUE_i = ',input_WE_PUE_i)
print('value = ',-solution.fun)
solution=Optimization_ipopt(8,LB_WE_i,UB_WE_i,input_WE_i)
input_WE_WUE_i=solution.x.tolist()
print('input_WE_WUE_i = ',input_WE_WUE_i) 
print('value = ',-solution.fun)
