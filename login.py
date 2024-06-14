from flask import Blueprint,render_template,jsonify,request
import db
import sys

users = Blueprint("users",__name__)

@users.route("/login")
def login():
    return render_template("login.html")

@users.route("/register")
def register():
    return render_template("register.html")




@users.route("/api/create-user", methods=["POST"])
def create_user():
    """get username and password from json and create user.
    Return session ID"""

    print(request.get_json(), file=sys.stdout)

    if not request.is_json:
        return "request is not json"

    elif request.method != "POST":
        return "request is not post"
        
    else:
        data = request.get_json()
        
        username = data["username"]
        password = data["password"]

        #Create user in database
        user_created = db.database.create_user(username,password)

        if user_created:
            return "User created"
        else:
            return "User already exists"

@users.route("/api/authenticate", methods=["POST"])
def authenticate():
    """get username and password from json and authenticate.
    Return session ID"""

    if not request.is_json():
        return "request is not json"

    elif request.method != "POST":
        return "request is not post"
        
    else:
        try:
            # Check 
            data = request.json
            username = request.form.get("username")
            password = request.form.get("password")
            sessionID = db.database.validate_user(username,password)

            return jsonify({"sessionID":sessionID})

        except Exception as e:
            print(e)
            return """
            json request invalid, payload should include username
             and password"""


