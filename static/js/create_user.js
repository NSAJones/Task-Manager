function create_user (){
    // Get base url and append api location
    var url = $(location).attr('origin').concat("/api/create-user");

    // Get username and password from register form
    var username = $("#username").val();
    var password = $("#password").val();

    var data = JSON.stringify({"username":username,"password":password});
    console.log(data)

    // Post Json to api location
    $.post(url,data,function(response){
        console.log(response);
    },"application/json");

    $.ajax({
        type:"post",
        url:url,
        data:data,
        success:(response)=>console.log(response),
        headers:{'Content-type':'application/json','Accept':'application/json'}
    })
}