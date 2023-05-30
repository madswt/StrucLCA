# -*- coding: utf-8 -*-
"""
Created on Sat May 27 13:28:33 2023

@author: ander
"""

import pandas as pd
import numpy as np

def find_index_of_max_value_below_threshold(lst, threshold1):
    max_value = float('-inf')
    max_index = -1
    for i, value in enumerate(lst):
        if value < threshold1 and value > max_value:
            max_value = value
            max_index = i
    return max_index

def steel_calc(p , l):
    steel_data = pd.read_csv('steel.csv' , sep=';')
    
    steel = steel_data.to_numpy()
    # steel = np.delete(steel,0,1)
    
    E = 210000          #[N/mm2]
    steel_grade = 275   #[N/mm2]
    safety_factor = 1.1
    
    M_ed = 1/8 * p * (l*1e3)**2          #calculate moment
    
    # selected_indices = []
    M_crd = np.zeros(len(steel))
    util = np.zeros(len(steel))
    deflections = np.zeros(len(steel))
        
    for i in range(0,len(steel)):
        M_crd[i] = steel[i,2] * steel_grade / safety_factor   #moment capacity
        deflections[i] = (5 / 384 * p * (l*1e3)**4 / (E * steel[i,3]))        #deflection
        util[i] = M_ed / M_crd[i]
        
    max_deflection = (l*1e3)/400    
    
    
    result_cap = find_index_of_max_value_below_threshold(util, 1)
    result_def = find_index_of_max_value_below_threshold(deflections, max_deflection)
    
    
    if deflections[result_cap] < max_deflection:
        result = result_cap
    else:
        result = result_def
        
        
    if util[result] < 1 and deflections[result] < max_deflection:
        best_profile = steel[result,:]
    else:
        best_profile = [0,0,0,0,0]
        
    deflection = deflections[result]
                
        
    
    
    return best_profile , deflection


beam_length = 8        #[m]
load        = 20        #[kN/m]

best_profile , deflection = steel_calc(load,beam_length)
print(best_profile)
print(deflection)

