function create_user (){
    // Get base url and append api location
    let url = $(location).attr('origin').concat("/api/create-user");

    // Get username and password from register form
    let username = $("#username").val();
    let password = $("#password").val();

    let data = JSON.stringify({"username":username,"password":password});
    console.log(data)

    // Post Json to api location
    $.ajax({
        type:"post",
        url:url,
        data:data,
        headers:{'Content-type':'application/json','Accept':'application/json'},
        success:function (response) {
            $("#warnings").empty()
            if (response == "User already exists"){
                $("#warnings").after($("<p>User exists, try again!</p>"))
            }else{
                $("#warnings").after($("<p>User created!</p>"))
            }
        }
    })
}