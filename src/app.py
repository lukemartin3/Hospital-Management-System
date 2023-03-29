from flask import Flask, render_template, request, session, url_for, redirect
import mysql.connector
# Always use Flask.session instead of the Session object for direct access.
from flask_session import Session

app = Flask(__name__)

__HOST = 'localhost'
__USERNAME = 'root'
__PASSWORD = 'Topher1028'
__DATABASE = 'FSEdb'

app.config['SECRET_KEY'] = "debug key" 
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False
Session(app)

con = mysql.connector.connect(host=__HOST, user=__USERNAME, password=__PASSWORD, database=__DATABASE)
mycursor = con.cursor()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM user WHERE username=%s AND password=%s',(username, password))
        record = mycursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[0]
            return redirect(url_for('home'))
        else:
            msg="Incorrect username or password"
    return render_template('login.html',msg=msg)

@app.route("/register", methods=["POST", "GET"])
def register_new_user():
    msg=''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('confirm_password')
        if password != confirm_pass:
            msg="Passwords do not match"
        else:
            mycursor.execute('SELECT * FROM user WHERE username=%s',(username,))
            record = mycursor.fetchone()
            if record:
                msg="Username already exists"
            else:
                mycursor.execute('INSERT INTO user (username, password) VALUES (%s, %s)',(username, password))
                con.commit()
                msg="You have successfully registered"
    return render_template('registration.html', msg=msg)

@app.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        # TODO: Send email
        return redirect("/")
    return render_template("forgot-password.html")

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect("/")

@app.route("/schedule-appointment", methods=["POST", "GET"])
def schedule():
    if not session.get("user_name"):
        return redirect("/login")
    if request.method == "POST":
        date = request.form.get('date')
        time = request.form.get('time')
        notes = request.form.get('notes')
        mycursor.execute('INSERT INTO appointments (username, date, time, notes) VALUES (%s, %s, %s, %s)',
                         (session['username'], date, time, notes))
        con.commit()
        return render_template("home.html")
    return render_template("scheduling.html")

if __name__ == "__main__":
    app.run(debug=True)


