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


james = Blueprint("james", __name__)
    
@james.route("/policy", methods=["GET"])
def get_policy():
    current_app.logger.info('GET /policy route')
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT factor_ID, urls, title, DATE_FORMAT(date_created, '%Y-%m-%d') as date_created
            FROM Policy_News
            ORDER BY date_created DESC
        """)
        policies = cursor.fetchall()
        cursor.close()

        return jsonify(policies), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500