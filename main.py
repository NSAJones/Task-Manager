from flask import Flask,render_template,url_for,request,url_for,redirect
import login,task,db

app = Flask(__name__,"/static")

# Import blueprints from modules
app.register_blueprint(login.users)
app.register_blueprint(task.task)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile")
def profile():
    if "sessionID" in request.cookies:
        sessionID = request.cookies["sessionID"]
        if db.database.sessionID(sessionID) is not None:
            return render_template("profile.html")
        
    return redirect(url_for("users.login"))


if __name__ =='__main__':
    app.run()