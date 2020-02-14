from flask import Flask, request, jsonify
import flask
import werkzeug
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def check():
    return 'OK'

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": "Welcome {param} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

@app.route('/image', methods = ['POST'])
def handle_request():
    files_ids = list(flask.request.files)
    print("\nNumber of Received Images : ", len(files_ids))
    image_num = 1
    for file_id in files_ids:
        print("\nSaving Image ", str(image_num), "/", len(files_ids))
        imagefile = flask.request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("Image Filename : " + imagefile.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        imagefile.save(filename)
        image_num = image_num + 1
    print("ML code running\n")
    from test import helper
    return "Image(s) Uploaded Successfully. Come Back Soon."
    
if __name__ == "__main__":
     app.run(host="0.0.0.0", port=4555, debug=True)
