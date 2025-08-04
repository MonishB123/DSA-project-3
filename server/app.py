from flask import Flask, Response, jsonify, request
import json
from flask_cors import CORS
import pandas as pd
import time
import matplotlib.figure as plt
from io import BytesIO
import base64
import growth

csv_path = "covid-variants.csv"
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
covid_data = pd.DataFrame()


# Sort countries using merge sort based on values in data mapping
def mergeSort(countries, country_dict):
    if len(countries) <= 1:
        return countries

    mid = len(countries) // 2
    left_sub = mergeSort(countries[:mid], country_dict)
    right_sub = mergeSort(countries[mid:], country_dict)

    sortedCountries = []
    leftI = 0
    rightI = 0

    while leftI < len(left_sub) and rightI < len(right_sub):
        if country_dict[left_sub[leftI]] < country_dict[right_sub[rightI]]:
            sortedCountries.append(left_sub[leftI])
            leftI += 1
        else:
            sortedCountries.append(right_sub[rightI])
            rightI += 1

    sortedCountries.extend(left_sub[leftI:])
    sortedCountries.extend(right_sub[rightI:])

    return sortedCountries


# Sort countries using quick sort based on values in data mapping
def quickSort(countries, country_dict):
    if len(countries) <= 1:
        return countries

    # pivot strategy: use last element
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


# Numerical number each country based on total growth during time period
@app.route('/sort-countries', methods=["POST"])
def sortCountries():
    countries = covid_data["location"].unique().tolist()
    # map country to total growth
    country_dict = {}
    for country in countries:
        country_cases = covid_data[covid_data["location"] == country]
        start_cases = float(country_cases.iloc[0]["num_sequences_total"])
        end_cases = float(country_cases.iloc[-1]["num_sequences_total"])
        country_dict.update({country: (end_cases - start_cases)})

    # measure time for both algorithms
    startTime = time.perf_counter_ns()
    sorted_countries = quickSort(countries, country_dict)
    quickSortTime = time.perf_counter_ns() - startTime

    startTime = time.perf_counter_ns()
    mergeSort(countries, country_dict)
    mergeSortTime = time.perf_counter_ns() - startTime

    data = {"countries": sorted_countries,
            "quickTime": quickSortTime,
            "mergeTime": mergeSortTime}
    return jsonify(data)


# Return Countries
@app.route('/get-countries', methods=["POST"])
def getCountries():
    countries = covid_data["location"].unique().tolist()

    data = {"countries": countries}
    return jsonify(data)


# Given a country name, returns a dict with all the countries variants
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
                data_dict[country][variant].update({date: infections})
            else:
                data_dict[country].update({variant: {date: infections}})
        else:
            data_dict.update({country: {variant: {date: infections}}})

    data = {"variants": variants,
            "most_infections": growth.growth(data_dict, country)}
    return jsonify(data)


# Given a country name and variant, return a dict with dates and the number of infections on that day
@app.route('/get-day-stats', methods=["POST"])
def getDayStats():
    data = request.get_json()
    country = data["country"]
    variant = data["variant"]

    df = covid_data[covid_data["location"] == country]
    df = df[df["variant"] == variant]
    infections_per_day = []
    cases = {}
    # Add number of cases for variant on each day
    for i, row in df.iterrows():
        cases.update({row["date"]: row["num_sequences"]})
        infections_per_day.append(row["num_sequences"])
    # plot data and save into data
    fig = plt.Figure()
    plots = fig.subplots()
    x = range(len(infections_per_day))
    plots.plot(x, infections_per_day)
    plots.set_xlabel("Day")
    plots.set_ylabel("Infections that day")
    plots.set_title(f"{country}'s Covid infections of variant {variant} over time")
    # encode in b64 for sending
    img = BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    plot_b64 = base64.b64encode(img.getvalue()).decode('utf8')
    plot_url = f"data:image/png;base64,{plot_b64}"

    data = {"info": cases,
            "plot": plot_url}
    return jsonify(data)


if __name__ == "__main__":
    covid_data = pd.read_csv(csv_path)
    app.run(debug=True)
