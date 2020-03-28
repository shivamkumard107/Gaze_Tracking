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

@app.route('/lock-check', methods = ['POST'])
def lock_check():
    files_ids = list(flask.request.files)
    image_num = 0
    file_name = ""
    from test import lockCheck
    # multiple image files can be recieved
    for file_id in files_ids:
        imagefile = flask.request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("Image Filename : " + imagefile.filename)
        imagefile.save(filename)
        file_name = filename
        image_num = image_num + 1
        focus = lockCheck(file_name)

    if focus >=0.80:
        return jsonify({
            "focused": True
        })
    else:
        return jsonify({
            "focused": False
        })

    
if __name__ == "__main__":
     app.run(host="0.0.0.0", port=4555, debug=True)
