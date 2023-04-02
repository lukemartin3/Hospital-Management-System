from flask import Flask, render_template, request, session, url_for, redirect
import mysql.connector
# Always use Flask.session instead of the Session object for direct access.
from flask_session import Session

app = Flask(__name__)

__HOST = 'localhost'
__USERNAME = 'root'
__PASSWORD = 'Topher1028'
__DATABASE = 'fsedb'

app.config['SECRET_KEY'] = "debug key" 
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False
Session(app)

con = mysql.connector.connect(host=__HOST, user=__USERNAME, password=__PASSWORD, database=__DATABASE)
mycursor = con.cursor()

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/admin")
def admin():
    if not session.get("username"):
        return redirect("/login")
    if session['username'] != 'admin':
        return redirect("/")
    return render_template("admin.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM user WHERE username=%s AND password=%s',
                         (username, password))
        record = mycursor.fetchone()
        print("this is record", record)
        if record:
            session['loggedin'] = True
            session['username'] = username  #record[0]
            print("this is current session username", session['username'])
            return redirect(url_for('home'))
        else:
            msg="Incorrect username or password"
    return render_template('login.html', msg=msg)

@app.route("/register", methods=["POST", "GET"])
def register_new_user():
    msg=''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_pass = request.form.get('password_confirm')
        if password != confirm_pass:
            msg="Passwords do not match"
        else:
            mycursor.execute('SELECT * FROM user WHERE email=%s OR username=%s',
                             (email, username))
            record = mycursor.fetchone()
            if record:
                if record[1] == email:
                    msg = 'Email already exists'
                else:
                    msg = "Username already exists"
            else:
                mycursor.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)',
                                 (username, email, password))
                con.commit()
                return redirect(url_for('login'))
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
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        date = request.form.get('date')
        time = request.form.get('time')
        date_time = date + ' ' + time
        mycursor.execute('INSERT INTO appointments (username, datetime) VALUES (%s, %s)',
                         # in 'appointments' table make row for username and 'datetime' with datatype: DATETIME
                         (session['username'], date_time))
        con.commit()
        return render_template("home.html")
    return render_template("scheduling.html")

@app.route("/see-appointments", methods=['POST', 'GET'])
def see_appointments():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        pass
    else:
        mycursor.execute('SELECT datetime FROM appointments WHERE username=%s', (session['username'],))
        appointments = mycursor.fetchall()
        return render_template("see-appointments.html", appointments=appointments)


@app.route("/see-patients", methods=['POST', 'GET'])
def see_patients():
    if not session.get("username"):
        return redirect("/login")
    mycursor.execute('SELECT username FROM user')
    result = mycursor.fetchall()
    print(result)
    usernames = [row[0] for row in result]
    print(usernames)
    return render_template("see-patients.html", usernames=usernames)

if __name__ == "__main__":
    app.run(debug=True)


