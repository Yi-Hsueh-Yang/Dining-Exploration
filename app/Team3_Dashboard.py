import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

st.header("Team 3: Las-Vegas general market and business landscape reviews towards customer and businesses owner")

st.markdown("Team Member: Xuye He, Xiangyu Bao, Jiaying Qian, Alex Yang")

st.markdown('')

st.markdown("The raw data used to produce the application: Yelp Dataset")
# df = pd.read_csv("data/overdose_data_092223.csv")
# df.death_date_and_time = pd.to_datetime(df.death_date_and_time)

# st.dataframe(df)

st.markdown("This is an application to give insights to both users and the businesses in Nevada")

st.subheader("Please choose a dashboard using the sidebar on the left.")
