import os
import time
import keras
import base64
import requests
import numpy as np
from PIL import Image
import mysql.connector
import tensorflow as tf
from keras.preprocessing import image
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from keras.applications.resnet50 import preprocess_input, decode_predictions

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'png', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def execute_querry(querry):
    print(querry)
    cursor = db.cursor()
    cursor.execute(querry)
    data = cursor.fetchall()
    cursor.close()
    return data

def check_server_availability(destination_url, timeout=30):
    try:
        response = requests.get(destination_url, timeout=timeout)
        if response.status_code == 400:
            return True
        else:
            return False
    except requests.exceptions.Timeout:
        return False

def getLabel():
    label = ['gadang', 'honai', 'joglo', 'panjang', 'tongkonan']
    return label

# Load pre-trained ResNet50 model
def loadmodel():
    model = keras.models.load_model('aruna-model.h5')
    return model

def predict_class(image_path):
    model = loadmodel()
    # Load and preprocess the image
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.asarray(img)
    img_array = np.expand_dims(img_array, axis=0)
    # Get model predictions
    predictions = model.predict(img_array)

    return predictions

# initialize database connection
db = mysql.connector.connect(
    host = os.environ["DB_HOST"],
    user = os.environ["DB_USER"],
    password = os.environ["DB_PASS"],
    database = os.environ["DB_NAME"]
)

@app.route("/", methods = ['GET'])
def homepage():
    return jsonify({
        "data": None,
        "status": {
            "code": 200,
            "message": "aruna api is running"
        },
    }), 200

@app.route("/api/predict", methods = ['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        image = request.files["image"]
        if image and allowed_extension(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            class_names = getLabel()
            predicted_class = predict_class(image_path)
            print(predicted_class)

            for label in class_names:
                score = tf.nn.softmax(predicted_class[0])

            os.remove(image_path)
            result_name = class_names[np.argmax(score)]
            result_confidence = 100 * np.max(score)

            # get specific information from database
            article = execute_querry("SELECT * FROM `articles` WHERE name LIKE '%" + result_name + "%'")

            if article:
                # reconstruct article into json format
                key_value_article = []
                for id, name, description, image in article:
                    key_value_article.append({
                        'id': id,
                        'name': name,
                        'description': description,
                        'image': image
                    })
                # get contact information from database
                contact = execute_querry('SELECT * FROM `contact_persons` WHERE `id_articles` = ' + str(key_value_article[0]["id"]))
                # reconstruct contact into json format
                key_value_contact = []
                for id, id_article, name, phone, contact_link in contact:
                    key_value_contact.append({
                        'id': id,
                        'name': name,
                        'phone': phone,
                        'contact_link': contact_link
                    })
                # return prediction result with additional information
                return jsonify({
                    "data": {
                        "class_name": result_name,
                        "confidence_score": result_confidence,
                        "information": key_value_article[0],
                        "contact": key_value_contact[0]
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
                        "code": 503,
                        "message": "failed to fetch result data. please try again."
                    },
                }), 503
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
        articles = execute_querry('SELECT * FROM `articles`')
        # reconstruct data into json format
        key_value_articles = []
        for row in articles:
            id = row[0]
            name = row[1]
            description = row[2]
            image = row[3]
            article = {
                'id': id,
                'name': name,
                'description': description,
                'image': image
            }
            key_value_articles.append(article)
        return jsonify({
            "data": key_value_articles,
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
        # get specific information from database
        article = execute_querry('SELECT * FROM `articles` WHERE id_articles = ' + str(article_id))

        if article:
            # reconstruct data into json format
            key_value_article = []
            for id, name, description, image in article:
                key_value_article.append({
                    'id': id,
                    'name': name,
                    'description': description,
                    'image': image
                })
            return jsonify({
                "data": key_value_article[0],
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

@app.route('/api/search', methods=['GET'])
def search():
    if request.method == 'GET':
        # Extract the search query from the request object
        query = request.args.get('q')
        # get specific information from database
        results = execute_querry("SELECT * FROM `articles` WHERE name LIKE '%" + query + "%'") # response.json()["predictions"][0]["labels"][0]
        
        if results:
            # reconstruct article into json format
            key_value_result = []
            for row in results:
                id = row[0]
                name = row[1]
                description = row[2]
                image = row[3]
                result = {
                    'id': id,
                    'name': name,
                    'description': description,
                    'image': image
                }
                key_value_result.append(result)

            return jsonify({
                "data": key_value_result,
                "status": {
                    "code": 200,
                    "message": "success searching articles"
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
