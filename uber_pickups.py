import streamlit as st
import numpy as np
import pandas as pd

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
#DATA_URL = 'uber-raw-data-sep14.csv.gz'
DATA_URL = 'uber-raw-data-sep14.csv'

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows = nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase,axis= 'columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data.... DONE!')

if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24,range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour',0,23,17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickup at %s:00' % hour_to_filter)
st.map(filtered_data)