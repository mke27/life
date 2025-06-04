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
from backend.ml_models import model02

users = Blueprint("users", __name__)
@users.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        current_app.logger.info(f'Starting get_user_by_id request for user_id={user_id}')
        cursor = db.get_db().cursor(dictionary=True)

        query = """
            SELECT u.user_ID, u.user_name, u.country_ID, r.role_name
            FROM User u
            JOIN User_Role r ON u.role_ID = r.role_ID
            WHERE u.user_ID = %s
        """
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Error as e:
        current_app.logger.error(f'Database error in get_user_by_id: {str(e)}')
        return jsonify({"error": str(e)}), 500
    

grace = Blueprint("grace", __name__)
@grace.route("/pred_scores", methods=["GET"])
def get_all_pred_scores():
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


@grace.route("/preferences", methods=["POST"])
def create_preference():
    try:
        current_app.logger.info('Starting create_preference request')
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        cursor = db.get_db().cursor()
        query = """
            INSERT INTO Preferences (user_ID, top_country, factorID_1, weight1, factorID_2, weight2, factorID_3, weight3,
            factorID_4, weight4, factorID_5, weight5)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('user_ID'),
            data.get('top_country'),
            data.get('factorID_1'),
            data.get('weight1'),
            data.get('factorID_2'),
            data.get('weight2'),
            data.get('factorID_3'),
            data.get('weight3'),
            data.get('factorID_4'),
            data.get('weight4'),
            data.get('factorID_5'),
            data.get('weight5')
        ))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info('Preference created successfully')
        return jsonify({"message": "Preference created successfully"}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_preference: {str(e)}')
        return jsonify({"error": str(e)}), 500


model = Blueprint("model", __name__)
@model.route("/cosine_similarity/<var_01>/<var_02>/<var_03>/<var_04>/<var_05>", methods=["GET"])
def get_cosine_similarity():
    try:
        current_app.logger.info("GET /cosine_similarity handler")
        
        similarity = model02.cosine_similarity(var_01, var_02, var_03, var_04, var_05)
        current_app.logger.info(f"Cosine similarity value returned is {similarity}")
        
        response_data = {
            "cosine_similarity": similarity,
            "input_variables": {
                "var01": var_01,
                "var02": var_02,
                "var03": var_03,
                "var04": var_04,
                "var05": var_05
            }
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