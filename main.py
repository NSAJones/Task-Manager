from flask import Flask,render_template,url_for
import login,task,db

app = Flask(__name__)

# Import blueprints from modules
app.register_blueprint(login.users)
app.register_blueprint(task.task)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")


if __name__ =='__main__':
    app.run()