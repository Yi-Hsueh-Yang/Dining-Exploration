#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:45:40 2024

@author: jiayingqian
"""

import json
import streamlit as st 
import pandas as pd 
import altair as alt 
import json

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

reviews_loc = '../data/nv_reviews.csv'
business_loc = '../data/nv_business.csv'

st.title("Interactive App for Customers: Explore Businesses in Nevada")

reviews = pd.read_csv(reviews_loc)
business = pd.read_csv(business_loc)


#if st.checkbox("Show Review Data:"):
    #st.write(reviews.head())
    
# Data Cleaning:
    # 1. Only include businesses which are now open
business = business[business["is_open"] == 1]
    # 2. Clean City column 
business["city"] = business["city"].str.lower().str.strip().str.replace(',', '')
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

business['city'] = business['city'].map(city_mapping)
    # 3. Clean hours 


# Sidebar filters
st.sidebar.header("Filters")

# Filter by city
cities = business["city"].unique()
selected_cities = st.sidebar.multiselect("Select City", list(cities))

# Filter by stars
min_stars = st.sidebar.slider("Minimum Review Stars", min_value=0, max_value=5, value=0)

# Select day
selected_day = st.sidebar.selectbox("Select Day", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])


# Filter by review count percentage
review_count_percentage_choices = [0, 25, 50, 75]  # Define choices
review_count_percentage = st.sidebar.selectbox("Select Review Count which Beats % Businesses", review_count_percentage_choices)
review_count_threshold = business['review_count'].quantile(review_count_percentage / 100)

# User input for category keyword
category_keyword = st.text_input("Enter Category Keyword")
if category_keyword:
    business = business[business['categories'].str.contains(category_keyword, case=False)]

# Filter by opening hours
def filter_by_opening_day(data, selected_day):
    filtered_data = []
    for index, row in data.iterrows():
        if row["hours"] != "unknown":
            if selected_day in row['hours'] and json.loads(row["hours"].replace("'", "\""))[selected_day]!='0:0-0:0':
                row['hours'] = json.loads(row["hours"].replace("'", "\""))[selected_day]
                filtered_data.append(row)
    return pd.DataFrame(filtered_data)

# Apply filters
filtered_data = business[(business["stars"] >= min_stars) &
                        (business["review_count"] >= review_count_threshold)]

if selected_cities:
    filtered_data = filtered_data[filtered_data["city"].isin(selected_cities)]
     

filtered_data = filter_by_opening_day(filtered_data, selected_day)



st.markdown("<h2 style='color: blue;'>Businesses You Maybe Interested in...</h2>",unsafe_allow_html=True)
table_data = filtered_data[['name','address','stars','review_count','hours','categories']]
# st.table(table_data.style.set_properties(**{'text-align': 'left'}))



st.dataframe(table_data,
    column_config={
        "stars": st.column_config.NumberColumn(
            format="%s ⭐"
    )},
        hide_index=True)


# Convert stars to scale compatible with map size
filtered_data['stars'] = filtered_data['stars'] * 10

# Show map
st.map(filtered_data, longitude='longitude', latitude='latitude', size='stars', zoom=10)