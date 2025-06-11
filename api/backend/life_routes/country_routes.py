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


country = Blueprint("country", __name__)

@country.route("/countries", methods=["GET"])
def get_countries():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT country_name FROM Country')
        rows = cursor.fetchall()
        cursor.close()

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