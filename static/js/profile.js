function update_profile() {

    let origin = $(location).attr('origin')
    let profile_url = origin.concat("/api/profile-data");
    let login_url = origin.concat("/login");

    let sessionID = Cookies.get("sessionID")
    

    // Check if user is logged in with sessionID
    if (sessionID){
        let data = JSON.stringify({"sessionID":sessionID})

        // Get username and todo lists from database
        $.ajax({
            type: "POST",
            url: profile_url,
            data: data,
            success: function (response) {
                console.log(response)

                username = response["username"]
                task_list = response["task_list"]

                // Change username element
                if (username){
                    $("#username").text(username)
                }

                // Create hyperlink to each todolist if user has some
                if (task_list.length != 0){
                    let login_url;
                    let id;
                    
                    for (task of task_list){
                        id = task[0];
                        login_url = origin + "/task-edit/" + id;
                        $("#todolists").append(
                            `<li>
                                <a href="${login_url}" target="_blank">
                                ${task[1]}</a>
                            </li>`)
                    }
                }
                // If user has no lists display message
                else{
                    $("#todolists").replaceWith(
                        `<div>
                        Oops! It's empty here, try making a todo list
                        </div>`
                    )
                }
            },
            headers:{'Content-type':'application/json','Accept':'application/json'}
        });

       
        let create_url = origin + "/api/create-todo"

        // Listener to create new list
        $("#new-list").click(function () {
            $.ajax({
                type: "POST",
                url: create_url,
                data: JSON.stringify({"sessionID":sessionID}),
                success: function (response) {
                    console.log(response)
                    // Open new page to new task
                    let login_url = origin + "/task-edit/" + response;
                    window.open(login_url)

                    // Refresh page
                    location.reload()

                },
                headers:{'Content-type':'application/json','Accept':'application/json'}
            });
        });

    }
    else{
        // Redirect to login if not logged in
        window.location.replace(login_url)
    }

   

}

$(document).ready(function () {
    update_profile()
});

