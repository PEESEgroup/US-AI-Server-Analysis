# This file import the historical AI server revenue data and compute the optimal Generalzied Bass model for projection.

from pyomo.environ import *
import numpy as np
import math

num_count=8
for num in range (num_count):
    # create pyomo model for optimization problem
    model = ConcreteModel()
    revenue_data_1=[0.701, 0.760, 0.792, 0.679, 0.634, 0.655, 0.726, 0.968, 1.141, 
                    1.752, 1.900, 1.903, 2.048, 2.366, 2.936, 3.263,3.750,3.833,3.806,3.616,4.284,10.323,14.514,18.40]
    L=len(revenue_data_1)
    #define peak period and final time
    tem_1=L+4*num-1
    tem_2=L+4*(num+1)-2
    final_tem=L+4*7-1

    # declare decision variables
    model.q = Var(domain=NonNegativeReals)
    model.p = Var(domain=NonNegativeReals)
    model.a = Var(domain=NonNegativeReals)
    model.c = Var(domain=Reals)
    model.m = Var(domain=NonNegativeReals)
    model.b = Var(domain=Reals)

    I_data=[]
    revenue_data=[]
    t_data=[]
    for i in range (L):
        revenue_data.append(sum(revenue_data_1[max(0,i-19):i+1]))
        t_data.append(i)
    # define constraints for the exponential shock
    for i in range (1000):
        if i<20.9:
            I_data.append(0)
        else:
            I_data.append(1)
    # define objective
    def obj_rule(model):
        objectives=0
        for i in range (0,L):
            cc=sum(1+model.c*exp(model.b*(j-model.a))*I_data[j] for j in range (0,i+1))
            value=model.m*(1-exp(-(model.p+model.q)*cc))/(1+model.q/model.p*exp(-(model.p+model.q)*cc))
            objectives=objectives+(value-revenue_data[i])**2
        return objectives

    # declare objective
    model.profit = Objective(rule = obj_rule, sense=minimize)


    # declare constraints for model parameters
    model.laborA11 = Constraint(expr = model.a <= 20.999)
    model.laborA12 = Constraint(expr = model.a >= 19.9)
    model.laborA21 = Constraint(expr = model.c <= 100)
    model.laborA22 = Constraint(expr = model.c >= -100)
    model.laborA31 = Constraint(expr = model.b >= -1)
    model.laborA32 = Constraint(expr = model.b <= 0)
    model.laborB11 = Constraint(expr = model.p <= 1.41/1e2)
    model.laborB12 = Constraint(expr = model.p >= 1.41/1e4)
    model.laborB21 = Constraint(expr = model.q <= 1.26)
    model.laborB22 = Constraint(expr = model.q >= 1.26/100)

    # define peak sale constraints for different model
    if num < 7:
        model.laborC1 = Constraint(expr = sum(1+model.c*exp(model.b*(j-model.a))*I_data[j] for j in range (0,tem_1+1)) <= (-log(model.p/model.q))/(model.p+model.q))
        model.laborC2 = Constraint(expr = sum(1+model.c*exp(model.b*(j-model.a))*I_data[j] for j in range (0,tem_2+1)) >= (-log(model.p/model.q))/(model.p+model.q))   
    else:
        model.laborC1 = Constraint(expr = sum(1+model.c*exp(model.b*(j-model.a))*I_data[j] for j in range (0,tem_1+1)) <= (-log(model.p/model.q))/(model.p+model.q))
   
    # declare solvers and solve the problem
    solver = SolverFactory('ipopt')
    solver.options['max_iter']= 30000
    solver.solve(model)


    print('\nProfit = ', model.profit())
    print('m = ', model.m())
    print('p = ', model.p())
    print('q = ', model.q())
    print('a = ', model.a())
    print('b = ', model.b())
    print('c = ', model.c())
