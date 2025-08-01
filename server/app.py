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
    
    #base data (testing API)
    countryVariants = {
        "United States" : ["B12", "Novid", "Idk", "OtherVariant"],
        "France" : ["Norovirus", "C19"]
    }
    data = {"variants" : countryVariants[country]}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)