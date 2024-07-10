"""
Created on Mon Apr 15 13:18:20 2024

@author: Alex Yang
"""
import streamlit as st 
import pandas as pd 
import altair as alt 

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

reviews = '../data/nv_reviews.csv'
business = '../data/nv_business.csv'
tip = '../data/nv_tips.csv'

st.title("Food Preference Map in Nevada")

reviews = pd.read_csv(reviews)
business = pd.read_csv(business)
tip = pd.read_csv(tip)

# Data Cleaning:
# 1. Select useful columns
business = business.iloc[:,[0,1,3,4,5,6,7,8,9,11,12]]
tip = tip.iloc[:,[0,1,3,4]]
reviews = reviews.iloc[:,:-1]
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
reviews['date'] = pd.to_datetime(reviews['date'])
tip['date'] = pd.to_datetime(tip['date'])
reviews['date'] = reviews['date'].dt.date
tip['date'] = tip['date'].dt.date
max_time = min(tip['date'].max(), reviews['date'].max())
min_time = max(tip['date'].min(), reviews['date'].min())

# Sidebar filters
st.sidebar.header("Select Your Filters")

# Allow user to enter category
input_categories = st.text_input("Enter Category Keyword, use comma(,) to separate multiple categories")

# Allow user to filter by attribute
# input_attributes = st.text_input("Enter Desired Attribute, use comma(,) to separate multiple attributes")

# Filter by city
cities = business["city"].unique()
selected_cities = st.sidebar.multiselect("Select City", list(cities))

# Filter by zipcode
zipcode = business['postal_code'].unique()
selected_zipcode = st.sidebar.multiselect("Select Zipcode", list(sorted(zipcode.astype(int))))

# Filter by time range
timestamp = st.sidebar.slider("Time Range", min_time, max_time, (min_time, max_time))
reviews_filtered = reviews[(reviews['date'].between(timestamp[0], timestamp[1]))]
tip_filtered = tip[(tip['date'].between(timestamp[0], timestamp[1]))]

# Select Food Category
categories = business['categories'].str.split(',').apply(lambda x: [item.strip() for item in x]).explode().unique()
selected_categories = st.sidebar.selectbox("Food Category", categories)

stars_groupby_business_id = reviews_filtered.groupby('business_id').mean('stars').round(2)
score_groupby_business_id = tip_filtered.groupby('business_id').sum('compliment_count')
# join stars_groupby_business_id into business and change the new column name to ratings
business = business.merge(stars_groupby_business_id, left_on='business_id', right_index=True, how='inner')
business = business.merge(score_groupby_business_id , left_on='business_id', right_index=True, how='inner')
business = business.rename(columns={'stars_x': 'stars', 'stars_y': 'ratings'})
business.compliment_count = business.compliment_count.fillna(0)
business.ratings = business.ratings.fillna(0)
# create a new column called feedback score and it is calculated by the average of normalized review_count and normalized compliment_count
business['feedback_score'] = (business.review_count/(business.review_count.max()) + business.compliment_count/(business.compliment_count.max()) )/2

filtered_data = business

# User input for category keyword
if input_categories:
    filtered_data = filtered_data[filtered_data['categories'].str.contains(input_categories, case=False)]
if selected_categories:
    filtered_data = filtered_data[filtered_data['categories'].str.contains(selected_categories, case=False)]
if selected_cities:
    filtered_data = filtered_data[filtered_data["city"].isin(selected_cities)]
if selected_zipcode:
    filtered_data = filtered_data[filtered_data["postal_code"].isin(selected_zipcode)]
     
st.markdown("<h3 style='color: yellow;'>Choose a Food Category to see its performance.</h3>",unsafe_allow_html=True)
st.write("Your Filtered Data in Tabular Format:", '\t' ,"Found", len(filtered_data), "businesses.")
table_data = filtered_data[['name','postal_code','stars','ratings','feedback_score','categories']].sort_values(by=['ratings', 'feedback_score'], ascending=False)
# st.table(table_data.style.set_properties(**{'text-align': 'left'}))

st.dataframe(table_data,
    column_config={
        "stars": st.column_config.NumberColumn(
            format="%s ⭐"
    )},
        hide_index=True)

# Convert ratings to scale compatible with map size
filtered_data['ratings'] = filtered_data['ratings'] * 10
filtered_data['feedback_score'] = filtered_data['feedback_score'] * 100

st.map(filtered_data, longitude='longitude', latitude='latitude', size='ratings', color='#ffaa0088', zoom=10)

st.markdown("<h3 style='color: yellow;'>Overall Feedback Score for Selected Business.</h3>",unsafe_allow_html=True)

st.map(filtered_data, longitude='longitude', latitude='latitude', size='feedback_score', color='#39F149', zoom=10)