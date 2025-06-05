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

@grace.route("/preferences/by_user/<int:user_id>", methods=["GET"])
def get_preferences_by_user(user_id):
    try:
        cursor = db.get_db().cursor(dictionary=True)
        cursor.execute("""
            SELECT pref_ID, pref_date, top_country 
            FROM Preference 
            WHERE user_ID = %s
            ORDER BY pref_date DESC
        """, (user_id,))
        preferences = cursor.fetchall()
        cursor.close()

        return jsonify(preferences), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@grace.route("/pred_scores/<int:country_id>", methods=["GET"])
def get_pred_scores_by_country(country_id):
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
            INSERT INTO Preference (user_ID, top_country, factorID_1, weight1, factorID_2, weight2, factorID_3, weight3,
            factorID_4, weight4)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            data.get('weight4')
        ))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info('Preference created successfully')
        return jsonify({"message": "Preference created successfully"}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_preference: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@grace.route("/preference/<int:pref_id>/top_country", methods=["GET"])
def get_pref_topcountry(pref_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT C.country_name 
            FROM Preference P
            JOIN Country C ON P.top_country = C.country_ID
            WHERE P.pref_ID = %s
        """, (pref_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return jsonify({"top_country": result[0]}), 200
        else:
            return jsonify({"error": "Preference not found"}), 404

    except Error as e:
        return jsonify({"error": str(e)}), 500


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
    
country = Blueprint("country", __name__)
@country.route("/countries", methods=["GET"])
def get_countries():
    try:
        cursor = db.get_db().cursor()  # no dictionary=True because your connector doesn't support it
        cursor.execute('SELECT country_name FROM Country')
        rows = cursor.fetchall()
        cursor.close()

        # since rows is a list of dicts, access by key
        countries = [row["country_name"] for row in rows]

        return jsonify(countries)
    except Error as e:
        return jsonify({"error": str(e)}), 500    
    
@country.route("/country", methods=["GET"])
def get_country_ID():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT country_ID, country_name FROM Country')
        rows = cursor.fetchall()
        cursor.close()

        countries = [{"country_name": row["country_name"], "country_ID": row["country_ID"]} for row in rows]

        return jsonify(countries), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

@country.route("/factor", methods=["GET"])
def get_factor_ID():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT factor_ID, factor_name FROM Factor')
        rows = cursor.fetchall()
        cursor.close()

        factors = [{"factor_name": row["factor_name"], "factor_ID": row["factor_ID"]} for row in rows]

        return jsonify(factors), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

    

faye = Blueprint("faye", __name__)
@faye.route("/orgs/<int:country_ID>/<int:factor_ID>", methods=["GET"])
def get_orgs_by_country_and_factor(country_ID, factor_ID):
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


