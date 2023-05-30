import os
import streamlit as st
from streamlit_echarts import st_echarts
from steel import steel_calc
from wood import wood_calc




# Disable warning for PyplotGlobalUse
st.set_option('deprecation.showPyplotGlobalUse', False)

# Change current working directory to your desired folder path
#folder_path = '/Users/madswestergaard/Desktop/StrucLCA'
#os.chdir(folder_path)


def main():
    st.title('Make informed design decisions:heavy_exclamation_mark: ')

    beam_length = st.number_input('Span (meters):', min_value=0, step=1)
    load = st.number_input('Load (kN/m):', min_value=0, step=1)

    if st.button('Enter'):
        # Perform calculations
        best_steel_profile, deflection = steel_calc(load, beam_length)
        best_wood_profile = wood_calc(load, beam_length)
        
        
        # Generate chart
        
        options = {
            "xAxis": {
                "type": "category",
                "data": [best_steel_profile[0], best_wood_profile[1], "Result 3"],
            },
            "yAxis": {"type": "value"},
            
            "series": [{"data": (([best_steel_profile[1]*1e-6*beam_length)*7,85)*1110, best_wood_profile[0]*10e-6*64.8,1], "type": "bar"}],
        }
        st_echarts(options=options, height="500px")
            
        



if __name__ == '__main__':
    main()


