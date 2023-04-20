from flask import Flask, render_template, request, session, url_for, redirect
import mysql.connector
# Always use Flask.session instead of the Session object for direct access.
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash


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
    if not session.get("username"):
        return redirect("/login")
    return render_template('home.html')


@app.route('/assign_roles', methods=["POST", "GET"])
def assign_roles():
    msg = ''
    if session.get('role') != 0:
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        specialty = request.form.get('specialization') if role == '3' else None
        mycursor.execute('UPDATE users SET roles=%s AND specialization=%s WHERE username=%s', (role, username, specialty))
        con.commit()
        msg = 'Successfully created Nurse/Physician!'

    return render_template('assign.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM users WHERE username=%s',
                         (username,))
        record = mycursor.fetchone()
        if record and check_password_hash(record[1], password):
            session['loggedin'] = True
            session['username'] = username
            session['role'] = record[15]
            return redirect(url_for('home'))
        else:
            msg="Incorrect username or password"
    return render_template('login.html', msg=msg)



@app.route("/register", methods=["POST", "GET"])
def register_new_user():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('password_confirm')
        unique_pin = request.form.get('four_pin')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip = request.form.get('zip')
        insurance = request.form.get('insurance')
        med_history = request.form.get('med_history')

        if unique_pin and len(unique_pin) > 4:
            msg = "Pin can not exceed 4 characters."
        elif password != confirm_pass:
            msg = "Passwords do not match"
        else:
            hashed_password = generate_password_hash(password)
            roles = 1
            # specialty = ' '
            mycursor.execute('SELECT * FROM users WHERE email=%s OR username=%s',
                              (email, username))
            record = mycursor.fetchone()
            if record:
                if record[5] == email:
                    msg = 'Email already exists'
                else:
                    msg = "Username already exists"
            else:
                mycursor.execute('INSERT INTO users (username, email, password, pin, '
                                 'fname, lname, dob, phone, address, city, states, zip, '
                                 'insurance, history, roles) VALUES (%s, %s, %s, %s, %s, %s, %s, '
                                 '%s, %s, %s, %s, %s, %s, %s, %s)', (username, email,
                                                                 hashed_password, unique_pin,
                                                                 first_name, last_name, dob,
                                                                 phone, address, city, state,
                                                                 zip, insurance, med_history, roles))
                con.commit()
                print("success")
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('home'))
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
        if record:
            session['loggedin'] = True
            session['username'] = username
            print("this is current session username", session['username'])
            return redirect(url_for('reset'))
        else:
            msg="Incorrect username, email, or pin"
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
            mycursor.execute('UPDATE fsedb.users SET password = %s WHERE username = %s',
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
    if session.get("role") != 0:
        return redirect("/login")
    if request.method == "POST":
        # doctor name
        # specialty
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


