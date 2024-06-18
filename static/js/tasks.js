class Task{
    constructor(name,description){
        this.name = name;
        this.description = description;
    }

    get t_name(){return this.name}
    get t_description(){return this.description}

    set t_name(n){this.name=n}
    set t_description(d){this.description=d}
}

class TodoList{
    constructor(name,task_list){
        this.name = name;
        this.task_list = task_list;
    }
    
    add_task(task){
        // Add task and return it's id
        this.task_list.push(task)
        return this.task_list.length-1
    }

    change_task(id,name,description){
        if (name){
            let task = this.task_list[id];
            task.name = name;
        }

        if (description){
            let task = this.task_list[id];
            task.description = description;
        }
    }

    get t_name(){return this.name}
    get t_task_list(){return this.task_list}

    set t_name(n){this.name = n}
}

const origin = $(location).attr('origin');
var todo;

function get_todo(id){
    let url = origin + "/api/task-data/" + id.toString();
    return $.get(url,).then(
        function (data) {
            console.log(data)

            let tasks = data["tasks"];
            let task_list = [];
            for (t of tasks){
                task_list.push(new Task(
                    t[2],
                    t[3]
                ))
            }
            let temp_todo = new TodoList(data["todolist"][1],task_list);
            todo = temp_todo;

            console.log(data["todolist"][1],todo.t_name)
            return todo
        }
    );
}

function create_task_dom(id,name,description,edit=true){
    let DOM;
    if (edit){
        if (name && description){
            DOM = `
            <li id=${id}>
                <input name="task" type="text" value="${name}">
                <textarea name="description" placeholder="description here (can be left blank)">
                ${description}
                </textarea>
            </li>
            `
        }else{
            DOM = `
            <li id=${id}>
                <input name="task" type="text" value="new task">
                <textarea name="description" placeholder="description here (can be left blank)"></textarea>
            </li>
            `
        }

        // Create element from HTML code
        DOM = $(DOM)

        // Add listeners to input and textarea
        $(DOM).children('input[name="task"]').on("input", function () {
            let id = $(this).parent().attr("id");
            todo.change_task(id,$(this).val())
        });
        $(DOM).children('textarea[name="description"]').on("input", function () {
            let id = $(this).parent().attr("id");
            todo.change_task(id,null,$(this).val())
        });
    }
    else{
        DOM = `
        <li>
            <h3 name="task">${name}</h3>
            <p name="description">${description}</p>
        </li>
        `
        DOM = $(DOM)
    }

    return DOM
}

$(document).ready(function () {
    // Get id of todolist from DOM
    let id = parseInt($("meta[name='task-id']").attr("content"));
    let sessionID = Cookies.get("sessionID")

    // If edit file
    if (window.location.href.indexOf("edit")>-1){
        // Create TodoList class
        get_todo(id).then(function(response){
            // Create DOM based off TodoList class (task_dom)

            // Change name to title of TodoList
            $("#todo-title").val(todo.name);

            // Add listener to todo-title input
            $("#todo-title").on("input",function(){
                todo.t_name = $(this).val()
            })


            // Create li elements for each task
            let task_dom;
            for (i in todo.t_task_list){
                t = todo.t_task_list[i]
                task_dom = $(create_task_dom(i,t.t_name,t.t_description));
                $("#todo-list").append(task_dom)
            }

            
            // Add listener to "add task button"
            $("#create-task").on("click",function(){
                let id = todo.add_task(new Task("new task"))
                task_dom = $(create_task_dom(id));
                $("#todo-list").append(task_dom)
            })

            // Add listener to save button
            $("#save-list").on("click",function(){
                let id = parseInt($("meta[name='task-id']").attr("content"));
                let url = origin + "/api/update-task/" + id.toString();

                $.ajax({
                    type: "POST",
                    url: url,
                    data: JSON.stringify(todo),
                    success: function (response) {
                        console.log(response)
                    },
                    headers:{'Content-type':'application/json','Accept':'application/json'}
                });
            })
        })
    }
    else{
        get_todo(id).then(function(){
            
            // Create task_dom
            let task_dom;
            for (i in todo.t_task_list){
                t = todo.t_task_list[i];
                task_dom = $(create_task_dom(i,t.t_name,t.t_description,false));
                $("#todo-list").append(task_dom);
            }

            // Change name to title of TodoList
            $("#todo-title").text(todo.t_name);
        })
    }
});