from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import db, sys


task = Blueprint("task", __name__)


@task.route("/task-view/<taskID>")
def task_view(taskID):
    return render_template("task-view.html", taskID=taskID)


@task.route("/task-edit/<taskID>")
def task_edit(taskID):
    cookies = request.cookies
    if "sessionID" in cookies:
        sessionID = request.cookies["sessionID"]
        if db.database.check_creator(sessionID, taskID):
            return render_template("task-edit.html", taskID=taskID)

    return redirect(url_for("task.task_view", taskID=taskID))


@task.route("/api/update-task/<taskID>", methods=["POST"])
def update_task(taskID: int):
    if not request.is_json:
        return "request is not json"
    else:
        response = request.get_json()
        cookies = request.cookies
        if "sessionID" in cookies:
            # Check user is the creator of the todolist
            if db.database.check_creator(cookies["sessionID"], taskID):
                db.database.update_task(taskID, response)
                return "list updated"
            else:
                return "invalid access"
        else:
            return redirect(url_for("users.login"))


@task.route("/api/task-data/<taskID>", methods=["GET"])
def task_data(taskID: int):
    task_dict = db.database.get_todolist(taskID)
    return task_dict


@task.route("/api/create-todo", methods=["POST"])
def create_todo():
    """Create a blank task, returns id of task created"""

    if not request.is_json:
        return "request is not json"
    elif not request.get_json()["sessionID"]:
        return redirect(url_for("users.login"))
    else:
        data = db.database.create_todolist(request.get_json()["sessionID"])
        return jsonify(data)


@task.route("/api/profile-data", methods=["POST"])
def profile_data():
    """Gets profile data such as the username or list of tasks"""

    if not request.is_json:
        return "request is not json"
    elif not request.get_json()["sessionID"]:
        return redirect(url_for("users.login"))
    else:
        response = request.get_json()
        # Get sessionID
        sessionID = response["sessionID"]
        # Get username
        username = db.database.get_user(sessionID)
        # Get task list
        task_list = db.database.get_todolists(username)

        data = jsonify({"username": username, "task_list": task_list})

        return data
