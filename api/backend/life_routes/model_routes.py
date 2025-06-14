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
from backend.ml_models import model01, model02


model = Blueprint("model", __name__)

@model.route("/prediction/<education>/<health>/<safety>/<environment>", methods=["GET"])
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
    

@model.route("/weights", methods=["GET"])
def get_weights():
    current_app.logger.info("GET /weights route")

    try:
        cursor = db.get_db().cursor()

        query = "SELECT * FROM Predicted_Score"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return jsonify(list(result.values())), 200

    except Exception as e:
        response = make_response(
            jsonify({"error": "Error processing weights request"}, {'e':e})
        )
        response.status_code = 500
        return response


@model.route("/raw_score/<country_name>", methods=["GET"])
def get_scores(country_name):
    current_app.logger.info("GET /raw_score/<country_name> route")

    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT country_name, score_year, qol_score
            FROM ML_Score_US
            WHERE country_name = %s
        """, (country_name,))
        scores = cursor.fetchall()
        cursor.close()

        return jsonify(scores)
    except Error as e:
        return jsonify({"error": str(e)}), 500
        

@model.route("/model_scores/<country_name>", methods=["GET"])
def get_model_scores(country_name):
    try:
        current_app.logger.info("GET /get handler")
        cursor = db.get_db().cursor()
        predicted_scores = model02.autoregressor_all(country_name)
        current_app.logger.info(f"Predicted scores for {country_name}: {predicted_scores}")

        return jsonify(predicted_scores), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    