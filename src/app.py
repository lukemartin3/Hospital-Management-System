from flask import Flask, render_template, request, session, url_for, redirect
import mysql.connector
# Always use Flask.session instead of the Session object for direct access.
from flask_session import Session

app = Flask(__name__)

__HOST = 'localhost'
__USERNAME = 'root'
__PASSWORD = 'pw'
__DATABASE = 'db'

app.config['SECRET_KEY'] = "debug key" 
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False
Session(app)

from flask import Flask
from flask_mail import Mail, Message

app2 = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'swe.team09@gmail.com'
app.config['MAIL_PASSWORD'] = 'vmxcgujzgzexmsfb'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

con = mysql.connector.connect(host=__HOST, user=__USERNAME, password=__PASSWORD, database=__DATABASE)
mycursor = con.cursor()

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/doctor-home")
def doctor_home():
    if not session.get("username"):
        return redirect("/login")
    if session.get("doctor"):
        return render_template("doctor-home.html")
    else:
        return redirect("/")


@app.route("/nurse-home")
def nurse_home():
    if not session.get("username"):
        return redirect("/login")
    if session.get("nurse"):
        return render_template("nurse-home.html")
    else:
        return redirect("/")


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
        mycursor.execute('SELECT * FROM users WHERE username=%s AND password=%s',
                         (username, password))
        record = mycursor.fetchone()
        print("this is record", record)
        if record:
            session['loggedin'] = True
            session['username'] = username
            session['doctor'] = record[4]
            session['nurse'] = record[5]
            if record[4]:
                return redirect(url_for('doctor_home'))
            elif record[5]:
                return redirect(url_for('nurse_home'))
            else:
                return redirect(url_for('home'))
        else:
            msg="Incorrect username or password"
    return render_template('login.html', msg=msg)



@app.route("/register", methods=["POST", "GET"])
def register_new_user():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_pass = request.form.get('password_confirm')
        unique_pin = request.form.get('four_pin')
        doctor = request.form.get('doctor') == 'on'
        nurse = request.form.get('nurse') == 'on'
        if unique_pin and len(unique_pin) > 4:
            msg = "Pin can not exceed 4 characters."
        elif password != confirm_pass:
            msg = "Passwords do not match"
        else:
            mycursor.execute('SELECT * FROM users WHERE email=%s OR username=%s',
                              (email, username))
            record = mycursor.fetchone()
            if record:
                if record[1] == email:
                    msg = 'Email already exists'
                else:
                    msg = "Username already exists"
            else:
                mycursor.execute('INSERT INTO users (username, email, password, pin, doctor, nurse) VALUES (%s, %s, %s, %s, %s, %s)',
                                  (username, email, password, unique_pin, doctor, nurse))
                con.commit()
                session['loggedin'] = True
                session['username'] = username
                session['doctor'] = doctor
                session['nurse'] = nurse
                return redirect(url_for('doctor_home' if doctor else 'nurse_home'))
    return render_template('registration.html', msg=msg)


@app.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():
    msg=''
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        unique_pin = request.form.get('four_pin')
        mycursor.execute('SELECT * FROM users WHERE username=%s AND email=%s AND pin=%s',
                         (username, email, unique_pin))
        record = mycursor.fetchone()
        mycursor.execute('SELECT pin FROM users WHERE username=%s AND email=%s', (username, email))
        send_pin = mycursor.fetchone()
        mycursor.execute('SELECT email FROM users WHERE username=%s AND email=%s', (username, email))
        send_email = mycursor.fetchone()

       
        if record:
            session['loggedin'] = True
            session['username'] = username  #record[0]
            print("this is current session username", session['username'])
            return redirect(url_for('reset'))
        else:
            msg="Incorrect username, email, or pin. Check your email for the correct pin."
            mycursor.execute('SELECT pin FROM users WHERE username=%s AND email=%s', (username, email))
            send_pin = mycursor.fetchone()
            mycursor.execute('SELECT email FROM users WHERE username=%s AND email=%s', (username, email))
            send_email = mycursor.fetchone()

            if send_pin == None or send_email == None:
                msg = "Incorrect username or pin."
            else: 
                msg2 = Message("Hello " + username,
                            sender = "swe.team09@gmail.com", 
                            recipients = ["swe.team09@gmail.com", send_email[0]])
                msg2.body = "here is your 4 digit pin: " + str(send_pin[0])
                mail.send(msg2)

        return render_template('forgot-password.html', msg=msg)
    return render_template("forgot-password.html")

@app.route("/reset-password", methods=["POST", "GET"])
def reset():
    msg=''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('password_confirm')
        if password != confirm_pass:
            msg="Passwords do not match"
        else:
            mycursor.execute('UPDATE users.users SET password = %s WHERE username = %s',
                                (password, username))
            con.commit()
            session['loggedin'] = True
            session['username'] = username  #record[0]
            print("this is current session username", session['username'])
            return redirect(url_for('login'))
    return render_template('reset-password.html', msg=msg)
    

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect("/")

@app.route("/schedule-appointment", methods=["POST", "GET"])
def schedule():
    if not session.get("doctor"): # "username"
        return redirect("/login")
    if request.method == "POST":
        date = request.form.get('date')
        time = request.form.get('time')
        mycursor.execute('INSERT INTO appointments (doctor_name, date, time) VALUES (%s, %s, %s)',
                         (session['doctor'], date, time))
        con.commit()
        return render_template("doctor-home.html")
    return render_template("scheduling.html")

@app.route("/see-appointments", methods=['POST', 'GET'])
def see_appointments():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        pass # TODO: What should we do here?
    else:
        mycursor.execute('SELECT * FROM appointments WHERE username=%s', (session['username'],))
        appointments = mycursor.fetchall()
        return render_template("see-appointments.html", appointments=appointments)


@app.route("/get-appointment", methods=["POST", "GET"])
def get_appointment():
    if not session.get("username"):
        return redirect("/login")
    mycursor.execute('SELECT * FROM appointments')
    records = mycursor.fetchall()
    if request.method == 'POST':
        appointment_id = request.form.get('appointment_id')
        if appointment_id:
            appointment_id = int(appointment_id)
            mycursor.execute('UPDATE appointments SET username = %s WHERE id = %s',
                             (session['username'], appointment_id))
            con.commit()
            return redirect(url_for('doctor_home' if session.get("doctor") else 'nurse_home'))
        else:
            pass # TODO: add handling for invalid appointment IDs
    return render_template('book-appointment.html', records=records)


@app.route("/see-patients", methods=['POST', 'GET'])
def see_patients():
    if not session.get("username"):
        return redirect("/login")
    mycursor.execute('SELECT username FROM users')
    result = mycursor.fetchall()
    usernames = [row[0] for row in result]
    return render_template("see-patients.html", usernames=usernames)

def run_app(debug=True):
    app.run(debug=debug)

if __name__ == "__main__":
    run_app(True)


