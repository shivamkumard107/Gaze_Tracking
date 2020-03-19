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
    param = request.get_json()
    url = param["url"]
    print("url: "+ str(url))
    from test import helper
    focus = helper(10, str(url))
    print("focus:", focus)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "score": focus
            # Add this option to distinct the POST request
        })
    else:
        return jsonify({
            "score": -1
        })

    
if __name__ == "__main__":
     app.run(host="0.0.0.0", port=4555, debug=True)
