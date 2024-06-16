from flask import Blueprint,render_template,request,jsonify
import db

class Task:
    def __init__(self,name:str,description:str) -> None:
        self.name = name
        self.description = description

class TodoList:
    def __init__(self,task_dict:dict[Task]={}) -> None:
        self._task_dict = task_dict
        self.completed = False

    def get_tasks(self) -> list:
        return list(self._task_dict.values())
    
    def add_task(self,task:Task):
        self._task_dict[task.name] = task



task = Blueprint("task",__name__)

@task.route("/task-view/<taskID>")
def task_view(taskID):
    return render_template("task-view.html")

@task.route("/task-edit/<taskID>")
def task_edit():
    return render_template("task-edit.html")

@task.route("api/create-task")

@task.route("api/update-task")

@task.route("api/profile-data",methods=["POST"])
def profile_data():
    """Gets profile data such as the username or list of tasks"""

    if not request.is_json:
        return "request is not json"
    elif not request.get_json()["sessionID"]:
        return "expected sessionID in request"
    else:
        response = request.get_json()
        # Get sessionID
        sessionID = response["sessionID"]
        # Get username
        username = db.database.get_user(sessionID)
        # Get task list
        task_list = db.database.get_todolists(username)

        data = jsonify({"username":username,"task_list":task_list})

        return data

    return render_template("profile.html",db.database.g)


