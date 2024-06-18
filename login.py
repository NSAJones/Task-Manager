from flask import Blueprint, render_template, jsonify, request, redirect, url_for
import db
import sys

users = Blueprint("users", __name__)


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

    if not request.is_json:
        return "request is not json"
    else:
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        # Create user in database
        user_created = db.database.create_user(username, password)
        print(user_created)
        if user_created:
            return "User created"
        else:
            return "User already exists"


@users.route("/api/authenticate", methods=["POST"])
def authenticate():
    """get username and password from json and authenticate.
    Return session ID"""

    if not request.is_json:
        return "request is not json"
    else:
        try:
            data = request.get_json()

            username = data["username"]
            password = data["password"]
            sessionID = db.database.validate_user(username, password)

            print(sessionID, file=sys.stdout)

            if sessionID is not None:
                return jsonify({"sessionID": sessionID})
            else:
                return "invalid user"

        except Exception as e:
            print(e)
            return """
            json request invalid, payload should include username
             and password"""
