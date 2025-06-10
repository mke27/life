from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)
from backend.db_connection import db 
from mysql.connector import Error
from backend.ml_models import model01


model = Blueprint("model", __name__)

@model.route("/predict/<education>/<health>/<safety>/<environment>", methods=["GET"])
def get_predict(education, health, safety, environment):
    try:
        current_app.logger.info("GET /predict handler")
        
        education = float(education)
        health = float(health)
        safety = float(safety)
        environment = float(environment)

        similarity = model01.predict(health, education, safety, environment)
        current_app.logger.info(f"Cosine similarity value returned is {similarity}")

        response_data = similarity.to_dict()

        return jsonify(response_data), 200

    except Exception as e:
        response = make_response(
            jsonify({"error": "Error processing prediction request"}, {'e':e})
        )
        response.status_code = 500
        return response


@model.route("/pred_scores/<var_01>/<var_02>", methods=["GET"])
def get_pred_scores(var_01, var_02):
    current_app.logger.info("GET /prediction handler")

    try:
        prediction = model03.predict(var_01, var_02)
        current_app.logger.info(f"prediction value returned is {prediction}")
        
        response_data = {
            "prediction": prediction,
            "input_variables": {"var01": var_01, "var02": var_02},
        }

        response = make_response(jsonify(response_data))
        response.status_code = 200
        return response

    except Exception as e:
        response = make_response(
            jsonify({"error": "Error processing prediction request"})
        )
        response.status_code = 500
        return response
    

@model.route("/weights", methods=["GET"])
def get_weights():
    try:
        current_app.logger.info("GET /weights handler")
        
        weights = model01.get_weights()
        current_app.logger.info(f"Model weights returned: {weights}")

        response_data = {"weights": weights}
        return jsonify(response_data), 200

    except Exception as e:
        response = make_response(
            jsonify({"error": "Error processing weights request"}, {'e':e})
        )
        response.status_code = 500
        return response
    