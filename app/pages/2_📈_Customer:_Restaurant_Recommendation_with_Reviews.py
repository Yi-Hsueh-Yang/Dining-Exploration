"""
Created on Mon Apr 15 18:38:35 2024

@author: Xiangyu Bao
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import folium
import pydeck as pdk
from streamlit_folium import folium_static

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

reviews_loc = 'data/nv_reviews.csv'
business_loc = 'data/nv_business.csv'

st.title("Categorical Analysis")
# st.markdown("This interactive dashboard supports the exploration of trends of the primary drugs involved in fatal accidental overdoses in Allegheny County.  You can filter by the date of the overdose incident, as well as select the number of top ranked primary drugs to show.")

reviews_df = pd.read_csv(reviews_loc)
business_df = pd.read_csv(business_loc)

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

restaurant_business_df = business_df[business_df['categories'].str.contains('restaurant')]

split_categories = restaurant_business_df['categories'].str.split(', ').explode()

feature_counts = split_categories.value_counts()

top_30_features = feature_counts.head(30)

top_30_feature_list = top_30_features.index.tolist()

print(len(split_categories.unique().tolist()))

print(top_30_features.index.tolist())

st.sidebar.header("View Toggles")

reviews = st.sidebar.toggle("Show Reviews")

st.sidebar.header("Filters")

selected_type = st.sidebar.selectbox("Select Type", top_30_feature_list)

target_df = restaurant_business_df[restaurant_business_df['categories'].str.contains(selected_type)]

ranked_df = target_df.sort_values(by='stars', ascending=False)

showing_df = ranked_df.head(5)

showing_df = showing_df.reset_index(drop=True)
showing_df.index += 1

# map = folium.Map(location=[showing_df['latitude'].mean(), showing_df['longitude'].mean()], zoom_start=11)
map = folium.Map(location=[showing_df['latitude'].mean(), showing_df['longitude'].mean()], zoom_start=11, tiles='CartoDB Positron')


# Add markers to the map with index labels
for index, row in showing_df.iterrows():
    label = f"{index}"  # Use index as label
    folium.Marker([row['latitude'], row['longitude']], popup=row['name'], tooltip=label).add_to(map)

# Display the Folium map in Streamlit using folium_static
folium_static(map)

# st.map(showing_df[['latitude', 'longitude']])

# Display the list of top 5 restaurants
st.header('Top 5 Restaurants')
for index, row in showing_df.iterrows():
    filrev_df = reviews_df[reviews_df['business_id'] == row['business_id']]
    filrev_df = filrev_df[filrev_df['text'] != '']
    latest_review = filrev_df.loc[filrev_df['date'].idxmax()]
    st.subheader(str(index) + ". " + row['name'])
    st.write(f"Type: {row['categories']}")
    st.write(f"Stars: {row['stars']}")
    st.write(f"Type: {row['categories']}")
    if reviews:
        st.write(f"Latest Review: {latest_review['text']}")