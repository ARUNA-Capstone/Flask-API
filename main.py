import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'png', 'jpeg'])
app.config['UPLOAD_DIRECTORY'] = 'static/uploads/'

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def predict(image_path):
    # do prediction here
    pass

@app.route("/", methods = ['GET'])
def homepage():
    return jsonify({
        "status": {
            "code": 200,
            "message": "api is running"
        },
        "data": None,
    }), 200

@app.route("/api/predict", methods = ['POST'])
def prediction():
    if request.method == 'POST':
        image = request.files["image"]

        if image and allowed_extension(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))
            # image_path = os.path.join(app.config['UPLOAD_DIRECTORY'], filename)

            # do prediction here 
            # class_name, confidence_score = predict(image_path)

            # get specific information from database

            return jsonify({
                "status": {
                    "code": 200,
                    "message": "success predicting image"
                },
                "data": {
                    "class_name": "joglo (dummy)",
                    "confidence_score": 0.9,
                    "information": {
                        "id": 1,
                        "name": "joglo",
                        "description": "lorem ipsum",
                        "image": "https://storage.googleapis.com/aruna-images/joglo.jpg",
                    }
                },
            }), 200
        
        else:
            return jsonify({
                "status": {
                    "code": 400,
                    "message": "invalid image extension. only accept jpg, jpeg, and png."
                },
                "data": None,
            }), 400

    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
            "data": None,
        }), 405


@app.route("/api/database/articles", methods = ['GET'])
def get_articles():
    if request.method == 'GET':
        # get specific information from database

        return jsonify({
            "status": {
                "code": 200,
                "message": "success getting articles"
            },
            "data": [
                {
                    "id": 1,
                    "name": "joglo",
                    "description": "lorem ipsum",
                    "image": "https://storage.googleapis.com/aruna-images/joglo.jpg",
                },
                {
                    "id": 2,
                    "name": "joglo",
                    "description": "lorem ipsum",
                    "image": "https://storage.googleapis.com/aruna-images/joglo.jpg",
                },
                {
                    "id": 3,
                    "name": "joglo",
                    "description": "lorem ipsum",
                    "image": "https://storage.googleapis.com/aruna-images/joglo.jpg",
                }
            ],
        }), 200

    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
            "data": None,
        }), 405

@app.route("/api/database/articles/<int:article_id>", methods = ['GET'])
def get_articles_by_id(article_id):
    if request.method == 'GET':
        # get specific information from database
        article = 1

        if article:
            return jsonify({
                "status": {
                    "code": 200,
                    "message": "success getting articles"
                },
                "data": {
                    "id": 1,
                    "name": "joglo",
                    "description": "lorem ipsum",
                    "image": "https://storage.googleapis.com/aruna-images/joglo.jpg",
                }
            }), 200
        
        else:
            return jsonify({
                "status": {
                    "code": 404,
                    "message": "article not found"
                },
                "data": None,
            }), 404

    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
            "data": None,
        }), 405


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
