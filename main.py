import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'png', 'jpeg'])

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods = ['GET'])
def homepage():
    return jsonify({
        "data": None,
        "status": {
            "code": 200,
            "message": "api is running"
        },
    }), 200

@app.route("/api/predict", methods = ['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        image = request.files["image"]
        if image and allowed_extension(image.filename):
            # do prediction here 
            # get specific information from database
            # get contact information from database
            return jsonify({
                "data": {
                    "class_name": "joglo (dummy)",
                    "confidence_score": 0.9,
                    "information": {
                        "id": 1,
                        "name": "joglo",
                        "description": "lorem ipsum",
                        "image": "https://storage.googleapis.com/aruna-images/joglo.jpg",
                    },
                    "contact": {
                        "id": 1,
                        "name": "joglo owner",
                        "phone": "081234567890"
                    }
                },
                "status": {
                    "code": 200,
                    "message": "success predicting image"
                },
            }), 200
        else:
            return jsonify({
                "data": None,
                "status": {
                    "code": 400,
                    "message": "invalid image extension. only accept jpg, jpeg, and png."
                },
            }), 400
    else:
        return jsonify({
            "data": None,
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
        }), 405


@app.route("/api/database/articles", methods = ['GET'])
def get_articles():
    if request.method == 'GET':
        # get specific information from database
        return jsonify({
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
            "status": {
                "code": 200,
                "message": "success getting articles"
            },
        }), 200

    else:
        return jsonify({
            "data": None,
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
        }), 405

@app.route("/api/database/articles/<int:article_id>", methods = ['GET'])
def get_articles_by_id(article_id):
    if request.method == 'GET':
        if 0 < article_id < 6:
            # get specific information from database
            return jsonify({
                "data": {
                    "id": 1,
                    "name": "joglo",
                    "description": "lorem ipsum",
                    "image": "https://storage.googleapis.com/aruna-images/joglo.jpg",
                },
                "status": {
                    "code": 200,
                    "message": "success getting articles"
                },
            }), 200
        else:
            return jsonify({
                "data": None,
                "status": {
                    "code": 404,
                    "message": "article not found"
                },
            }), 404
    else:
        return jsonify({
            "data": None,
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
        }), 405


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
