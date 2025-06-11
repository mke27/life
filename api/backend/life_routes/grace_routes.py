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


grace = Blueprint("grace", __name__)

@grace.route("/pred_scores", methods=["GET"])
def get_all_pred_scores():
    current_app.logger.info('GET /pred_scores route')
    try:
        current_app.logger.info('Starting get_all_pred_scores request')
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        scores = request.args.get("pred_score")
        factor = request.args.get("factor_id")
        country = request.args.get("country_id")

        current_app.logger.debug(f'Query parameters - country_id: {country}, factor_id: {factor}, pred_score: {scores}')

        # Prepare the Base query
        query = "SELECT * FROM Predicted Scores WHERE 1=1"
        params = []

        # Add filters if provided
        if country:
            query += " AND country_ID = %s"
            params.append(country)
        if factor:
            query += " AND factor_ID = %s"
            params.append(factor)
        if scores:
            query += " AND pred_score = %s"
            params.append(scores)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        grace_scores = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(grace_scores)} countries')
        return jsonify(grace_scores), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_pred_scores: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@grace.route("/pred_scores/<int:country_id>", methods=["GET"])
def get_pred_scores_by_country(country_id):
    current_app.logger.info('GET /pred_scores route')
    try:
        cursor = db.get_db().cursor(dictionary=True)
        cursor.execute("""
            SELECT factor_ID, pred_score 
            FROM Predicted_Score 
            WHERE country_ID = %s
        """, (country_id,))
        scores = cursor.fetchall()
        cursor.close()

        if scores:
            return jsonify(scores), 200
        else:
            return jsonify({"error": "No scores found for country"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500

@grace.route("/university/<int:country_id>", methods=["GET"])
def get_unis_by_country(country_id):
    current_app.logger.info('GET /university route')
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM University WHERE Country_ID = %s", (country_id,))
        universities = cursor.fetchall()
        cursor.close()

        return jsonify(universities), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@grace.route("/preference", methods=["POST"])
def create_preference():
    try:
        current_app.logger.info('Starting create_preference request')
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        cursor = db.get_db().cursor()
        query = """
            INSERT INTO Preference (user_ID, pref_date, top_country, factorID_1, weight1, factorID_2, weight2, factorID_3, weight3,
            factorID_4, weight4)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('user_ID'),
            data.get('pref_date'),
            data.get('top_country'),
            data.get('factorID_1'),
            data.get('weight1'),
            data.get('factorID_2'),
            data.get('weight2'),
            data.get('factorID_3'),
            data.get('weight3'),
            data.get('factorID_4'),
            data.get('weight4')
        ))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info('Preference created successfully')
        return jsonify({"message": "Preference created successfully"}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_preference: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@grace.route("/preference/<int:user_ID>", methods=["GET"])
def get_pref_topcountry(user_ID):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT pref_ID, top_country, weight1, weight2, weight3, weight4
            FROM Preference
            WHERE user_ID = %s
            ORDER BY pref_date DESC
            LIMIT 5
        """, (user_ID,))
        prefs = cursor.fetchall()
        cursor.close()

        pref_list = [
            {"pref_ID": row["pref_ID"], "top_country": row["top_country"], "weight1": row["weight1"], "weight2": row["weight2"], "weight3": row["weight3"], "weight4": row["weight4"]}
            for row in prefs
        ]

        return jsonify(pref_list), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

