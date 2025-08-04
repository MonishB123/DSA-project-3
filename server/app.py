from flask import Flask, Response, jsonify, request
import json
from flask_cors import CORS
import pandas as pd

csv_path = "covid-variants.csv"
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
covid_data = pd.DataFrame()


#Sort countries using quick sort based on values in data mapping
def quickSort(countries, country_dict):
    if len(countries) <= 1:
        return countries

    #pivot strategy: use last element
    pivot = countries[-1]
    less_sub = []
    high_sub = []
    for country in countries:
        if country_dict[country] < country_dict[pivot]:
            less_sub.append(country)
        elif country_dict[country] > country_dict[pivot]:
            high_sub.append(country)
    
    less_sub = quickSort(less_sub, country_dict)
    high_sub = quickSort(high_sub, country_dict)  

    sortedCountries = less_sub + [pivot] + high_sub
    return sortedCountries


#Given a country name, returns a dict with all the countries variants
@app.route('/get-variants', methods=["POST"])
def getVariants():
    data = request.get_json()
    country = data["country"]

    df = covid_data[covid_data["location"] == country]
    variants = df["variant"].unique().tolist()

    data_dict = {}
    for i, row in df.iterrows():
        country = row["location"]
        variant = row["variant"]
        date = row["date"]
        infections = row["num_sequences"]
        if country in data_dict:
            if variant in data_dict[country]:
                data_dict[country][variant].update({date : infections})
            else:
                data_dict[country].update({variant : {date : infections}})
        else:
            data_dict.update({country : {variant : {date : infections}}})
 
    data = {"variants" : variants,
            "most_infections" : growth.growth(data_dict, country)}
    return jsonify(data)


#Given a country name and variant, return a dict with dates and the number of infections on that day
@app.route('/get-day-stats', methods=["POST"])
def getDayStats():
    #Read input
    data = request.get_json()
    country = data["country"]
    variant = data["variant"]

    #example data (testing API)
    dailyData = {
        "United States" : {"B12" : {"10-12-21" : 2,
                                    "10-13-21" : 3,
                                    "10-14-21" : 10,}},
        "France" : {"Norovirus" : {"10-10-21" : 10,
                                    "10-11-21" : 2,
                                    "10-12-21" : 10,}},                
    }
    data = {"info" : dailyData[country][variant]}
    return jsonify(data)


if __name__ == "__main__":
    covid_data = pd.read_csv(csv_path)
    app.run(debug=True)
