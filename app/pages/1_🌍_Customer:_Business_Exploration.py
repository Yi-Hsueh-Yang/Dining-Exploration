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

reviews_loc = 'data/nv_reviews.csv'
business_loc = 'data/nv_business.csv'

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
# st.sidebar.header("Filters")

# Filter by city
cities = business["city"].unique()
selected_cities = st.multiselect("Select City", list(cities))

# Create three columns
col1, col2, col3 = st.columns([3, 1, 3])

# Filter by stars (first column)
min_stars = col1.slider("Minimum Review Stars", min_value=0, max_value=5, value=0)

# Filter by review count percentage (third column)
review_count_percentage_choices = [25, 50, 75,100]  # Define choices
review_count_percentage = col3.selectbox("Review Count in Top %", review_count_percentage_choices)
review_count_threshold = business['review_count'].quantile((100-review_count_percentage) / 100)

# User input for category keyword
category_keyword = st.text_input("Enter Business Category Keyword: ")
if category_keyword:
    business = business[business['categories'].str.contains(category_keyword, case=False)]


# Select day
selected_day = st.selectbox("Choose a Day to Visit the Business", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])


# Filter by opening day
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

import datetime

# Function to check if a business is open at the given time
def is_business_open(hours_str, target_time):
    try:
        hours = hours_str.split("-")
        open_time = datetime.datetime.strptime(hours[0], "%H:%M").time()
        close_time = datetime.datetime.strptime(hours[1], "%H:%M").time()
        return open_time <= target_time <= close_time
    except ValueError:
        return False

# Get user input for the target time
target_time_str = st.text_input("Enter the time to visit:", "13:15")
try:
    target_time = datetime.datetime.strptime(target_time_str, "%H:%M").time()

    # Filter businesses based on the entered time
    filtered_businesses = [business for business in filtered_data.iterrows() if is_business_open(business[1]['hours'], target_time)]

    # Display filtered businesses
    if filtered_businesses:
#        st.write("Businesses open at", target_time_str)
        business_table = pd.DataFrame(columns=['Name', 'Address', 'Stars', 'Review Count', 'Hours', 'Categories'])
        for index, business in filtered_businesses:
            #business_table = business_table.append({'Name': business['name'], 
                                                    #'Address': business['address'], 
                                                    #'Stars': business['stars'], 
                                                    #'Review Count': business['review_count'], 
                                                    #'Hours': business['hours'], 
                                                    #'Categories': business['categories'],
                                                    #'longitude': business['longitude'],
                                                    #'latitude': business['latitude']},
                                                    #ignore_index=True)
            new_row = pd.DataFrame({'Name': [business['name']], 
                        'Address': [business['address']], 
                        'Stars': [business['stars']], 
                        'Review Count': [business['review_count']], 
                        'Hours': [business['hours']], 
                        'Categories': [business['categories']],
                        'longitude': [business['longitude']],
                        'latitude': [business['latitude']]})
            business_table = pd.concat([business_table, new_row], ignore_index=True)
    else:
        st.write("No businesses open at", target_time_str)
except ValueError:
    st.write("Please enter the time in the correct format (HH:MM)")


st.markdown("<h2 style='color: red; font-size: 20px;'>Discover Businesses You Might Like...</h2>", unsafe_allow_html=True)

#table_data = filtered_data[['name','address','stars','review_count','hours','categories']]
# st.table(table_data.style.set_properties(**{'text-align': 'left'}))

# st.dataframe(business_table[['Name','Address','Stars','Review Count','Hours','Categories']],
    #column_config={
        #"Stars": st.column_config.NumberColumn(
            #format="%s ⭐"
    #)},
        #hide_index=True)

import numpy as np
import math
def format_stars(stars):
    if np.isnan(stars):  # Handle missing values
        return ""
    full_stars = int(stars)
    ceil = math.ceil(stars-full_stars)
    return "★" * full_stars + "☆" * ceil

# Apply formatting to the "Stars" column
business_table["Stars"] = business_table["Stars"].apply(format_stars)


# Display the DataFrame with custom formatting
st.data_editor(business_table[['Name','Address','Stars','Review Count','Hours','Categories']],
    column_config={
        "Stars": st.column_config.TextColumn(),  # Use TextColumn to preserve custom formatting
        "Review Count": st.column_config.ProgressColumn("Review Count", format="%s",max_value=1500)
       
    },
    hide_index=True)

# Convert stars to scale compatible with map size
# filtered_data['stars'] = filtered_data['stars']


st.map(business_table, longitude='longitude', latitude='latitude', size='stars', zoom=10)

import random

st.markdown("<h2 style='color: red; font-size: 20px;'>Still not Decided? Press the Button to Get a Random Business...</h2>", unsafe_allow_html=True)
# Define a button to select a random business
if st.button("Select Random Business"):
    random_index = random.randint(0, len(business_table) - 1)
    random_business = business_table[['Name','Address','Stars','Review Count','Hours','Categories']].iloc[random_index]
    st.write("Randomly Selected Business:")
    st.write(random_business)
