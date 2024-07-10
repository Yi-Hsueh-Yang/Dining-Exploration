"""
Created on Mon Apr 15 18:38:35 2024

@author: Xuye He
"""
import streamlit as st
import pandas as pd
from utils.predict import get_cities_and_categories, get_checkin_prediction

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

st.title('Check-ins HeatMap')

business_csv = "data/nv_business.csv"
checkin_csv = "data/nv_checkin.csv"

business_df = pd.read_csv(business_csv)
checkin_df = pd.read_csv(checkin_csv)

# cleaning business.csv
business_df["city"] = business_df["city"].str.lower().str.strip().str.replace(',', '')
city_mapping = {
    'reno': 'reno',
    'sparks': 'sparks',
    'fernley': 'fernley',
    'virginia city': 'virginia city',
    'spanish springs': 'spanish springs',
    'sun valley': 'sun valley',
    'verdi': 'verdi',
    'washoe valley': 'washoe valley',
    'reno ap': 'reno',
    'reno nevada': 'reno',
    'vc highlands': 'vc highlands',
    'cold springs': 'cold springs',
    'nevada': 'reno',
    'washoe': 'washoe',
    'mount laurel': 'mount laurel',
    'carson city': 'carson city',
    'mccarran': 'mccarran',
    'new washoe city': 'new washoe city',
    'reno city': 'reno',
    'stead': 'stead',
    'south reno': 'reno',
    'reno sparks': 'sparks'
}
business_df['city'] = business_df['city'].map(city_mapping)
business_df["categories"] = business_df["categories"].str.lower()

st.header("Check-ins Explorer")

col1, col2 = st.columns(2)

# select time
checkin_df['date'] = pd.to_datetime(checkin_df['date'])
max_date = checkin_df['date'].dt.date.max()
min_date = checkin_df['date'].dt.date.min()

cities_list, categories_list = get_cities_and_categories()

with col1:
    selected_cities = st.multiselect('Select cities:', cities_list)

with col2:
    selected_date_range = st.slider("Date Range",
                                    min_value=min_date,
                                    max_value=max_date,
                                    value=(min_date, max_date),
                                    format="YYYY-MM-DD")


checkin_counts = checkin_df[checkin_df['date'].dt.date.between(selected_date_range[0], selected_date_range[1])] \
                            .groupby('business_id').size().reset_index(name='checkin_count')

# Note that businesses with 0 checkins will be filtered out
merged_df = pd.merge(business_df, checkin_counts, on='business_id')
merged_df.dropna(subset=['city', 'categories', 'hours'], inplace=True)

filtered_df = merged_df[merged_df['city'].isin(selected_cities)]

st.markdown("View number of checkins in selected cities:")
if selected_cities:
    sorted_df = filtered_df[['name', 'city', 'stars', 'checkin_count']].sort_values('checkin_count', ascending=False)
    st.dataframe(sorted_df, hide_index=True)

# Map for check-ins
st.map(filtered_df,
       latitude='latitude',
       longitude='longitude',
       size='checkin_count',
       zoom=9)


st.header("Looking forward to opening a business?")
# Predictive model for # of checkins

open_ctgrs = st.multiselect("Your business type:", categories_list)
open_cities = st.selectbox("Where you want to open your business in Nevada?", cities_list)
open_hours = st.slider("Weekly opening hours",
                                    min_value=1,
                                    max_value=144,
                                    value=55)

if st.button("Predict"):
    if open_ctgrs:
        res = get_checkin_prediction(open_ctgrs, open_cities, open_hours)
        st.text(f"You will get {res} checkins!")

    else:
        st.text("Please fill the options above!")
