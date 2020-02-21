from flask import Flask, request, jsonify
import flask
import werkzeug
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyrebase
import statistics

app = Flask(__name__)
config = {
    "apiKey" : "AIzaSyB1OyBIvLggIAGWoCDjQK4PId9WJfXnREE",
    "authDomain": "mcandlefocus.firebaseapp.com",
    "databaseURL": "https://mcandlefocus.firebaseio.com",
    "projectId": "mcandlefocus",
    "storageBucket": "mcandlefocus.appspot.com",
    "messagingSenderId": "140073311865",
    "appId": "1:140073311865:web:12426f96cae1f3c88a7ea8",
    "measurementId": "G-H6DWEDR9Z7"
};

# Fetch the service account key JSON file contents
cred = credentials.Certificate('firebase-adminsdk.json')
# Initialize the app with a service account, granting admin privileges

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mcandlefocus.firebaseio.com/'
})
firebase = pyrebase.initialize_app(config)


@app.route('/', methods=['GET'])
def check():
    return 'OK'

@app.route('/post', methods=['POST'])
def post_something():
    param = request.get_json()
    url = param["url"]
    print("url: "+ str(url))
    from test import helper
    focussed = helper(10, str(url))
    print("focus:" + str(statistics.mean(focussed)))
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "score": statistics.mean(focussed)
            # Add this option to distinct the POST request
        })
    else:
        return jsonify({
            "score": -1
        })

    
if __name__ == "__main__":
     app.run(host="0.0.0.0", port=4555, debug=True)
