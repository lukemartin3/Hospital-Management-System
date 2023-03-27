from flask import Flask, render_template, redirect, request, session
# Always use Flask.session instead of the Session object for direct access.
from flask_session import Session

app = Flask(__name__)

app.config['SECRET_KEY'] = "debug key" 
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False
Session(app)

@app.route("/")
def index():
    if not session.get("user_name"):
        return redirect("/login")
    return render_template('welcome.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["user_name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register_new_user():
    if request.method == "POST":
        # TODO: Database stuff
        return redirect("/login")
    return render_template("register.html")

@app.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        # TODO: Send email
        return redirect("/")
    return render_template("forgot-password.html")

@app.route("/logout")
def logout():
    session["user_name"] = None
    return redirect("/")

@app.route("/schedule-appointment", methods=["POST", "GET"])
def schedule():
    if not session.get("user_name"):
        return redirect("/login")
    return render_template("scheduling.html")

if __name__ == "__main__":
    app.run(debug=True)


