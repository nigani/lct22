import streamlit as st
import datetime

import glob
import json
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import altair as alt

st.set_page_config(layout="wide")
st.sidebar.title('Мониторинг аномалий')


d = st.sidebar.date_input("Выберите дату", datetime.date(2021, 11, 6))
t = st.sidebar.time_input('Выберите время', datetime.time(15, 0))
interval = st.sidebar.slider('Выберите интервал в часах', min_value=1, max_value=6)

@st.cache
def load_aniomalii_1():
    rezult = pd.read_pickle('../data/anomalii_1.pickle')
    return rezult

aniomalii_1 = load_aniomalii_1()

@st.cache
def load_UNOM():
    rezult = pd.read_pickle('../data/UNOM_geoData.pickle')
    return rezult

UNOM = load_UNOM()


@st.cache
def load_df():
    rezult = pd.read_pickle('../data/Full_16_09_22-cat.pickle')
    rezult.УНОМ = rezult.УНОМ.astype(int)
    rezult = rezult[rezult.УНОМ.isin(set(UNOM.index))]    
    return rezult

df = load_df()

tz = datetime.timezone(datetime.timedelta(seconds=19800))
dt_end = datetime.datetime.combine(d, t, tzinfo = tz)
dt_start = dt_end - datetime.timedelta(hours=interval)

st.sidebar.write(f"Всего загружено {len(df)} закрытых заявок")
df_limit = df[df['Дата закрытия'].between(dt_start, dt_end, inclusive='both')]
st.sidebar.write(f"В текущем интервале {len(df_limit)} заявок")

df_ano_1 = aniomalii_1[aniomalii_1['Дата закрытия'].between(dt_start, dt_end, inclusive='both')]

st.sidebar.write(f"в том числе аномалий: {len(df_ano_1)}")

with st.expander("Аномальные заявки"):
    st.write(df_ano_1.reset_index(drop=True))
    

# m = folium.Map(location=[37.1462997018576, 55.9870634033471], zoom_start=16)

# for elem in UNOM.loc[df_ano_1.УНОМ.astype(int)].geoData:
#     el = elem['coordinates'][0][0]
#     folium.Marker([el[1], el[0]]).add_to(m)

# # call to render Folium map in Streamlit
# folium_static(m)
