
function authenticate(){
    // Get username and password from form
    let username = $("#username").val();
    let password = $("#password").val();

    // Get api location
    let url = $(location).attr('origin').concat("/api/authenticate");

    // Create JSON data
    let data = JSON.stringify({"username":username,"password":password});

    // Send data via POST
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (response) {
            // If sessionID is recieved in response, create cookie of it
            if (response["sessionID"]){
                Cookies.set("sessionID",response["sessionID"])
            }
        },
        headers:{'Content-type':'application/json','Accept':'application/json'}
    });

    

    
}