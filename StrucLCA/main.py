import os
import streamlit as st
from streamlit_echarts import st_echarts
from steel import steel_calc
from wood import wood_calc
from concrete import concrete_calc





# Disable warning for PyplotGlobalUse
st.set_option('deprecation.showPyplotGlobalUse', False)

# Change current working directory to your desired folder path
#folder_path = '/Users/madswestergaard/Desktop/StrucLCA'
#os.chdir(folder_path)


def main():
    st.title('Make informed design decisions:heavy_exclamation_mark: ')
    "---"
    """
    
    Hey there, Tim! :sunglasses:

    We're delighted to have you join our little tool.
    
    Curious about the best beam material for minimizing CO2 emissions? :earth_americas:
    
    Just input your load and span, click "Calculate", and see a simple bar chart comparing steel, wood, and concrete in terms of their estimated CO2 equivalent emissions.
    
    
    
            
    """       

    beam_length = st.number_input('Span (meters):', min_value=0, step=1)
    load = st.number_input('Load (kN/m):', min_value=0, step=1)

    if st.button('Calculate'):
        # Perform calculations
        best_steel_profile, deflection = steel_calc(load, beam_length)
        best_wood_profile = wood_calc(load, beam_length)
        best_concrete_profile = concrete_calc(load, beam_length)
        "---"
        st.header(Wupti! :100:)
        """
        Below, you'll find three cross-sections along with their corresponding CO2 emissions. 
        Please keep in mind that if the load or span exceeds the capabilities of a particular material, the bar chart will display a zero value for that material.
        """
        
        # Generate chart
        
        options = {
            "xAxis": {
                "type": "category",
                "data": [best_steel_profile[0], best_wood_profile[1], best_concrete_profile[0]],

            },
            "yAxis": {"type": "value"},
            
            "series": [{"data": [(best_steel_profile[1]*1e-6*beam_length)*(1110*7.85), 
                                 (best_wood_profile[0]*10e-6*beam_length)*64.8,
                                 ((best_concrete_profile[1]*1e-9*beam_length*301.24)+(best_concrete_profile[2]*1e-9*beam_length*439*7.7))], 
                                 "type": "bar"}],
        }
        st_echarts(options=options, height="500px")
        
        
        
            
        



if __name__ == '__main__':
    main()

