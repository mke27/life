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

@users.route("/role/<role_name>", methods=["GET"])
def get_usernames_by_role_name(role_name):
    current_app.logger.info('GET /role/<role_name> route')
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT u.user_name, u.user_ID, u.first_name, ur.role_ID
            FROM User u
            JOIN User_Role ur ON u.role_ID = ur.role_ID
            WHERE ur.role_name = %s
        """
        cursor.execute(query, role_name)
        users = cursor.fetchall()
        cursor.close()

        if not users:
            return jsonify({"error": "No usernames found for this role"})

        return jsonify(users), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_user_by_role_name: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@users.route('/users/remove/<int:user_ID>', methods=["DELETE"])
def remove_user(user_ID):
    current_app.logger.info('DELETE /users/remove/<int:user_ID> route')
    try:
        cursor = db.get_db().cursor()
        query = 'DELETE FROM User WHERE user_ID = %s'
        cursor.execute(query, (user_ID,))
        
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({'error': 'User not found'}), 404

        db.get_db().commit()
        cursor.close()
        return jsonify({'message': f'User {user_ID} deleted successfully'}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500

  
@users.route('/update/username', methods=['PUT'])
def update_username():
    current_app.logger.info('PUT /update/username route')
    try:
        user_info = request.json
        user_ID = user_info['user_ID']
        user_name = user_info['user_name']

        if not user_ID or not user_name:
            return jsonify({'error': 'Missing user_ID or user_name'}), 400

        query = 'UPDATE User SET user_name = %s WHERE user_ID = %s'
        data = (user_name, user_ID)

        cursor = db.get_db().cursor()
        cursor.execute(query, data)
        db.get_db().commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({'error': 'User not found'}), 404

        cursor.close()
        return jsonify({'message': 'User name updated successfully'}), 200

    except Exception as e:
        current_app.logger.error(f'Error updating user name: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@users.route('/update/first-name', methods=['PUT'])
def update_first_name():

    current_app.logger.info('PUT /update/username route')
    try:
        user_info = request.json
        user_ID = user_info['user_ID']
        first_name = user_info['first_name']

        if not user_ID or not first_name:
            return jsonify({'error': 'Missing user_ID or user_name'}), 400

        query = 'UPDATE User SET first_name = %s WHERE user_ID = %s'
        data = (first_name, user_ID)

        cursor = db.get_db().cursor()
        cursor.execute(query, data)
        db.get_db().commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({'error': 'User not found'}), 404

        cursor.close()
        return jsonify({'message': 'First name updated successfully'}), 200

    except Exception as e:
        current_app.logger.error(f'Error updating first name: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500
