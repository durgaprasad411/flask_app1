from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from .models import User

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/submit', methods=['POST'])
def submit():
    data = request.form
    name = data.get('name')
    mobile = data.get('mobile')

    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        user = User(name=name, mobile=mobile, resume=filename)
        return jsonify({
            "message": "Data received successfully",
            "name": user.name,
            "mobile": user.mobile,
            "resume": user.resume
        }), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

@main.route('/submit', methods=['GET'])
def get_submit():
    users = User.get_all_users()
    return jsonify(users), 200

@main.route('/submit/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.form
    name = data.get('name')
    mobile = data.get('mobile')

    if 'resume' in request.files:
        file = request.files['resume']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            return jsonify({"error": "File type not allowed"}), 400
    else:
        filename = None

    user = User.update_user(user_id, name, mobile, filename)
    if user:
        return jsonify({
            "message": "User updated successfully",
            "name": user.name,
            "mobile": user.mobile,
            "resume": user.resume
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

@main.route('/submit/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if User.delete_user(user_id):
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
