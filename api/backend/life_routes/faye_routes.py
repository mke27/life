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
    
@faye.route("/scores", methods=["GET"])
def get_scores():
    current_app.logger.info('GET /scores route')
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT C.country_name, S.health_score, S.education_score, S.safety_score, S.environment_score
            FROM ML_Score S
            JOIN Country C ON S.country_ID = C.country_ID
            WHERE S.score_year = 2022
        """)
        scores = cursor.fetchall()
        cursor.close()

        return jsonify(scores)
    except Error as e:
        return jsonify({"error": str(e)}), 500

