from app import app
from modals.task import Task, todo_list
from modals.account import User, accounts
from flask import json, jsonify, request
from flask_jwt_extended import create_access_token
from validation import Validation


@app.route("/api/user/register", methods=["POST"])
def register_user():
    reg_info = request.get_json()
    search_keys = ("username", "email", "password")

    if all(key in reg_info.keys() for key in search_keys):
        user_name = reg_info.get("username")
        email    = reg_info.get("email")
        password = reg_info.get("password")
        
        validate = Validation.auth_validation(user_name=user_name, email=email, password=password)
        if validate:
            return jsonify({"message": validate}), 400

        new_user = User(username=user_name, email=email, password=password)
        if (new_user.add_account()):
            return jsonify({"New User Created": new_user.__dict__}), 201
        else:
            return jsonify({"message": "User not added or username already exists"}), 400
    return jsonify({"message": "a 'key(s)' is missing in your registration body"}), 400   


@app.route("/api/user/login", methods=["POST"])
def login():
    login_info = request.get_json()
    search_keys = ("username", "password")

    if all(key in login_info.keys() for key in search_keys):
        user_name = login_info.get("username").strip()
        password = login_info.get("password")

        validate = Validation.login_validation(user_name, password)
        if validate:
            return jsonify({"message": validate}), 400
        login = User.login(username=user_name, password=password)
        user_token = {}
        if login:
            access_token = create_access_token(identity= user_name)
            user_token["token"] = access_token
            return jsonify(user_token), 200

        return jsonify({"message": "user does not exist, register and login again"}), 404
    return jsonify({"message": "a 'key(s)' is missing in login body"}), 400   








    


