from flask import Flask, Response, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#Given a country name, returns a dict with all the countries variants
@app.route('/get-variants', methods=["POST"])
def getVariants():
    data = request.get_json()
    country = data["country"]
    
    #example data (testing API)
    countryVariants = {
        "United States" : ["B12", "Novid"],
        "France" : ["Norovirus", "C19"]
    }
    data = {"variants" : countryVariants[country]}
    return jsonify(data)

#Given a country name and variant, return a dict with dates and the number of infections on that day
@app.route('/get-day-stats', methods=["POST"])
def getDayStats():
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
    app.run(debug=True)