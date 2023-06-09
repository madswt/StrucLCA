import pandas as pd
import numpy as np



def wood_calc(p, L):
    
    # Load data 
    wood_data = pd.read_csv('/app/struclca/StrucLCA/wood.csv' , sep=';')
    wood = wood_data.to_numpy()
    
    
    
    # Strength and stifness parameters, GL30h
    sigma_m_k = 30
    kmod = 0.8
    gamma = 1.3
    sigma_m_d = sigma_m_k/gamma * kmod
    E_0 = 13600 #[MPa]
    
    
    # For loops for calculating utility rate of bending capacity
    utility_rate_column = []
    for i in range(len(wood)):
        utility_rate = 1/8 * p * L**2 * (10**6) / wood[i,4] / sigma_m_d
        utility_rate_column.append(utility_rate)
    wood_with_utility = np.column_stack((wood, np.array(utility_rate_column)))
    
    
    # For loops for calculating deflection
    kdef = 0
    deflection_column = []
    for i in range(len(wood)):
        deflection_fin = (5/384 * ((p * (L*10**3)**4) / (E_0 * (1/12 * wood[i,1] * wood[i,2]**3)))) * (1 + 1 * kdef)
        deflection_column.append(deflection_fin)
    wood_full_matrix = np.column_stack((wood_with_utility, np.array(deflection_column)))
    
    
    # Delete every row where utility > 1 and deflection > req
    req = L * 10**3 / 400
    filtered_matrix = []
    
    for row in wood_full_matrix:
        if row[5] < 1 and row[6] < req:
            filtered_matrix.append(row)
    filtered_matrix_result = np.array(filtered_matrix)
    
    
    # Return the beam with lowest possible cross section area
    lowest_value = float('inf')
    lowest_value_col1 = None
    
    for row in filtered_matrix_result:
        if row[3] < lowest_value:
            lowest_value = row[3]
            lowest_value_col1 = row[0]
            
      
    best_wood_beam = [lowest_value, lowest_value_col1]
    
   
    if len(filtered_matrix_result) == 0:
        return [0,0] 
    else:    
        return best_wood_beam
            
    
    
    
best_profile = wood_calc(20,20)


# print("Lowest value in column 5:", lowest_value)
# print("Corresponding value from column 1:", lowest_value_col1)    


  
        
    
