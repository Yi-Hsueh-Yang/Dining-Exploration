"""
Created on Mon Apr 15 13:18:20 2024

@author: Alex Yang
"""
import streamlit as st
import pandas as pd
import altair as alt
from sklearn.preprocessing import MinMaxScaler
import folium
from streamlit_folium import folium_static


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

reviews = 'data/nv_reviews.csv'
business = 'data/nv_business.csv'
tip = 'data/nv_tips.csv'
reviews = pd.read_csv(reviews)
business = pd.read_csv(business)
tip = pd.read_csv(tip)

#read from a google sheet
# # sheet_url = "https://docs.google.com/spreadsheets/d/1W7rIt4gG7BZOl9_oJ3LUmXHlku7oeXLuSzaGjtxjlFQ/export?format=csv"
# business_url = "https://docs.google.com/spreadsheets/d/1Z1-T4cdTT6aY0XdqprlY2RXU_d9vrZF76vcSlwvEDxA/export?format=csv"
# business = pd.read_csv(business_url)
# reviews_url = "https://docs.google.com/spreadsheets/d/1Z1-T4cdTT6aY0XdqprlY2RXU_d9vrZF76vcSlwvEDxA/export?format=csv"
# reviews = pd.read_csv(reviews_url)
# tip_url = "https://docs.google.com/spreadsheets/d/1qoE6NxaNxPtv3ZJ2_kHI0YEpwZIy83nZJpzNcRg2w78/export?format=csv"
# tip = pd.read_csv(tip_url)

st.title("Food Preference Map in Nevada")

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
scaler = MinMaxScaler(feature_range=(0, 1))
business['feedback_score'] = ((scaler.fit_transform(business[['review_count']]) + scaler.fit_transform(business[['compliment_count']]) )/2 * 100).round(2)

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

st.dataframe(table_data,
    column_config={
        "stars": st.column_config.NumberColumn(
            format="%s ⭐"
    )},
        hide_index=True)

# Create the histogram using Altair
histogram = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('ratings:Q', bin=alt.Bin(maxbins=25), title='Ratings'),
    y='count()'
).properties(
    width=600,  # You can adjust the width to fit your layout
    height=400,
    title='Distribution of Ratings'
)

st.altair_chart(histogram, use_container_width=True)

map = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=11, tiles='CartoDB Positron')

# Add markers to the map with index labels
for index, row in filtered_data.iterrows():
    if row['ratings'] >= 4.5:
        icon = folium.Icon(color='red', icon='fire')
    elif row['ratings'] >= 4 and row['ratings'] < 4.5:
        icon = folium.Icon(color='blue', icon='thumbs-up')
    elif row['ratings'] >= 3 and row['ratings'] < 4:
        icon = folium.Icon(color='green', icon='ok-sign')
    else:
        icon = folium.Icon(color='gray', icon='cutlery')
    tooltip = f"{row['name']} - Ratings: {row['ratings']}"
    folium.Marker([row['latitude'], row['longitude']],
                  icon=icon, popup=row['name'], tooltip=tooltip).add_to(map)

st.markdown("<h3 style='color: yellow;'>Ratings for Selected Business ⭐</h3>",unsafe_allow_html=True)
st.write("Select a certain type of food category to see how it is performing in the selected city/zipcode, and consider any possible investment or promotion to be involved in the marketing.")
st.write("🔥: 4.5 and above, 👍: 4 and above, ✅️: 3 and above, 🍴: below 3")


folium_static(map)

map2 = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=11, tiles='CartoDB Positron')

# Add markers to the map with index labels
for index, row in filtered_data.iterrows():
    if row['feedback_score'] >= 20:
        icon = folium.Icon(color='red', icon='fire')
    elif row['feedback_score'] >= 5 and row['feedback_score'] < 20:
        icon = folium.Icon(color='blue', icon='thumbs-up')
    elif row['feedback_score'] >= 1 and row['feedback_score'] < 5:
        icon = folium.Icon(color='green', icon='ok-sign')
    else:
        icon = folium.Icon(color='gray', icon='cutlery')
    tooltip = f"{row['name']} - Score: {row['feedback_score']}"
    folium.Marker([row['latitude'], row['longitude']],
                  icon=icon, popup=row['name'], tooltip=tooltip).add_to(map2)

st.markdown("<h3 style='color: yellow;'>Feedback Score for Selected Business 📜</h3>",unsafe_allow_html=True)
st.write("Select a certain type of food category to see how it is performing in the selected city/zipcode, and consider any possible investment or promotion to be involved in the marketing.")
st.write("🔥: 20 and above, 👍: 5 and above, ✅️: 1 and above, 🍴: below 1")

folium_static(map2)

histogram = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('feedback_score:Q', bin=alt.Bin(maxbins=25), title='Feedback_score'),
    y='count()'
).properties(
    width=600,  # You can adjust the width to fit your layout
    height=400,
    title='Distribution of Feedback Score'
)

st.altair_chart(histogram, use_container_width=True)
