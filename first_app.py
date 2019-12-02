import streamlit as st
import numpy as np
import pandas as pd
import time

st.title("My First App")

# st.write("First attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first_col': [1,2,3,4],
#     'second_col': [10,20,30,40]
# }))

"""
# First attempt at using data to create a table:
"""

df = pd.DataFrame({
    'first_col': [1,2,3,4],
    'second_col': [10,20,30,40]
})

df

#LINE
# chart_data = pd.DataFrame(
#     np.random.randn(74,3),
#     columns=['a','b','c'])
# st.line_chart(chart_data)

# MAP
# map_data =pd.DataFrame(np.random.randn(100,2) / [50,50] + [37.76,-122.4],
#                         columns=['lat','lon'])
# st.map(map_data)

# CHECKBOX
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20,3),
        columns = ['a','b','c'])
    st.line_chart(chart_data)

# WIDGET
option = st.sidebar.selectbox('Which number do you like best?',df['first_col'])

'You select: ',option

# PROGRESS
'Starting a long computation...'

## placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    ##update progress bar with each iteration
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.4)

'.... and now we are done!'