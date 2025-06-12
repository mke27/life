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


faye = Blueprint("faye", __name__)

@faye.route("/orgs/<int:country_ID>/<int:factor_ID>", methods=["GET"])
def get_orgs_by_country_and_factor(country_ID, factor_ID):
    current_app.logger.info('GET /orgs route')
    try:   
        cursor = db.get_db().cursor()
        query = """
            SELECT * FROM Organization
            WHERE org_country = %s AND org_factor = %s
        """
        cursor.execute(query, (country_ID, factor_ID))
        orgs = cursor.fetchall() 
        cursor.close()
    
        if not orgs:
            return jsonify({"error": "No organizations found for that factor and country"}), 404

        return jsonify(orgs), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@faye.route("/scores_standardized", methods=["GET"])
def get_scores_standardized():
    current_app.logger.info('GET /scores_standardized route')
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT country_name, health_score, education_score, safety_score, environment_score
            FROM ML_Score
            WHERE score_year = 2022
        """)
        scores = cursor.fetchall()
        cursor.close()

        return jsonify(scores)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@faye.route("/scores_unstandardized", methods=["GET"])
def get_scores_unstandardized():
    current_app.logger.info('GET /scores_unstandardized route')
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT country_name, health_score, education_score, safety_score, environment_score
            FROM ML_Score_US
            WHERE score_year = 2022
        """)
        scores = cursor.fetchall()
        cursor.close()

        return jsonify(scores)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@faye.route("/scores/<country_name>", methods=["GET"])
def get_scores_by_country(country_name):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT country_name, health_score, education_score, safety_score, environment_score
            FROM ML_Score
            WHERE score_year = 2022 AND country_name = %s
        """, (country_name,))
        scores = cursor.fetchall()
        cursor.close()

        return jsonify(scores)
    except Error as e:
        return jsonify({"error": str(e)}), 500

