from app import app
from modals.task import Task, todo_list, deleted_tasks
from modals.account import User, accounts
from flask import json, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from validation import Validation

blacklist = set()

@app.route("/api/users/register", methods=["POST"])
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


@app.route("/api/users/login", methods=["POST"])
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
            refresh_token = create_refresh_token(identity=user_name)
            user_token["access_token"] = access_token
            user_token["refresh_token"] = refresh_token
            return jsonify(user_token), 200

        return jsonify({"message": "user does not exist, register and login again"}), 404
    return jsonify({"message": "a 'key(s)' is missing in login body"}), 400

# @app.route('/api/users/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     current_user = get_jwt_identity()
#     resp = {
#         'access_token': create_access_token(identity=current_user)
#     }
#     return jsonify(resp), 200

@app.route("/api/users/delete_account", methods=["DELETE"])
@jwt_required
def delete_account():
    logged_user = get_jwt_identity()
    password = None
    for user in range(len(accounts)):
        if accounts[user]["username"] == logged_user:
            password = accounts[user]["password"]
        if password != None:
            delete_account = User.delete_account(logged_user, password)
            if delete_account:
                return jsonify({"message": "Successfully deleted account"}), 200
            return jsonify({"message": "account not deleted"}), 400    
        return jsonify({"message": "not authorised to delete account"}), 401

@app.route("/api/users/logout", methods=["DELETE"])
@jwt_required
def logout():
    jti = get_raw_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200   

@app.route("/api/tasks/add", methods=["POST"])
@jwt_required
def creat_task():
    task_info = request.get_json()
    if "title" in task_info.keys():
        title = task_info.get("title")
        status = "to-do"
        task_id = len(todo_list)+1
        logged_user = get_jwt_identity()

        validate = Validation.validate_task(title)
        if validate:
            return jsonify({"message": validate}), 400
        new_task = Task(task_id=task_id, title=title, owner=logged_user, status=status)
        if(new_task.create_task()):
            return jsonify({"New task Created": new_task.__dict__}), 201
        return jsonify({"message": "Task not added"}), 400
    return jsonify({"message": "a 'key' is missing in your task body"}), 400

@app.route("/api/tasks/delete/<task_id>", methods=["DELETE"])
@jwt_required
def delete_single_task(task_id):
    logged_user = get_jwt_identity()
    task_id = task_id
    validate = Validation.validate_input_type(task_id)
    if validate:
        return jsonify({"message": validate}), 400
    delete_task = Task.delete_task(int(task_id), logged_user)
    if delete_task:
        return jsonify({"message": "Task successfully deleted"}), 200
    return jsonify({"message": "Task not deleted or doesn't exist"}), 400

@app.route("/api/tasks/delete", methods=["DELETE"])
@jwt_required
def delete_all_tasks():
    logged_user = get_jwt_identity()
    list2 = Task.delete_all_tasks(owner=logged_user)
    print(list2)
    if list2:
        return jsonify({"message": "Your tasks successfully deleted", "Remaining Tasks":[     
            task for task in todo_list
        ]}), 200
    return jsonify({"message": "Tasks not deleted or list is empty"}),400  

@app.route("/api/tasks/finish/<task_id>", methods=["PUT"])
@jwt_required
def finish_a_task(task_id):
    task_id = task_id
    validate = Validation.validate_input_type(task_id)
    if validate:
        return jsonify({"message": validate}), 400
    finish_task = Task.mark_as_finished(int(task_id))
    if finish_task:
        return jsonify({"message": "Task successfully finished", "Updated Tasks":[     
            task for task in todo_list
        ]}), 200
    return jsonify({"message": "Task not finished or doesn't exist"}), 400         

@app.route("/api/tasks/unfinish/<task_id>", methods=["PUT"])
@jwt_required
def unfinish_a_task(task_id):
    task_id = task_id
    validate = Validation.validate_input_type(task_id)
    if validate:
        return jsonify({"message": validate}), 400
    unfinish_task = Task.mark_as_unfinished(int(task_id))
    if unfinish_task:
        return jsonify({"message": "Task successfully updated","Updated Tasks":[     
            task.__dict__ for task in todo_list
        ]}), 200
    return jsonify({"message": "Task not updated or doesn't exist"}), 400

@app.route("/api/tasks/recover", methods=["GET"])
@jwt_required
def recover_deleted_tasks():
    logged_user = get_jwt_identity()
    list2 = [task for task in deleted_tasks if task.get('owner', '') == logged_user]
    if list2:
        return jsonify({"message": "Tasks successfully recovered", "Recovered Tasks":[     
            task.__dict__ for task in list2
        ]}), 200
        
        

   
    








    


