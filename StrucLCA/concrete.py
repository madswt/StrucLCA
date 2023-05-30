import pandas as pd
import numpy as np

# L = 15 #[m]
# p = 20 #[kN/m]


def concrete_calc(p, L):
    
    # Load data 
    concrete_data = pd.read_csv('/app/struclca/StrucLCA/concrete.csv' , sep=';')
    concrete = concrete_data.to_numpy()
    
    
    
    # Strength and stifness parameters, GL30h
    fyd = 458 #[MPa]
    fcd = 20.7 #[MPa]
    E_0 = 50000 #[MPa]
    
    
    # For loops for calculating utility rate of bending capacity
    utility_rate_column = []
    for i in range(len(concrete)):
        utility_rate = 1/8 * p * L**2 * (10**6) / (fyd * concrete[i,5] * ((concrete[i,2]-40) - (fyd * concrete[i,5])/(2*fcd*concrete[i,1])))
        utility_rate_column.append(utility_rate)
    concrete_with_utility = np.column_stack((concrete, np.array(utility_rate_column)))
    
    
    # For loops for calculating deflection
    deflection_column = []
    for i in range(len(concrete)):
        deflection_fin = 5*(5/384 * ((p * (L*10**3)**4) / (E_0 * (1/12 * concrete[i,1] * concrete[i,2]**3)))) 
        deflection_column.append(deflection_fin)
    concrete_full_matrix = np.column_stack((concrete_with_utility, np.array(deflection_column)))
    
    
    # Delete every row where utility > 1 and deflection > req
    req = L * 10**3 / 400
    filtered_matrix = []
    
    for row in concrete_full_matrix:
        if row[11] < 1 and row[12] < req:
            filtered_matrix.append(row)
    filtered_matrix_result = np.array(filtered_matrix)
    
    
    # Return the beam with lowest possible cross section area
    highest_value = float('-inf')
    highest_value_col1 = None
    highest_value_col2 = None
    
    for row in filtered_matrix_result:
        if row[11] > highest_value:
            highest_value = row[10]
            highest_value_col1 = row[0]
            highest_value_col2 = row[9]
            
      
    best_concrete_beam = [highest_value_col1, highest_value, highest_value_col2]

    
    if len(filtered_matrix_result) == 0:
        return [0,0,0]
    else:    
        return best_concrete_beam
            
    
    
            
            
best_profile = concrete_calc(20,20)

# print("Lowest value in column 5:", lowest_value)
# print("Corresponding value from column 1:", lowest_value_col1)    


  
        
    
