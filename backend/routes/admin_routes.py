from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import users_collection  # Assuming you have the users collection model

# Create the Blueprint for admin routes
admin_routes = Blueprint("admin_routes", __name__)

# Example: Admin Dashboard - View Admin Data
@admin_routes.route('/admin-dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_user = get_jwt_identity()  # Get the username (identity)
    
    # Fetch the user details from the database
    user = users_collection.find_one({"username": current_user})
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Ensure the user has an admin role
    if user['role'] != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403

    # Return some admin-specific data
    return jsonify({
        "message": f"Welcome, {current_user}! You have admin access.",
        "admin_data": "Here is some admin-specific data..."
    }), 200

# Example: View all users (Admin only)
@admin_routes.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()  # Get the username (identity)
    
    # Fetch the user details from the database
    user = users_collection.find_one({"username": current_user})
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Ensure the user has an admin role
    if user['role'] != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403
    
    # Retrieve all users from the database
    users = users_collection.find()
    users_list = [{"username": u["username"], "role": u["role"]} for u in users]

    return jsonify({
        "message": "Here are all the users:",
        "users": users_list
    }), 200

# Example: Delete a user (Admin only)
@admin_routes.route('/delete-user/<username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    current_user = get_jwt_identity()  # Get the username (identity)
    
    # Fetch the user details from the database
    user = users_collection.find_one({"username": current_user})
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Ensure the user has an admin role
    if user['role'] != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403
    
    # Find and delete the user by username
    user_to_delete = users_collection.find_one({"username": username})
    if not user_to_delete:
        return jsonify({"message": f"User '{username}' not found."}), 404
    
    users_collection.delete_one({"username": username})
    
    return jsonify({
        "message": f"User '{username}' has been successfully deleted."
    }), 200

# Example: Edit user role (Admin only)
@admin_routes.route('/edit-user-role/<username>', methods=['PUT'])
@jwt_required()
def edit_user_role(username):
    current_user = get_jwt_identity()  # Get the username (identity)
    
    # Fetch the user details from the database
    user = users_collection.find_one({"username": current_user})
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Ensure the user has an admin role
    if user['role'] != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403
    
    # Retrieve the new role from the request
    data = request.json
    new_role = data.get('role', None)
    
    if not new_role or new_role not in ['user', 'admin']:
        return jsonify({"message": "Invalid role. Choose 'user' or 'admin'."}), 400
    
    # Find the user to update
    user_to_edit = users_collection.find_one({"username": username})
    if not user_to_edit:
        return jsonify({"message": f"User '{username}' not found."}), 404
    
    # Update the role
    users_collection.update_one({"username": username}, {"$set": {"role": new_role}})
    
    return jsonify({
        "message": f"User '{username}' role updated to '{new_role}'."
    }), 200
