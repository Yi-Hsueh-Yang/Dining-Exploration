import numpy as np
import json
import xgboost as xgb

with open('model/categories.json', 'r') as f:
    categories_list = json.load(f)

with open('model/cities.json', 'r') as f:
    cities_list = json.load(f)

model = xgb.XGBRegressor()
model.load_model('model/regressor_exp.json')


def get_feature_vector(selected_ctgrs, selected_city, open_hours):
    length = len(categories_list) + len(cities_list) + 1
    vec = np.zeros(length)

    one_indices = [categories_list.index(c) for c in selected_ctgrs]
    city_idx = cities_list.index(selected_city)
    one_indices.append(city_idx + len(categories_list))
    vec[one_indices] = 1
    vec[-1] = open_hours
    return vec.reshape(1, -1)


def get_checkin_prediction(selected_ctgrs, selected_city, open_hours):
    vector = get_feature_vector(selected_ctgrs, selected_city, open_hours)

    # in training, we transformed y with log(y+1),
    # hence we need to revert with exp
    prediction = np.exp(model.predict(vector)[0]) - 1
    return int(prediction)


def get_cities_and_categories():
    return cities_list, categories_list
