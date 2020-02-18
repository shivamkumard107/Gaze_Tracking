from flask import Flask, request, jsonify
import flask
import werkzeug
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def check():
    return 'OK'

@app.route('/post', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    from test import helper
    helper(10)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": "Welcome " + param + " to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

    
if __name__ == '__main__':
    app.run()
