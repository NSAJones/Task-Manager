from flask import Blueprint,render_template

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

@task.route("/task-edit")
def task_edit():
    return render_template("task-edit.html")

